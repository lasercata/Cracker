#!/bin/python3
# -*- coding: utf-8 -*-
'''Module including P@ssw0rd_Test0r functions.'''

pwd_testor__auth = 'lasercata'
pwd_testor__date = '07.06.2020'
pwd_testor__version = '1.0,1'

##-import
from math import *
from getpass import getpass
from time import sleep

from modules.base.console.color import color, c_prog, c_input, c_output
from modules.base.base_functions import set_prompt

##-ini
alf_0_1 = ('0', '1')
alf_0_9 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
alf_hex = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a','b','c','d','e', 'f', 'A', 'B', 'C', 'D', 'E', 'F')
alf_a_z = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q', 'r','s','t','u','v','w','x','y','z')
alf_A_Z = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
 
alf_spe = (' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
'.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{',
'|', '}', '~', '£', '§', '¨', '°', '²', 'µ', '’', '€')

alf_acc = ('À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ð', 'Ñ', 'Ò',
 'Ó', 'Ô', 'Õ', 'Ö', 'Ú', 'Û', 'Ü', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ç', 'è', 'é',
 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ù', 'ú',
 'û', 'ü', 'ý', 'ÿ')

alf_alt = ('☺', '☻', '♥', '♦', '♣', '♠', '•', '◘', '○', '◙', '♂', '♀', '♪', '♫', '☼', '►',
 '◄', '↕', '‼', '¶', '§', '▬', '↨', '↑', '↓', '→', '←', '∟', '↔', '▲', '▼', ' ',
 '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0',
 '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'N', 'O', 'P', 'Q',
 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a'
, 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q'
, 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '⌂', 'Ç', 'ü'
, 'é', 'â', 'ä', 'à', 'å', 'ç', 'ê', 'ë', 'è', 'ï', 'î', 'ì', 'Ä', 'Å', 'æ', 'Æ'
, 'ô', 'ö', 'ò', 'û', 'ù', 'ÿ', 'Ö', 'Ü', 'ø', '×', 'ƒ', 'á', 'í', 'ó', 'ú', 'ñ'
, 'Ñ', 'ª', 'º', '¿', '®', '¬', '½', '¼', '¡', '«', '»', '░', '▒', '▓', '│', '┤'
, 'Á', 'Â', 'À', '©', '╣', '║', '╗', '╝', '¢', '¥', '┐', '└', '┴', '┬', '├', '─'
, '┼', 'ã', 'Ã', '╚', '╔', '╩', '╦', '╠', '═', '╬', '¤', 'ð', 'ð', 'Ð', 'Ê', 'Ë'
, 'È', 'ı', 'Í', 'Î', 'Ï', '┘', '┌', '█', '▄', '¦', 'Ì', '▀', 'Ó', 'ß', 'Ô', 'Ò'
, 'õ', 'Õ', 'µ', 'þ', 'Þ', 'Ú', 'Û', 'Ù', 'ý', 'Ý', '¯', '´', '\xad', '±', '‗', 
'¾', '§', '÷', '¸', '°', '¨', '·', '¹', '³', '²', '■', '\xa0')

alfs = (alf_0_1, alf_0_9, alf_hex, alf_a_z, alf_A_Z, alf_spe, alf_acc, alf_alt)


freq_pwd = ('!@#$%^&*', '0000', '1111', '111111', '123', '123123', '1234', '12345',
'123456', '1234567', '12345678', '123456789', '1234567890', '222222', '55555', 
'654321', '666', '666666', '66666666', '987654321', 'Password', 'abc123', 'admin',
'administrateur', 'administrator', 'azerty', 'azertyuiop', 'dragon', 'football',
'freedom', 'hello', 'iloveyou', 'letmein', 'login', 'master', 'monkey', 'p@ssw0rd',
'p@ssword', 'passw0rd', 'password', 'password1', 'password123', 'qazwsx', 'qwerty',
'qwertyuiop', 'shadow', 'starwars', 'trustno1', 'welcome', 'whatever')


##-functions
#------------------------------------------------------------------------pwd_sth
def pwd_sth(lth, n):
    '''
    Return the password's entropy in bits (log2( n ^ lth )).
    lth : password's lenth ;
    n : password's alphabet's lenth.
    '''
    
    return log2(n **lth)
    

#----------------------------------------------------------------------pwd_entro
def pwd_entro(H=None, N=None, L=None):
    '''
    Return the unknown value.
    One and only one of the 3 variables should be None.
    
    H : entropy of the password ;
    N : alphabet's lenth ;
    L : password's lenth.
    '''
    
    a = None
    if (H == a and N == a) or (H == a and L == a) or (N == a and L == a) or (H == a and N == a and L == a):
        return '\nOnly one var should be None !!!'
        
    elif H == a:
        return log2(N **L)
        
    elif L == a:
        return round(H / log2(N))
        
    elif N == a:
        return round(2 **(H / L))
        
    else:
        return '\nAt least 1 var should be None !!!'
    

#---------------------------------------------------------------------------wlth
def wlth(word):
    '''Return the sort list of all differents word's characters, in one occurence.'''
    
    if type(word) != str:
        raise ValueError('"word" argument should be a string, but "{}", of type "{}" was found !'.format(word, type(word)))

    ret = list(set(word))
    ret.sort()
    return ret
    

# def wlth(obj):
#     '''Return the sorted list of all the differents characters, in one occurence.
#     obj : the object to parse. Should be a string, or a list of string.
#     '''
#     
#     def wlth_str(word):
#         if type(word) != str:
#             raise ValueError('Found a non string object : "{}", of type "{}" !'.format(word, type(word)))
#             
#         ret = list(set(word))
#         ret.sort()
#         return ret
#     
#     
#     if type(obj) == str:
#         return tuple(wlth_str(obj))
#     
#     
#     lst = set(obj) #remove duplicates
#     
#     lst_occ = []
#     for k in lst:
#         lst_occ += wlth_str(k)
#     
#     lst_occ = list(set(lst_occ))
#     lst_occ.sort()
#     
#     return tuple(lst_occ)
    

#---------------------------------------------------------------------------walf
def walf(word):
    '''
    Function which search the alphabets used in "word".
    Return (alfs_lth, alf), where alfs_lth is the alphabets' length, and alf is a tuple containing the alphabets' names.
    '''

    char = {'09' : [], 'az' : [], 'AZ' : [], 'spe' : []}
    lst_chr = []
    
    #---------get last alphabet character
    #------sort the word's charaters
    for k in word:
        if k in alf_0_9:
            char['09'].append(k)
            
        elif k in alf_a_z:
            char['az'].append(k)
            
        elif k in alf_A_Z:
            char['AZ'].append(k)
            
        elif k in alf_spe:
            char['spe'].append(k)
    
    #------get the last character of each alphabet
    for k in char:
        char[k].sort()
        
        if char[k] != []:
            lst_chr.append(char[k][-1]) #last character
            
    
    #---------get alfs
    bi = dec = hex_ = alph = alph_up = spe = False
    
    for k in lst_chr:
        if k in alf_0_1: #binary
            bi = True
            
        elif k in alf_0_9[2:]: #decimal
            dec = True
            
        elif k in alf_hex[10:] and (k not in alf_a_z[6:] and k not in alf_A_Z[6:]): #hexadecimal
            hex_ = True
            
        elif k in alf_a_z[6:]: #alphabetic lowercases
            alph = True
            
        elif k in alf_A_Z: #alphabetic uppercases
            alph_up = True
            
        elif k in alf_spe: #specials
            spe = True
    
    
    #---------get the alphabets
    ret_alfs = []
    alf_lth = 0
    
    if hex_:
        ret_alfs.append('Hexadecimal')
        alf_lth += 16
        
    elif dec:
        ret_alfs.append('Decimal')
        alf_lth += 10
        
    elif bi:
        ret_alfs.append('Binary')
        alf_lth += 2
        
        
    if alph_up:
        ret_alfs.append('Alphabetic uppercases')
        alf_lth += 26
        
    if alph:
        ret_alfs.append('Alphabetic lowercases')
        alf_lth += 26


    if spe:
        ret_alfs.append('Specials')
        alf_lth += len(alf_spe)
    
    
    return alf_lth, tuple(ret_alfs)
    

#------------------------------------------------------------------------get_sth
def get_sth(word):
    '''Print infomations and return word strenth, in bits.'''
    
    if word == '':
        print('\nYou should enter something !!!')
        return -3 #Abort
    
    entro = None
    
    #---------get lenths
    lth = len(word) #word's lenth
    lth_occ = len(wlth(word)) #word's lenth of characters in one occurence
    
    walfs = walf(word)
    lth_alfs = walfs[0]  #pwd's alphabets lenth
    
    #---------get alfs
    alfs = walfs[1]
    ret_alfs = set_prompt(alfs)
    
    #---------print info on the word (alphabets, lenths)
    color(c_output)
    ret = '\n' + '-'*60
    ret += '\nReturn for : ' + '*'*lth
    
    ret += '\n\nAlphabets : ' + ret_alfs
    
    ret += '\n\nYour word\'s lenth : ' + str(lth)
    ret += '\nNumber of differents characters : ' + str(lth_occ)
    ret += '\nLenth of the alphabet containing your word : ' + str(lth_alfs) + '\n'
    
    
    #---------tests
    weak_freq = weak_occ = weak_year = False
    
    if lth_occ <= 3 and lth > 4: #test if there is less than 3 differents characters in a word with a lenth bigger than 4
        weak_occ = True


    if word in freq_pwd: #test if the password is in the most used ones
        entro = log2(len(freq_pwd))
        weak_freq = True

    elif lth == 4: #test if word is a year in [1900 ; 2100]
        try:
            wd = int(word)
            
            if 1900 <= wd <= 2100:
                entro = log2(200)
                weak_year = True
                
            else:
                entro = pwd_entro(None, lth_alfs, lth)
                
        except:
            entro = pwd_entro(None, lth_alfs, lth)
    
    else:
        entro = pwd_entro(None, lth_alfs, lth)


    #---------set the scale (from https://www.ssi.gouv.fr/administration/precautions-elementaires/calculer-la-force-dun-mot-de-passe/ and me)
    dct_wk_lvl = {0 : 'uncrackable !!!', 1 : 'very strong', 2 : 'strong', 3 : 'strong',
    4 : 'medium', 5 : 'weak', 6 : 'weak', 7 : 'very weak', 8 : 'too much weak !', 9 : 'so bad !'}
    
    lst_entro_lvl = (512, 200, 128, 104, 82, 78, 65, 49, 39, 0)
    
    for k in range(len(lst_entro_lvl)): #set scale of weakness : 0 is the most strong (>512), 9 the weakest (>0).
        if entro > lst_entro_lvl[k]:
            weakness = k
            break
        
    wk_lvl = dct_wk_lvl[weakness]
        
        
    #---------next_
    if weakness > 0: #get add vars
        next_ = weakness- 1
        next_entro = lst_entro_lvl[next_]
            
        total_add_lth = pwd_entro(next_entro, lth_alfs, None) #get total lenth for having a weakness - 1 password
        total_add_alf_lth = pwd_entro(next_entro, None, lth)
        
        add_lth = total_add_lth - lth + 1 #get add lenth
        add_alf_lth = total_add_alf_lth - lth_alfs + 1
        
        
        total_add_lth_med = pwd_entro(82, lth_alfs, None) #get total lenth for having a medium password
        total_add_alf_lth_med = pwd_entro(82, None, lth)
        
        add_lth_med = total_add_lth_med - lth + 1 #get add lenth
        add_alf_lth_med = total_add_alf_lth_med - lth_alfs + 1

    
    #---------return
    ret += '_'*25
    
    if weak_freq:
        print(type(ret))
        ret += '\n\nYour password is in the top 25 weakest passwords !!!\nIt has an entropy of ~' + str(round(entro, 3)) + 'bits.'
        ret += '\nYou shall choose an other password.'
        
        
    elif weak_occ:
        ret += '\n\nYour password contain only ' + str(lth_occ) + ' differents characters !!!\nIt has an entropy of ~ ' +  str(round(entro, 3)) + ' bits.'
        ret +='\nYou should add more differents characters.'
        
        
    elif weak_year:
        ret += '\n\nYour password is a PIN took from a date in [1900 : 2100] !!!\nIt has an entropy of ~' + str(round(entro, 3)) + ' bits.'
        
        
    else:
        ret += '\n\nYour password is ' + str(wk_lvl) + ' (' + str(round(weakness / 9 * 100, 3)) + '% (' + str(weakness) + '/9) of weakness) ;'
        ret += '\nIt has an entropy of ~' + str(round(entro, 3)) + ' bits.'
        
        if weakness != 0:
            ret += ('\n\nTo get a ' + dct_wk_lvl[weakness - 1] +
            ' password (' + str(weakness - 1) + '/9 of weakness, with an entropy of ' + str(next_entro) + '), you can add ' +
            str(add_lth) + ' characters to your password.')

        if weakness in [9, 8, 7, 6]: #get medium
            ret += ('\n\nTo get a ' + dct_wk_lvl[4] + ' password (4/9 of weakness, with an entropy of 82), you can add ' +
            str(add_lth_med) + ' characters to your password.')
            
    return ret
    
##-using function
def use():
    color(c_prog)
    print('\nEnter the password to test :')
    color(c_input)
    word = getpass('>')
    color(c_prog)
    
    print(get_sth(word))
    
    color(c_input)
    input('---End---')
    color(c_prog)
    
##-test module
if __name__ == '__main__':
    use()
