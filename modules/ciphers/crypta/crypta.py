#!/bin/python3
# -*- coding: utf-8 -*-
"""Crypta is a cryptology program including cryptography and cryptanalysis functions."""

#auth = 'Elerias'
#date = '16.05.2020'
#version = '3.0'

crypta__auth = 'Elerias'
crypta__last_update = '31.08.2020'
crypta__ver = '3.1'

update_notes = """
Crypta v3.0      16.05.2020
Improvements (from 2.9) :
    - New ciphers :
        * Autoclave cipher
        * Gronsfeld cipher
        * Tritheme cipher
        * UBCHI cipher
        * ABC cipher
        * Beaufort cipher
        * Porta cipher
        * Albam, Achbi and Avgad codes
        * Fleissner cipher
    - Simplification of reverse_code
    - ver_plain_text works now for the french thanks to the list of all the tetragrams in french generated
    - prob_plain_text gives the possibility to the program to know if a text is "more french" than another. Therefore, the Hill-climbing can be used with a bank of famous books.
    - Corrections :
        * inverse
        * affine.crack
        * scytale.crack
        * caesar.crack
        * reverse_code.crack
        * atbash.crack
    - Beginning of function crack
    - Sort of the ciphers
    - New crack functions :
        * morse.crack
        * tritheme.crack
        * columnar_transposition.crack
        * UBCHI.crack
        * monosub.crack with the Hill-climbing method
        * albam, achbi and avgad crack
    - Adding test of Friedman
    - Adding Assist_cryptanalysis to help for the cryptanalysis of simple substitution
Crypta v2.9
Improvements (from 2.8) :
    - Joining AES cipher
Crypta v2.8
Improvements (from 2.7) :
    - Adding Playfair cipher
    - Beginning ver_plain_text
    - Adding crack function in 6 ciphers/codes (caesar, affine, atbash, rail fence, scytale, reverse)
Crypta v2.7       05.03.2020
Improvements (from 2.6.2) :
    - Correcting columnar transposition
    - Adding polybius square
    - Adding ADFGX and ADFGVX ciphers
    - Program works now if Cracker functions are not imported""" 

sites = ("https://www.lama.univ-savoie.fr/pagesmembres/hyvernat/Enseignement/1920/info910/tp1.html", 'http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/expose_vigenere.html') #the second one is to crack vigenre.


##-initialisation

from os import getcwd, chdir
from math import gcd, log
import itertools
from random import shuffle, choice, randint
path = getcwd()
for k in range(3):
    try:
        from modules.prima import prima
        from modules.base.matrix import *
        from modules.crypta import AES
    except:
        pass
    chdir('..')
try:
    from modules.base.console.color import color, cl_out, cl_inp, c_succes, c_output, c_wrdlt, c_error, c_prog, c_ascii
    from modules.base.base_functions import use_menu, inp_lst, inp_int, fact, space
    from modules.ciphers.BaseCipher import BaseCipher #this will not be redefined below !
    from modules.base.base_functions import chd
    from modules.base import glb
        
except ModuleNotFoundError as ept:
    err = str(ept).strip("No module named")
    print('Crypta : module {} not found, it could mean that Craker was not found, redefining the functions !'.format(err))

    # If we can't import Cracker, functions have to be defined for the good working of program
    def color(arg):
        pass
    def cl_inp(t):
        return input(t)
    def cl_out(a, t):
        print(t)
    def c_succes(t):
        print(t)
    def c_output(t):
        print(t)
    def c_wrdlt(t):
        print(t)
    def c_error(t=""):
        print(t)
    def c_prog(t):
        print(t)
    def c_ascii(t):
        print(t)
    def use_menu(t):
        t()
    def inp_lst(t, a):
        return input(t)
    def inp_int(t):
        return input(t)
chdir(path)


alf_az = 'abcdefghijklmnopqrstuvwxyz'
alf_AZ = alf_az.upper()
alf_azAZ = alf_az + alf_AZ

alf_wrt = ' .,:;!?"\'-'
alf_usual = alf_azAZ + alf_wrt

alf_25 = alf_az.replace('j', '')

##-plain text checker

def inD(t):
    global D_quad
    return D_quad.get(t) != None

def ver_plain_text(text, wprocess=True):
    """Return True if the text means something, False otherwise."""
    
    if wprocess:
        text = msgform(text, "min", False, False)
        
    lt = len(text)
    
    if lt < 5:
        return False
        
    if text[0] == text[1] and text[1] == text[2] and text[2] == text[3] and text[3] == text[4]:
        return False
        
    # Level 1 : Speed test
    err = 0
    if not(inD(text[0:4])):
        err += 1
    if not(inD(text[-4:lt])):
        err += 1
    if not(inD(text[1:5])):
        err += 1
    if not(inD(text[-5:lt-1])):
        err += 1

    if err > 1:
        return False

    # Level 2 : Check tetragrams
    err = 0
    for k in range(lt - 3):
        if not inD(text[k:k+4]):
            err += 1
            
    if err > 0.10 * (lt-3):
        return False
        
    return True #todo: improve this algorithm !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def prob_plain_text(text, wprocess=False):
    """Return a probability that the text is french or english."""
    global D_quad
    lt = len(text)
    if lt < 5:
        return 0
    p = 0
    for k in range(lt-3):
        r = D_quad.get(text[k:k+4])
        if r != None and r != 0:
            p = p + log(r)
        else:
            p = p + log(0.01) - log(2456316)
    p = p / (lt-3)
    return p


##-base functions

def bezout(a, b):
    """Return the Bezout's coefficient of a and b.
    r = a % b
    r = ua + vb
    lu : last u
    lv : last v
    q : quotient
    """
    r = a % b
    lu = 1
    lv = 0
    u = 0
    v = 1
    while r > 1:
        r = a % b
        q = (a-r) // b
        u, lu = lu - q*u, u
        v, lv = lv - q*v, v
        a = b
        b = r
    return u, v

def inverse(a, n):
    """Return the inverse of a in base n."""
    u, v = bezout(a, n)
    inverse = u % n
    return inverse

def msgform(M, f='min', space=False, number=False, alf='abcdefghijklmnopqrstuvwxyz'):
    """Delete the special characters and replace the majuscules and the accent"""
    
    #spe = "àåâæáāăãäąçćčďđėéęèěêĕëəēģğíıìįïīîķłľļĺňņńñőóøòöœõôŕřß§śšşþťțţųüűúůùūûýźżžÀÅÂÆÁĀĂÃÄĄÇĆČĎĐĖÉĘÈĚÊĔËƏĒĢĞÍIÌĮÏĪÎĶŁĽĻĹŇŅŃÑŐÓØÒÖŒÕÔŔŘSS§ŚŠŞÞŤȚŢŲÜŰÚŮÙŪÛÝŹŻŽ"
    #nor = "aaaaaaaaaacccddeeeeeeeeeeggiiiiiiikllllnnnnoooooooorrsssssttttuuuuuuuuyzzzAAAAAAAAAACCCDDEEEEEEEEEEGGIIIIIIIKLLLLNNNNOOOOOOOORRSSSSSTTTTTUUUUUUUUYZZZ"
    
    d = {'à': 'a', 'å': 'a', 'â': 'a', 'æ': 'ae', 'á': 'a', 'ā': 'a', 'ă': 'a', 'ã': 'a',
        'ä': 'a', 'ą': 'a', 'ç': 'c', 'ć': 'c', 'č': 'c', 'ď': 'd', 'đ': 'd', 'ė': 'e',
        'é': 'e', 'ę': 'e', 'è': 'e', 'ě': 'e', 'ê': 'e', 'ĕ': 'e', 'ë': 'e', 'ə': 'e',
        'ē': 'e', 'ģ': 'g', 'ğ': 'g', 'í': 'i', 'ı': 'i', 'ì': 'i', 'į': 'i', 'ï': 'i',
        'ī': 'i', 'î': 'i', 'ķ': 'k', 'ł': 'l', 'ľ': 'l', 'ļ': 'l', 'ĺ': 'l', 'ň': 'n',
        'ņ': 'n', 'ń': 'n', 'ñ': 'n', 'ő': 'o', 'ó': 'o', 'ø': 'o', 'ò': 'o', 'ö': 'o',
        'œ': 'oe', 'õ': 'o', 'ô': 'o', 'ŕ': 'r', 'ř': 'r', 'ß': 's', '§': 'S', 'ś': 's',
        'š': 's', 'ş': 's', 'þ': 't', 'ť': 't', 'ț': 't', 'ţ': 't', 'ų': 'u', 'ü': 'u',
        'ű': 'u', 'ú': 'u', 'ů': 'u', 'ù': 'u', 'ū': 'u', 'û': 'u', 'ý': 'y', 'ź': 'z',
        'ż': 'z', 'ž': 'z', 'À': 'A', 'Å': 'A', 'Â': 'A', 'Æ': 'AE', 'Á': 'A', 'Ā': 'A',
        'Ă': 'A', 'Ã': 'A', 'Ä': 'A', 'Ą': 'A', 'Ç': 'C', 'Ć': 'C', 'Č': 'C', 'Ď': 'D',
        'Đ': 'D', 'Ė': 'E', 'É': 'E', 'Ę': 'E', 'È': 'E', 'Ě': 'E', 'Ê': 'E', 'Ĕ': 'E',
        'Ë': 'E', 'Ə': 'E', 'Ē': 'E', 'Ģ': 'G', 'Ğ': 'G', 'Í': 'I', 'I': 'I', 'Ì': 'I',
        'Į': 'I', 'Ï': 'I', 'Ī': 'I', 'Î': 'I', 'Ķ': 'K', 'Ł': 'L', 'Ľ': 'L', 'Ļ': 'L',
        'Ĺ': 'L', 'Ň': 'N', 'Ņ': 'N', 'Ń': 'N', 'Ñ': 'N', 'Ő': 'O', 'Ó': 'O', 'Ø': 'O',
        'Ò': 'O', 'Ö': 'O', 'Œ': 'OE', 'Õ': 'O', 'Ô': 'O', 'Ŕ': 'R', 'Ř': 'R', 'S': 'S',
        'Ś': 'S', 'Š': 'S', 'Ş': 'T', 'Þ': 'T', 'Ť': 'T', 'Ț': 'T', 'Ţ': 'T', 'Ų': 'U',
        'Ü': 'U', 'Ű': 'U', 'Ú': 'U', 'Ů': 'U', 'Ù': 'U', 'Ū': 'U', 'Û': 'U', 'Ý': 'Y',
        'Ź': 'Z', 'Ż': 'Z', 'Ž': 'Z'} #Using a dict allow to replace 'œ' by 'oe', and not by 'o'
    
    aut = ""
    Mf = ""
    for k in d:
        M = M.replace(k, d[k])
        
    if f == 'maj':
        M = M.upper()
        aut += alf.upper()
        
    elif f == 'min':
        M = M.lower()
        aut += alf.lower()
        
    else:
        aut += alf.lower() + alf.upper()
        
    if number:
        aut += '0123456789'
        
    if space:
        aut += ' '
        
    for k in M:
        if k in aut:
            Mf += k
            
    return Mf

def read_lines(T):
    """Return the text issue of the reading in lines of the list of list T."""
    text = ""
    for k in T:
        text = text + "".join(k)
    return text

def read_columns(T):
    """Return the text issue of the reading in columns of the list of list T."""
    text = ""
    for i in range(len(T[0])):
        for j in range(len(T)):
            if len(T[j]) > i:
                text = text + T[j][i]
    return text

def write_lines_c(text, nc):
    """Return the list of the list T issue of the writing in lines of the text in nc columns."""
    T = [[]]
    i = 0
    for k in range(len(text)):
        T[i].append(text[k])
        if k % nc == nc - 1:
            i = i + 1
            T.append([])
    return T

def write_columns_c(text, nc):
    """Return the list of the list T issue of the writing in columns of the text in nc columns."""
    T = []
    nl = len(text) // nc
    r = 0
    if len(text) % nc != 0:
        nl = nl + 1
        r = len(text) % nc
    for k in range(nl):
        T.append([])
    i = 0
    for k in range(len(text)):
        T[i].append(text[k])
        i = (i+1) % nl
        if i == nl - 1 and len(T[i]) == r:
            i = 0
    return T

def gen_dic_ite(L):
    """Generate a dictionnary with an iterable
    Ex : gen_dic_ite('abc') return {'a': 0, 'b': 1, 'c': 2}"""
    D = {}
    for k in range(len(L)):
        D[L[k]] = k
    return D

def generate_alphabet_word(word, alph='abcdefghijklmnopqrstuvwxyz'):
    """Return the cipher alphabet generated with a word key."""
    cipher_alph = ""
    for k in word:
        if k in alph:
            i = alph.index(k)
            alph = alph[0:i] + alph[i + 1:len(alph)]
            cipher_alph = cipher_alph + k
    cipher_alph = cipher_alph + alph
    return cipher_alph

def word_to_square(word, size=5):
    """Return the square issue of a key word."""
    if size == 5:
        alph = 'abcdefghiklmnopqrstuvwxyz'
        for k in range(len(word)):
            if word[k] == 'j':
                word = word[0:k] + 'i' + word[k + 1:len(word)]
        L = [[], [], [], [], []]
    elif size == 6:
        alph = 'abcdefghijklmnopqrstuvwxyz0123456789'
        L = [[], [], [], [], [], []]
    else:
        raise ValueError('The size should be 5 or 6 !!!')
    alph = generate_alphabet_word(word, alph)
    for i in range(size):
        for j in range(size):
            L[i].append(alph[i*size + j])
    return L

def word_to_transposition_key(word, alph='abcdefghijklmnopqrstuvwxyz'):
    """Return a transposition key generated with a word key."""
    L = []
    for k in range(len(word)):
        i = alph.index(word[k])
        L.append((i, k))
    L.sort()
    tra_k = []
    for k in L:
        tra_k.append(k[1])
    return tra_k

def read_file(f):
    """Return the text read of a file f after deleting of the \n."""
    a = open(f, 'r')
    t = a.read()
    t = t.split('\n')
    t = ' '.join(t)
    a.close()
    return t

def read_file_use():
    """Use read_file."""
    f = cl_inp('Name of the file to read : ')
    try:
        return read_file(f)
    except FileNotFoundError:
        cl_out(c_error, 'The file was NOT found !!!')
        return read_file_use()

def write_file(f, t):
    """Write in a file f the text t."""
    a = open(f, 'a')
    if type(t) == list:
        t = '\n'.join(t)
    a.write(t)
    a.close()

def write_file_use(t=""):
    """Use write_file."""
    f = cl_inp('Name of the file to write the data : ')
    if t == "":
        t = cl_inp('Text : ')
    write_file(f, t)
    print('Operation successfully realised')

def ask_text():
    """Use write_file or ask the text."""
    f = inp_lst('Read text from file ? (y/n) : ', ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui', 'n', 'no', 'non', 'Non', 'No', 'N', 'NON', 'NO'))
    if f in ('y', 'yes', 'Y', 'YES', 'Yes', 'o', 'O', 'oui', 'OUI', 'Oui'):
        t = read_file_use()
    else:
        t = cl_inp('Enter the text :')
    return t

def give_result(res):
    """Use write_file or print the result."""
    r = cl_inp('Write the result in a file ? (y/n) : ')
    if r in ('y', 'yes', 'Y', 'YES', 'o', 'O', 'oui', 'OUI'):
        write_file_use(res)
    else:
        print('Result :\n')
        print(res)


ciph_types = { # Used in make_ciph
    'verbose, interface': (
        'Morse',
        'Reverse code',
        'Reverse code word',
    ),
    
    'key, interface': (
        'Playfair',
    ),
    
    'key, verbose, interface': (
        'Scytale',
        'Rail fence'
    ),
    
    'key, key2, alf, interface': (
        'Four squares',
    ),
    
    'key, alf, interface': (
        'Fleissner',
        'Hill'
    ),
    
    'key, alf, ignore, interface': (
        'ABC',
    ),
    
    'key, alf, verbose, interface': (
        'Columnar transposition',
        'UBCHI'
    ),
    
    'alf, ignore, verbose, interface': (
        'Achbi',
        'Atbash',
        'Albam',
        'Avgad',
        'Tritheme'
    ),
    
    'key, alf, ignore, verbose, interface': (
        'Caesar',
        'Monoalphabetic substitution',
        'Porta',
        'Vigenere',
        'Beaufort',
        'Gronsfeld',
        'Autoclave'
    ),
    
    'key, key2, alf, ignore, interface': (
        'ADFGX',
        'ADFGVX'
    ),
    
    'key, key2, alf, ignore, verbose, interface': (
        'Affine',
    ),
    
    'key, indexes, alf, ignore, space, verbose, interface': (
        'Polybius',
    )
}


ciph_sort = {
    '0_key': (
        'Morse',
        'Reverse code',
        'Reverse code word',
        'Atbash',
        'Albam',
        'Achbi',
        'Avgad',
        'Tritheme'
    ),
    
    '1_key_str': (
        'Columnar transposition',
        'UBCHI',
        'Polybius',
        'Monoalphabetic substitution',
        'Porta',
        'Vigenere',
        'Beaufort',
        'Autoclave',
        'Playfair',
        'ABC'
    ),
    
    '1_key_int': (
        'Scytale',
        'Rail fence',
        'Caesar',
        'Gronsfeld'
    ),
    
    '1_key_list': (
        'Fleissner',
        'Hill'
    ),
    
    '2_key_int': (
        'Affine',
    ),
    
    '2_key_str': (
        'Four squares',
        'ADFGX',
        'ADFGVX'
    ),

    'alf': (
        'Fleissner',
        'Columnar transposition',
        'UBCHI',
        'Atbash',
        'Albam',
        'Achbi',
        'Avgad',
        'Caesar',
        'Affine',
        'Polybius',
        'Monoalphabetic substitution',
        'Tritheme',
        'Porta',
        'Vigenere',
        'Beaufort',
        'Gronsfeld',
        'Autoclave',
        'Four squares',
        'Hill',
        'ABC',
        'ADFGX',
        'ADFGVX'
    ),
}


def get_ciph(cipher, *args, **kargs):
    """Return the cipher. object."""
    
    return crypta_ciphers[cipher](*args, **kargs)


def make_ciph(ciph, key=None, key2=None, alf=alf_az, ignore=False, verbose=True, interface=None, **kargs):
    """Return the cipher usable to encrypt."""
    
    #Todo: There is certainly a better way to do this.
    
    if ciph in ciph_types['verbose, interface']:
        if ciph == 'Reverse code word':
            return ReverseCode('word', verbose, interface)
            
        return get_ciph(ciph, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['key, interface']:
        return get_ciph(ciph, key=key, interface=interface)
    
    elif ciph in ciph_types['key, verbose, interface']:
        return get_ciph(ciph, key=key, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['key, key2, alf, interface']:
        return get_ciph(ciph, key, key2, alf=alf, interface=interface)
    
    elif ciph in ciph_types['key, alf, interface']:
        return get_ciph(ciph, key=key, alf=alf, interface=interface)
    
    elif ciph in ciph_types['key, alf, ignore, interface']:
        return get_ciph(ciph, key=key, alf=alf, ignore=ignore, interface=interface)
    
    elif ciph in ciph_types['key, alf, verbose, interface']:
        return get_ciph(ciph, key=key, alf=alf, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['alf, ignore, verbose, interface']:
        return get_ciph(ciph, alf=alf, ignore=ignore, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['key, alf, ignore, verbose, interface']:
        return get_ciph(ciph, key=key, alf=alf, ignore=ignore, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['key, key2, alf, ignore, interface']:
        return get_ciph(ciph, key, key2, alf=alf, ignore=ignore, interface=interface)
    
    elif ciph in ciph_types['key, key2, alf, ignore, verbose, interface']:
        return get_ciph(ciph, key, key2, alf=alf, ignore=ignore, verbose=verbose, interface=interface)
    
    elif ciph in ciph_types['key, indexes, alf, ignore, space, verbose, interface']:
        return get_ciph(ciph, key, alf=alf, ignore=ignore, verbose=verbose, interface=interface, **kargs)
    
    else:
        raise NotImplemented('The cipher "{}" was NOT found !!!\nIf it exists, please add it to the dict "ciph_types".'.format(ciph))
    
    
    
    
##------codes

#todo: add a description for every code ! (from wikipedia, like Decrypto)

#todo: add Binary code.

class Morse(BaseCipher):
    """Define the Morse code."""
    
    def __init__(self, a='.', b='-', c_sep=' ', w_sep='/', verbose=True, interface=None):
        """Initiate the Morse code.
        
        - a       : Short signal ;
        - b       : Long signal ;
        - c_sep   : Character separation ;
        - w_sep   : Word separation ;
        - verbose : A boolean. Print 'Morse' in `meaning` if True.
        """
        
        super().__init__('Morse', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        self.verbose = verbose
        
        self.alf = {
            'a': a + b,
            'b': b + a*3,
            'c': b + a + b + a,
            'd': b + a*2,
            'e': a,
            'f': 2*a + b + a,
            'g': 2*b + a,
            'h': 4*a,
            'i': 2*a,
            'j': a + 3*b,
            'k': b + a + b,
            'l': a + b + a + a,
            'm': 2*b,
            'n': b + a,
            'o': 3*b,
            'p': a + 2*b + a,
            'q': 2*b + a + b,
            'r': a + b + a,
            's': 3*a,
            't': b,
            'u': 2*a + b,
            'v': 3*a + b,
            'w': a + 2*b,
            'x': b + 2*a + b,
            'y': b + a + 2*b,
            'z': 2*b + 2*a,
            
            '0': 5*b,
            '1': a + 4*b,
            '2': 2*a + 3*b,
            '3': 3*a + 2*b,
            '4': 4*a + b,
            '5': 5*a,
            '6': b + 4*a,
            '7': 2*b + 3*a,
            '8': 3*b + 2*a,
            '9': 4*b + a,
            
            ' ': w_sep
        }
        
        self.alf_d = {} #Same dict, but keys/values reversed.
        for k in self.alf:
            self.alf_d[self.alf[k]] = k
        
        self.c_sep = c_sep #Character separation
        self.w_sep = w_sep #Words separation


    def encrypt(self, txt):
        """Encode 'txt' using the Morse code."""
        
        txt = msgform(txt)
        
        ret = ''
        for k in txt:
            if k in self.alf:
                ret += self.alf[k] + ' '
        
        return ret


    def decrypt(self, txt):
        """Decode the Morse code."""
        
        txt = txt.split(self.c_sep)
        
        ret = ''
        for k in txt:
            if k in self.alf_d:
                ret += self.alf_d[k]
        
        return ret
    
    def break_(self, txt):
        """Return txt decoded using the self.decrypt method."""
        
        return self.decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """Use the function 'ver_plain_text' which search if the text mean something."""
        
        if self.verbose:
            print('Morse')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk, False):
            return (True, brk)
            
        else:
            return (False,)


##------ciphers


##---transposition

#---------Reverse code
class ReverseCode(BaseCipher):
    """Defining the reverse code."""
    
    def __init__(self, mode='all', verbose=True, interface=None):
        """
        Initiate the reverse code.
        
        mode : how to encode. Should be in ('all', 'word').
            .all :
                reverse the whole string ;
            
            .word :
                reverse the words.
        """
        
        super().__init__('Reverse code', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if mode not in ('all', 'word'):
            raise ValueError('"mode" arg should be "all", or "word", but "{}" found !!!'.format(mode))
        
        self.mode = mode
        self.verbose = verbose
        

    def encrypt(self, txt):
        """Encode 'txt' using the reverse code."""
        
        if self.mode == 'all':
            return txt[::-1]
        
        else:
            lst = txt.split(' ')
            
            ret = ''
            for k in lst:
                ret += k[::-1] + ' '
                
            ret = ret[:-1] #Revome last space
            
            return ret
    
    
    def decrypt(self, txt):
        """Decode 'txt' using the reverse code. Same as self.encrypt."""
        
        return self.encrypt(txt)
    
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """Use the function 'ver_plain_text' which search if the text mean something."""
        
        if self.verbose:
            print('Reverse code')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)

#---------Scytale
class Scytale(BaseCipher):
    """Defining the Scytale cipher."""
    
    def __init__(self, key=None, verbose=True, interface=None):
        """Initiate the Scytale cipher.
        
        key : an intenger, or None to brute-force it ;
        verbose : A boolean. Print 'Scytale' in meaning if True.
        """
        
        super().__init__('Scytale', pb_mn=1, interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if key != None:
            try:
                self.key = int(key)
            
            except ValueError:
                raise ValueError('"key" should be an int, but "{}" of type "{}" was found !!!'.format(key, type(key)))
        
        else:
            self.key = None
        
        self.verbose = verbose
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' with the Scytale cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        T = write_lines_c(txt, self.key)
        return read_columns(T)
    
    def decrypt(self, txt):
        """Decrypt 'txt' with the Scytale cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        T = write_columns_c(txt, self.key)
        return read_lines(T)
    
    def brute_force(self, txt):
        """Return a dict cointaining all the possibles decryptions, associated with their keys."""
        
        lth = len(txt)
        
        brk = {}
        for k in range(1, lth):
            brk[k] = Scytale(k).decrypt(txt)
        
            self.pb_set(k, lth, bar='brk')
        
        return brk
    
    def meaning(self, txt, brk=None):
        """Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if self.verbose:
            print('Scytale\nMethod : brute-force')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], k)
            
        return (False,)
    
    def gen_key(self, txt_lth):
        """Generate a Scytale key."""
        
        return randint(1, txt_lth - 1)


#---------Rail fence
class RailFence(BaseCipher):
    """Defining the Rail fence cipher."""
    
    def __init__(self, key=None, verbose=True, interface=None):
        """Initiate the Rail fence cipher.
        
        key : an intenger, or None to brute-force it ;
        verbose : A boolean. Print 'Rail fence' in meaning if True.
        """
        
        super().__init__('Rail fence', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
            
        self.verbose = verbose
        
        if key != None:
            try:
                self.key = int(key)
            
            except ValueError:
                raise ValueError('"key" should be an int, but "{}" of type "{}" was found !!!'.format(key, type(key)))
            
            self.lst = []
            for k in range(key):
                self.lst.append([]) # Creating a list of the levels
        
        else:
            self.key = None
            self.lst = None
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' with the Rail fence cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        lst = list(self.lst) #Creating a copy
        
        lvl = 0 #Level
        m = 1 #step
        
        for k in txt:
            lst[lvl].append(k)
            
            if lvl == self.key - 1:
                m = -1
            
            elif lvl == 0:
                m = 1
            
            lvl += m
    
        ret = ''
        for k in lst:
            ret += ''.join(k)
        
        return ret
    
    def decrypt(self, txt):
        """Decrypt 'txt' with the Rail fence cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        lst = list(self.lst) #Creating a copy
        
        lth = len(txt)
        ttest = 'X'*lth
        lvl = 0
        m = 1
        
        for k in ttest:
            lst[lvl].append(k)
            
            if lvl == self.key - 1:
                m = -1
                
            elif lvl == 0:
                m = 1
            
            lvl += m
        
        n = 0
        for k in lst:
            for i, j in enumerate(k):
                k[i] = txt[n]
                n += 1
        
        ret = ''
        lvl = 0
        m = 1
        
        while len(ret) != lth:
            if lvl >= len(lst) or lvl < 0:
                m = 0 - m
                lvl += 2 * m
            
            if len(lst[lvl]) != 0:
                ret += lst[lvl][0]
                del lst[lvl][0]
            
            lvl += m
    
        return ret
    
    
    def brute_force(self, txt):
        """Return a dict cointaining all the possibles decryptions, associated with their keys."""
        
        lth = len(txt)
        brk = {}
        
        for k in range(2, lth):
            brk[k] = RailFence(k).decrypt(txt)

            self.pb_set(k, lth, bar='brk')
        
        return brk
    
    def meaning(self, txt, brk=None):
        """Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if self.verbose:
            print('Rail fence\nMethod : brute-force')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], k)
            
        return (False,)
    
    def gen_key(self, txt_lth):
        """Generate a Rail fence key."""
        
        return randint(2, txt_lth - 1)


#---------Fleissner
class Fleissner(BaseCipher):
    """Defining the Fleissner cipher."""
    
    def __init__(self, key=[], alf=alf_az, interface=None):
        """Initiate the Fleissner cipher.
        
        key : a square matrix (list of lists). Ex :
            0 1 0 0
            1 1 0 0
            0 0 0 0
            0 0 0 1
            key = [[0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]] ;
        
        alf : the alphabet to use.
        """
        
        super().__init__('Fleissner', interface=interface)
        
        if type(key) not in (list, tuple, set):
            raise ValueError('The argument "key" should be a list (a square matrix), but a "{}" was found !!!'.format(type(key)))
        
        #------check if the key is a square matrix and get the size
        self.size = len(key)
        for j, k in enumerate(key):
            if type(k) not in (list, tuple, set):
                raise ValueError('The argument "key" should be a list of lists (a square matrix), but "key[{}]" is a "{}" !!!'.format(j, type(k)))
            
            if len(k) != self.size:
                raise ValueError('The argument "key" should be a square matrix (list of lists), but "key[{}]" has not the same size as "key" !!!'.format(j))
        
        #------define the self values
        self.L_key = [key]
        for k in range(3):
            self.L_key.append(self._right_turn_key(self.L_key[k]))
        
        self.n = self.size **2
        
        self.key = list(key)
        self.alf = alf
    
    
    def __repr__(self):
        """Represent the Fleissner cipher object."""
        
        ret_key = '\n'
        for line in self.key:
            ret_key += '\t'
            for k in line:
                ret_key += str(k) + ' '
            
            ret_key += '\n'
        
        return "Fleissner(alf='{}', interface='{}', key={})".format(
            self.alf,
            self.interface,
            ret_key
        )
    
    
    def _right_turn_key(self, L):
        L2 = []
        for i in range(self.size):
            L2.append([])
            for j in range(self.size - 1, -1, -1):
                L2[i].append(L[j][i])

        return L2


    def encrypt(self, txt):
        """Encrypt 'txt' with the Fleissner cipher."""
        
        txt_e = ""
        grid = ""
        
        while len(txt) % self.n != 0:
            txt += choice(self.alf)
        
        for i in range(0, len(txt), self.n):
            block = txt[i:i + self.n]
            grid = [""] * self.n
            c = 0
            
            for j in range(4):
                L = self.L_key[j]
                
                for k in range(self.n):
                    if L[k // self.size][k % self.size] in (1, '1'):
                        grid[k] = block[c % len(block)]
                        c += 1
                    
            txt_e += "".join(grid)

        return txt_e
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Fleissner cipher."""
        
        if len(txt) % self.n != 0:
            raise ValueError('The length of the text is not a square number !!!')
        
        txt_d = ""
        grid = ""
        
        for i in range(0, len(txt), self.n):    # Cutting the text in blocks of length self.size²
            grid = txt[i:i + self.n]
            
            for j in range(4):                  # Four times because we turn the key four times
                L = self.L_key[j]
                
                for k in range(self.n):
                    if L[k // self.size][k % self.size] in (1, '1'):    #If there is a whole (1)
                        txt_d += grid[k]
        
        return txt_d
    
    
    def gen_key(self, size):
        """Generate a Fleissner key.
        In __init__, set the key to [] to generate a key : key = Fleissner([]).gen_key(size).
        """
        
        if type(size) != int:
            raise ValueError('The argument "size" should be an intenger, but "{}" of type "{}" was found !!!'.format(size, type(size)))
        
        key = []
        
        for k in range(size):
            key.append([randint(0, 1) for k in range(size)])
        
        return key


class ColumnarTransposition(BaseCipher):
    """Defining the columnar transposition cipher."""
    
    def __init__(self, key=None, alf=alf_az, verbose=True, interface=None):
        """Initiate the columnar transposition cipher.
        
        - key : the key. Should be a string, or a list ;
        - alf : the alphabet to use (to make the key). Default is alf_az ;
        - verbose : a boolean. If True, print the cipher's name in self.brute_force ;
        - interface : the interface using the class (used in BaseCipher).
        """
        
        super().__init__('Columnar transposition', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.alf = alf
        
        if type(key) not in (str, tuple, list, set) and key != None:
            raise ValueError('The key should be a string, but "{}" of type "{}" was found !!!'.format(key, type(key)))
        
        if key == None:
            self.key = None
            self.nc = None
            
        else:
            if type(key) == str:
                self.key = word_to_transposition_key(key, alf)
            else:
                self.key = key
                
            self.nc = len(self.key)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the columnar transposition cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        T = write_lines_c(txt, self.nc)
        c = ""
        
        for k in range(self.nc):
            i = self.key[k]
            
            for l in T:
                if len(l) > i:
                    c += l[i]
        
        return c
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the columnar transposition cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        nl = len(txt) // self.nc
        r = len(txt) % self.nc
        
        T = []
        
        if r != 0:
            nl += 1
        
        for k in range(nl):
            if k == nl - 1 and r != 0:
                T.append([""] * r)
            
            else:
                T.append([""] * self.nc)
        
        for i in range(self.nc):
            j = self.key[i]
            
            for k in range(nl):
                if k != nl - 1 or r == 0 or j < r:
                    T[k][j] = txt[0]
                    txt = txt[1:len(txt)]
        
        return read_lines(T)
    
    
    def brute_force(self, txt):
        """
        Return a dict of the from {k0 : d0, k1 : d1, ..., kn : dn}, 
        where k is the key, and d the decrypted message with that key.
        """
        
        if self.verbose:
            print('Columnar transposition cipher')
            print('Method : Brute force (on all the keys of 9 letters)')
        
        L = [0]
        brk = {}
        
        total = sum(fact(k) for k in range(1, 10)) * 9 # Is it the right amount ?
        
        for j in range(1, 10):
            L.append(j)
            
            for i, k in enumerate(itertools.permutations(L, j + 1)):
                brk[k] = ColumnarTransposition(k, self.alf).decrypt(txt)
                
                if i % 2**4 == 0:
                    self.pb_set(i, total, bar='brk')

            self.pb_set(i, total, bar='brk')

        self.pb_set(i, total, bar='brk')
        
        return brk
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        # if self.verbose:
        #     print('Columnar transposition\nMethod : brute-force (on all the keys of 9 letters)')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], k)
            
        return (False,)
    
    
    def gen_key(self, lth):
        """
        Generate a Columnar transposition string key.
        
        - lth : the key's length.
        """
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


class UBCHI(BaseCipher):
    """Defining the UBCHI cipher (double columnar transposition)."""
    
    def __init__(self, key=None, alf=alf_az, verbose=True, interface=None):
        """Initiate the UBCHI cipher.
        
        - key : the key. Should be a string, or a list ;
        - alf : the alphabet to use (to make the key). Default is alf_az ;
        - verbose : a boolean. If True, print the cipher's name in self.brute_force ;
        - interface : the interface using the class (used in BaseCipher).
        """
        
        super().__init__('UBCHI', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.alf = alf
        
        self.col_trans = ColumnarTransposition(key, self.alf, self.verbose, self.interface)
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the UBCHI cipher."""
        
        return self.col_trans.encrypt(self.col_trans.encrypt(txt))
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the UBCHI cipher."""
        
        return self.col_trans.decrypt(self.col_trans.decrypt(txt))
    
    def brute_force(self, txt):
        """
        Return a dict of the from {k0 : d0, k1 : d1, ..., kn : dn}, 
        where k is the key, and d the decrypted message with that key.
        """
        
        if self.verbose:
            print('UBCHI cipher')
            print('Method : Brute force (on all the keys of 9 letters)')
        
        L = [0]
        brk = {}
        
        total = sum(fact(k) for k in range(1, 10)) * 9 #todo: is it it ?
        
        for j in range(1, 10):
            L.append(j)
            
            for i, k in enumerate(itertools.permutations(L, j + 1)):
                brk[k] = UBCHI(k, self.alf).decrypt(txt)
                
                if i % 2**4 == 0:
                    self.pb_set(i,total, bar='brk')

            self.pb_set(i,total, bar='brk')

        self.pb_set(i,total, bar='brk')
        
        return brk
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if self.verbose:
            print('UBCHI\nMethod : brute-force (on all the keys of 9 letters)')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], k)
            
        return (False,)
    
    
    def gen_key(self, lth):
        """Return an UBCHI string key (same as Columnar transposition key)"""
        
        return self.col_trans.gen_key(lth)


##---substitution
    

##-monoalphabetic

class Atbash(BaseCipher):
    """Defining the Atbash code."""
    
    def __init__(self, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Atbash code.

        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Atbash', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')

        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        self.alf = alf
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Atbash code"""
        
        dct = gen_dic_ite(self.alf)
        alf_2 = "".join(reversed(self.alf))
        msg_c = ''
        
        for k in txt:
            if dct.get(k):
                msg_c += alf_2[dct[k]]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Atbash code."""
        
        return self.encrypt(txt)
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Atbash code')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)


class Albam(BaseCipher):
    """Defining the Albam code."""
    
    def __init__(self, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Albam code.
        Cf to the Caesar class for more infos on the arguments.
        """
        
        super().__init__('Albam', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.alf = alf
        
        self.caesar = Caesar(13, alf, ignore, self.verbose, self.interface)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Albam code."""
        
        return self.caesar.encrypt(txt)
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Albam code."""
        
        return self.encrypt(txt)
    
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Albam code')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)


class Achbi(BaseCipher):
    """Definig the Achbi code."""
    
    def __init__(self, alf=alf_az, ignore=False, verbose=True, interface=None):
        """Initiate the Achbi code."""
        
        super().__init__('Achbi', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        self.alf = alf
        alf_1 = alf[:len(alf)//2][::-1] #[::-1] reverse the string.
        alf_2 = alf[len(alf)//2:][::-1]
        self.alf_c = alf_1 + alf_2
    
    def encrypt(self, txt):
        """Encrypt 'txt' with the Achbi code."""
        
        return MonoSub(self.alf_c, self.alf, self.ignore, self.verbose, self.interface).encrypt(txt)
    
    def decrypt(self, txt):
        """Decrypt 'txt' with the Achbi code."""
        
        return self.encrypt(txt)
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Achbi code')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)


class Avgad(BaseCipher):
    """Defining the Avgad code."""
    
    def __init__(self, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Avgad code.
        Cf to the Caesar class for more info on the arguments.
        """
        
        super().__init__('Avgad', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.alf = alf
        
        self.caesar = Caesar(1, self.alf, ignore, self.verbose, self.interface)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Avgad code."""
        
        return self.caesar.encrypt(txt)
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Avgad code."""
        
        return self.caesar.decrypt(txt)
    
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Achbi code')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)


class Caesar(BaseCipher):
    """Defining the Caesar cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Caesar cipher.
        
        - key : the Caesar key. Should be an int, or a string. If it is a string,
        it should have a length of 1, and be in alf ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Caesar', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        self.alf = alf
        
        if key != None:
            if type(key) not in (int, str):
                raise ValueError('The key must be either a string or an intenger, but "{}", of type "{}" was found !!!'.format(key, type(key)))
            
            elif type(key) == str:
                if len(key) != 1:
                    raise ValueError('The key, if a string, must have a length of one, but "{}", of length {} was found !!!'.format(key, len(key)))
                
                elif key not in alf:
                    raise ValueError('The key, if a string, should be contained in the alphabet !!!')
                
                self.key = alf.index(key)
            
            else:
                self.key = key % 26
        
        else:
            self.key = None
        
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Caesar cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        msg_c = ''
        
        for k in txt:
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(k) + self.key) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Caesar cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        key_d = self.lalf - self.key
        
        return Caesar(key_d, self.alf, self.ignore, self.verbose, self.interface).encrypt(txt)
    
    
    def brute_force(self, txt):
        """
        Return a dict of the from {'alf' : alf, k0 : d0, k1 : d1, ..., k26 : d26}, 
        where k is the key, and d the decrypted message with that key.
        """
        
        if self.verbose:
            print('Caesar cipher')
            print('Method : brute-force')
        
        brk = {'alf' : self.alf}
        for k in range(1, len(self.alf) + 1):
            brk[k] = Caesar(k, self.alf, interface=self.interface).decrypt(txt)
        
        return brk
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if self.verbose:
            print('Caesar cipher')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], k, 1, brk['alf'])
                
            else:
                return (False,)
    
    
    def gen_key(self):
        """Return a random number in [1 ; 25]."""
        
        return randint(1, 25)


class Affine(BaseCipher):
    """Defining the Affine cipher."""
    
    def __init__(self, keyA=None, keyB=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Affine cipher.
        
        The key is of the form `y = (ax + b) mod 26`, where `x` is the position
        of the letter in the alphabet. `y` is the final position in the alphabet.
        `a` and len(alf) must be co-prime.
        
        - keyA : the `a` part of the key. Should be an int, or None to brute-force it ;
        - keyB : the `b` part of the key. Should be an int, or None to brute-force it ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Affine', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        self.alf = alf
        self.lalf = len(alf)
        
        if keyA == keyB == None:
            self.keyA = None
            self.keyB = None
        
        elif keyA != keyB == None or keyB != keyA == None:
            raise ValueError('The keys `a` and `b` should be both None (to brute-force a message), or both intengers, but only one was None !!!')
        
        elif type(keyA) != int or type(keyB) != int:
            raise ValueError('The keys should be intengers (or None to brute-force a message) !!!')
        
        elif gcd(keyA, self.lalf) != 1:
            raise ValueError("the key `a` must be co-prime with the alphabet's length !!!")
        
        else:
            self.keyA = keyA
            self.keyB = keyB
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Affine cipher."""
        
        if None in (self.keyA, self.keyB):
            raise ValueError("Can't encrypt with empty keys !!!")
        
        msg_c = ''
        
        for k in txt:
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(k) * self.keyA + self.keyB) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Affine cipher."""
        
        if None in (self.keyA, self.keyB):
            raise ValueError("Can't decrypt with empty keys !!!")
        
        keyA = inverse(self.keyA, self.lalf)
        
        msg_d = ''
        
        for k in txt:
            if k in self.alf:
                msg_d += self.alf[((self.alf.index(k) - self.keyB) * keyA) % self.lalf]
            
            elif not self.ignore:
                msg_d += k
        
        return msg_d
    
    
    def _get_bf_lth(self, lth=26):
        """
        Return the number of iteration the method 'brute_force' will have to
        do, for the progress bar.
        """
        
        n = 0
        
        for a in range(lth):
            if gcd(a, lth) == 1:
                for b in range(lth):
                    n += 1
        
        return n
    
    
    def brute_force(self, txt):
        """
        Return a dict of the from {(ka0, kb0) : d0, (ka1, kb1) : d1, ..., (kan, kbn) : dn}, 
        where k is the key, and d the decrypted message with that key.
        """
        
        if self.verbose:
            print('Affine cipher')
            print('Method : brute-force')
        
        lth = self._get_bf_lth(self.lalf)
        i = 0
        
        brk = {'alf' : self.alf}
        for kA in range(self.lalf):
            if gcd(kA, self.lalf) == 1:
                for kB in range(self.lalf):
                    brk[(kA, kB)] = Affine(kA, kB, self.alf).decrypt(txt)
                    
                    self.pb_set(i, lth, 'brk')
                    i +=1
        
        return brk
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if self.verbose:
            print('Affine cipher\nMethod : brute-force')
        
        if brk == None:
            brk = self.brute_force(txt)
        
        for k in brk:
            if ver_plain_text(brk[k]):
                return (True, brk[k], *k, brk['alf'])
            
        return (False,)
    
    
    def gen_key(self):
        """
        Return affine keys, according to self.lalf, in a tuple of the form :
            (kA, kB).
        """
        
        kA = 0
        while gcd(kA, self.lalf) != 1:
            kA = randint(1, self.lalf)
        
        kB = randint(1, self.lalf)
        
        return (kA, kB)

    
class Polybius(BaseCipher):
    """Defining the Polybius square code."""
    
    def __init__(self, key='', indexes='12345', alf=alf_25, ignore=False, space=True, verbose=True, interface=None):
        """
        Initiate the Polybius square code.
        
        - key : the string used in 'word_to_square'. Default is '' ;
        - indexes : the list of the indexes for the square. Default are '12345' ;
        - alf the alphabet to use. Defaut is alf_25, which is alf_az without 'j' ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return ;
        - space : a boolean which indicate if there is spaces between the encoded letters.
        """
        
        super().__init__('Polybius', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if len(indexes) not in (5, 6):
            raise ValueError('The length of "indexes" should be of 5 or 6, but it has a length of "{}" !!!'.format(len(indexes)))
        
        self.size = len(indexes)
        self.square = word_to_square(key, self.size)
        self.ind = tuple(list(indexes))
        self.alf = alf
        self.space = space
        
        self.d_e = {}
        for a, i in enumerate(self.square):
            for b, j in enumerate(i):
                self.d_e[j] = self.ind[a] + self.ind[b]
        
        self.d_d = {} #Same dict, but keys/values reversed.
        for k in self.d_e:
            self.d_d[self.d_e[k]] = k
        
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Polybius square code."""
        
        msg_c = ''
        
        for k in txt:
            if k in self.d_e:
                msg_c += self.d_e[k]
                
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        if self.space:
            msg_c = space(msg_c, 2)
    
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Polybius square code."""
        
        msg_d = ''
        
        if not self.space:
            txt = space(txt, 2)
        
        txt = txt.split(' ')
        
        for k in txt:
            if k in self.d_d:
                msg_d += self.d_d[k]
            
            elif not self.ignore:
                msg_d += k
            
            else:
                print('Unknown encrypted group "{}" !'.format(k))
    
        return msg_d
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


class MonoSub(BaseCipher):
    """Define the Monoalphabetic substitution cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Monoalphabetic substitution cipher.
        
        - key : the MonoSub key. Should be a string, or a list ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Monoalphabetic substitution', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if key != None:
            if type(key) not in (str, list, tuple, set):
                raise ValueError('The key should be a string, or a list, but "{}" of type "{}" was found !!!'.format(key, type(key)))

            self.alf_c = generate_alphabet_word(key, alf)
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Monoalphabetic substitution cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        msg_c = ''
        
        for k in txt:
            if k in self.alf:
                msg_c += self.alf_c[self.alf.index(k)]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Monoalphabetic substitution cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        msg_d = ''
        
        for k in txt:
            if k in self.alf:
                msg_d += self.alf[self.alf_c.index(k)]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Unknown "{}" ! (try ignore=False)'.format(k))
        
        return msg_d
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key
    
    
    def break_(self, txt, n=10**4, alea=False):
        """
        Try to get the decryption of 'txt' without the key.
        
        - txt : the text to break ;
        - n : the number of tries ;
        - alea : a boolean which indicates if use some random values.
        
        Return :
            txt_brk, key, score.
        """
        
        if self.verbose:
            print('Monoalphabetic substitution cipher')
            print('Method : Hill-climbing')
        
        f_ana = FreqAna().ana(txt)
        key = list(alf_az)
        alf = str(alf_az) #todo: take the self.alf ? + take FreqAna.comp ?
        freq = 'easintrulodcpmvqgfhbjxyzkw' #todo: change if english or french.
        
        for j, k in enumerate(f_ana):
            a = key.index(k[0])
            b = alf.index(freq[j])
            key[a], key[b] = key[b], key[a]
        
        txt2 = MonoSub(key, ignore=self.ignore, interface=self.interface).decrypt(txt)
        print('\n---------\n{}\n---------\n'.format(txt2))
        
        score = prob_plain_text(txt2)
        
        for k in range(n):
            key_2 = key.copy()
            
            for i in range((1, randint(0, 25))[alea]):
                a = randint(0, 25)
                b = randint(0, 25)
                
                if a == b:
                    b = (b + 1) % 26
                
                key_2[a], key_2[b] = key_2[b], key_2[a]
            
            txt3 = MonoSub(key_2, ignore=self.ignore, interface=self.interface).decrypt(txt)
            s2 = prob_plain_text(txt3)
            
            if s2 > score:
                print(f'score : {score}')
                key = key_2
                score = s2
                txt2 = txt3
        
        
        return txt2, ''.join(key), score
        
        
    def meaning(self, txt, brk=None, n=10**4, alea=False):
        """
        Use the function 'ver_plain_text', which search if the text mean 
        something, to find out if an item in the break list makes sense.
        """
        
        if brk == None:
            txt_brk, key, score = self.break_(txt, n, alea)
        
        else:
            txt_brk, key, score = brk

        if ver_plain_text(txt_brk, False):
            return (True, txt_brk, ''.join(key))
            
        else:
            print(txt_brk, score)
            return (False,)



##-polyalphabetic

class Tritheme(BaseCipher):
    """Class defining the Tritheme cipher."""
    
    def __init__(self, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Tritheme cipher.

        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Tritheme', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        self.alf = alf
        self.lalf = len(alf)


    def encrypt(self, txt):
        """Encrypt 'txt' using the Tritheme cipher."""
        
        msg_c = ''
        
        for j, k in enumerate(txt):
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(k) + j) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c


    def decrypt(self, txt):
        """Decrypt 'txt' using the Tritheme cipher."""
        
        msg_d = ''
        
        for j, k in enumerate(txt):
            if k in self.alf:
                msg_d += self.alf[(self.alf.index(k) - j + self.lalf) % self.lalf]
            
            elif not self.ignore:
                msg_d += k
            
            elif self.verbose:
                print('Unknown "{}" ! (try ignore=False)'.format(k))
        
        return msg_d
    
    
    def break_(self, txt):
        """Return self.decrypt(txt)"""
        
        return self.decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Tritheme cipher')
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk):
            return (True, brk)
            
        else:
            return (False,)


class Porta(BaseCipher):
    """Defining the Porta cipher."""
    
    def __init__(self, key, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Porta cipher.
        
        - key : a string ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Porta', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if type(key) != str:
            raise ValueError('The key must be a string, but "{}", of type "{}" was found !!!'.format(key, type(key)))
        
        self.key = key
        self.lkey = len(key)
        
        self.alf = alf
        self.alf_0 = alf[:len(alf) // 2]
        self.alf_1 = alf[len(alf) // 2:]
        
        self.lalf_0 = len(self.alf_0)        
        self.lalf_1 = len(self.alf_1)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Porta cipher."""
        
        msg_c = ''
        
        for j, k in enumerate(txt):
            ck = self.alf.index(self.key[j % self.lkey])
            
            if k in self.alf_0:
                msg_c += self.alf_1[(self.alf_0.index(k) - ck // 2) % self.lalf_1]
                
            elif k in self.alf_1:
                msg_c += self.alf_0[(self.alf_1.index(k) + ck // 2) % self.lalf_0]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Porta cipher."""
        
        return self.encrypt(txt)
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key
    


class Vigenere(BaseCipher):
    """Defining the Vigenere cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Vigenere cipher.
        
        - key : a string. All the characters of the keys should be in the alphabet ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Vigenere', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if key != None:
            if type(key) != str:
                raise ValueError('The key must be a string, but "{}", of type "{}" was found !!!'.format(key, type(key)))
            
            for j, k in enumerate(key):
                if k not in alf:
                    raise ValueError('Invalid character "{}" at position {} in the key !!! (it is not in the alphabet)'.format(k, j, key))

            self.lkey = len(key)
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Vigenere cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        msg_c = ''
        
        for j, k in enumerate(txt):
            ck = self.alf.index(self.key[j % self.lkey])
            
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(k) + ck) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
        
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Vigenere cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        msg_d = ''
        
        for j, k in enumerate(txt):
            ck = self.alf.index(self.key[j % self.lkey])
            
            if k in self.alf:
                msg_d += self.alf[(self.alf.index(k) - ck + self.lalf) % self.lalf]
            
            elif not self.ignore:
                msg_d += k
            
            elif self.verbose:
                print('Unknown character "{}" ! It is not in the alphabet ! (try ignore=False)'.format(k))
        
        return msg_d
    
    
    def _lth_key(self, txt, grp=3):
        """
        This function determines the length of the key, it
        mark the groups of 'grp' letters which are repeated in the coded msg
        and assume that there is a very high probability that the same group of 'grp'
        letters be encoded with the same 'grp' letters of the message and the same 'grp'
        letters of the key.
        
        Example :
            message  : .....DES...........DES...........DES.........DES....DES
            key      : ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD
            code     : .....EGV.........................EGV.........EGV..........
            distance :      <----------24--------------><----8----->
    
            The length of the key divides the GCD by 24 and 8.
        
        site : 'http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/expose_vigenere.html'
        """

        #---reading the message to get every position
        dct = {}
        for k in range(len(txt) - 2):
            t = txt[k:k + grp]
            
            if t in dct:
                dct[t].append(k)
            
            else:
                dct[t] = [k]

        #---distance
        dis = []
        for d in dct :
            p = dct[d]
            if len(p) > 1:
                for i in range(0, len(p) - 1):
                    dis.append(p[i+1] - p[i])
                    
                    if self.verbose:
                        print(d, p[i + 1] - p[i], '---', float(p[i + 1] - p[i]) / 8)

        #---GCD
        if len(dis) == 0:
            raise Exception('Impossible to determine the key') #todo: improve this error message

        elif len(dis) == 1:
            return dis[0]

        lth = gcd(dis[0], dis[1])
        for d in dis :
            lth = gcd(lth, d)

        if lth > 5: #if the length is sufficient, the result may be good.
            return lth
            
        else: #Else, relaunching the algo with bigger groups.
            return self._lth_key(txt, grp + 1)
    
    
    def _find_key(self, txt, lth, mfl='e'):
        """
        Determine the key of the encrypted message 'txt', knowing its length,
        assuming that the letter 'mfl' is the most frequent.
        
        - txt : encrypted message ;
        - lth : supposed length of the key ;
        - mfl : the supposed most frequent letter. Should be a string, of length 1 and be in the alphabet.
        
        Return the key.
        
        site : 'http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/expose_vigenere.html'
        """
        
        if type(mfl) != str:
            raise ValueError('The argument "mfl" should be a string !!!')
        
        elif len(mfl) != 1:
            raise ValueError('The argument "mfl" should have a length of 1 !!!')
        
        elif mfl not in self.alf:
            raise ValueError('The argument "mfl" should be in the alphabet !!!')

        key = ''
        for k in range(lth):
            nb = [0 for k in self.alf]
            lt = txt[k:len(txt):lth] #Extracting all the letters (k, k + lth, k + 2lth, ...)
            
            for j in lt:
                nb[self.alf.index(j)] += 1
            
            mx_v = max(nb)
            mx = nb.index(mx_v)
            
            #Finding the letter which has encrypted the 'mfl' at self.alf[mx]
            key += self.alf[(mx + self.lalf - self.alf.index(mfl)) % self.lalf]
        
        return key
    
    
    def break_(self, txt, mfl='e'):
        """Return :
            (key, txt_d).
        
        key : the founded key ;
        txt_d : 'txt' decrypted with the founded key.
        """
        
        txt = msgform(txt)
        
        key_lth = self._lth_key(txt)
        key = self._find_key(txt, key_lth, mfl)
        
        return key, Vigenere(key, self.alf, self.ignore, self.verbose, self.interface).decrypt(txt)
    
    
    def meaning(self, txt, brk=None):
        """
        Use the function 'ver_plain_text', which search if the text mean
        something, to find out if the broken item makes sense.
        """
        
        if self.verbose:
            print('Vigenere cipher')
        
        
        if Ic(True).calc(txt) > 0.065:
            return (False,)
            
        f = Friedman().ana(txt)
        if f[1][f[0] - 1] < 0.065:
            return (False,)
        
        if brk == None:
            brk = self.break_(txt)
        
        if ver_plain_text(brk[1]):
            return (True, brk[1], brk[0])
            
        else:
            return (False,)
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


class Beaufort(BaseCipher):
    """Defining the Beaufort cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Beaufort cipher.
        
        - key : a string ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Beaufort', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if key != None:
            if type(key) != str:
                raise ValueError('The key must be a string, but "{}", of type "{}" was found !!!'.format(key, type(key)))
            
            self.lkey = len(key)
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Beaufort cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        msg_c = ''
        lth = len(txt)
        key = self.key * int(lth / lth + 2)
        
        for j, k in enumerate(txt):
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(key[j % self.lkey]) - self.alf.index(k) + self.lalf) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
            
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Beaufort cipher."""
        
        return self.encrypt(txt)
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


class Gronsfeld(BaseCipher):
    """Defining the Gronsfeld cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """Initiate the Gronsfeld cipher.
        
        - key : an intenger ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Gronsfeld', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if key != None:
            if type(key) != int:
                raise ValueError('The key must be an int, but "{}", of type "{}" was found !!!'.format(key, type(key)))
            
            self.lkey = len(str(key))
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Gronsfeld cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        msg_c = ''
        lth = len(txt)
        key = str(self.key) * int(lth / lth + 2)
        
        for j, k in enumerate(txt):
            if k in self.alf:
                msg_c += self.alf[(self.alf.index(k) + int(key[j % self.lkey])) % self.lalf]
            
            elif not self.ignore:
                msg_c += k
            
            elif self.verbose:
                print('Omitting "{}" because it is not in the alphabet !'.format(k))
            
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Gronsfeld cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        msg_d = ''
        lth = len(txt)
        key = str(self.key) * int(lth / lth + 2)
        
        for j, k in enumerate(txt):
            if k in self.alf:
                msg_d += self.alf[(self.alf.index(k) - int(key[j % self.lkey]) + self.lalf) % self.lalf]
            
            elif not self.ignore:
                msg_d += k
            
            elif self.verbose:
                print('Unknown character "{}" ! It is not in the alphabet ! (try ignore=False)'.format(k))
            
        return msg_d
    
    
    def gen_key(self, mn, mx):
        """Return a random number in [mn ; mx]"""
        
        key = randint(mn, mx)
        
        return key


class Autoclave(BaseCipher):
    """Defining the Autoclave cipher."""
    
    def __init__(self, key=None, alf=alf_az, ignore=False, verbose=True, interface=None):
        """
        Initiate the Autoclave cipher.
        
        - key : a string ;
        - alf : the alphabet to use ;
        - ignore : a boolean which indicates what to do if a character of txt (in
        encrypt / decrypt) is not in the alphabet :
            if False, add the character not encrypted (usefull to keep spaces with alf_az),
            else, don't add the character to the return.
        """
        
        super().__init__('Autoclave', interface=interface)
        
        if verbose not in (0, 1):
            raise ValueError('"verbose" arg should be a boolean !!!')
        
        if ignore not in (0, 1):
            raise ValueError('"ignore" arg should be a boolean !!!')
            
        self.verbose = verbose
        self.ignore = ignore
        
        if key != None:
            if type(key) != str:
                raise ValueError('The key must be a string, but "{}", of type "{}" was found !!!'.format(key, type(key)))
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Autoclave cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        key = self.key + txt
        
        return Vigenere(key, self.alf, self.ignore, self.verbose, self.interface).encrypt(txt)
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Autoclave cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        msg_d = ''
        key = self.key
        
        for j, k in enumerate(txt):
            if k in self.alf:
                char = self.alf[(self.alf.index(k) - self.alf.index(key[j]) + self.lalf) % self.lalf]
            
            elif not self.ignore:
                char = k
            
            else:
                char = ''
            
            key += char
            msg_d += char
        
        return msg_d
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


##-polygraphic

class Playfair(BaseCipher):
    """Defining the Playfair cipher."""
    
    def __init__(self, key=None, interface=None):
        """
        Initiate the Playfair cipher.
        
        - key : a string.
        """
        
        super().__init__('Playfair', interface=interface)
        
        if type(key) != str and key != None:
                raise ValueError('The key must be a string, but "{}", of type "{}" was found !!!'.format(key, type(key)))
        
        self.key = key
        self.square = word_to_square(key)
    
    
    def _crypt(self, txt, a=1):
        """Encrypt or decrypt 'txt' using the Playfair cipher."""
        
        if a not in (-1, 1):
            raise ValueError('The arg "a" must be 1 or -1, but "{}" was found !!!'.format(a))
        
        msg = ''
        i1, i2, j1, j2 = 0, 0, 0, 0
        
        txt = txt.replace('j', 'i')
        
        if len(txt) % 2 == 1:
            txt += 'x'
        
        for l in range(len(txt) // 2):
            bi = txt[l * 2:l*2 + 2]
            
            if bi[0] == bi[1]:
                bi = bi[0] + 'q'
            
            for i in range(5):
                for j in range(5):
                    if self.square[i][j] == bi[0]:
                        i1, j1 = i, j
                    
                    elif self.square[i][j] == bi[1]:
                        i2, j2 = i, j
            
            if i1 == i2:
                msg += self.square[i1][(j1 + a) % 5] + self.square[i1][(j2 + a) % 5]
            
            elif j1 == j2:
                msg += self.square[(i1 + a) % 5][j1] + self.square[(i2 + a) % 5][j2]
            
            else:
                msg += self.square[i1][j2] + self.square[i2][j1]
        
        return msg
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' with the Playfair cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        return self._crypt(txt, a=1)
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' with the Playfair cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        return self._crypt(txt, a=-1)
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        key = ''
        for k in range(lth):
            key += choice(self.alf)
        
        return key


class FourSquares(BaseCipher):
    """Defining the Delastelle's Four squares cipher."""
    
    def __init__(self, key1=None, key2=None, alf=alf_az, interface=None):
        """
        Initiate the Four squares cipher.
        
        - key1 : The key #1. Should be a string ;
        - key2 : the key #2. Should also be a string ;
        - alf : the alphabet to use.
        """
        
        super().__init__('Four squares', interface=interface)
        
        if key1 != key2 == None or key2 != key1 == None:
            raise ValueError('The keys 1 and 2 should be both None, or both intengers, but only one was None !!!')
        
        elif (type(key1) != str or type(key2) != str) and not (key1 == key2 == None):
            raise ValueError('The keys should be strings (or None) !!!')
        
        self.key1 = key1
        self.key2 = key2
        self.alf = alf
        
        if key1 != None:
            self.sq_1 = word_to_square(key1)
            self.sq_2 = word_to_square(key2)
        
            alf_sq = word_to_square('')
            self.dct = {}
            for i in range(5):
                for j in range(5):
                    self.dct[alf_sq[i][j]] = (i, j)
            
            self.dct['j'] = self.dct['i']
            
            self.db = {} # Dictionnary of bigrams
            for k in itertools.product(self.alf, repeat=2):
                k0 = self.dct[k[0]]
                k1 = self.dct[k[1]]
                
                self.db[k[0] + k[1]] = self.sq_1[k0[0]][k1[1]] + self.sq_2[k0[1]][k1[0]]
            
            self.db_d = {} #Same, but to decrypt.
            for k in self.db:
                self.db_d[self.db[k]] = k
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Four square cipher."""
        
        if None in (self.key1, self.key2):
            raise ValueError("Can't encrypt with empty key !!!")
        
        msg_c = ''
        
        if len(txt) % 2 == 1:
            txt += 'x'
        
        txt = txt.replace('j', 'i')
        
        for k in range(len(txt) // 2):
            msg_c += self.db[txt[k * 2 : k*2 + 2]]
        
        return msg_c
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Four square cipher."""
        
        if None in (self.key1, self.key2):
            raise ValueError("Can't decrypt with empty key !!!")
        
        msg_d = ''
        
        if len(txt) % 2 == 1:
            txt += 'x'
        
        txt = txt.replace('j', 'i')
        
        for k in range(len(txt) // 2):
            msg_d += self.db_d[txt[k * 2 : k*2 + 2]]
        
        return msg_d
    
    
    def gen_key(self, lth, lth1=None):
        """
        Return a Four squares keys of the form :
            (str, str)
        
        - lth : the length of the first str ;
        - lth1 : the length of the second str. If None (default), take the same as lth.
        """
        
        if lth1 == None:
            lth1 = lth
        
        key1 = ''
        for k in range(lth):
            key1 += choice(self.alf)
        
        key2 = ''
        for k in range(lth1):
            key2 += choice(self.alf)
        
        return (key1, key2)


class Hill(BaseCipher):
    """Defining the Hill cipher."""
    
    def __init__(self, key=None, alf=alf_az, interface=None):
        """
        Initiate the Hill cipher.
        
        - key : the key. Should be a Matrix object (cf modules/base/matrix.py), or 
        a matrixable object, i.e. a list, tuple, or set, containing list, tuple, or set ;
        - alf : the alphabet to use.
        """
        
        super().__init__('Hill', interface=interface)
        
        if key != None:
            if type(key) != Matrix:
                key = Matrix(key) #Errors are tested here (the key's type)
            
            self.dim = len(key[0])
        
        self.key = key
        
        self.alf = alf
        self.lalf = len(alf)
    
    
    def _crypt(self, txt, key):
        """Encrypt or decrypt 'txt' using the Hill cipher."""
        
        txt += 'x'*((self.dim - len(txt) % self.dim) % self.dim)
        
        msg_c = ''
        
        for k in range(len(txt) // self.dim):
            C = [] # Column vector
            
            for l in txt[k * self.dim : (k + 1) * self.dim]:
                C.append([self.alf.index(l)])
            
            C2 = Matrix(C)
            C2 = (key * C2) % self.lalf
            
            for l in C2:
                msg_c += self.alf[int(l[0])]
        
        return msg_c
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the Hill cipher."""
        
        if self.key == None:
            raise ValueError("Can't encrypt with an empty key !!!")
        
        return self._crypt(txt, self.key)
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the Hill cipher."""
        
        if self.key == None:
            raise ValueError("Can't decrypt with an empty key !!!")
        
        return self._crypt(txt, self.key.inverse(self.lalf)) #todo: there will ba an error here (cf inverse in Matrix (+ comatrice))
    
    
    def gen_key(self, size, mn=0, mx=9):
        """Return a Hill key."""
        
        key = [[randint(mn, mx) for i in range(size)] for j in range(size)]
        key = Matrix(key)
        
        return key


class hill:
    def hill(M, text, mode, alphabet='abcdefghijklmnopqrstuvwxyz') :
        if type(M) != Matrix:
            M = Matrix(M)
        la = len(alphabet)
        if mode == 1 :
            M = M.inverse(la)
        dimension = len(M[0])
        text = text + 'x' * ((dimension - len(text) % dimension) % dimension)
        text_c = ""
        for k in range(len(text) // dimension):
            C = []    # column vector
            for l in text[k * dimension:(k+1) * dimension]:
                C.append([alphabet.index(l)])
            C2 = Matrix(C)
            C2 = M * C2
            C2 = C2 % la
            for l in C2:
                text_c = text_c + alphabet[int(l[0])]
        return text_c
    def use():
        print('\nHill cipher')
        alf = cl_inp('Alphabet (let empty to use normal) :')
        if alf == "":
            alf = 'abcdefghijklmnopqrstuvwxyz'
        m = int(inp_lst('Mode (crypt : 0 ; decrypt : 1) :', ('0', '1')))
        t = ask_text()
        tM = inp_int("Dimension of the sqare matrix :")
        M = []
        for k in range(tM):
            L = []
            for l in range(tM):
                t = cl_inp('Line ' + str(k + 1) + ' column ' + str(l + 1) + ' : ')
                L.append(int(t))
            M.append(L)
        print(M)
        M = Matrix(M)
        print(M)
        res = hill.hill(M, t, m, alf)
        give_result(res)


##---substitution and transposition

class ABC(BaseCipher):
    """Defining the ABC cipher."""
    
    def __init__(self, key, alf=alf_az, ignore=False, interface=None):
        """Initiate the ABC cipher."""
        
        super().__init__('ABC', interface=interface)
        
        self.key = key
        self.alf = alf
        
        self.col_tr = ColumnarTransposition(key, alf, interface=interface)
        self.vig = Vigenere('abc', alf, ignore, interface=interface)
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the ABC cipher."""
        
        return self.col_tr.encrypt(
            self.vig.encrypt(txt)
        )
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the ABC cipher."""
        
        return self.vig.decrypt(
            self.col_tr.decrypt(txt)
        )
    
    
    def gen_key(self, lth):
        """Return a random string of length lth."""
        
        return ColumnarTransposition().gen_key(lth)


class ADFGX(BaseCipher):
    """Defining the ADFGX cipher."""
    
    def __init__(self, key1=None, key2='', alf=alf_az, ignore=False, interface=None):
        """
        Initiate the ADFGX cipher.
        
        - key1 : the Columnar transposition key ;        
        - key2 : The Polybius key.
        """
        
        super().__init__('ADFGX', interface=interface)
        
        ind = ('A', 'D', 'F', 'G', 'X')
        
        self.col_tr = ColumnarTransposition(key1, alf, interface=interface)
        self.poly = Polybius(key2, ind, alf, ignore, space=False, interface=interface)
        
        self.alf = alf
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the ADFGX cipher."""
        
        return self.col_tr.encrypt(self.poly.encrypt(txt))
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the ADFGX cipher."""
        
        return self.poly.decrypt(self.col_tr.decrypt(txt))
    
    
    def gen_key(self, lth, lth1=None):
        """
        Return an ADFGX keys of the form :
            (str, str)
        
        - lth : the length of the first str ;
        - lth1 : the length of the second str. If None (default), take the same as lth.
        """
        
        if lth1 == None:
            lth1 = lth
        
        key1 = ''
        for k in range(lth):
            key1 += choice(self.alf)
        
        key2 = ''
        for k in range(lth1):
            key2 += choice(self.alf)
        
        return (key1, key2)


class ADFGVX(BaseCipher):
    """Defining the ADFGVX cipher."""
    
    def __init__(self, key1=None, key2='', alf=alf_az, ignore=False, interface=None):
        """
        Initiate the ADFGVX cipher.
        
        - key1 : The Columnar transposition key ;
        - key2 : the Polybius key.
        """
        
        super().__init__('ADFGVX', interface=interface)
        
        ind = ('A', 'D', 'F', 'G', 'V', 'X')
        
        self.col_tr = ColumnarTransposition(key1, alf, interface=interface)
        self.poly = Polybius(key2, ind, alf, ignore, space=False, interface=interface)
        
        self.alf = alf
    
    
    def encrypt(self, txt):
        """Encrypt 'txt' using the ADFGVX cipher."""
        
        return self.col_tr.encrypt(self.poly.encrypt(txt))
    
    
    def decrypt(self, txt):
        """Decrypt 'txt' using the ADFGVX cipher."""
        
        return self.poly.decrypt(self.col_tr.decrypt(txt))
    
    
    def gen_key(self, lth, lth1=None):
        """
        Return an ADFGX keys of the form :
            (str, str)
        
        - lth : the length of the first str ;
        - lth1 : the length of the second str. If None (default), take the same as lth.
        """
        
        if lth1 == None:
            lth1 = lth
        
        key1 = ''
        for k in range(lth):
            key1 += choice(self.alf)
        
        key2 = ''
        for k in range(lth1):
            key2 += choice(self.alf)
        
        return (key1, key2)


##------cryptanalysis

class FreqAna:
    """Class which analyse the character's frequency."""
    
    def __init__(self, wprocess=False, n=1, sort=None):
        """
        Initiate the FreqAna class.
        
        - wprocess : A boolean which indicates if the text should be passed trought msgform ;
        - n : the size of the group of character to analyse. Default is 1 ;
        - sort : the way how to sort the result. Should be None, 'char', or 'occ'.
        """
        
        if wprocess not in (0, 1):
            raise ValueError('The arg "wprocess" should be a boolean, but "{}" of type "{}" was found !!!'.format(wprocess, type(wprocess)))
        
        if type(n) != int:
            raise ValueError('The argument "n" should be an intenger, but "{}" of type "{}" was found !!!'.format(n, type(n)))
        
        elif n < 1:
            raise ValueError('The arg "n" should be a positive intenger different from 0 !!!')
        
        if sort not in (None, 'char', 'occ'):
            raise ValueError('The arg "sort" should be None, "char", or "occ", but "{}" was found !!!'.format(sort))
        
        self.wprocess = wprocess
        self.n = n
        self.sort = sort
        
        self.fr_freq = ('e', 'a', 's', 'i', 'n', 't', 'r', 'l', 'u', 'o', 'd', 'c', 'p', 'm', 'v', 'g', 'f', 'b', 'q', 'h', 'x', 'j', 'y', 'z', 'k', 'w')
        self.en_freq = ('e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z')
    
    
    def occ(self, txt):
        """Return the number of occurences the text."""
        
        if self.wprocess:
            txt = msgform(txt, 'min')
        
        return len(txt) // self.n
    
    
    def ana(self, txt):
        """
        Analyse the characters occurences in 'txt'.
        Return a dict sorted by key of the form {c0 : n0 ; c1 : n1 ; ...},
        where cx is the character ('a', 'Z', ...), and nx is the number of time it appear.
        """
        
        if self.wprocess:
            txt = msgform(txt, 'min')
        
        txt += '~' * ((self.n - len(txt) % self.n) % self.n)
        
        d_ana = {}
        
        for k in range(len(txt) // self.n):
            c = txt[self.n * k : self.n * (k + 1)]
            
            if c in d_ana:
                d_ana[c] += 1
            
            else:
                d_ana[c] = 1
        
        #-sort the dict  
        d_ana_s0 = {}     
        d_ana_s = {}
        
        if self.sort == None:
            return d_ana
        
        for k in sorted(d_ana.keys()): #sort by characters (dict's keys)
            d_ana_s0[k] = d_ana[k]
            
        if self.sort == 'occ': #sort by occurences (dict's values)
            lst = sorted(
                [(k, d_ana_s0[k]) for k in d_ana_s0],
                key=lambda x: x[1],
                reverse=True
            ) #List of tuples : {c0 : n0, ...} -> [(c0, n0), ...]
            
            for k in lst:
                d_ana_s[k[0]] = k[1]
        
        else:
            d_ana_s = d_ana_s0
        
        return d_ana_s
        
    
    def ana_pr(self, txt, prec=3):
        """
        Same as ana, but the frequency are in percentage.
        
        - txt : the text to analyse ;
        - prec : the precition in round. Default is 3.
        """
        
        d_ana = self.ana(txt)
        occ = self.occ(txt)
        
        d_ana_pr = {}
        for k in d_ana:
            d_ana_pr[k] = round(d_ana[k] / occ * 100, prec)
        
        return d_ana_pr
    
    
    def comp(self, txt):
        """
        Compare the current text frequency to the english and french frequencies.
        Return a dict of the form : {c : (cE, cF), ...}, where c is the character,
        cE the english character, and cF, the french character.
        """
        
        if self.n != 1:
            raise ValueError('To get the comparaison, "n" should be 1 !!!')
        
        ana = FreqAna(True, sort='occ').ana(txt)
        
        dct = {}
        
        for j, k in enumerate(ana):
            if k in self.en_freq:
                dct[k] = (self.en_freq[j], self.fr_freq[j])
        
        return dct
    
    
    def comp_str(self, txt):
        """Return the self.comp analyse in a readable format."""
        
        d_ana_comp = self.comp(txt)
        
        ret = 'Character correspondance (Text : English - French) :'
        for k in d_ana_comp:
            ret += "\n\t'{}' : '{}' - '{}'".format(k, d_ana_comp[k][0], d_ana_comp[k][1])
        
        return ret
    
    
    def analyse(self, txt, prec=1, verbose=True):
        """Return the frequency analysis of 'txt', in a readable format."""
        
        d_ana = self.ana(txt)
        d_ana_pr = self.ana_pr(txt, prec)
        occ = self.occ(txt)
        
        ret=''
        
        if verbose:
            ret = 'Number of total characters : {}'.format(len(txt))
            if self.wprocess:
                ret += '\nNumber of characters (after word processing) : {}'.format(len(msgform(txt, 'min')))
            ret += '\nNumber of total occurences : {}\n\n'.format(occ)
        
        if self.sort == None:
            ret += 'Occurences count :'
        
        elif self.sort == 'char':
            ret += 'Occurences count (by character) :'
        
        else:
            ret += 'Occurences count (by occurence) :'
            
        for k in d_ana:
            ret += "\n\t'{}' : {} % ({} occ)".format(k, d_ana_pr[k], d_ana[k])
        
        return ret


def freqana_str(txt, wprocess=False, n=1, prec=1):
    """Use FreqAna. Return a string."""
    
    ret = FreqAna(wprocess, n, sort='occ').analyse(txt, prec)
    ret += '\n\n' + FreqAna(wprocess, n, sort='char').analyse(txt, prec, False)
    
    if n == 1:
        ret += '\n\n' + FreqAna().comp_str(txt)
    
    return ret
    


class Ic:
    """Class defining the coincidence index."""
    
    def __init__(self, wprocess=False):
        """Initiate the Ic class."""
        
        if wprocess not in (0, 1):
            raise ValueError('The arg "wprocess" should be a boolean, but "{}" of type "{}" was found !!!'.format(wprocess, type(wprocess)))
        
        self.wprocess = wprocess
    
    
    def calc(self, txt):
        """Calculate the index of coincidence."""
        
        if self.wprocess:
            txt = msgform(txt, 'min')
        
        lth = len(txt)
        
        if lth == 1:
            return 0
        
        dct = {}
        for k in txt:
            if k in dct:
                dct[k] += 1
            
            else:
                dct[k] = 1
        
        ic = 0
        for k in dct:
            n = dct[k]
            ic += n * (n - 1)
        
        return ic / (lth * (lth-1))


class Kasiki:
    """Defining the Kasiki analysis."""
    
    def __init__(self, wprocess=False):
        """Initiate the Kasiki object."""
        
        if wprocess not in (0, 1):
            raise ValueError('The arg "wprocess" should be a boolean, but "{}" of type "{}" was found !!!'.format(wprocess, type(wprocess)))
        
        self.wprocess = wprocess
    
    
    def ana(self, txt):
        """
        Analyse 'txt' with the Kasiki examination.
        
        Return a dict of the form {str: (int, int, int, (bool, [int, int]))}
        """
        
        if self.wprocess:
            txt = msgform(txt, 'maj', number=True)
        
        lth = len(txt)
        d_3 = {}
        d_4 = {}
        d_rep = {}
        
        for k in range(lth):
            if k <= lth - 3:
                tri = txt[k:k + 3]
                
                if tri in d_3:
                    d = k - d_3[tri]
                    d_rep[tri] = (d_3[tri] + 1, k + 1, d, prima.trial_division(d))
                
                else:
                    d_3[tri] = k
                
                if k <= lth - 4:
                    quad = tri + txt[k + 3]
                    
                    if quad in d_4:
                        d = k - d_4[quad]
                        d_rep[quad] = (d_4[quad] + 1, k + 1, d, prima.trial_division(d))
                    
                    else:
                        d_4[quad] = k
        
        return d_rep
    
    
    def analyse(self, txt):
        """Return the analysis in a readable string."""
        
        ana = self.ana(txt)
        
        ret = 'Kasiki examination :\n'
        
        for i in ana:
            lst = ana[i]
            r = '\t{} : '.format(i)
            
            for j in range(len(lst) - 2):
                r += str(lst[j])
                
                if j < len(lst) - 3:
                    r += '-'
                
                elif j == len(lst) - 3:
                    r += ' --> {}'.format(lst[j])
            
            ret += '{} --> {}\n'.format(r, lst[-1][1])
        
        return ret


class Friedman:
    """Defining the Friedman's test."""
    
    def __init__(self, wprocess=True, n=20, prec=6):
        """
        Initiate the Friedman object.
        
        - wprocess : a boolean which indicates if the text should be processed ;        
        - n : a number ;
        - prec : the precision in round for the numbers.
        """
        
        if wprocess not in (0, 1):
            raise ValueError('The arg "wprocess" should be a boolean, but "{}" of type "{}" was found !!!'.format(wprocess, type(wprocess)))
        
        self.wprocess = wprocess
        self.prec = prec
        self.n = n


    def ana(self, txt):
        """
        Analyse the text 'txt'.
        
        Return a tuple of the following form :
            (int, [int, int, ...])
        """
        
        lth = len(txt)
        n = (self.n, lth)[lth < self.n] #If lth < self.n: n = lth, else: n = self.n
        lst = []
        mx = (0, 0)
        
        for i in range(1, n + 1):
            m = 0
            
            for j in range(0, i):
                t2 = ''
                
                for k in range(j, lth, i):
                    t2 += txt[k]
                
                ic_t2 = Ic(False).calc(t2)
                m += ic_t2
            
            m /= i
            
            if m > mx[1]:
                mx = (i, m)
            
            lst.append(round(m, self.prec))
        
        return (mx[0], lst)
    
    
    def analyse(self, txt):
        """Return the analysis in a readable string."""
        
        ana = self.ana(txt)
        ret = "Friedman's test :"
        
        for j, k in enumerate(ana[1]):
            ret += '\n\t{} : {}'.format(j + 1, k)
        
        ret += '\n\tMax : {}, for length of {}.'.format(ana[1][ana[0] - 1], ana[0])
        
        return ret

def textana(txt, wprocess=False, prec=3):
    """Use the previous classes to give a complete analysis of 'txt'."""
    
    ret = ''
    ret += freqana_str(txt, wprocess, prec=prec)
    ret += '\n\nIndex of coincidence : {}\n\n'.format(round(Ic(wprocess).calc(txt), 3))
    ret += Kasiki(wprocess).analyse(txt)
    ret += '\n'
    ret += Friedman(wprocess).analyse(txt)
    
    return ret


class Assist_cryptanalysis:
    """Class to assist humen for the difficult task which is cryptanalysis."""
    def simplesub():
        text = ask_text()
        t2 = ""
        D = {} # Dictionnary of susbsitution
        alf = cl_inp('Alphabet (let empty to use normal) : ')
        if alf == "":
            alf = 'abcdefghijklmnopqrstuvwxyz'
        c = cl_inp('Text in majuscule ? [yn ] ')
        if c == 'y':
            alf = alf.upper()
            text = text.upper()
        alf = alf.upper()
        print("Put ! to quit")
        print("Examples : B -> E transform all B in E\nf gives you the frequences of the letters")
        c = ''
        while c != '!':
            print()
            if c != '':
                c2 = ''
                for k in c:
                    if k != ' ':
                        c2 += k
                c = c2
                if '->' in c:
                    c = c.split('->')
                elif '=' in c:
                    c = c.split('=')
                try:
                    for k in range(len(c[0])):
                        D[c[0][k]] = c[1][k]
                except:
                    print('Error')
            t2 = ''
            for k in text:
                c2 = D.get(k)
                if c2 == None or c2 == "":
                    c2 = " "
                t2 += c2
            l2 = ""
            for k in range(len(text)):
                if k != 0 and k % 30 == 0:
                    print('\n'+l2)
                    l2 = ""
                print(text[k], end='')
                l2 = l2 + t2[k]
            print('\n'+l2)
            print("Plain alphabet :  " + alf)
            print('Cipher alphabet : ', end='')
            D2 = {}
            for k in D:
                D2[D[k]] = k
            for k in alf:
                c2 = D2.get(k)
                if c2 == None or c2 == '':
                    c2 = " "
                print(c2, end='')
            print()
            c = input('>> ')
            while c == 'f':
                freqana.use(text, False)
                c = input('>> ')

##-crack

def correct(M, com):
    if M[0]:
        if com:
            print(True, M[1], M[2])
            a = input('Correct text ? [yn] ')
            if a == 'y':
                return True
        else:
            return True
    return False


def open_D_quad(interface=None):
    '''open quad.wrdlst and make the dict D_quad.'''
    
    global D_quad
    D_quad = {}
    
    #------chdir to the wordlist
    try:
        old_path = chd('Crack')
    
    except FileNotFoundError:
        msg = 'Folder "Crack" not found !!! You may have remove it by error, please re-download it and replace it !!!'
        msg += "\nThe software won't start until the folder will be here."
        
        if interface == None:
            print(msg)
        
        elif interface == 'console':
            cl_out(c_error, msg)
        
        else:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            app = QApplication([])
            QMessageBox.critical(None, 'Fatal error !!!', '<h2>{}</h2>'.format(msg))
        
        import sys
        sys.exit('Folder "Crack" is missing. It should be in Cracker_v3.0.0/Live or in ~/.Cracker.')
    
    #------read it
    with open('quad_f.wrdlst', 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip('\n')
            quad, nb = line.split(' ')
            
            D_quad[quad] = int(nb) / 2_456_316 # Number of tetragrams
        

    chdir(old_path)
    

def crack(text, com=True): #todo: move this in modules/crack ; add GUI com, ...

    global D_quad
    D_quad = {}
    try:
        a = open('quad_f.wrdlst', 'r', encoding='latin-1')
    except:
        try:
            a = open('modules\\crypta\\quad.wrdlst', 'r', encoding='latin-1')
            #todo: use slashes (/) (works on both Windows and Linux)
        except:
            print(path, "Can't import quad.wrdlst")
            a = False
    if a != False:
        c = a.readline()
        while c != "\n" and c != "":
            c = c.split(" ")
            D_quad[c[0]] = int(c[1][0:-1]) / 2456316 # number of tetragrams
            c = a.readline()
        a.close()

    t2 = text
    text = msgform(text, 'min')
    C = [atbash.crack, albam.crack, achbi.crack, avgad.crack, caesar.crack, affine.crack, reverse_code.crack, scytale.crack, rail_fence.crack, morse.crack, tritheme.crack, monosub.crack,  columnar_transposition.crack, UBCHI.crack]
    for k in C:
        if k == morse.crack:
            M = k(t2, com) #Text not processed
        else:
            M = k(text, com=com)
        if correct(M, com):
            return True, (k, M)
        if com: print(False, '\n')                    
    return False, None

def crack_use():
    t = ask_text()
    print()
    print(crack(t))

##-using



crypta_ciphers = {
    'Morse': Morse,
    'Reverse code': ReverseCode,
    'Reverse code word': ReverseCode,
    'Scytale': Scytale,
    'Rail fence': RailFence,
    'Fleissner': Fleissner,
    'Columnar transposition': ColumnarTransposition,
    'UBCHI': UBCHI,
    'Atbash': Atbash,
    'Albam': Albam,
    'Achbi': Achbi,
    'Avgad': Avgad,
    'Caesar': Caesar,
    'Affine': Affine,
    'Polybius': Polybius,
    'Monoalphabetic substitution': MonoSub,
    'Tritheme': Tritheme,
    'Porta': Porta,
    'Vigenere': Vigenere,
    'Beaufort': Beaufort,
    'Gronsfeld': Gronsfeld,
    'Autoclave': Autoclave,
    'Playfair': Playfair,
    'Four squares': FourSquares,
    'Hill': Hill,
    'ABC': ABC,
    'ADFGX': ADFGX,
    'ADFGVX': ADFGVX,
}

crypta_ana = {
    'Frequency analysis': freqana_str,
    'Index of coincidence': Ic,
    'Kasiki': Kasiki,
    'Friedman': Friedman,
    
}


broken_ciph = []
for k in crypta_ciphers:
    try:
        foo = crypta_ciphers[k].meaning
    
    except AttributeError:
        pass
    
    else:
        broken_ciph.append(k)


broken_ciph_dict = {'break_': [], 'brute_force': []}
for k in crypta_ciphers:
    try:
        foo = crypta_ciphers[k].break_
    
    except AttributeError:
        try:
            foo = crypta_ciphers[k].brute_force
        
        except AttributeError:
            pass
        
        else:
            broken_ciph_dict['brute_force'].append(k)
    
    else:
        broken_ciph_dict['break_'].append(k)




def use(): #todo: move this somewhere else
    """Use crypta fonctions."""

    d = {'1': textana, '1a': freqana.use, '1b': ic.use, '1c': kasiki.use, '1d': friedman.use, '1e': Assist_cryptanalysis.simplesub, '2a': morse.use, '3a1': atbash.use, '3a2': albam.use, '3a3': achbi.use, '3a4': avgad.use, '3b': caesar.use, '3c': affine.use, '3d': polybius.use, '3e': monosub.use, '4a': reverse_code.use, '4b': rail_fence.use, '4c': scytale.use, '4d': fleissner.use, '4e': columnar_transposition.use, '4f': UBCHI.use, '5a': tritheme.use, '5b': porta.use, '5c': vigenere.use, '5d': beaufort.use, '5e': gronsfeld.use, '5f': porta.use, '6a': playfair.use, '6b': four_squares.use, '6c': hill.use, '7a': ABC.use, '7b': ADFGX.use, '7c': ADFGVX.use, '8a': AES.use, '9': crack_use}
    c = ""
    while c not in ('0', 'q'):

        color(c_succes)
        print()
        print('\\'*50)

        color(c_prog)
        print('\nCrypta menu :\n')

        color(c_error)
        print('\t0.Exit')

        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t1.Cryptanalysis')
        print('\t\ta.Frequence analysis\tc.Kasiki examination\te.Help for simple sub')
        print('\t\tb.Index of coincidence\td.Test of Friedman')

        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t2.Codes')
        print('\t\ta.Morse code')

        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t3.Monoalphabetic ciphers')
        print('\t\ta.(1: Atbash, 2: Albam, 3: Abchi, 4: Avgad) \tc.Affine\te.Monoalphabetic substitution')
        print('\t\tb.Caesar\td.Polybius')

        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t4.Transposition ciphers')
        print('\t\ta.Reverse code\tc.Scytale\te.Columnar transposition')
        print('\t\tb.Rail fence\td.Fleissner\tf.UBCHI cipher')
        
        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t5.Polyalphabetic ciphers')
        print('\t\ta.Tritheme\tc.Vigenere\te.Gronsfeld')
        print('\t\tb.Porta\td.Beaufort\tf.Autoclave')
        
        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t6.Polygraphic ciphers')
        print('\t\ta.Playfair\tb.Four squares\tc.Hill')

        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t7.Substitution and transposition ciphers')
        print('\t\ta.ABC\tb.ADFGX\tc.ADFGVX')
        
        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t8.Modern ciphers')
        print('\t\ta.AES cipher')
        
        color(c_succes)
        print('    ' + '-'*25)
        color(c_ascii)
        print('\t9.Crack unknown code (Atbash, Atbash, Albam, Abchi, Avgad, Caesar, Affine, Reverse code, Scytale, Rail Fence, Morse, Tritheme, Columnar transposition, Monoalphabetic substitution)')
        print()
        color(c_prog)

        c = ""
        c = input('>> ')

        if c not in d and c not in ('q', '0'):
            prnt = c + ' is NOT an option of this menu !'
            cl_out(c_error, prnt)
        elif c not in ('q', '0'):
            use_menu(d[c])
            color(c_succes)
            cl_inp('\n---End---')
            color(c_prog)


##-setup
open_D_quad(glb.interface)