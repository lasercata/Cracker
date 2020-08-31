#!/bin/python3
# -*- coding: utf-8 -*-

'''Module including color fonctions'''

color__auth = 'lasercata'
color__last_update = '02.02.2020'
color__version = '2.2'


##-import
import ctypes
import platform

#from modules.base.base_functions import inp_lst

if platform.system() == 'Windows':
    handle = ctypes.windll.kernel32.GetStdHandle(-11)

    col = lambda x : ctypes.windll.kernel32.SetConsoleTextAttribute(handle, x)

    dct_col = {'invisible' : 0, 'orange' : 1, 'blue' : 9, 'green' : 10, 'light_blue' : 11,
    'red' : 12, 'pink' : 13, 'yellow' : 14, 'white' : 15}


elif platform.system() == 'Linux':
    col = lambda x : print('\033[' + str(x) + 'm', end='')

    dct_col = {'none' : 0, 'bold' : 1, 'lite' : 2, 'italics' : 3, 'underline' : 4,
    'flaches' : 5, 'norm' : 6, 'reverse' : 7, 'invisible' : 8, 'cross' : 9,

    'black' : 30, 'red' : 31, 'green' : 32, 'orange' : 33, 'light_blue' : 34,
    'pink' : 35, 'blue' : 35, 'white' : 37}

c_prog = 'light_blue'
c_input = 'green'
c_error = 'red'
c_wrdlt = 'pink'
c_admin = 'green'
c_succes = 'green'
c_ascii = 'orange'

if platform.system() == 'Windows':
    c_output = 'yellow'

elif platform.system() == 'Linux':
    c_output = 'blue'


##-color

def color(choice_color):
    '''Changes the color ;
    Return False if there was no error ;
    Return True if choice_color is not in dct_col (if an error occur).'''

    global dct_col

    try:
        col(dct_col[choice_color])

    except KeyError:
        print('The input is not a color !!!')
        return True

    else:
        return False


##-color_input

def cl_inp(prompt): #color input, works like normal input : var = cl_inp(prompt)
    color(c_prog)
    print('')
    print(prompt)
    color(c_input)
    ret = input('>')
    color(c_prog)

    return ret

def cl_inp_2(color_prompt, prompt, color_input, color_prog): #color_input_2, more precise in the colors.
    color(color_prompt)
    print('')
    print(prompt)
    color(color_input)
    ret = input('>')
    color(color_prog)

    return ret

def cl_out(color_1, prompt, color_2=c_prog, sp=True): #color_output, works like print, with the colors. ex : cl_out(c_error, 'Error')
    color(color_1)
    if sp:
        print('')
    print(prompt)
    color(color_2)

def cl_out_2(color_1, prompt, color_2, prompt_2, color_3=c_prog): #color_output_2, used to print 2 lines with different colors.
    color(color_1)
    print('')
    print(prompt)
    color(color_2)
    print(prompt_2)
    color(color_3)


##-change_color

def c_use(c_use, c_old):

    while True:
        c_in = cl_inp('Enter new ' + c_use + ' color (0 to keep the color) :')
        if c_in in ('0', ''):
            return c_old
        elif color(c_in):
            cl_out(c_error, 'The color was NOT founded !')
        else:
            return str(c_in)

def c_color():
    global c_prog
    global c_input
    global c_output
    global c_error
    global c_wrdlt
    global c_succes
    global c_ascii

    c_lst = [c_prog, c_input, c_output, c_error, c_wrdlt, c_succes, c_ascii]
    c_lst_prnt = ('program', 'input', 'output', 'error', 'wordlist', 'succes', 'ascii art')

    print('\nCurrent colors :\n')
    color(c_prog)
    print('    Program color : ', c_prog)
    color(c_input)
    print('    Input color : ', c_input)
    color(c_output)
    print('    Output color : ', c_output)
    color(c_error)
    print('    Error color :', c_error)
    color(c_wrdlt)
    print('    Wordlists color : ', c_wrdlt)
    color(c_succes)
    print('    Succes color : ', c_succes)
    color(c_ascii)
    print('    Ascii art color : ', c_ascii)
    color(c_prog)


    c = inp_lst('Change colors ? (y/n) :', ('y', 'n'))

    if c == 'y':
        ch = inp_lst('Restore default program colors (1) or change colors one by one (2) ? :', ('1', '2'))

        if ch == '1':
            c_prog = 'light_blue'
            c_input = 'green'
            c_output = 'yellow'
            c_error = 'red'
            c_wrdlt = 'pink'
            c_succes = 'green'
            c_ascii = 'orange'

            cl_out(c_succes, 'Done !\nBack menu ...')

        else:
            for k in range(len(c_lst)):
                c_lst[k] = c_use(c_lst_prnt[k], c_lst[k])

            c_prog = c_lst[0]
            c_input = c_lst[1]
            c_output = c_lst[2]
            c_error = c_lst[3]
            c_wrdlt = c_lst[4]
            c_succes = c_lst[5]
            c_ascii = c_lst[6]


    else:
        print('\nBack menu ...')

##-other
def inp_lst(prompt, lst):
    '''Works like input but accepts only values in the list lst, reask if not.'''
    c = ''
    c = cl_inp(prompt)
    while c not in lst:
        cl_out(c_error, '\nWhat you entered is NOT in list !')
        c = cl_inp(prompt)
    return c