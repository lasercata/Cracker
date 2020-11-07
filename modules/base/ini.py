#!/bin/python3
# -*- coding: utf-8 -*-

'''Initiate Cracker's needed data.'''

ini__auth = 'Lasercata'
ini__last_update = '06.11.2020'
ini__version = '1.1.3'

##-import
#---------packages
#------gui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QCloseEvent, QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QStyleFactory,
    QLabel, QGridLayout, QLineEdit, QMessageBox, QWidget, QPushButton, QCheckBox,
    QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget, QTableWidget, QFileDialog,
    QRadioButton, QTextEdit, QButtonGroup, QSizePolicy, QSpinBox, QFormLayout,
    QSlider)

#------other
from os import chdir, getcwd
from os.path import isfile
import sys

from datetime import datetime as dt
from getpass import getpass
from time import sleep

from ast import literal_eval #safer than eval

#---------Cracker modules
try:
    from modules.base.matrix import *
    from modules.base.base_functions import *
    from modules.base.progress_bars import *

    from modules.base.console.color import *
    from modules.base.gui.lock_gui import Lock
    from modules.base.gui.GuiStyle import GuiStyle
    from modules.base.gui.TextEditor import TextEditor
    from modules.base.gui.Popup import Popup

    from modules.crack import crack

    from modules.ciphers.hashes import hasher
    from modules.ciphers.crypta import crypta
    from modules.ciphers.kris import AES, RSA, KRIS

    from modules.wordlists import wordlist_generator as w_gen
    from modules.wordlists.wordlist_analyzer import * #as w_ana

    from modules.prima import prima
    from modules.b_cvrt.b_cvrt import BaseConvert
    from modules.password_testor import pwd_testor
    from modules.anamer0 import anamer0


except ModuleNotFoundError as ept:
    err = str(ept).strip("No module named")

    try:
        cl_out(c_error, 'Put the module ' + err + ' back !!!')

    except NameError:
        print('\nPut the module ' + err + ' back !!!')

    sys.exit()


##-ini
#---------version
try:
    with open('version.txt', 'r') as f:
        cracker_version_0 = f.read()
    cracker_version = ""
    for k in cracker_version_0:
        if not ord(k) in (10, 13):
            cracker_version += k

except FileNotFoundError:
    cl_out(c_error, 'The file "version.txt" was not found. A version will be set but can be wrong.')
    cracker_version = '3.0.0 ?'

else:
    if len(cracker_version) > 16:
        cl_out(c_error, 'The file "version.txt" contain more than 16 characters, so it certainly doesn\'t contain the actual version. A version will be set but can be wrong.')
        cracker_version = '3.0.0 ?'

#---------modules_ver
try:
    with open('versions_modules.txt') as f_:
        modules_ver = f_.read()

except FileNotFoundError: #todo: if not found, use the headers var (i.g. crypta__ver)
    cl_out(c_error, 'The file "versions_modules.txt" was NOT found !!!')
    modules_ver = ''

#---------update_notes (histrory)
try:
    with open('Updates/history.txt') as f_:
        update_notes = f_.read()

except FileNotFoundError:
    cl_out(c_error, 'The file "history.txt" was NOT found !!!')
    update_notes = ''


#---------passwords

#todo: Check if there is a file with this data in ./Data/pwd
#todo + add a salt for passwords ?


pwd_h = 'SecHash'
pwd_loop = 512

try:
    with open('Data/pwd') as f:
        pwd = f.read().strip('\n')

    if len(pwd) != 128:
        raise FileNotFoundError #Set the password to the default

    for k in pwd:
        if k not in '0123456789abcdef':
            raise FileNotFoundError

except FileNotFoundError:
    pwd = '0c0bf58bf97b83c9dd7c260ff3eefea72455d6c7768810cefb41697f266d97f8db06b9bfcce0dd1fa9f3c656b01876bd837f201c9e605ed4d357a22f7aa94cff'

# pwd_h = 'sha512'
# pwd = '6a0cc613e360caf70250b1ddbe169554ddfe9f6edc8b0ec33d61d80d9d0b11090434fcf27d24b40f710bc81e01c05efd78a0086b4673bd042b213e8c7afb4b0c'

#pwd = 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec'

admin_h = 'SecHash'
admin_loop = 512
admin_pwd = '164c53d1a85ae8eff014e162af6ee7dfe6d8eaeb0f01cefcf451b6ed2894c3d4f92903449644db163723e4a77cfac881a562e9285b9f76852fea0417c581d934'

# admin_h = 'sha512'
# admin_pwd = '0e1faf4b92c262ea33c915792b3245b890bc9c30efc3aed327ac559b2731355a8531a2ba7a04efc36eefda6aa64fca6e375e123a4c8c84a856c1121429a6357d'


#---------logo
cracker = r"""
 _______  ______ _______ _______ _     _ _______  ______
 |       |_____/ |_____| |       |____/  |______ |_____/
 |_____  |    \_ |     | |_____  |    \_ |______ |    \_"""
# http://patorjk.com/software/taag/#p=display&f=Cyberlarge&t=Cracker

auth_ascii_lasercata = r"""
       _______ _______ _______  ______ _______ _______ _______ _______
|      |_____| |______ |______ |_____/ |       |_____|    |    |_____|
|_____ |     | ______| |______ |    \_ |_____  |     |    |    |     |"""

auth_ascii_Elerias = r"""
 _______        _______  ______ _____ _______ _______
 |______ |      |______ |_____/   |   |_____| |______
 |______ |_____ |______ |    \_ __|__ |     | ______|"""


#---------Usefull lists/dicts
lst_encod = ('utf-8', 'ascii', 'latin-1')


ciphers_list = {
    'KRIS' : ('KRIS-AES-256', 'KRIS-AES-192', 'KRIS-AES-128'),

    'AES' : ('AES-256', 'AES-192', 'AES-128'),

    'RSA' : ('RSA', 'RSA signature'),

    'Crypta' : tuple(crypta.crypta_ciphers.keys()),

    'analysis' : ('Text analysis', 'Frequence analysis', 'Index of coincidence', \
        'Kasiki examination', "Friedman's test"),

    'hash' : hasher.h_str + ('SecHash',)
}

crack_method_list = ('Brute-force', 'Dictionary attack', 'Advanced brute-force', 'Code break')


prima_algo_list = {
    'Decomposition' : ('Trial division', 'Wheel factorization', "Fermat's factorization", \
    "Pollard's rho", 'p - 1'),

    'Probabilistic' : ("Fermat's test", "Miller-Rabin's test"),

    'Sieves' : ('Sieve of Erathostenes', 'Segmented sieve of Erathostenes')
}

b_cvrt_alf_list = {
    'alf_base10': '0123456789',
    'alf_base16': '0123456789ABCDEF',
    'alf_base32': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    'alf_base32hex': '0123456789ABCDEFGHIJKLMNOPQRSTUV',
    'alf_base36': '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'alf_base62': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
    'alf_base64': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
    'alf_base140': r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿ'
}

crypta_alf_list = {
    'alf_25': crypta.alf_25,
    'alf_az': crypta.alf_az,
    'alf_az09': crypta.alf_az09
}
