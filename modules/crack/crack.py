#!/bin/python3
# -*- coding: utf-8 -*-

crack__auth = 'lasercata'
crack__ver = '1.0.1'
crack__last_update = '21.09.2020'

##-import
#---------Cracker's modules
from modules.base.progress_bars import *
from modules.base.base_functions import chd, list_files, NewLine
from modules.base.console.color import color, cl_inp, cl_out, c_error, c_wrdlt, c_output, c_prog, c_succes

#---------Packages
from random import shuffle
from datetime import datetime as dt
from os import chdir, mkdir, getcwd
from PyQt5.QtWidgets import QMessageBox


##-ini
week_pwd = (
    '!@#$%^&*', '0000', '000000', '1111', '111111', '121212', '123', '123123',
    '1234', '12345', '123456', '1234567', '12345678', '123456789', '1234567890',
    '1qaz2wsx', '2000', '222222', '55555', '654321', '666', '666666', '66666666',
    '6969', '696969', '987654321', 'Football', 'Password', 'abc123', 'access',
    'admin', 'administrateur', 'administrator', 'adobe123', 'amanda', 'andrew',
    'asdfgh', 'ashley', 'asshole', 'austin', 'azerty', 'azertyuiop', 'bailey',
    'baseball', 'batman', 'bigdog', 'biteme', 'buster', 'charlie', 'cheese',
    'chelsea', 'computer', 'corvette', 'cowboy', 'dallas', 'daniel', 'diamond',
    'donald', 'dragon', 'flower', 'football', 'freedom', 'fuck', 'fucker',
    'fuckme', 'fuckyou', 'george', 'ginger', 'golfer', 'hammer', 'harley',
    'heather', 'hello', 'hockey', 'hottie', 'hunter', 'iloveyou', 'jennifer',
    'jessica', 'jesus', 'jordan', 'joshua', 'killer', 'letmein', 'login', 'love',
    'loveme', 'maggie', 'martin', 'master', 'matthew', 'merlin', 'michael',
    'michelle', 'monkey', 'mustang', 'nicole', 'ninja', 'orange', 'p@ssw0rd',
    'p@ssword', 'pass', 'passw0rd', 'password', 'password1', 'password123',
    'patrick', 'pepper', 'photoshop', 'princess', 'pussy', 'qazwsx', 'qwerty',
    'qwerty123', 'qwertyuiop', 'ranger', 'richard', 'robert', 'secret', 'sexy',
    'shadow', 'silver', 'soccer', 'solo', 'sparky', 'starwars', 'summer',
    'sunshine', 'superman', 'taylor', 'test', 'thomas', 'thunder', 'tigger',
    'trustno1', 'welcome', 'whatever', 'william', 'yankees', 'yellow', 'zaq1zaq1'
)


##-functions
#---------chd_wrdlst
def chd_wrdlst():
    '''
    Change current directory to [chd]/Wordlists. Cf to the function chd
    (modules/base/base_functions.py) for more info on the path [chd].

    If folder "Wordlists" doesn't exist, create it.

    Return the old path
    '''

    old_path = chd('.')

    try:
        chdir('Wordlists')

    except FileNotFoundError:
        mkdir('Wordlists')
        print('"Wordlists" folder created at "{}" !'.format(getcwd()))
        chdir('Wordlists')


    return old_path


##-Basic brute-force
class BruteForce:
    '''Class which allow to brute-force some text.'''

    def __init__(self, func, wrdlst, encod='utf-8', interface=None):
        '''
        Initiate the BruteForce class.

        - func : the encrypt function. It should take one arg : txt ;

        - wrdlst : the wordlist to use. If it is a string, try to open the
         corresponding wordlist, else if it is a list, use it ;

        - encod : Wordlist's encoding, if wrdlst is a string ;

        - interface : the interface using this class. Should be None,
         'gui', or 'console'. Used to choose the progress bar.
        '''

        #------tests
        #---interface
        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", or "console", but {} of type {} was found !!!'.format(interface, type(interface)))

        self.interface = interface
        self.encod = encod
        self.func = func

        #---wrdlst
        if type(wrdlst) == str:
            self.wrdlst_typ = 'str'

            try:
                self.lth = sum(1 for line in open(wrdlst, 'rb'))

            except FileNotFoundError:
                raise FileNotFoundError('The wordlist named "{}" was not found !!!'.format(wrdlst))

        elif type(wrdlst) in (list, tuple, set):
            self.wrdlst_typ = 'list'
            self.lth = len(wrdlst)
            wrdlst = list(wrdlst)
            shuffle(wrdlst)

        else:
            raise ValueError('The argument "wrdlst" should be a string, list, set, or a tuple, but a "{}" was found !!!'.format(type(wrdlst)))

        self.wrdlst = wrdlst

        #------creating the progress bar
        if interface == 'console':
            self.pb = ConsoleProgressBar()

        elif interface == 'gui':
            self.pb = GuiProgressBar(title='Brute-forcing... ― Cracker', verbose=True)


    def crack(self, txt):
        '''
        Method which brute-force 'txt' with the selected wordlist, by redirecting
        to the good method.
        '''

        if self.wrdlst_typ == 'str':
            return self._crack_str(txt)

        else:
            return self._crack_lst(txt)


    def _crack_str(self, txt):
        '''
        Method wich brute-force 'txt' by reading the wordlist line by line.

        Return the cracked text if found, None otherwise.
        '''

        with open(self.wrdlst, encoding=self.encod) as f:
            for j, word in enumerate(f):
                word = word.strip('\n')
                word_enc = self.func(word)

                if word_enc == txt:
                    return word #Found !!!

                if self.interface != None:
                    self.pb.set(j, self.lth)

        return None #Not found.


    def _crack_lst(self, txt):
        '''
        Method wich brute-force 'txt' with the list 'self.wrdlst'.

        Return the cracked text if found, None otherwise.
        '''

        for j, word in enumerate(self.wrdlst):
            word_enc = self.func(word)

            if word_enc == txt:
                return word #Found !!!

            if self.interface != None:
                self.pb.set(j, self.lth)

        return None #Not found.



##-Advanced brute-force
class SmartBruteForce:
    '''Class which allow to crack some text.'''

    def __init__(self, func, verbose=True, interface=None):
        '''
        Initiate the SmartBruteForce class.

        - func : The encrypt function. It should take one arg : txt ;
        - verbose : a boolean which indicates if print infos ;
        - interface : the interface using this class. Should be None,
         'gui', or 'console'. Used to choose the progress bar.
        '''

        #------tests
        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", or "console", but {} of type {} was found !!!'.format(interface, type(interface)))

        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')

        #------ini
        self.func = func
        self.verbose = verbose
        self.interface = interface

        #------creating the progress bar
        if interface == 'console':
            self.pb = ConsoleProgressBar()

        elif interface == 'gui':
            self.pb = GuiProgressBar(title='Brute-forcing... ― Cracker', verbose=False)
            self.pb_db = GuiDoubleProgressBar(title='Brute-forcing... ― Cracker')
            self.pb.hide()
            self.pb_db.hide()

        self.pb_sender = None


    def _pb_set(self, i, n, bar=1):
        '''Set the good progress bar to i/n.'''

        if self.interface == None:
            return None #stop

        elif self.interface == 'console':
            self.pb.set(i, n)
            return None

        if self.pb_sender == 'crack':
            self.pb_db.show()
            self.pb_db.set(i, n, bar)

        else:
            self.pb.show()
            self.pb.set(i, n)


    def crack(self, txt):
        '''Try to crack 'txt' using some wordlists.'''

        self.pb_sender = 'crack'

        #------test 1
        self._pb_set(0, 7, 0)

        if self.verbose:
            print('Test 1/7 ― Week passwords list ― {} values'.format(len(week_pwd)))

        for j, k in enumerate(week_pwd):
            if self.func(k) == txt:
                return k

            if self.interface != None:
                self._pb_set(j, len(week_pwd), 1)

        #------test 2
        if self.verbose:
            print('Test 2/7 ― Keyboard sequence ― 1300*4 + 8*20 = 5360 values')

        for alf in (
            'azertyuiopqsdfghjklmwxcvbn', 'AZERTYUIOPQSDFGHJKLMWXCVBN',
            'qwertyuiopasdfghjklzxcvbnm', 'QWERTYUIOPASDFGHJKLZXCVBNM',
            '0123456789', """"²&é"'(-è_çà)=""", '0123456789°+',
            'azertyuiop^$qsdfghjklmù*wxcvbn,;:!'
        ):
            ret = self._keyboard_seq(txt, alf)
            if ret != None:
                return ret

        self._pb_set(2, 7, 0)

        #------test 3
        if self.verbose:
            print('Test 3/7 ― 1-4 letters a-z ― 475 255 values')

        for lth in range(1, 5):
            ret = self.permutation(txt, lth, 'abcdefghijklmnopqrstuvwxyz')
            if ret != None:
                return ret

        self._pb_set(3, 7, 0)

        #------test 4
        if self.verbose:
            print('Test 4/7 ― 1-4 letters A-Z ― 475 255 values')

        for lth in range(1, 5):
            ret = self.permutation(txt, lth, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if ret != None:
                return ret

        self._pb_set(4, 7, 0)

        #------test 5
        if self.verbose:
            print('Test 5/7 ― 1-6 numbers ― 1 111 110 values')

        for lth in range(1, 7):
            ret = self.permutation(txt, lth, '0123456789')
            if ret != None:
                return ret

        self._pb_set(5, 7, 0)

        #------test 6
        if self.verbose:
            print('Test 6/7 ― 1-3 all ― 6 895 291 values')

        for lth in range(1, 4):
            ret = self.permutation(txt, lth, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _&ÃƒÆ’Ã‚Â©~"#\'\\{([-|ÃƒÆ’Ã‚Â¨`ÃƒÆ’Ã‚Â§^ÃƒÆ’ @)Ãƒâ€šÃ‚Â°]=+}$Ãƒâ€šÃ‚Â£Ãƒâ€šÃ‚Â¤Ãƒâ€šÃ‚Â¨ÃƒÆ’Ã‚Â¹%*Ãƒâ€šÃ‚Âµ!Ãƒâ€šÃ‚Â§:/.;?,<>Ã‚Â²')
            if ret != None:
                return ret

        self._pb_set(6, 7, 0)

        #------test 7
        if self.verbose:
            print('Test 7/7 ― Wordlists :')

        old_path = chd_wrdlst()
        wlsts = list_files()
        if len(wlsts) == 0:
            msg = 'The wordlists were not found !!!'

            if self.interface == None:
                print(msg)

            elif self.interface == 'console':
                cl_out(c_error, msg)

            else:
                QMessageBox.critical(None, '!!! Wordlists not found !!!', '<h2>{}</h2>'.format(msg))

        elif self.verbose:
            for k in wlsts:
                if k != wlsts[-1]:
                    print("\t- '{}' ;".format(k))

                else:
                    print("\t- '{}'.".format(k))

        else:
            for k, w in enumerate(wlsts):
                try:
                    ret = BruteForce(self.func, w, interface=self.interface).crack(txt)

                except UnicodeDecodeError:
                    ret = BruteForce(self.func, w, encod='cp437', interface=self.interface).crack(txt)

                if ret != None:
                    chdir(old_path)
                    return ret

                self._pb_set(k, len(wlsts), 1)


        if self.verbose:
            print('Tests finished ― password not found.')

        chdir(old_path)
        self._pb_set(7, 7, 0)
        self.pb_sender = None


    def _keyboard_seq(self, txt, alf='azertyuiopqsdfghjklmwxcvbn'):
        '''Test, using the alphabet, if the text 'txt' match to a linear keyboard sequence.'''

        alf = 2 * alf
        alf_i = alf[::-1]

        nb = len(alf) // 2
        k = 0

        for i in range(nb):
            for j in range(nb):
                word = alf[i:i + j + 1]
                word_i = alf_i[i:i + j + 1]

                for w in (word, word_i):
                    if self.func(w) == txt:
                        return w

                self._pb_set(k, nb **2, 1)
                k += 1


    def permutation(self, txt, lth, alf='0123456789'):
        '''
        Try to crack the text 'txt' with the alf's ordered permutation.
        Do the same as wordlist_generator, but is faster because it doesn't save
        tries in a file.

        - txt : the text to crack ;
        - lth : the length of the formed words ;
        - alf : the alphabet to permute.
        '''

        self.permut_rep = 0
        self.permut_tt_rep = len(alf) **lth

        t0 = dt.now()
        ret = self._permut(txt, lth, alf)
        t_end = dt.now() - t0

        #print('Done in {}s !'.format(t_end))

        return ret


    def _permut(self, txt, lth, alf='0123456789', dw=''):
        '''
        Try to crack the text 'txt' with the alf's ordered permutation.

        - txt : the text to crack ;
        - lth : the length of the formed words ;
        - alf : the alphabet to permute (same as in wordlist generator).

        Don't call this method, but self.permutation, else the progress bar will be wrong.
        '''

        if lth == 1:
            for k in alf:
                word = dw + k

                if self.func(word) == txt:
                    return word

                if self.permut_rep % 2**10 == 0:
                    self._pb_set(self.permut_rep, self.permut_tt_rep, 1)

                self.permut_rep += 1

        else:
            for k in alf:
                pwd = self._permut(txt, lth - 1, alf, dw + k)

                if pwd != None:
                    return pwd



    def brute_force(self, lth, alf='0123456789', type_=str):
        '''
        This method is usefull for one key ciphers.

        It return a dict containing all the decryptions of txt.
        self.func should be a function with one arg (key) and which decrypt some text.
        For example : `lambda key: Gronsfeld(key).decrypt(txt)`.

        Do the same as self.permutation, but instead of encrypting txt, it decrypts
        it with the alf's permutation as key.

        - lth : the length of the formed words ;
        - alf : the alphabet to permute ;
        - type_ : the type of the charaters in the alf. Should be 'str' or 'int'.
         If 'int', try to int every char.
        '''

        self.bf_rep = 0
        self.bf_tt_rep = len(alf) **lth

        self.brk = {}

        t0 = dt.now()
        ret = self._brute_force(lth, alf, type_)
        t_end = dt.now() - t0

        #print('Done in {}s !'.format(t_end))

        return self.brk


    def _brute_force(self, lth, alf, type_, dw=''):
        '''
        Cf self.brute_force for the doc.

        Don't call this method, but self.brute_force, else the progress bar will be wrong.
        '''

        if lth == 1:
            for k in alf:
                if type_ == int:
                    try:
                        key = int(dw + k)

                    except ValueError:
                        key = dw + k

                else:
                    key = dw + k

                self.brk[key] = self.func(key) #todo: add an option to ver_plain_text here.

                if self.bf_rep % 2**10 == 0:
                    self._pb_set(self.bf_rep, self.bf_tt_rep, 1)

                self.bf_rep += 1

        else:
            for k in alf:
                pwd = self._brute_force(lth - 1, alf, type_, dw + k)

                if pwd != None:
                    return pwd


    def brute_force_str(self, lth, alf='0123456789', type_=str, ldm=False):
        '''
        Same as self.brute_force, but return the result in a readable string.

        - ldm : Low Detail Mode. If True, remove the keys which have the same decryption.
        '''

        brk = self.brute_force(lth, alf, type_)

        if ldm:
            old_brk = brk
            brk = {}
            for k in old_brk:
                if old_brk not in brk.values():
                    brk[k] = old_brk[k]

        ret = 'Possible decryptions (key - decryption) :'

        for k in brk:
            ret += NewLine(c='\n\t').text_set('\n\t{} - {}'.format(k, brk[k]))

        return ret






##-Determinist function
def deter(txt, alf='abcdefghijklmnopqrstuvwxyz', only_hash=False):
    '''
    Try to determine which cipher was used to encrypt 'txt'.

    - txt : the encrypted text with the unknow function ;
    - alf : the possible alphabet used ;
    - only_hash : a bool which indicates if you know that 'txt' is a hash.

    Return a tuple containing all the possibles ciphers.
    '''

    lst = []

    if not only_hash:
        #------Crypta
        #---Morse
        c = True
        for k in txt:
            if k not in '-. /':
                c = False
                break

        if c:
            lst.append('Morse')

        #---Ciphers which keep the normal alf
        c = True
        for k in txt:
            if k not in alf:
                c = False
                break

        if c:
            lst.extend(
                ['Reverse code', 'Reverse code word', 'Atbash', 'Albam', 'Achbi',
                'Avgad', 'Tritheme', 'Columnar transposition', 'UBCHI',
                'Monoalphabetic substitution', 'Porta', 'Vigenere', 'Beaufort',
                'Autoclave', 'Playfair', 'ABC', 'Scytale', 'Rail fence', 'Caesar',
                'Gronsfeld', 'Fleissner', 'Hill', 'Four squares', 'Affine']
            )

        #---Polybius
        c = True
        for k in txt:
            if k not in '0123456 ':
                c = False
                break

        if c:
            lst.append('Polybius')


        #---ADFGX
        c = True
        for k in txt:
            if k not in 'ADFGX':
                c = False
                break

        if c:
            lst.append('ADFGX')


        #---ADFGVX
        c = True
        for k in txt:
            if k not in 'ADFGVX':
                c = False
                break

        if c:
            lst.append('ADFGVX')


        #------RSA
        c = True
        for k in txt:
            if k not in '0123456789':
                c = False
                break

        if c:
            lst.append('RSA')


        #------KRIS
        if txt.count(' ') == 1:
            rsa, aes = txt.split(' ')

            if 'RSA' in deter(rsa) and 'AES' in deter(aes):
                lst.append('KRIS')


    #------Hashes
    h = True
    for k in txt:
        if k not in '0123456789abcdef':
            h = False
            break

    if h:
        if not only_hash:
            lst.extend(['AES-256', 'AES-192', 'AES-128'])

        h_lth = { #HashID is so much better...
            'blake2b': 128,
            'blake2s': 64,
            'md4': 32,
            'md5': 32,
            'md5-sha1': 72,
            'ripemd160': 40,
            'sha1': 40,
            'sha224': 56,
            'sha256': 64,
            'sha384': 96,
            'sha3_224': 56,
            'sha3_256': 64,
            'sha3_384': 96,
            'sha3_512': 128,
            'sha512': 128,
            'sha512_224': 56,
            'sha512_256': 64,
            'shake_128': 256,
            'shake_256': 512,
            'sm3': 64,
            'whirlpool': 128
        }

        for k in h_lth:
            if len(txt) == h_lth[k]:
                lst.append(k)


    return tuple(lst)












































