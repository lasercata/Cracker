#!/bin/python3
# -*- coding: utf-8 -*-
'''Module incuding wordlist_analyzer function'''

wrdlst_ana__auth = 'Lasercata'
wrdlst_ana__last_update = '09.06.2020'
wrdlst_ana__version = '3.0'

##-import
#---------Cracker's modules
from modules.base.console.color import color, cl_inp, cl_out, c_error, c_wrdlt, c_output, c_prog, c_succes
from modules.base.base_functions import set_prompt, inp_lst, FileInfo
from modules.base.progress_bars import *
from modules.password_testor.pwd_testor import walf, wlth
from modules.b_cvrt.b_cvrt import space_b

#------packages
from datetime import datetime as dt

##-main
class WordlistAnalyzer:
    '''Class dealing with wordlists analysis'''


    def __init__(self, fn, binary=True, encod='utf-8', interface=None):
        '''Initiate the object.

        .fn : the worslist's name ;
        .binary : Should be a boolean. Correspond to the binary mode while opening ;
        .encod : the encoding. Default is 'utf-8' ;
        .interface : the interface using this function. Should be None,
        'gui', or 'console'. Used to choose the progress bar.
        '''

        if binary not in (True, False):
            raise ValueError('The argument "binary" should be a boolean, but \
                "{}" of type "{}" was found !!!'.format(binary, type(binary)))

        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", \
                or "console", but {} of type {} was found !!!'.format(interface, type(interface)))


        self.fn = fn
        self.binary = binary
        self.interface = interface

        if binary:
            self.encod = None

        else:
            self.encod = encod

        validity = self.is_valid_file()

        if validity in (-1, -2):
            return validity



    def __repr__(self):
        '''Represent the object'''

        return "WordlistAnalyser('{}', '{}', '{}', '{}')".format(self.fn, self.binary, self.encod, self.interface)


    def __str__(self):
        '''Return the analysis in a readable string.'''

        try:
            ana = self.analysis #don't analyse again if already done

        except AttributeError:
            ana = self.ana()

        if ana == -1:
            msg_err = 'The file "" was NOT found !!!'.format(self.fn)

        elif ana == -2:
            msg_err = 'Bad encoding "{}" for the file "{}"'.format(self.encod, self.fn)

        if ana in (-1, -2):
            if self.interface == None:
                raise FileNotFoundError(msg_err)

            elif self.interface == 'console':
                cl_out(c_error, msg_err)
                return ana

            elif self.interface == 'gui':
                QMessageBox.critical(None, '!!! File error !!!', msg_err)
                return ana


        sizes = ana[0]
        times = ana[1]
        infos = ana[2]

        ret = 'Filename : {} ;'.format(self.fn)
        ret += '\n\nSize : {} ({}) ;'.format(*sizes)

        ret += '\n\nLast modification : {} ;'.format(times[0])
        ret += '\nLast access : {} ;'.format(times[1])
        ret += '\nCreation : {} ;'.format(times[2])

        ret += '\n\nMinimum line length : {} characters ;'.format(infos['min'])
        ret += '\nMaximum line length : {} characters ;'.format(infos['max'])
        ret += "\nWordlist's length : {} lines ;".format(space_b(infos['nb_lines']))

        ret += '\n\nLength of the alphabet : {} characters ;'.format(infos['alf_lth'])
        ret += '\nAlphabets : {} ;'.format(set_prompt(infos['lst_alf']))

        ret += '\n\nNumber of differents characters : {} ;'.format(infos['nb_occ'])
        ret += "\nCharacters' repartition :"

        for k in infos['dct_occ']:
            ret += "\n\t'{}' : {} ;".format(k, space_b(infos['dct_occ'][k]))

        ret = ret[:-2] + '.' #replace ' ;' by '.' at the last line.


        return ret


    def ana(self, print_verbose=False):
        '''
        Function which analyse a wordlist.

        .self.fn : the worslist's name ;
        .self.binary : Should be a boolean. Correspond to the binary mode while opening ;
        .self.encod : the encoding. Default is 'utf-8' ;
        .self.interface : the interface using this function. Should be None,
        'gui', or 'console'. Used to choose the progress bar ;
        .print_verbose : if True, print 'Processing ...' when activated.

        .Return :
            (size_b, size_d), (mtime, atime, ctime), infos ; where 'infos' is a dict containing some informations
        '''


        if self.interface == 'gui':
            pb = GuiProgressBar(title='Reading "{}" ... ― Cracker'.format(self.fn), verbose=True, mn=1)

        elif self.interface == 'console':
            pb = ConsoleProgressBar()


        md = ('r', 'rb')[self.binary]

        dct_occ = {}
        mn = 10**6
        mx = 0
        i = 0

        if print_verbose:
            print('Processing ...')

        t0 = dt.now()

        f_info = FileInfo(self.fn)

        size_d = f_info.h_size(bi=False) #KB, MB, ...
        size_b = f_info.h_size() #KiB, MiB, ...

        mtime = f_info.h_dates('m')
        atime = f_info.h_dates('a')
        ctime = f_info.h_dates('c')

        nb_lines = self.count_lines()


        with open(self.fn, mode=md, encoding=self.encod) as f:
            for j, line in enumerate(f):

                if self.binary:
                    line = line.decode(errors='ignore')

                line = line.strip('\r\n')

                #------number of lines
                i += 1

                #------occ
                for char in line:
                    try:
                        dct_occ[char] += 1

                    except KeyError:
                        dct_occ[char] = 1


                #------min
                if len(line) < mn:
                    mn = len(line)

                #------max
                if len(line) > mx:
                    mx = len(line)


                #------progress bar
                if j % 2**10 == 0:
                    if self.interface in ('gui', 'console'):
                        pb.set(i, nb_lines)


        lst_alf = walf(list(dct_occ.keys()))
        nb_occ = len(list(dct_occ.keys()))

        t_end = dt.now()
        self.show_time(t_end - t0)


        self.nb_lines = nb_lines #for the show_lines function


        #-sort the dct_occ :
        old_dct_occ = dct_occ
        dct_occ = {}

        for k in sorted(old_dct_occ):
            dct_occ[k] = old_dct_occ[k]



        infos = {
            'dct_occ' : dct_occ,        #Counted occurences (dict) ;
            'lst_alf' : lst_alf[1],     #Tuple of the alphabets ;
            'alf_lth' : lst_alf[0],     #Length of the alphabets ;
            'nb_occ' : nb_occ,          #Number of differents characters ;
            'nb_lines' : nb_lines,      #Number of lines ;
            'min' : mn,                 #Smaller line length ;
            'max' : mx                  #Longer line length.
        }

        ret = (size_b, size_d), (mtime, atime, ctime), infos

        self.analysis = ret
        return ret



    def show_lines(self, nb=20):
        '''Return a dict containing the nb head and bottom lines.
        If 'nb' > 2*nb_lines, return -4.
        '''

        try:
            nb_lines = self.nb_lines

        except AttributeError:
            nb_lines = self.count_lines()


        if nb > 2 * nb_lines:
            return -4


        s_lines = {'head' : [], 'bottom' : []}

        md = ('r', 'rb')[self.binary]

        with open(self.fn, mode=md, encoding=self.encod) as f:
            for j, line in enumerate(f):
                if self.binary:
                    line = line.decode(errors='ignore')

                line = line.strip('\r\n')

                if j <= nb:
                    s_lines['head'].append(line)

                elif j >= nb_lines - nb:
                    s_lines['bottom'].append(line)


        return s_lines



    def count_lines(self):
        '''Return the number of lines of the wordlist.'''

        nb_lines = sum(1 for line in open(self.fn, 'rb'))

        self.nb_lines = nb_lines
        return nb_lines



    def show_time(self, time):
        '''Show the time, according to the self.interface arg.'''

        msg = 'Done in {} s !'.format(time)

        if self.interface == None:
            print(msg)

        elif self.interface == 'console':
            cl_out(c_succes, msg)

        else:
            QMessageBox.about(None, 'Done !', msg)


    def is_valid_file(self):
        '''Check if the file is reachable with the options.

        .Return :
            -1 if the file was not found ;
            -2 if an encoding error occur.
        '''

        try:
            md = ('r', 'rb')[self.binary]
            with open(self.fn, mode=md, encoding=self.encod) as f:
                char_1 = f.read(1)

                if self.binary:
                    char_1 = char_1.decode()

        except FileNotFoundError:
            ret = -1

        except UnicodeDecodeError:
            ret = -2

        else:
            ret = 0


        if ret == -1:
            msg_err = 'The file "{}" was NOT found !!!'.format(self.fn)

        elif ret == -2:
            msg_err = 'Bad encoding "{}" for the file "{}"'.format(self.encod, self.fn)

        if ret in (-1, -2):
            if self.interface == None:
                raise FileNotFoundError(msg_err)

            elif self.interface == 'console':
                cl_out(c_error, msg_err)

            elif self.interface == 'gui':
                QMessageBox.critical(None, '!!! File error !!!', msg_err)

        return ret



def use_open_w(): #todo: move (in the console file) and improve this
    try:
        file_name = cl_inp('Enter the wordlist\'s name :')
        wordlist_f = open(file_name, 'r')

    except FileNotFoundError:
        cl_out(c_error, 'No file of this name !!! \nBack menu ...')

    else:
        wordlist_f.close()
        open_w(file_name)

