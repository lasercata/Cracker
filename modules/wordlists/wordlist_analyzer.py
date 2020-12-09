#!/bin/python3
# -*- coding: utf-8 -*-
'''Module incuding wordlist_analyzer function'''

wrdlst_ana__auth = 'Lasercata'
wrdlst_ana__last_update = '09.12.2020'
wrdlst_ana__version = '3.2'

##-import
#---------Cracker's modules
from modules.base.console.color import color, cl_inp, cl_out, c_error, c_wrdlt, c_output, c_prog, c_succes
from modules.base.base_functions import set_prompt, inp_lst, FileInfo
from modules.base.progress_bars import *
from modules.password_testor.pwd_testor import walf, wlth
from modules.b_cvrt.b_cvrt import space_b
from Languages.lang import translate as tr

#------packages
from datetime import datetime as dt
import platform
import ctypes
import os

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
            raise ValueError(tr('The argument "binary" should be a boolean, but "{}" of type "{}" was found !!!').format(binary, type(binary)))

        if interface not in (None, 'gui', 'console'):
            raise ValueError(tr('The argument "interface" should be None, "gui", or "console", but {} of type {} was found !!!').format(interface, type(interface)))


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
            msg_err = tr('The file "{}" was NOT found !!!').format(self.fn)

        elif ana == -2:
            msg_err = tr('Bad encoding "{}" for the file "{}"').format(self.encod, self.fn)

        if ana in (-1, -2, -3):
            if self.interface == None:
                raise FileNotFoundError(msg_err)

            elif self.interface == 'console':
                cl_out(c_error, msg_err)
                return ana

            elif self.interface == 'gui':
                QMessageBox.critical(None, tr('!!! File error !!!'), msg_err)
                return ana


        sizes = ana[0]
        times = ana[1]
        infos = ana[2]
        lib_C = ana[3][0]
        infosLibC = ana[3][1]

        ret = tr('Filename : {} ;').format(self.fn)
        ret += '\n\n' + tr('Size : {} ({}) ;').format(*sizes)

        ret += '\n\n' + tr('Last modification : {} ;').format(times[0])
        ret += '\n' + tr('Last access : {} ;').format(times[1])
        ret += '\n' + tr('Creation : {} ;').format(times[2])
        
        if lib_C:
            ret += '\n\n' + tr('Number of characters : {} ;').format(infosLibC['nb_car'])

        ret += '\n\n' + tr('Minimum line length : {} characters ;').format(infos['min'])
        ret += '\n' + tr('Maximum line length : {} characters ;').format(infos['max'])
        if lib_C:
            ret += '\n' + tr('Average line length : {} characters ;').format(infosLibC['av_len'])
            ret += '\n' + tr('Median line length : {} characters ;').format(infosLibC['med_len'])
        ret += '\n' + tr("Wordlist's length : {} lines ;").format(space_b(infos['nb_lines']))
        if lib_C:
            ret += '\n' + tr('Wordlength repartition :')
            
            for k in infosLibC['dct_len_w']:
                ret += "\n\t'{}': {} ;".format(k, space_b(infosLibC['dct_len_w'][k]))

        ret += '\n\n' + tr('Length of the alphabet : {} characters ;').format(infos['alf_lth'])
        ret += '\n' + tr('Alphabets : {} ;').format(set_prompt(infos['lst_alf']))

        ret += '\n\n' + tr('Number of differents characters : {} ;').format(infos['nb_occ'])
        ret += '\n' + tr("Characters' repartition :")

        for k in infos['dct_occ']:
            ret += "\n\t'{}': {} ;".format(k, space_b(infos['dct_occ'][k]))

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
            pb = GuiProgressBar(title=tr('Reading "{}" ... ― Cracker').format(self.fn), verbose=True, mn=1)

        elif self.interface == 'console':
            pb = ConsoleProgressBar()
            
        lib_C = True
        try:
            if platform.system() == 'Windows':
                dll_fn = 'wordlist_analyzer_win.dll'
            else:
                dll_fn = 'wordlist_analyzer_unix.dll'
       
            lib = ctypes.cdll.LoadLibrary('{}/modules/wordlists/library/{}'.format(os.getcwd(), dll_fn))
            f_ana = lib.analyzeWordlist
            f_ana.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
            f_ana.restype = ctypes.POINTER(ctypes.c_ulonglong)
            
            if self.encod == 'utf-8':
                encoding = 1
            else:
                encoding = 0

            L = f_ana(os.path.abspath(self.fn).encode('ascii'), "\n".encode('ascii'), encoding)
            if L[0] != 0:
                if L[0] == 1: # File not found
                    return -1
                else:
                    return -3 # Other error, access denied for example
            
            D = {}
            D["Size in octets"] = L[2]
            D["Number of characters"] = L[3]
            D["Number of different characters (without separators)"] = L[4]
            D["Code point minimum"] = L[5]
            D["Code point maximum"] = L[6]
            D["Number of words"] = L[7]
            D["Minimum length"] = L[8]
            D["Maximum length"] = L[9]
            D["Average length"] = L[10] / 1000
            if L[11] != 2**64 -1:
                D["Median length"] = L[11] / 10
            else:
                D["Median length"] = 'Not calculated'
           
        except:
            lib_C = False


        md = ('r', 'rb')[self.binary]

        dct_occ = {}
        mn = 10**6
        mx = 0
        i = 0

        if print_verbose:
            print(tr('Processing ...'))

        t0 = dt.now()

        f_info = FileInfo(self.fn)

        size_d = f_info.h_size(bi=False) #KB, MB, ...
        size_b = f_info.h_size() #KiB, MiB, ...

        mtime = f_info.h_dates('m')
        atime = f_info.h_dates('a')
        ctime = f_info.h_dates('c')
        
        
        if not lib_C:
   
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
        
        else:
    
            mn = D["Minimum length"]
            mx = D["Maximum length"]
            nb_lines = D["Number of words"]
            for k in range(268 + D["Code point minimum"], 268 + D["Code point maximum"] + 1):
                if L[k] != 0:
                    dct_occ[chr(k-268)] = L[k]
            lst_alf = walf(list(dct_occ.keys()))
            nb_occ = D["Number of different characters (without separators)"]
            
            if mx > 254:
                mx2 = 254
            else:
                mx2 = mx
                
            W = {}
           
            for k in range(12 + mn, 12 + mx2 + 1):
                if L[k] != 0:
                    W[k-12] = L[k]
            
            if L[267] != 0:
                W['>254'] = L[267]
            

        t_end = dt.now()
        self.show_time(t_end - t0)


        self.nb_lines = nb_lines #for the show_lines function


        #-sort the dct_occ :
        old_dct_occ = dct_occ
        dct_occ = {}

        for k in sorted(old_dct_occ):
            dct_occ[k] = old_dct_occ[k]



        infos = {
            'dct_occ': dct_occ,        #Counted occurences (dict) ;
            'lst_alf': lst_alf[1],     #Tuple of the alphabets ;
            'alf_lth': lst_alf[0],     #Length of the alphabets ;
            'nb_occ': nb_occ,          #Number of differents characters ;
            'nb_lines': nb_lines,      #Number of lines ;
            'min': mn,                 #Smaller line length ;
            'max': mx                  #Longer line length.
        }
        
        infosLibC = {}
        
        if lib_C:
            infosLibC = {
                'nb_car': D["Number of characters"],
                'av_len': D["Average length"],
                'med_len': D["Median length"],
                'dct_len_w': W  #Repartition of word length
            }

        ret = (size_b, size_d), (mtime, atime, ctime), infos, (lib_C, infosLibC)

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

        msg = tr('Done in {} s !').format(time)

        if self.interface == None:
            print(msg)

        elif self.interface == 'console':
            cl_out(c_succes, msg)

        else:
            QMessageBox.about(None, tr('Done !'), msg)


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
            msg_err = tr('The file "{}" was NOT found !!!').format(self.fn)

        elif ret == -2:
            msg_err = tr('Bad encoding "{}" for the file "{}"').format(self.encod, self.fn)

        if ret in (-1, -2):
            if self.interface == None:
                raise FileNotFoundError(msg_err)

            elif self.interface == 'console':
                cl_out(c_error, msg_err)

            elif self.interface == 'gui':
                QMessageBox.critical(None, tr('!!! File error !!!'), msg_err)

        return ret



def use_open_w(): #todo: move (in the console file) and improve this
    try:
        file_name = cl_inp(tr("Enter the wordlist's name :"))
        wordlist_f = open(file_name, 'r')

    except FileNotFoundError:
        cl_out(c_error, tr('No file of this name !!!') + ' \n' + tr('Back menu ...'))

    else:
        wordlist_f.close()
        open_w(file_name)
