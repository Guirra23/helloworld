# -*- coding: utf-8 -*-
import os

src = '/home/guirra/log'
dst = '/home/guirra/aulas/logs'

# This creates a symbolic link on python in tmp directory
os.symlink(src, dst)

print "symlink created"
"""
logs_dir = '/home/guirra/log'
link = '/home/guirra/Documents'

if not os.path.exists(logs_dir):
    os.makedirs('%s' % logs_dir) and os.makedirs('ln -s %s logs' % link)
"""
