#!/bin/python3
# -*- coding: utf-8 -*-

'''Launch Cracker with the menu console interface.'''

Cracker_console__auth = 'Lasercata'
Cracker_console__last_update = '06.11.2020'
Cracker_console__version = '1.2'


##-import/ini
with open('Data/interface', 'w') as f:
    f.write('console')


from modules.base.ini import *


##-helpful functions
def get_text():
    '''
    Return a string cointaining text to process.
    Can read from a file or from the console.
    '''

    src = inp_lst('Read text from file ? (y/n) : ', ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui', 'n', 'no', 'non', 'Non', 'No', 'N', 'NON', 'NO'))

    if src in ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui'):
        while True:
            fn = cl_inp("Enter the file to read's name :")

            try:
                with open(fn) as f:
                    ret = f.read()

            except FileNotFoundError:
                cl_out(c_error, 'The file "{}" was NOT found !!!'.format(fn))

            else:
                break

    else:
        ret = cl_inp('Type your text :')


    return ret


def get_alf():
    '''Return an alphabet.'''

    in_alf = ''
    while in_alf not in (*w_gen.alfs, 'write'):
        in_alf = cl_inp('Which alphabet choose ? \n(a-z ; 0-9 ; a-z, 0-9 ; A-Z ; A-Z, 0-9 ; a-z, A-Z ; a-z, A-Z, 0-9 ; 0-1 ; hex (0-9, A-F) ; spe ; all (a-z, A-Z, 0-9, spe) ; write) :')

    if in_alf == 'write':
        alf = cl_inp('Enter your alphabet (no separator, i.g. "0123abc") :')
        alf = list(alf)

    else:
        alf = w_gen.alfs[in_alf]

    return alf


def get_fn(prompt='Enter the filename :'):
    '''Return the filename, after checking if the file exists.'''

    while True:
        fn = cl_inp(prompt)

        if isfile(fn):
            return fn

        cl_out(c_error, 'The file was NOT found !!!')


def give_text(txt):
    '''Give text to the user, and ask hime to save or not in a file.'''

    cl_out(c_output, txt)

    src = inp_lst('Save text in a file ? (y/n) : ', ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui', 'n', 'no', 'non', 'Non', 'No', 'N', 'NON', 'NO'))

    if src in ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui'):
        while True:
            fn = cl_inp('Enter the file name :')

            if isfile(fn):
                cl_out(c_error, 'The file "{}" already exist !!!'.format(fn))
                ow = inp_lst('Overwrite it ? (y/n) :', ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui', 'n', 'no', 'non', 'Non', 'No', 'N', 'NON', 'NO'))

                if ow in ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui'):
                    break

            else:
                break

        with open(fn, 'w') as f:
            f.write(txt)

        cl_out(c_succes, 'Done !\nThe text has been be wrote in the file "{}".'.format(fn))

    pause()


def use_func(func, *args, **kargs):
    '''Launch the function and avoid Exceptions.'''

    try:
        print('Press ctrl + C to back to menu, anytime.')
        ret = func(*args, **kargs)

    except KeyboardInterrupt:
        cl_out(c_error, '\nKeyboard interrupt.\nBack menu ...')
        sleep(0.5)

    except MemoryError:
        cl_out(c_error, 'Memory Error.\nBack menu ...')
        sleep(0.5)

    except Exception as ept:
        cl_out(c_error, 'An error occurred : ' + str(ept) + '.\nBack menu ...')
        sleep(0.5)

    try:
        return ret

    except UnboundLocalError:
        return None


def pause():
    '''Block the console while the user don't press <enter>.'''

    color(c_succes)
    input('\n---Press <enter> to continue---')
    color(c_prog)


##-main
class CrackerConsole:
    '''Class defining Cracker's console user interface.'''

    def __init__(self):
        '''Initiate the Cracker's console interface.'''

        self.menu_on = True

        self.bf_ciph = (
            'Unknow',
            'Unknow hash',
            *crypta.ciph_sort['0_key'],
            *crypta.ciph_sort['1_key_str'],
            *crypta.ciph_sort['1_key_int'],
            *ciphers_list['hash']
        )

        self.dct_ciph = (
            'Unknow',
            'Unknow hash',
            *crypta.ciph_sort['0_key'],
            *ciphers_list['hash']
        )


    def heading(self):
        '''Print the Cracker's heading (ascii art).'''

        color(c_ascii)
        print(cracker)
        color(c_output)
        print('\nby Lasercata, Elerias')
        print('v' + cracker_version)

        color(c_input)
        print('\\'*60)
        color(c_prog)


    def sep(self, c_out):
        '''Print a separation in the menus.'''

        color(c_input)
        print('    ' + '-' * 16)
        color(c_out)


    def main_menu(self):
        '''Show the main menu'''

        c = ''
        while self.menu_on:
            self.heading()

            color(c_prog)
            print('\nMenu :\n')

            color(c_error)
            print('    0.Quit')
            print('    l.Lock')

            self.sep(c_ascii)

            print('    1.Crack menu')
            print('    2.Cipher menu')
            print('    3.Wordlists menu')
            print('    4.Prima menu')
            print('    5.Base convert')
            print('    6.Test your password\'s strenth')
            print('    7.Get info on a french phone number')

            self.sep(c_wrdlt)

            print('    8.Settings menu')

            color(c_prog)
            print('\nYour choice :')

            color(c_input)
            c = input('>')
            color(c_prog)

            if c not in ('quit', 'exit', 'q', 'l', *[str(k) for k in range(9)]):
                cl_out(c_error, '"{}" is NOT an option of this menu !!!'.format(c))
                sleep(0.5)

            elif c.lower() == 'l':
                self.lock(pwd)

            elif c == '1':
                use_func(self.crack_menu)

            elif c == '2':
                use_func(self.cipher_menu)

            elif c == '3':
                use_func(self.wordlists_menu)

            elif c == '4':
                use_func(prima.use, True)

            elif c == '5':
                use_func(use_b_cvrt)

            elif c == '6':
                use_func(pwd_testor.use)

            elif c == '7':
                use_func(use_anamer0)

            elif c == '8':
                use_func(self.stng_menu)


            elif c in ('quit', 'exit', 'q', '0'):
                self.quit(c)


    #------Crack
    #---main crack menu
    def crack_menu(self):
        '''Show the crack menu.'''

        c = ''
        while c.lower() not in ('quit', 'exit', '0', 'q'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nCrack menu :\n')

            color(c_error)
            print('    0.Main menu')

            self.sep(c_ascii)

            for j, k in enumerate(crack_method_list):
                print('    {}.{}'.format(j + 1, k))

            color(c_prog)

            c = cl_inp('Your Choice :')

            if c.lower() not in ('quit', 'exit', '0', 'q', '1', '2', '3', '4'):
                cl_out(c_error, '"{}" is NOT an option of this menu !!!'.format(c))
                sleep(0.5)

            elif c == '1':
                use_func(self.brute_force_menu)

            elif c in ('2', '3'):
                meth = crack_method_list[int(c) - 1]
                use_func(self.da_abf_menu, meth)

            elif c == '4':
                use_func(self.code_break_menu)


    #---Brute-force menu
    def brute_force_menu(self):
        '''Show brute-force menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nBrute-force menu :\n')

            color(c_error)
            print('    0.Crack menu')

            self.sep(c_ascii)

            for j, k in enumerate(self.bf_ciph):
                print('    {}.{}'.format(j + 1, k))

                if j in (1, 23):
                    self.sep(c_ascii)

            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', *[str(k) for k in range(45)], *self.bf_ciph):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c in (*[str(k) for k in range(1, 45)], *self.bf_ciph):
                if c not in self.bf_ciph:
                    ciph = self.bf_ciph[int(c) - 1]

                else:
                    ciph = c

                use_func(UseCrack('Brute-force', ciph).crack)


    #---Dictionary attack / Advanced brute-force menu
    def da_abf_menu(self, meth):
        '''Show Dictionary attack / Advanced brute-force menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\n{} menu :\n'.format(meth))

            color(c_error)
            print('    0.Crack menu')

            self.sep(c_ascii)

            for j, k in enumerate(self.dct_ciph):
                print('    {}.{}'.format(j + 1, k))

                if j in (1, 9):
                    self.sep(c_ascii)

            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', *[str(k) for k in range(45)], *self.dct_ciph):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c in (*[str(k) for k in range(1, 45)], *self.dct_ciph):
                if c not in self.dct_ciph:
                    ciph = self.dct_ciph[int(c) - 1]

                else:
                    ciph = c

                use_func(UseCrack(meth, ciph).crack)


    #---Code break menu
    def code_break_menu(self):
        '''Show Code break menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nCode break menu :\n')

            color(c_error)
            print('    0.Crack menu')

            self.sep(c_ascii)

            for j, k in enumerate(crypta.broken_ciph):
                print('    {}.{}'.format(j + 1, k))

            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', *[str(k) for k in range(45)], *crypta.broken_ciph):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c in (*[str(k) for k in range(1, 45)], *crypta.broken_ciph):
                if c not in crypta.broken_ciph:
                    ciph = crypta.broken_ciph[int(c) - 1]

                else:
                    ciph = c

                use_func(UseCrack('Code break', ciph).crack)


    #------Cipher
    #---main cipher menu
    def cipher_menu(self):
        '''Show the cipher menu.'''

        c = ''
        while c.lower() not in ('quit', 'exit', '0', 'q'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nCipher menu :\n')

            color(c_error)
            print('    0.Main menu')

            i = 1
            ciphers_list['RSA'] = ('RSA', 'RSA signature', 'RSA keys management menu ...')
            for ciph in ciphers_list:
                if ciph not in ('Crypta', 'hash'):
                    self.sep(c_ascii)

                    for k in ciphers_list[ciph]:
                        print('    {}.{}'.format(i, k))
                        i += 1

            self.sep(c_ascii)
            print('    {}.Crypta ciphers ...'.format(i))
            self.sep(c_ascii)
            print('    {}.Hashes ...'.format(i + 1))

            ciphers_list['RSA'] = ('RSA', 'RSA signature')

            color(c_prog)

            c = cl_inp('Your Choice :')

            if c.lower() not in ('quit', 'exit', 'q', *[str(k) for k in range(17)]):
                cl_out(c_error, '"{}" is NOT an option of this menu !!!'.format(c))
                sleep(0.5)

            elif c in ('1', '2', '3'): #KRIS
                AES_md = (256, 192, 128)[int(c) - 1]
                use_func(use_kris, AES_md)

            elif c in ('4', '5', '6'): #AES
                AES_md = (256, 192, 128)[int(c) - 4]
                use_func(use_AES, AES_md)

            elif c == '7': #RSA
                use_func(use_RSA)

            elif c == '8': #RSA Sign
                use_func(use_RSA_Sign)

            elif c == '9': #RSA keys management
                use_func(self.RSA_keys_menu)

            elif c in ('10', '11', '12', '13', '14'):
                use_func(use_txtana, c)

            elif c == '15': #Crypta
                use_func(self.crypta_menu)

            elif c == '16': #Hashes
                use_func(self.hash_menu)


    #---RSA keys menu
    def RSA_keys_menu(self):
        '''Show the RSA keys menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nRSA key management menu :\n')

            color(c_error)
            print('    0.Cipher menu')

            self.sep(c_ascii)

            print('    1.Generate new keys')
            print('    2.Export to public key')
            print('    3.Show infos about keys')
            print('    4.Rename keys')
            print('    5.Convert keys')
            print('    6.Show keys')
            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', '0', '1', '2', '3', '4', '5', '6'):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c == '1':
                use_func(use_gen_k)

            elif c == '2':
                use_func(use_exp_k)

            elif c == '3':
                use_func(use_info_k)

            elif c == '4':
                use_func(use_rn_k)

            elif c == '5':
                use_func(use_cvrt_k)

            elif c == '6':
                use_func(use_show_k)


    #---Hash menu
    def hash_menu(self):
        '''Show the hash menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nHash menu :\n')

            color(c_error)
            print('    0.Cipher menu')

            self.sep(c_ascii)

            for j, k in enumerate(ciphers_list['hash']):
                print('    {}.{}'.format(j + 1, k))

            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', *[str(k) for k in range(23)], *ciphers_list['hash']):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c in (*[str(k) for k in range(1, 23)], *ciphers_list['hash']):
                if c not in ciphers_list['hash']:
                    h = ciphers_list['hash'][int(c) - 1]

                else:
                    h = c

                use_func(use_hash, h)


    #---Crypta menu
    def crypta_menu(self):
        '''Show the hash menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nCrypta menu :\n')

            color(c_error)
            print('    0.Cipher menu')

            self.sep(c_ascii)

            for j, k in enumerate(ciphers_list['Crypta']):
                print('    {}.{}'.format(j + 1, k))

            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('quit', 'exit', 'q', *[str(k) for k in range(30)], *ciphers_list['Crypta']):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c in (*[str(k) for k in range(1, 30)], *ciphers_list['Crypta']):
                if c not in ciphers_list['Crypta']:
                    ciph = ciphers_list['Crypta'][int(c) - 1]

                else:
                    ciph = c

                use_func(use_crypta, ciph)


    #------Wordlists
    def wordlists_menu(self):
        '''Show the wordlist menu.'''

        c = ''
        while c not in ('quit', 'exit', 'q', '0'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nWordlists menu :\n')

            color(c_error)
            print('    0.Main menu')

            self.sep(c_ascii)

            print('    1.Generate a wordlist')
            print('    2.Open a wordlist')
            color(c_prog)

            c = ''
            c = cl_inp('Your Choice :')


            if c not in ('0', '1', '2', 'q'):
                cl_out(c_error, '"{}" is NOT an option of this menu !'.format(c))
                sleep(0.5)

            elif c == '1':
                use_func(use_wrdlst_gen)

            elif c == '2':
                use_func(use_wrdlst_ana)


    #------Settings
    def stng_menu(self):
        '''Show the Settings menu.'''

        c = ''
        while c.lower() not in ('quit', 'exit', '0', 'q'):

            color(c_succes)
            print('')
            print('\\'*50)

            color(c_prog)
            print('\nSettings menu :\n')

            color(c_error)
            print('    0.Main menu')

            self.sep(c_ascii)

            print('    1.Change directory')
            print('    2.Change colors')
            print('    3.Change password')
            print('    4.Show infos about Cracker')

            color(c_prog)

            c = cl_inp('Your Choice :')

            if c.lower() not in ('quit', 'exit', '0', 'q', '1', '2', '3', '4'):
                cl_out(c_error, '"{}" is NOT an option of this menu !!!'.format(c))
                sleep(0.5)

            elif c == '1':
                use_func(self.cd)

            elif c == '2':
                use_func(c_color)

            elif c == '3':
                use_func(change_pwd)

            elif c == '4':
                use_func(self.about)



    def about(self):
        '''Show infos about Cracker.'''

        msg = '''
Cracker is a software developed and updated by Lasercata and by Elerias. It is written in Python 3 and in C.



This software is a toolbox application that allow you to do many things : you can encrypt
securely a secret message using one of the many ciphers presents in Cracker (KRIS, AES, RSA, ...),
sign it with a hash function, decrypt it.

If you have a message without the key, but you need to read the content, you can try to
crack it using a wordlist that you made with Cracker, or let the algorithm try to crack
it using its wordlist bank.

You don't remember which was your favourite wordlist ? Don't worry ! You can analyze
them with the wordlist tab to get numerous informations on them.

You need to convert a number from binary to hexadecimal ? You need to do a special convertion
using your own base alphabet ? Check the "Base convert" tab.

Like you can see, there is a lot of functions, often about cracking. But Cracker
can also help to improve your security : if you need a strong password, hard to be
cracked by brute-force, the "P@ssw0rd_Test0r" tab is for you ! It gives a lot of informations
about the password you entered, like its entropy.
        '''

        msg += '\n\nVersions :{}'.format(indent(modules_ver))

        print(msg)
        pause()



    def cd(self):
        '''Change the directory.'''

        cl_out_2(c_prog, 'Current working directory :', c_input, '\t' + getcwd())

        try:
            path = cl_inp('Path of the new repertory (0 or <ctrl + C> to abort) (/ between folders) :')

            if path in ('0', ''):
                cl_out(c_error, 'Aborting ...\nBack menu ...')

            else:
                chdir(path)

        except FileNotFoundError:
            cl_out(c_error, 'The path was NOT found !\nBack menu ...')

        else:
            cl_out(c_succes, 'Success !!!')


        sleep(0.5)



    def lock(self, pwd=pwd, pwd_hash=pwd_h, pwd_l=pwd_loop, mx=3):
        '''put self.lock in a try block, to exit if <ctrl + C> was pressed..'''

        try:
            self._lock(pwd, pwd_hash, pwd_l, mx)

        except KeyboardInterrupt:
            cl_out(c_error, 'Quitting ...')
            sleep(0.25)
            sys.exit()

    def _lock(self, pwd=pwd, pwd_hash=pwd_h, pwd_l=pwd_loop, mx=3):
        '''Lock the app with the password, after clearing the console.'''

        cls()

        while True:
            self.heading()
            print('\nEnter your password :')
            color(c_input)
            inp = getpass('>')
            color(c_prog)

            h_inp = hasher.Hasher(pwd_hash, pwd_loop).hash(inp)

            mx -= 1

            if h_inp == pwd:
                cl_out(c_succes, 'Good password !')
                sleep(0.25)
                cls()
                break

            elif mx > 0:
                cls()
                cl_out(c_error, 'Bad password !!!\nOnly {} tries remaining !!!'.format(mx))
                sleep(0.3)

            if mx == 0:
                cls()
                cl_out(c_error, 'Bad password !!!\nIt was your last try.'.format(mx))
                sleep(1)
                sys.exit()



    def quit(self, menu_choice):
        '''Quit Cracker.'''

        sure = ''
        if menu_choice not in ('quit', 'q'): #tap 'q' or 'quit' to exit faster (don't need to confirm)
            try:
                while sure not in ('y', 'n'):
                    color(c_error)
                    sure = input('\nAre you sure ? (y/n) :\n>')
                    color(c_prog)

            except KeyboardInterrupt:
                self.quit(menu_choice)

        if sure == 'y' or menu_choice in ('quit', 'q'):
            cl_out(c_output, 'By Lasercata, Elerias')
            sleep(0.15)
            cl_out(c_ascii, auth_ascii_Elerias)
            sleep(0.30)
            cl_out(c_ascii, auth_ascii_lasercata)
            sleep(0.5)
            cl_out(c_error, 'Quitting ...')
            sleep(0.25)

            self.menu_on = False

        else:
            print('\nBack menu ...')
            #self.menu_choice = False



    def use():
        '''Use this function to launch the console app'''

        app = CrackerConsole()
        app.lock()

        while app.menu_on:
            try:
                app.main_menu()

            except KeyboardInterrupt:
                app.quit('exit')




##-Using functions
#---------Crack
#------Brute-force
def use_brute_force(ciph):
    '''Try to crack text by brute-force.'''

    #---get user's infos
    txt = get_text()
    lth = inp_int("Generated words' length :")
    alf = get_alf()


    #---get the cipher
    if ciph in ciphers_list['hash']:
        C = hasher.Hasher(ciph).hash
        prnt = 'hash'

    elif ciph in crypta.ciph_sort['0_key']:
        C = crypta.make_ciph(ciph, interface='console').encrypt
        prnt = 'cipher'

    elif ciph in (*crypta.ciph_sort['1_key_int'], *crypta.ciph_sort['1_key_str']):
        C = lambda key: crypta.crypta_ciphers[ciph](key).decrypt(txt)
        prnt = 'cipher'


    #---crack the text
    if ciph in ciphers_list['hash'] + crypta.ciph_sort['0_key']:
        pwd = crack.SmartBruteForce(
            C,
            interface='console'
        ).permutation(txt, lth, alf)

    elif ciph in crypta.ciph_sort['1_key_str']:
        #-check the alphabet, to know if there is numbers in
        for k in alf:
            if k in '0123456789':
                cl_out(c_error, "There is at least one number in your alphabet, but that's useless since the cipher only takes string keys.")
                return -3

        brk = crack.SmartBruteForce(C, interface='console').brute_force_str(lth, alf, str, ldm=True)

        self._ret_append(brk, ciph)

    elif ciph in crypta.ciph_sort['1_key_int']:
        #-check the alphabet
        for k in alf:
            if k not in '0123456789':
                cl_out(c_error, "There is at least one character which is not a number in your alphabet, so that's useless since the cipher only takes numbers keys.")
                return -3

        brk = crack.SmartBruteForce(C, interface='console').brute_force_str(lth, alf, int, ldm=True)

        self._ret_append(brk, ciph)



class UseCrack:
    '''Use the Crack part.'''

    def __init__(self, meth, ciph):
        '''Initiate this class.'''

        self.meth = meth
        self.ciph = ciph

        self.msg_f = '\n\tThe clear text has not be found.' #Message False (not found)


    def _ret_append(self, txt, ciph=None):
        '''Append 'txt' to the console, adding some info behind.'''

        if ciph == None:
            ciph = self.ciph

        sep = '\n' + '―'*20 + '\n'

        cl_out(
            c_output,
            '{}{} - {} on {} : {}\n'.format(
                sep,
                str(dt.now())[:-7],
                self.meth,
                ciph,
                txt
            )
        )
        pause()


    def _crack(self, C, ciph=None, f_verbose=True):
        '''Try to crack the text.'''

        if ciph == None:
            ciph = self.ciph

        pwd = False

        if self.meth == 'Brute-force':
            if ciph in ciphers_list['hash'] + crypta.ciph_sort['0_key']:
                pwd = crack.SmartBruteForce(
                    C,
                    interface='console'
                ).permutation(self.txt, self.wlst_lth, self.wlst_alf)

            elif ciph in crypta.ciph_sort['1_key_str']:
                #------check the alphabet, to know if there is numbers in
                for k in self.wlst_alf:
                    if k in '0123456789':
                        cl_out(c_error, "There is at least one number in your alphabet, but that's useless since the cipher only takes string keys.")
                        return -3

                brk = crack.SmartBruteForce(C, interface='console').brute_force_str(self.wlst_lth, self.wlst_alf, str, ldm=True)

                self._ret_append(brk, ciph)

            elif ciph in crypta.ciph_sort['1_key_int']:
                #------check the alphabet
                for k in self.wlst_alf:
                    if k not in '0123456789':
                        cl_out(c_error, "There is at least one character which is not a number in your alphabet, so that's useless since the cipher only takes numbers keys.")
                        return -3

                brk = crack.SmartBruteForce(C, interface='console').brute_force_str(self.wlst_lth, self.wlst_alf, int, ldm=True)

                self._ret_append(brk, ciph)

        elif self.meth == 'Dictionary attack':
            pwd = crack.BruteForce(C, self.wrdlst, interface='console').crack(self.txt)

        elif self.meth == 'Advanced brute-force':
            pwd = crack.SmartBruteForce(C, interface='console').crack(self.txt)


        if pwd == False:
            pass

        elif pwd == None:
            self._ret_append(self.msg_f, ciph)

        else:
            self._ret_append('\n\t{}.'.format(NewLine(c='\n\t').set('{} ===> {}'.format(pwd, self.txt))), ciph)

            return pwd


    def crack(self):
        '''Method which use the Crack part.'''

        self.txt = get_text()

        if self.meth == 'Brute-force':
            self.wlst_lth = inp_int("Generated words' length :")
            self.wlst_alf = get_alf()

        elif self.meth == 'Dictionary attack':
            self.wrdlst = get_fn("Wordlist's name :")


        self.t0 = dt.now()

        if self.ciph not in ('Unknow', 'Unknow hash'):
            #------get the encryption function
            if self.ciph in ciphers_list['hash']:
                C = hasher.Hasher(self.ciph).hash
                self.prnt = 'hash'

            elif self.ciph in crypta.ciph_sort['0_key']:
                C = crypta.make_ciph(self.ciph, interface='console').encrypt
                self.prnt = 'cipher'

            elif self.ciph in (*crypta.ciph_sort['1_key_int'], *crypta.ciph_sort['1_key_str']):
                C = lambda key: crypta.crypta_ciphers[self.ciph](key).decrypt(self.txt)
                self.prnt = 'cipher'


            if self.meth in ('Brute-force', 'Dictionary attack', 'Advanced brute-force'):
                ret = self._crack(C)
                if ret == -3:
                    return -3


            elif self.meth == 'Code break':
                C = crypta.make_ciph(self.ciph, interface='console')

                if self.ciph in crypta.broken_ciph_dict['break_']:
                    try:
                        brk = C.break_(self.txt)

                    except Exception as ept:
                        cl_out(c_error, 'An error occurred : {}.\nBack menu ...'.format(ept))
                        return -3

                    self._ret_append('\n\t{}'.format(NewLine(c='\n\t').set('{} ===> {}'.format(brk, self.txt))))

                else:
                    brk = C.brute_force(self.txt)
                    m = C.meaning(self.txt, brk)

                    if m[0] == False:
                        answer = inp_lst('The list of broken word does not seem to contain something which makes sense.\nShow the list anyway ? (y/n) :', ('y', 'n'))

                        if answer == 'y':
                            ret = 'Possible decryptions (key - decryption) :'
                            for k in brk:
                                ret += NewLine(80, c='\n\t').text_set('\n\t{} - {}'.format(k, brk[k]))

                            self._ret_append(ret)

                        else:
                            self._ret_append(self.msg_f)

                    else:
                        self._ret_append('\n\t{}'.format(NewLine(c='\n\t').set('{} ===> {}'.format(m, self.txt)))) #todo: improve this return : it just show the list (True, txt_c, [key, [alf]])


        elif self.ciph == 'Unknow':
            pos_algo = crack.deter(self.txt)

            if pos_algo == ():
                cl_out(c_error, 'It is impossible to identify the cipher !!!')
                return -3

            self._ret_append('\nPossibles used algorithms :' + set_lst(pos_algo))

            rep = inp_lst('Try to crack these ciphers ? (y/n) :', ('y', 'n'))

            if rep == 'n':
                return -3

            for k in pos_algo:
                if k in ciphers_list['hash']:
                    C = hasher.Hasher(k).hash
                    self.prnt = 'hash'

                elif k in crypta.ciph_sort['0_key']:
                    C = crypta.make_ciph(k, interface='console').encrypt
                    self.prnt = 'cipher'

                elif k in (*crypta.ciph_sort['1_key_int'], *crypta.ciph_sort['1_key_str']):
                    C = lambda key: crypta.crypta_ciphers[k](key).decrypt(self.txt)
                    self.prnt = 'cipher'

                else:
                    C = None
                    self.prnt = None
                    print('Not trying to crack with the {} cipher.'.format(k))


                if C != None:
                    print(k)
                    ret = self._crack(C, ciph=k, f_verbose=False)

                    if ret not in (-3, None):
                        break


        else: #self.ciph == 'Unknow hash'
            pos_hash = crack.deter(self.txt, only_hash=True)

            if pos_hash == ():
                cl_out(c_error, 'It is impossible to identify the hash !!!')
                return -3

            self._ret_append('\nPossibles used hashes :' + set_lst(pos_hash))

            rep = inp_lst('Try to crack these hashes ? (y/n) :', ('y', 'n'))

            if rep == 'n':
                return -3

            for k in pos_hash:
                print(k)
                C = hasher.Hasher(k).hash
                ret = self._crack(C, 'hash', algo=k, f_verbose=False)

                if ret not in (-3, None):
                    break



#---------Cipher
#------KRIS
def use_kris(AES_mode):
    '''Collect infos to encrypt/decrypt with KRIS.'''

    md = inp_lst('Encrypt or decrypt ? (e/d) :', ('e', 'd'))
    msg = get_text()

    keys = (RSA.list_keys('all'), RSA.list_keys('pvk_without_pbk'))[md == 'd']
    key = inp_lst('Available keys :\n\t{}.\n\nChosen key :'.format(NewLine(c='\n\t').text_set(set_prompt(keys))), keys)

    try:
        C = KRIS.Kris(key, AES_mode, interface='console')

    except FileNotFoundError: #Key not found
        return -3

    if md == 'e':
        msg_ = C.encrypt(msg)
        msg_ = '{} {}'.format(msg_[0], msg_[1])

    else:
        try:
            msg_ = C.decrypt(msg.split(' '), True)

        except ValueError:
            return -3 #The error message is printed in Kris.

    give_text(msg_)


#------AES
def use_AES(AES_mode):
    '''Collect infos to encrypt/decrypt with AES.'''

    md = inp_lst('Encrypt or decrypt ? (e/d) :', ('e', 'd'))
    msg = get_text()
    key = cl_inp('Key :')


    try:
        C = AES.AES(AES_mode, key, False)

    except ValueError as err:
        cl_out(c_error, str(err))

    if md == 'e':
        msg_ = C.encryptText(msg, mode_c='hexa')

    else:
        msg_ = C.decryptText(msg, mode_c='hexa')

    give_text(msg_)


#------RSA
def use_RSA():
    '''Collect infos to encrypt/decrypt with RSA.'''

    md = inp_lst('Encrypt or decrypt ? (e/d) :', ('e', 'd'))
    msg = get_text()

    keys = RSA.list_keys('all')
    key = inp_lst('Available keys :\n\t{}.\n\nChosen key :'.format(NewLine(c='\n\t').text_set(set_prompt(keys))), keys)


    C = RSA.RSA(key, interface='console')

    if md == 'e':
        msg_ = C.encrypt(msg)

    else:
        msg_ = C.decrypt(msg)

    give_text(msg_)


#------RSA Sign
def use_RSA_Sign():
    '''Collect infos to sign/check with RSA Sign.'''

    md = inp_lst('Sign or check ? (s/c) :', ('s', 'c'))
    msg = get_text()

    keys = RSA.list_keys('all')
    key = inp_lst('Available keys :\n\t{}.\n\nChosen key :'.format(NewLine(c='\n\t').text_set(set_prompt(keys))), keys)

    C = RSA.RsaSign(key, interface='console')

    if md == 's':
        cl_out(c_output, C.str_sign(msg))

    else:
        if C.str_check(msg):
            cl_out(c_succes, 'The signature match to the message.')

        else:
            cl_out(c_error, 'The signature does not match to the message !\nYou may not have selected the right RSA key, or the message was modified before you received it !!!')

    pause()


#------RSA keys management
#---Generate RSA keys
def use_gen_k():
    '''Generate RSA keys.'''

    while True:
        size = inp_int("Keys' size (2048 at least is recomended) :")

        if 512 < size < 5120:
            break

        else:
            cl_out(c_error, 'The size must be in [512 ; 5120] !!!')

    name = cl_inp("Keys' name :")

    stg_md = inp_lst('Store in decimal, or in hexadecimal (default is hexa, it takes less storage space) ? (d/h) :', ('d', 'h', ''))

    stg = ('dec', 'hexa')[stg_md in ('h', '')]


    ret = RSA.RsaKeys(name).generate(size, md_stored=stg)

    if ret == -2:
        cl_out(c_error, 'The set of keys already exists !!!')

        ow = inp_lst('Overwrite it ? (y/n) :', ('y', 'n'))
        if ow == 'y':
            ret = RSA.RsaKeys(name, 'console').generate(size, md_stored=stg, overwrite=True)

        else:
            return -3 #Abort

    cl_out(c_succes, 'Done !')
    print('Your brand new RSA keys "{}" are ready !\n`n` size : {} bits.'.format(name, ret[2]))
    pause()


#---Export RSA keys
def use_exp_k():
    '''Export RSA keys.'''

    pvk = RSA.list_keys('pvk_without_pbk')

    print('Full keys :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(pvk))), sp=False)

    key = inp_lst('Select a key :', pvk)

    stg_md = inp_lst('Store in decimal, or in hexadecimal (default is hexa, it takes less storage space) ? (d/h) :', ('d', 'h', ''))

    stg = ('dec', 'hexa')[stg_md in ('h', '')]


    ret = RSA.RsaKeys(key, 'console').export(stg)

    if ret == -1:
        cl_out(c_error, 'The full keys were NOT found !!!')

    else:
        cl_out(c_succes, 'The keys "{}" have been be exported !'.format(key))

    sleep(0.5)


#---infos
def use_info_k():
    '''Choose a key and show infos on it.'''

    key_list = RSA.list_keys('all')

    print('Full keys :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(key_list))), sp=False)

    k_name = inp_lst('Select a key :', key_list)


    keys = RSA.RsaKeys(k_name, 'console')

    md_stg = keys.show_keys(get_stg_md=True)

    if md_stg == -1:
        cl_out(c_error, 'The keys were NOT found !!!')
        return -1 #File not found

    lst_keys, lst_values, lst_infos = keys.show_keys()

    if len(lst_infos) == 2: #Full keys
        (pbk, pvk), (p, q, n, phi, e, d), (n_strth, date_) = lst_keys, lst_values, lst_infos

        prnt = 'The keys were created the ' + date_
        prnt += '\nThe n\'s strenth : ' + n_strth + ' bytes ;\n'

        prnt += '\n\nValues :\n\tp : ' + str(p) + ' ;\n\tq : ' + str(q) + ' ;\n\tn : ' + str(n)
        prnt += ' ;\n\tphi : ' + str(phi) + ' ;\n\te : ' + str(e) + ' ;\n\td : ' + str(d) + ' ;\n'

        prnt += '\n\tPublic key : ' + str(pbk) + ' ;'
        prnt += '\n\tPrivate key : ' + str(pvk) + '.'

    else: #Public keys
        pbk, (n, e), (n_strth, date_, date_exp) = lst_keys, lst_values, lst_infos

        prnt = 'The keys were created the ' + date_ + '\nAnd exported the ' + date_exp
        prnt += '\nThe n\'s strenth : ' + n_strth + ' bytes ;\n'

        prnt += '\n\nValues :\n\tn : ' + str(n) + ' ;\n\te : ' + str(e) + ' ;\n'

        prnt += '\n\tPublic key : ' + str(pbk) + '.'

    cl_out(c_output, prnt)
    pause()


#---Rename keys
def use_rn_k():
    '''Ask for the new name and rename RSA keys.'''

    key_list = RSA.list_keys('all')

    print('Keys :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(key_list))), sp=False)

    k_name = inp_lst('Select a key :', key_list)

    new_name = cl_inp('Enter the new name :')

    ret = RSA.RsaKeys(k_name, 'console').rename(new_name)

    if ret == -1:
        cl_out(c_error, 'The keys were NOT found !!!')

    else:
        cl_out(c_succes, 'The keys "{}" have been be renamed "{}" !'.format(k_name, new_name))

    sleep(0.5)


#---Convert keys
def use_cvrt_k():
    '''Ask for the key and convert it.'''

    stg_md = inp_lst('Is the key stored in decimal, or in hexadecimal ? (d/h) :', ('d', 'h'))

    stg = ('dec', 'hexa')[stg_md == 'h']

    if stg_md == 'h':
        k_lst = (*RSA.list_keys('pvk_hex'), *RSA.list_keys('pbk_hex'))
        prnt = 'Hexa keys :'

    else:
        k_lst = (*RSA.list_keys('pvk'), *RSA.list_keys('pbk'))
        prnt = 'Decimal keys :'

    print(prnt, end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(k_lst))), sp=False)

    k_name = inp_lst('Select a key :', k_lst)

    ret = RSA.RsaKeys(k_name, 'console').convert()

    if ret == -1:
        cl_out(c_error, 'The full keys were NOT found !!!')

    elif ret == -2:
        cl_out(c_error, 'The keys already exists !!!')

    else:
        cl_out(c_succes, 'The keys "{}" have been be converted in {} !'.format(k_name, stg))

    sleep(0.5)


#---Show keys
def use_show_k():
    '''Show the keys.'''

    pvk_d = RSA.list_keys('pvk')
    pvk_h = RSA.list_keys('pvk_hex')
    pbk_d = RSA.list_keys('pbk')
    pbk_h = RSA.list_keys('pbk_hex')
    all_ = RSA.list_keys('all')

    print('\nFull keys stored in decimal :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(pvk_d))), sp=False)

    print('\nFull keys stored in hexadecimal :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(pvk_h))), sp=False)

    print('\nPublic keys stored in decimal :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(pbk_d))), sp=False)

    print('\nPublic keys stored in hexadecimal :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(pbk_h))), sp=False)


    print('\nAll keys :', end='')
    cl_out(c_output, '\n\t{}'.format(NewLine(c='\n\t').text_set(set_prompt(all_))), sp=False)

    pause()


#------Crypta
def use_crypta(ciph):
    '''Collect infos to encrypt/decrypt with Crypta ciphers.'''

    #---questions
    #-encrypt/decrypt, text
    md = inp_lst('Encrypt or decrypt ? (e/d) :', ('e', 'd'))
    msg = get_text()

    #-key.s
    key = None
    key2 = None

    if ciph in crypta.ciph_sort['1_key_str']:
        key = cl_inp('Enter the key :')

    elif ciph in crypta.ciph_sort['1_key_int']:
        key = inp_int('Enter the int key :')

    elif ciph in crypta.ciph_sort['2_key_str']:
        key = cl_inp('Enter the first key :')
        key2 = cl_inp('Enter the second key :')

    elif ciph in crypta.ciph_sort['2_key_int']:
        key = inp_int('Enter the first int key :')
        key2 = inp_int('Enter the second int key :')

    elif ciph == 'Fleissner':
        key = []
        size = inp_int('Side size of the grid :')
        print('\n1 for whole else 0\nExample of a line : 0010')

        for k in range(size):
            while True:
                l = list(cl_inp('Line {} :'.format(k + 1)))
                err = False

                if len(l) != size:
                    cl_out(c_error, 'Not the right size !!! Please retry !')
                    err = True

                for i in l:
                    if i not in ('0', '1'):
                        cl_out(c_error, 'the line can only contain "0" and "1", but "{}" was found !!!'.format(i))
                        err = True
                        break

                if not err:
                    break

            key.append(l)

        print(Matrix(key))

    elif ciph == 'Hill':
        key = []
        size = inp_int('Dimension of the square matrix :')
        print('\nExample of a line for size 4 : 9534')

        for k in range(size):
            while True:
                l = list(cl_inp('Line {} :'.format(k + 1)))
                err = False

                if len(l) != size:
                    cl_out(c_error, 'Not the right size !!! Please retry !')
                    err = True

                l2 = []
                for i in l:
                    try:
                        l2.append(int(i))

                    except ValueError:
                        cl_out(c_error, 'The line can only contain int, but "{}" was found !!!'.format(i))
                        err = True
                        break

                if not err:
                    break

            key.append(l2)

        key = Matrix(key)
        print(key)


    #-Alphabet
    if ciph in crypta.ciph_sort['alf']:
        alf = cl_inp('Alphabet (let emty to use normal) :')

    else:
        alf = ''

    if alf == '':
        alf = crypta.alf_az


    #-Ignore
    for k in crypta.ciph_types:
        if ciph in crypta.ciph_types[k] and 'ignore' in k:
            ig = inp_lst('What to do with characters not in the alphabet ? Insert them, or ignore them ? (i/g) :', ('i', 'g', ''))
            if ig in ('i', ''):
                ignore = False

            else:
                ignore = True

            break

        else:
            ignore = None


    #---Make cipher
    try:
        C = crypta.make_ciph(ciph, key, key2, alf, ignore, interface='console')

    except Exception as err:
        cl_out(c_error, str(err))


    #---encrypt/decrypt
    if md == 'e':
        msg_ = C.encrypt(msg)

    else:
        msg_ = C.decrypt(msg)

    give_text(msg_)


#------Analysis
def use_txtana(c):
    '''Analyse a message.'''

    msg = get_text()

    if c == '11':
        while True:
            n = cl_inp('Group size (default is 1) :')

            if n not in (*[str(k) for k in range(100)], ''):
                cl_out(c_error, 'Please enter an int in [0 ; 99] !!!')

            else:
                if n == '':
                    n = 1

                else:
                    n = int(n)

                break

        msg_ = crypta.freqana_str(msg, True, n)


    elif c == '10':
        msg_ = crypta.textana(msg, True)

    elif c == '12':
        msg_ = str(crypta.Ic(wprocess=True).calc(msg))

    elif c == '13':
        msg_ = crypta.Kasiki(wprocess=True).analyse(msg)

    elif c == '14':
        msg_ = crypta.Friedman(wprocess=True).analyse(msg)

    give_text(msg_)


#------Hashes
def use_hash(h):
    '''Collect infos to hash a message.'''

    msg = get_text()

    if h == 'SecHash':
        loop = inp_int('Number of loops :')

    else:
        loop = None

    C = hasher.Hasher(h, loop)
    msg_ = C.hash(msg)

    give_text(msg_)


#---------Wordlists
#------generation
def use_wrdlst_gen():
    '''Allow to use wordlist generator in console.'''

    #---questions
    #-length
    lth = inp_int("Words' length :")

    #-alphabet
    alf = get_alf()

    #-name
    f_name = cl_inp("Wordlist's name :")


    #---generate
    try:
        generator = w_gen.WordlistGenerator(
            f_name,
            lth,
            alf,
            interface='console'
        )

    except FileExistsError:
        return -3 #Abort

    generator.generate()


#------analyser
def use_wrdlst_ana():
    '''Show informtions about a wordlist.'''

    fn = cl_inp('Enter the wordlist\'s name :')

    analyser = WordlistAnalyzer(fn, interface='console')

    if analyser in (-1, -2):
        return -3

    print('\nProcessing ...')
    t0 = dt.now()
    lines = analyser.show_lines()
    #lines['bottom'].reverse()
    print('\nStep 1/2 done in {} s'.format(dt.now() - t0))

    print('\nAnalysing ...')
    str_ret = str(analyser)

    cl_out(c_output, 'Analysis :\n{}'.format(indent(str_ret)))
    pause()



#---------Base convert
def use_b_cvrt():
    '''Ask to the user, using the console, the 3 values needed to convert a number.'''

    cl_out(c_output, "Pro tip : if you want to convert using the IEEE754 standard, type 'ieee754' as base !")

    correct = False

    while not correct: #Entry of n, nb, b
        try:
            n = cl_inp('Enter the number to convert :')

            nb = cl_inp("Enter number's base :")
            if nb.lower() != 'ieee754':
                nb = int(nb)

            alf_nb = cl_inp('Alphabet (let empty to use normal) : ')
            if alf_nb == "":
                if nb <= 36 and nb != 32:
                    alf_nb = b_cvrt_alf_list['alf_base36']
                elif nb == 32:
                    r = inp_lst('Base32 hex ? (y/n) ', ('y', 'yes', 'Yes', 'YES', 'n', 'no', 'No', 'NO'))
                    if r in ('y', 'yes', 'Yes', 'YES'):
                        alf_nb = b_cvrt_alf_list['alf_base32hex']
                    else:
                        alf_nb = b_cvrt_alf_list['alf_base32']
                elif nb <= 64:
                    alf_nb = b_cvrt_alf_list['alf_base64']
                else:
                    alf_nb = b_cvrt_alf_list['alf_base140']

            b = cl_inp("Enter return's base :")
            if b.lower() != 'ieee754':
                b = int(b)

            alf_b = cl_inp('Alphabet (let empty to use normal) : ')
            if alf_b == "":
                if b <= 36 and b != 32:
                    alf_b = b_cvrt_alf_list['alf_base36']
                elif b == 32:
                    r = inp_lst('Base32 hex ? (y/n) ', ('y', 'yes', 'Yes', 'YES', 'n', 'no', 'No', 'NO'))
                    if r in ('y', 'yes', 'Yes', 'YES'):
                        alf_b = b_cvrt_alf_list['alf_base32hex']
                    else:
                        alf_b = b_cvrt_alf_list['alf_base32']
                elif b <= 64:
                    alf_b = b_cvrt_alf_list['alf_base64']
                else:
                    alf_b = b_cvrt_alf_list['alf_base140']

        except ValueError:
            cl_out(c_error, 'The value must be an interger !!!')

        else:
            correct = True


    #---create number
    number = BaseConvert(n, nb, alf=alf_nb)


    NEG = False
    if nb == 2:
        NEG = ''
        while NEG not in ('y', 'yes', 'Yes', 'YES', 'n', 'no', 'No', 'NO'):
            NEG = cl_inp("Is the binary digit encoded negatively with the two's complement's standard ? (y/n) :")

        if NEG in ('y', 'yes', 'Yes', 'YES'):
            NEG = True

        else:
            NEG = False

    elif number.FL or number.INT:
        if float(n) < 0:
            NEG = True


    cl_out(c_output, number.convert(b, NEG=NEG, alf_b=alf_b))
    pause()


#---------Anamer0
def use_anamer0():
    '''Allow to use anamer0 in menu console interface.'''

    cl_out(c_output, anamer0.use())

    color(c_input)
    input('--- Press <enter> to continue ---')
    color(c_prog)


#---------Change password
def change_pwd():
    '''Change Cracker's password'''

    global pwd

    old_pwd = cl_inp('\nActual password :', getpass)

    if hasher.SecHash(old_pwd) != pwd:
        cl_out(c_error, 'Wrong password !!!')
        sleep(0.5)
        return -3

    pwd1 = cl_inp('New password :', getpass)

    entro = pwd_testor.get_sth(pwd1, True)

    if entro < 40:
        cl_out(c_error, 'The password is too much weak !!!\nIt should have an entropy of 40 bits at least, but it has an entropy of {} bits !!!'.format(round(entro)))
        sleep(0.5)
        return -3

    pwd2 = cl_inp('Confirm password :', getpass)

    if pwd1 != pwd2:
        cl_out(c_error, 'The passwords does not correspond !')
        sleep(0.5)
        return -3

    #---good
    pwd = hasher.SecHash(pwd1)

    try:
        with open('Data/pwd', 'w') as f:
            f.write(pwd)

    except Exception as err:
        cl_out(c_error, str(err))
        return -1

    else:
        cl_out(c_succes, 'Done !\nYour password has been be changed.\nIt has an entropy of {} bits.'.format(round(entro)))
        sleep(0.5)



##-run
if __name__ == '__main__':
    color(c_prog)

    #------If first time launched, introduce RSA keys
    chdir(RSA.chd_rsa('.', first=True, interface='console'))

    #------Launch the program
    CrackerConsole.use()


