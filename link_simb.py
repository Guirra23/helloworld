# -*- coding: utf-8 -*-
import os

logs_dir = '/home/guirra/log'
src = '/home/guirra/aulas/'
link_simb = '/home/guirra/aulas/teste'

if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

# os.chdir(src)
#  if not os.path.exists(link_simb):
#    os.symlink(logs_dir, link_simb)

os.chdir(src)
if not os.path.islink('teste'):
    os.symlink(logs_dir, link_simb)
