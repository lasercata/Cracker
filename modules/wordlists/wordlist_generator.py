#!/bin/python3
# -*- coding: utf-8 -*-
'''Module incuding wordlist_generator fonctions'''

wrdlst_gen__auth = 'Lasercata, Elerias'
wrdlst_gen__last_update = '11.06.2020'
wrdlst_gen__version = '7.0'


##-import
from datetime import datetime as dt
from os.path import isfile

from modules.base.base_functions import inp_int, space, use_menu, set_prompt, inp_lst, h_size
from modules.base.progress_bars import *
from modules.base.console.color import cl_inp, cl_out, c_error, c_prog, c_succes, c_wrdlt, c_ascii, c_output, color

##-ini
alf_01 = '01'
alf_09 = '0123456789'
alf_hex = alf_09 + 'abcdef'
alf_az = 'abcdefghijklmnopqrstuvwxyz'
alf_AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

alf_az09 = alf_az + alf_09
alf_AZ09 = alf_AZ + alf_09
alf_azAZ = alf_az + alf_AZ
alf_azAZ09 = alf_azAZ + alf_09

alf_spe = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~£§¨°²µ’€'

alf_all = alf_azAZ09 + alf_spe

#alfs = (alf_0_1, alf_0_9, alf_hex, alf_a_z, alf_A_Z, alf_a_z_0_9, alf_A_Z_0_9, alf_a_z_A_Z, alf_a_z_A_Z_0_9, alf_spe, alf_all)

#inp_alf = ('0-1', '0-9', 'hex', 'a-z', 'A-Z', 'a-z, 0-9', 'A-Z, 0-9', 'a-z, A-Z', 'a-z, A-Z, 0-9', 'spe', 'all', 'write')

alfs = {
    '0-1' : alf_01,
    '0-9' : alf_09,
    'hex' : alf_hex,
    'a-z' : alf_az,
    'A-Z' : alf_AZ,
    'a-z, 0-9' : alf_az09,
    'A-Z, 0-9' : alf_AZ09,
    'a-z, A-Z' : alf_azAZ,
    'a-z, A-Z, 0-9' : alf_azAZ09,
    'spe' : alf_spe,
    'all' : alf_all
}




##-main
class WordlistGenerator:
    '''Class which allow to generate wordlists'''

    def __init__(self, fn, w_lth, alf, binary=True, encod='utf-8', interface=None):
        '''
        Initiate the WordlistGenerator object.

        fn : the wordlist's file name ;
        w_lth : the words' length. Should be an int ;
        alf : the alphabet to use. If type = str and in alfs, use the corresponding alphabet ;
        binary : Should be a boolean. Correspond to the binary mode while writting ;
        encod : the file's encoding ;
        interface : the interface using this function. Should be None,
            'gui', or 'console'. Used to choose the progress bar.
        '''

        #------check values
        if binary not in (True, False):
            raise ValueError('The argument "binary" should be a boolean, but \
                "{}" of type "{}" was found !!!'.format(binary, type(binary)))

        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", \
                or "console", but {} of type {} was found !!!'.format(interface, type(interface)))

        if type(alf) not in (str, list, set, tuple):
            raise ValueError('The argument "alf" should be an iterable, but a \
                "{}" found !!!'.format(type(alf)))

        if type(w_lth) != int:
            raise ValueError('The argument "w_lth" should be an int, but a "{}" \
                was found !!!'.format(type(w_alf)))


        #------check if the file already exist
        if isfile(fn): #os.path.isfile
            msg = 'The file "{}" already exist !!!'.format(fn)

            if interface == None:
                raise FileExistsError(msg)

            elif interface == 'console':
                cl_out(c_error, msg)
                raise FileExistsError(msg)

            else:
                QMessageBox.critical(None, '!!! File already exist !!!', '<h2>{}</h2>'.format(msg))
                raise FileExistsError(msg)


        #------initiate the self values
        if type(alf) == str and alf in alfs:
            self.alf = alfs[alf]

        else:
            self.alf = alf

        self.fn = fn
        self.w_lth = w_lth
        self.binary = binary
        self.encod = encod
        self.interface = interface


        #------others values
        self.alf_lth = len(self.alf)
        self.wrdlst_lth = self.alf_lth **self.w_lth
        self.size = self.wrdlst_lth * (self.w_lth + 2) #the number of characters. +2 bc of the CRLF.

        self.nb_rep = sum(self.alf_lth**k for k in range(self.w_lth - 1))

        self.new_l = ('\n', b'\n')[self.binary]



    def __repr__(self):
        '''Represent the WordlistGenerator object.'''

        return "WordlistGenerator(fn='{}', w_lth='{}', alf='{}', binary='{}', encod='{}', interface='{}')".format(
            self.fn,
            self.w_lth,
            self.alf,
            self.binary,
            self.encod,
            self.interface
        )



    #---------ini
    def ini(self):
        '''Initiate some values and objects. Used with self._gen.'''

        print('Processing ...')

        #self.t0 = dt.now()

        if self.binary:
            self.file = open(self.fn, 'wb')

        else:
            self.file = open(self.fn, 'w', encoding=self.encod)


        if self.interface == 'gui':
            self.pb = GuiProgressBar(title='Writing "{}" ... ― Cracker'.format(self.fn), verbose=True, mn=1)

        elif self.interface == 'console':
            self.pb = ConsoleProgressBar()

        self.rep = 0



    #---------_gen
    def _gen(self, lth, b_word):
        '''
        Generate and write the wordlist in the file self.fn.

        lth : the remaining letters to add to the word ;
        b_word : the begin of the word.
        '''

        if lth == self.w_lth : #if it is main function (to open only one time)
            self.ini()

        if self.binary and type(b_word) != bytes:
            b_word = b_word.encode(encoding=self.encod, errors='replace')


        if lth == 1:
            for k in self.alf:
                if self.binary:
                    k = k.encode(encoding=self.encod, errors='replace')

                self.file.write(b_word + k + self.new_l)

        else :
            for k in self.alf:
                if self.binary:
                    k = k.encode(encoding=self.encod, errors='replace')

                self._gen(lth - 1, b_word + k)

            #---print the progression
            self.rep += 1

            if self.interface in ('gui', 'console'):
                self.pb.set(self.rep, self.nb_rep)



        if lth == self.w_lth:
            #self.t_end = dt.now()
            self.file.close()


    #---------generate
    def generate(self):
        '''Use the function self._gen to generate and write the wordlist.'''

        msg = "Words' length : {} characters ;".format(self.w_lth)
        msg += "\nAlphabet's length : {} characters ;".format(self.alf_lth)
        msg += "\nWordlist's length : {} lines ;".format(space(str(self.wrdlst_lth)))
        msg += "\nWordlist's size : {} ({} bytes).".format(h_size(self.size), space(str(self.size)))


        if self.interface == None:
            print(msg)
            sure = 'y'

        elif self.interface == 'console':
            cl_out(c_output, msg)
            sure = inp_lst('Generate ? (y/n) :', ('y', 'n'))

        else:
            msg_ = msg + '\n\nGenerate ?'

            sure = QMessageBox.question(
                None, 'Generate ?', msg_, \
                QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)


        if sure in ('y', QMessageBox.Yes):
            self._gen(self.w_lth, '')












#todo: remove this

##-main function
def wordlist_generator_6(alf, dep_lth, lth, f_name, b_word):
    '''Write a wordlist in a file.

    Keywords arguments :
    alf : the alphabet used to write the wordlist
    dep_lth : the lenth of the words in the wordlist
    lth : the remaining letters to add to the word
    f_name : the filename
    b_word : the begin of the word
    '''

    global file_
    global rep
    global lst_rep

    len_alf = len(alf)
    lth_wrdlst = len_alf**int(dep_lth)

    nb_rep = sum(len_alf**k for k in range(dep_lth - 1))


    if lth == dep_lth : #if it is main function (to open only one time)
        file_ = open(f_name, 'w')

        print('Processing ...\n')
        t1 = dt.now()
        rep = 0
        lst_rep = []


    if lth == 1:
        for k in alf:
            file_.write(b_word + k + '\n')

    else :
        for k in alf:
            wordlist_generator_6(alf, dep_lth, lth-1, f_name, b_word + k)

        #print the progression
        rep += 1
        rep50 = round(rep/nb_rep*50)

        color(c_wrdlt)
        if rep > 1:
            print('\b'*52, end='')
        print('|' + '#'*rep50 + ' '*(50-rep50) + '|', end='')
        color(c_prog)



    if lth == dep_lth:
        t2 = dt.now() #calc the time duration
        t_dif = t2 - t1
        cl_out(c_succes, '\nDone in ' + str(t_dif) + ' second(s)')

        file_.close()


##-using function
def use_wrdlst_gen(f_name=None, lenth=None, in_alf=None): #todo: move this in console_launcher
    global alf_a_z, afl_A_Z, alf_0_9, alf_a_z_0_9, alf_a_z_A_Z, alf_A_Z_0_9, alf_a_z_A_Z_0_9, alf_hex, alf_0_1, alf_spe, alf_all, alfs, inp_alf

    #---------if used in menu console, args are None
    if f_name == None and lenth == None and in_alf == None:
        #---------questions
        #name
        f_name = cl_inp('What name give to the wordlist ? (Warning, it will overwrite any other file of the same name !) :')

        #lenth
        lenth = inp_int("What lenth for the words ? :")

        #alphabet
        in_alf = ''
        while in_alf not in inp_alf:
            in_alf = cl_inp('What alphabet choose ? \n(a-z ; 0-9 ; a-z, 0-9 ; A-Z ; A-Z, 0-9 ; a-z, A-Z ; a-z, A-Z, 0-9 ; 0-1 ; hex (0-9, A-F) ; spe ; all (a-z, A-Z, 0-9, spe) ; write) :')

        if in_alf == 'write':
            alf = cl_inp('Enter your alphabet ("," between caracters, no space !) :')
            alf = alf.split(',')

        else:
            for k in range(len(inp_alf)):
                if inp_alf[k] == in_alf:
                    alf = list(alfs[k])

    #---------if used with parser
    else:
        if in_alf not in inp_alf:
            alf = list(in_alf)

        else:
            for k in range(len(inp_alf)):
                if inp_alf[k] == in_alf:
                    alf = list(alfs[k])


    #---------confirm
    len_alf = len(alf)
    len_wordlist = len_alf**int(lenth)

    prnt = 'Lenth of the words : ' + str(lenth) + '\nLenth of the alphabet : ' + space(len_alf)
    prnt += '\nLenth of the wordlist : ' + space(len_wordlist) + ' lines.'
    cl_out(c_output, prnt)

    choice = inp_lst('Generate ? (y/n) :', ('y', 'n'))

    if choice == 'y':
        wordlist_generator_6(alf, lenth, lenth, f_name, '')

    else:
        raise KeyboardInterrupt

##-using function (menu with open_w)
def use():
    '''Use wordlist_generator functions''' #todo: move this in console_launcher

    #---menu
    c = ''
    while c not in ('quit', 'exit', '0', 'q'):

        color(c_succes)
        print('')
        print('\\'*50)

        color(c_prog)
        print('\nWordlists menu :\n')

        color(c_error)
        print('    0.Main menu')

        color(c_succes)
        print('    ' + '-'*16)
        color(c_ascii)

        print('    1.Generate a wordlist')
        print('    2.Open a wordlist')
        color(c_prog)

        c = ''
        c = cl_inp('Your Choice :')


        if c not in ('0', '1', '2', 'q'):
            prnt = '"' + c + '" is NOT an option of this menu !'
            cl_out(c_error, prnt)

        if c == '1':
            use_menu(use_wrdlst_gen)

        elif c == '2':
            #use_menu(use_open_w)
            print('todo.')


##-test module
if __name__ == '__main__':
    use()

    #wordlist_generator_6(alf_a_z, 4, 4, 'w4az', '')