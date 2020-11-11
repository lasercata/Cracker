#!/bin/python3
# -*- coding: utf-8 -*-

'''Module including color fonctions'''

color__auth = 'lasercata'
color__last_update = '11.11.2020'
color__version = '2.3'


##-import
import ctypes
import platform

from Languages.lang import translate as tr

if platform.system() == 'Windows':
    handle = ctypes.windll.kernel32.GetStdHandle(-11)

    col = lambda x : ctypes.windll.kernel32.SetConsoleTextAttribute(handle, x)

    dct_col = {tr('invisible'): 0, tr('orange'): 1, tr('blue'): 9, tr('green'): 10, tr('light_blue'): 11,
    tr('red'): 12, tr('pink'): 13, tr('yellow'): 14, tr('white'): 15}


elif platform.system() == 'Linux':
    col = lambda x : print('\033[' + str(x) + 'm', end='')

    dct_col = {tr('none'): 0, tr('bold'): 1, tr('lite'): 2, tr('italics'): 3, tr('underline'): 4,
    tr('flaches'): 5, tr('norm'): 6, tr('reverse'): 7, tr('invisible'): 8, tr('cross'): 9,

    tr('black'): 30, tr('red'): 31, tr('green'): 32, tr('orange'): 33, tr('light_blue'): 34,
    tr('pink'): 35, tr('blue'): 35, tr('white'): 37}

c_prog = tr('light_blue')
c_input = tr('green')
c_error = tr('red')
c_wrdlt = tr('pink')
c_admin = tr('green')
c_succes = tr('green')
c_ascii = tr('orange')

if platform.system() == 'Windows':
    c_output = tr('yellow')

elif platform.system() == 'Linux':
    c_output = tr('blue')


##-color

def color(choice_color):
    '''Changes the color ;
    Return False if there was no error ;
    Return True if choice_color is not in dct_col (if an error occur).'''

    global dct_col

    try:
        col(dct_col[choice_color])

    except KeyError:
        print(tr('The input is not a color') + ' !!!')
        return True

    else:
        return False


##-color_input

def cl_inp(prompt, func=input):
    '''Color input, works like normal input : var = cl_inp(prompt)'''

    color(c_prog)
    print('')
    print(prompt)
    color(c_input)
    ret = func('>')
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
        c_in = cl_inp(tr('Enter new color of') + " " + c_use + " " + tr('(0 to keep the color)') + ' :')
        if c_in in ('0', ''):
            return c_old
        elif color(c_in):
            cl_out(c_error, tr('The color was NOT founded') + ' !')
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
    c_lst_prnt = (tr('program'), tr('input'), tr('output'), tr('error'), tr('wordlist'), tr('succes'), tr('ascii art'))

    print('\n' + tr('Current colors') + ' :\n')
    color(c_prog)
    print('    ' + tr('Program color') + ' :', c_prog)
    color(c_input)
    print('    ' + tr('Input color') + ' :', c_input)
    color(c_output)
    print('    ' + tr('Output color') + ' :', c_output)
    color(c_error)
    print('    ' + tr('Error color') + ' :', c_error)
    color(c_wrdlt)
    print('    ' + tr('Wordlists color') + ' :', c_wrdlt)
    color(c_succes)
    print('    ' + tr('Succes color') + ' :', c_succes)
    color(c_ascii)
    print('    ' + tr('Ascii art color') + ' :', c_ascii)
    color(c_prog)


    c = inp_lst(tr('Change colors ?') + " " + tr('(y/n)') + ' :', (tr('y'), tr('n')))

    if c == tr('y'):
        ch = inp_lst(tr('Restore default program colors (1) or change colors one by one (2) ?') + ' :', ('1', '2'))

        if ch == '1':
            c_prog = tr('light_blue')
            c_input = tr('green')
            c_output = tr('yellow')
            c_error = tr('red')
            c_wrdlt = tr('pink')
            c_succes = tr('green')
            c_ascii = tr('orange')

            cl_out(c_succes, tr('Done') + ' !\n' + tr('Back menu') + ' ...')

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
        cl_out(c_error, '\n' + tr('What you entered is NOT in list') + ' !')
        c = cl_inp(prompt)
    return c
