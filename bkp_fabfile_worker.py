# -*- coding: utf-8 -*-
"""
Deployment automation Fabric script for titans-sms-gateway workers
"""
import os

from fabric.api import cd, env, parallel, prefix, run, sudo, roles
from fabric.colors import red
from fabric.context_managers import settings
from fabric.contrib.files import contains, exists
from tnt.fabric import *

DEFAULT_PIP_PARAMS = '%s -i http://pypi.titansgroup.net/simple --trusted-host pypi.titansgroup.net'

# Default settings
env.project_name = 'titans-sms-gateway'
env.forward_agent = True
env.name = None
env.new_relic = False
env.repository = 'git@github.com:titansgroup/sms-gateway.git'
env.user = os.environ.get('SSH_USER', os.environ.get('USER'))

env.deployer_user = 'deployer'
env.deployer_group = 'tgadmin'
env.deployer_home = '/home/%s' % env.deployer_user
env.user_home = '/home/%s' % env.deployer_user

env.src_path = '%s/%s' % (env.user_home, env.project_name)
env.venv_path = '%s/.venv' % env.src_path
env.new_relic_app_name = 'Titans SMS Gateway'

env.new_relic_api_key = '3cd49b165aaf52eb1402b21616d095f44f8c4db6'

env.logs_dir = '/var/log/apps'


def uat():
    """
    Set the production settings
    """

    env.name = 'uat'
    env.new_relic = True

    env.hosts = [
        '10.0.246.245',
    ]
    env.roledefs = {"single": [env.hosts[0]],
                    }


def production():
    """
    Set the production settings
    """
    env.name = 'production'
    env.new_relic = True

    env.hosts = [
        '10.0.246.186',
        '10.0.247.77',
    ]
    env.roledefs = {"single": [env.hosts[0]]}


# Tasks
def deploy(commit='master', use_internal_pypi=True):
    """
    Deploy the app in the server
    """
    if not env.name:
        raise Exception(u'You MUST set the environment variable.')

    # SSH exclude key checking for github.com
    if not exists('%s/.ssh' % env.deployer_home):
        run_deployer('mkdir %s/.ssh' % env.deployer_home)

    ssh_config = '%s/.ssh/config' % env.deployer_home
    if not contains(ssh_config, 'Host github.com'):
        run_deployer('echo "Host github.com" >>%s' % ssh_config)
        run_deployer('echo "     StrictHostKeyChecking no" >>%s' % ssh_config)
        run_deployer('echo "     UserKnownHostsFile /dev/null" >>%s' % ssh_config)

    # clone the repo into the env.src_path
    if not exists(env.src_path):
        run_deployer('git clone %s %s' % (env.repository, env.src_path))

    with cd(env.src_path):
        # fetch the changes
        run_deployer('git fetch --prune')
        run_deployer('git branch --merged | grep -v master | grep -v develop | xargs git branch -d', warn_only=True)

        # if is a production deploy make sure we're deploying a tag
        if env.name == 'production' and False:
            with settings(warn_only=True):
                if run_deployer('git tag | grep \'^%s$\'' % commit).failed:
                    raise RuntimeError(u'In production deploy only tags')

        # checkout to the selected commit/tag/branch
        run_deployer('git checkout --force %s' % commit)

        # if the selected commit is the master branch, merge the changes
        with settings(warn_only=True):
            is_branch = run_deployer('git branch -r | grep \'%s\'' % commit).succeeded

            # if the selected commit is the master branch, merge the changes
            if is_branch:
                run_deployer('git merge origin/%s' % commit)

        # create the deployment specific folders
        if not exists('pid') or not exists('sock') or not exists('locks') or not exists('bin'):
            run_deployer('mkdir -p pid sock locks bin')

        # create virtualenv if needed
        if not exists(env.venv_path):
            python = '/usr/bin/python'
            run_deployer('virtualenv -p %(python)s %(path)s' % {'path': env.venv_path, 'python': python})

        with prefix('source %s/bin/activate' % env.venv_path):
            run_deployer('pip install pip==8.1.0 -qq --disable-pip-version-check')
            commands = ['pip install -r requirements.txt']
            for command in commands:
                if use_internal_pypi:
                    command = DEFAULT_PIP_PARAMS % command
                run_deployer(command)

        # create logs symlink
        if not exists(env.logs_dir):
            sudo('mkdir -p %s' % env.logs_dir)
            sudo('chown -R %s:%s %s' % (env.deployer_user,
                                        env.deployer_group,
                                        env.logs_dir))

        with cd(env.src_path):
            if not exists('logs'):
                run_deployer('ln -s %s logs' % env.logs_dir)

        run_deployer('make clean')

    # Copy celery init script and configure it for boot startup
    with cd('%s/config/init.d' % env.src_path):
        sudo('cp -f celeryd* /etc/init.d/')
        sudo('chmod +x /etc/init.d/celeryd*')

    if env.name == 'production':
        notify_deploy()

    print red("WARNING: deploy does not restart the workers!")


@parallel
def restart():
    """
    Setup services configurations and restart them
    """
    if not env.name:
        raise Exception(u'You MUST set the environment variable.')
    celery_stop()
    sudo('SMS_GATEWAY_APPLICATION_SETTINGS=%s /etc/init.d/celeryd.sh restart' % env.name, pty=False)
    stash_del()


@parallel
def celery_stop():
    """
    Setup services configurations and restart them
    """
    if not env.name:
        raise Exception(u'You MUST set the environment variable.')

    if exists(env.src_path):
        stash_add()
        # setup Celery configs
        with cd('%s/config/celery' % env.src_path):
            sudo('rm -f celeryd*')
            sudo('ln -sf %s/celeryd .' % env.name)
        if env.new_relic:
            with cd('%s/config/newrelic' % env.src_path):
                sudo('ln -sf %s/titans-sms-gateway.ini titans-sms-gateway.ini' % env.name)
        sudo('SMS_GATEWAY_APPLICATION_SETTINGS=%s /etc/init.d/celeryd.sh stop' % env.name, pty=False)


def setup_app_server():
    """
    Setup server applications
    """
    sudo('apt-get update -qq')
    sudo('apt-get install -y -qq build-essential git-core libmysqlclient-dev \
         libxml2-dev libxslt1-dev libmemcached-dev libncurses5-dev \
         python-distribute python-pip python-dev libjpeg-dev libfreetype6-dev \
         liblcms1-dev gettext curl ntp')
    sudo('pip install virtualenv')


def command(arg):
    run_deployer(arg)


@parallel
def clean_pyc_pyo():
    """
    Stop uWSGI and delete all .pyc and .pyo
    """
    run_deployer('find %s -iname \*.pyc -delete' % env.src_path)
    run_deployer('find %s -iname \*.pyo -delete' % env.src_path)


@parallel
def logs(match='*', follow=True, i_want_newrelic_log_lines=False):
    """
    Run tail command in all logs
    """

    log_dir = '%s/logs/' % env.src_path

    app_log_files = '%s/SMSGW_*.log' % log_dir
    celery_log_files = '%s/celery/z-%s*.log' % (log_dir, match)

    if follow:
        args = '-f'

    cmd = 'tail %s %s %s' % (args, app_log_files, celery_log_files)

    if i_want_newrelic_log_lines:
        run_deployer(cmd)
    else:
        run_deployer('%s | %s ' % (cmd, 'grep -vi newrelic'))


def version():
    """
    Get the deployed commit
    """
    with cd(env.src_path):
        run_deployer('git log --pretty=oneline | head -n 1')


@roles("single")
def cancel_consumer(*args):
    management('cancel_consumer', *args)


@roles("single")
def add_consumer(*args):
    management('add_consumer', *args)


def management(*args):
    """
    Run a management command with n arguments
    """
    if len(args) == 0:
        args = ('help', )
    with prefix('source %s/bin/activate' % env.venv_path):

        env_name = env.name
        if env_name.startswith('production'):
            env_name = 'production'

        run_deployer('SMS_GATEWAY_APPLICATION_SETTINGS=%s python %s/manage.py %s' % (
            env_name, env.src_path, ' '.join(args)))


@parallel
def celery_check():
    result = run_deployer('ps ax | grep -i celery | grep -v "grep" | wc -l', quiet=True)
    print('{} running instances.'.format(result))


def run_deployer(command, *args, **kwargs):
    return sudo(
        'env HOME={} {}'.format(
            env.deployer_home, command),
        user=env.deployer_user, group=env.deployer_group, *args, **kwargs)
