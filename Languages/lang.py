#!/bin/python3
# -*- coding: utf-8 -*-

lang__auth = 'Elerias'
lang__ver = '1.0.4'
lang__last_update = '24.11.2020'


##-import

import os


##-ini

global D_langs
D_langs = {}
L_en = []

global langs_lst
langs_lst = [] #List of the available languages (i.g. ['en', 'fr']).

global lang

try:
    with open('Data/lang.txt', 'r') as f:
        lang = f.read()

    lang = lang.strip('\n')

except FileNotFoundError:
    print('The file "lang.txt" was not found')
    lang = 'en'

try:
    with open('Languages/en.txt', 'r', encoding='utf-8') as f:
        for k in f:
            L_en.append(k[:-1])
except FileNotFoundError:
    print('The file "en.txt" was not found')

for i in os.listdir('Languages'):
    if i[-4:] == '.txt' and i != 'lang.txt':
        langs_lst.append(i.strip('.txt'))

        D_langs[i[:-4]] = {}
        n = 0
        with open('Languages/'+i, 'r', encoding='utf-8') as f:
            for j in f:
                D_langs[i[:-4]][L_en[n]] = j[:-1]
                n += 1


##-translate

def translate(text_en, lang=lang):
    global D_langs
    return D_langs[lang][text_en]
