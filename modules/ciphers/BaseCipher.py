#!/bin/python3
# -*- coding: utf-8 -*-

'''This script define a mother class for the ciphers.'''

BaseCipher__auth = 'Lasercata'
BaseCipher__last_update = '18.01.2021'
BaseCipher__version = '1.0'


##-import
#---------Cracker's modules
from modules.base.progress_bars import *

#---------Packages
#------PyQt5
from modules.base import glb
if glb.interface == 'gui':
    from PyQt5.QtWidgets import QMessageBox


##-main
class BaseCipher:
    '''Mother class for the ciphers.'''

    def __init__(self, cipher=None, pb_mn=0, interface=None):
        '''Initiate self.

        - cipher : The cipher which inherits from this class. Used to name the GUI progress bars ;
        - pb_mn : The GUI progress bar minumum (cf to modules.base.progress_bar) ;
        - interface : The interface using the cipher. Should be None,
         'gui', or 'console'. Used to choose the progress bar.
        '''

        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", \
                or "console", but {} of type {} was found !!!'.format(interface, type(interface)))

        self.interface = interface

        self.cipher = cipher

        #---creating the progress bar
        if interface == 'console':
            self.pb = ConsoleProgressBar()

        elif interface == 'gui':
            self.pb = GuiProgressBar(
                title='Encrypting ... | {} ― Cracker'.format(cipher),
                verbose=True
            )

        self.titles = (
            'Encrypting ... | {} ― Cracker'.format(cipher),
            'Decrypting ... | {} ― Cracker'.format(cipher),
            'Breaking ... | {} ― Cracker'.format(cipher)
        )

    def pb_set(self, i, n, bar='brk'):
        '''Use the 'set' method of the progress bars'''

        if bar not in ('enc', 'dec', 'brk'):
            raise ValueError('"bar" arg should be "enc", "dec", or "brk", but "{}" was found !!!'.format(bar))

        if self.interface == None:
            return None

        elif self.interface == 'gui':
            title = self.titles[('enc', 'dec', 'brk').index(bar)]
            self.pb.setTitle(title)

        self.pb.set(i, n)


    # def encrypt(self, txt=None):
    #     '''This method should be redefined in the sub class, but if it is not
    #     the case, a warning is shown here.
    #     '''
    #
    #     msg = 'Impossible to encrypt using this cipher !!!'
    #
    #     if self.interface == None:
    #         print(msg)
    #
    #     elif self.interface == 'console':
    #         cl_out(c_error, msg)
    #
    #     else:
    #         QMessageBox.critical(None, '!!! Impossible !!!', '<h2>{}</h2>'.format(msg))
    #
    #
    # def decrypt(self, txt=None):
    #     '''This method should be redefined in the sub class, but if it is not
    #     the case, a warning is shown here.
    #     '''
    #
    #     msg = 'Impossible to decrypt using this cipher !!!'
    #
    #     if self.interface == None:
    #         print(msg)
    #
    #     elif self.interface == 'console':
    #         cl_out(c_error, msg)
    #
    #     else:
    #         QMessageBox.critical(None, '!!! Impossible !!!', '<h2>{}</h2>'.format(msg))
    #
    #
    # def break_(self, txt=None):
    #     '''This method should be redefined in the sub class, but if it is not
    #     the case, a warning is shown here.
    #     '''
    #
    #     msg = 'Impossible to break this cipher !!!'
    #
    #     if self.interface == None:
    #         print(msg)
    #
    #     elif self.interface == 'console':
    #         cl_out(c_error, msg)
    #
    #     else:
    #         QMessageBox.critical(None, '!!! Impossible !!!', '<h2>{}</h2>'.format(msg))