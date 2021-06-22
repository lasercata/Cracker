#!/bin/python3
# -*- coding: utf-8 -*-

'''Initiate the Cracker's global variables.'''

glb__auth = 'Lasercata'
glb__last_update = '31.08.2020'
glb__version = '1.1'

##-import
from os import getcwd
from os.path import expanduser, isdir


##-main
#---------Path vars
Cracker_running_path = getcwd()
Cracker_data_path = Cracker_running_path + '/Data'


#------Interface
with open('{}/interface'.format(Cracker_data_path)) as f:
    interface = f.read()

#------Home mode
if isdir(expanduser('~/.RSA_keys')):
    home = True

else:
    home = False

















































