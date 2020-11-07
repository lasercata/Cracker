#!/bin/python3


##-head

auth = 'Elerias'
date = '06.11.2020'
version = '1.1.2'
update_notes = """
1.1.2 <- 1.1 Stable :
    - Including this script in Cracker
    - The function use return a string and don't print anything (to be used in GUI).

1.1 <- 1.0
- Adding accents
- Adding analyze function
- Now can analyze many phone numbers in the same time
- We can give phone numbers as arguments when anamer0.py is called
- Bug corrections
"""
doc = ('https://extranet.arcep.fr/portail/Op%C3%A9rateursCE/Num%C3%A9rotation.aspx#PUB', 'https://fr.wikipedia.org/wiki/Liste_des_pr%C3%A9fixes_des_op%C3%A9rateurs_de_t%C3%A9l%C3%A9phonie_mobile_en_France', 'https://fr.wikipedia.org/wiki/Liste_des_indicatifs_t%C3%A9l%C3%A9phoniques_en_France')
linked_files = ('MAJNUM.csv', 'MAJOPE.csv')


##-ini
#---------packages
from os import getcwd, chdir, path
from sys import argv

#---------Cracker's modules
from modules.base.console.color import cl_inp


##-main

def analyze(phoneNumbers):
    """Analyze the phone numbers in arguments."""

    L = []
    for i in range(len(phoneNumbers)):
        L.append({'Phone number': ""})
        for j in phoneNumbers[i]:
            if j in '0123456789':
                L[i]['Phone number'] += j

    f_numberZones = open('modules/anamer0/MAJNUM.csv', 'r', encoding='utf-8')
    for i in f_numberZones:
        l = i.split(",")
        for j in L:
            if l[0] == j['Phone number'][0:len(l[0])]:
                j['Block'] = l[0]
                j['Operator'] = l[1]
                j['Area'] = l[2]
                j['Allocation date'] = l[3][0:-1]
    f_numberZones.close()

    for i in L:
        if len(i) == 1:
            i['Recognized'] = False
        else:
            i['Recognized'] = True
            if int(i['Phone number'][1]) <= 5:
                i['Phone type'] = 'Home phone'
                D = {'1': 'Ile-de-France', '2': 'Northwest region', '3': 'Northeast region', '4': 'Southeast region', '5': 'Southwest region or oversea territories'}
                i['Big area'] = D[i['Phone number'][1]]
                if len(i['Phone number']) != 10:
                    i['Recognized'] = False
            elif i['Phone number'][1] in '67':
                i['Phone type'] = 'Cellphone'
                if len(i['Phone number']) != 10:
                    i['Recognized'] = False
            else:
                i['Phone type'] = 'Unknown'

    f_op = open('modules/anamer0/MAJOPE.csv', 'r', encoding='utf-8')
    for i in f_op:
        l = i.split(",")
        for j in L:
            if l[0] == j.get('Operator'):
                j['Operator'] = l[1][0:-1]
    f_op.close()
    return L

def use(phoneNumbers=[], lang='en'):

    if lang in ('fr', 'french', 'francais', 'français'):
        T = {0: 'Entrer un ou plusieurs numéros de téléphone français ("," entre) :', 1: 'Numéro :', 2: 'Non attribué ou non reconnu', 3: 'Téléphone fixe', 'Ile-de-France': 'Île-de-France', 'Northwest region': 'Région nord-ouest', 'Northeast region': 'Région nord-est', 'Southeast region': 'Région sud-est', 'Southwest region or oversea territories': "Région sud-ouest ou territoires d'outre-mer", 4: 'Téléphone portable', 5: 'Bloc', 6: 'Zone', 7: 'Opérateur', 8: "Date d'attribution"}
    else:
        T = {0: 'Enter french phone number(s) ("," between) :', 1: 'Number :', 2: 'Unassigned or unrecognized', 3: 'Home phone', 'Ile-de-France': 'Ile-de-France', 'Northwest region': 'Northwest region', 'Northeast region': 'Northeast region', 'Southeast region': 'Southeast region', 'Southwest region or oversea territories': 'Southwest region or oversea territories', 4: 'Cellphone', 5: 'Block', 6: 'Area', 7: 'Operator', 8: 'Allocation date'}

    lr = False # Line return

    ret = ''

    if phoneNumbers == []:
        answer = cl_inp(T[0])
        phoneNumbers = answer.split(',')
        lr = True

    L = analyze(phoneNumbers)


    for k in L:
        if lr:
            ret += '\n'
        else:
            lr = True

        if len(k['Phone number']) != 10:
            ret += '\n' + T[1] + ' ' + k['Phone number']
        else:
            ret += '\n' + T[1] + ' ' + k['Phone number'][0:2] + ' ' + k['Phone number'][2:4] + ' ' + k['Phone number'][4:6] + ' ' + k['Phone number'][6:8] + ' ' + k['Phone number'][8:10]

        if k['Recognized']:
            if k['Phone type'] == 'Home phone':
                ret += '\n' +  T[3]
                ret += '\n' + T[k['Big area']]

            elif k['Phone type'] == 'Cellphone':
                ret += '\n' + T[4]

            ret += '\n' + T[5] + ' : ' + k['Block']
            ret += '\n' + T[6] + ' : ' + k['Area']
            ret += '\n' + T[7] + ' : ' + k['Operator']
            ret += '\n' + T[8] + ' : ' + k['Allocation date']
        else:
          ret += '\n' + T[2]

    return ret


# ##-start
#
# if __name__ == '__main__':
#
#     lang = 'en'
#
#     phoneNumbers = []
#     ch_lang = False
#     if len(argv) > 1:
#         for k in range(1, len(argv)):
#             if argv[k] == '-l' or argv[k] == '--lang':
#                 ch_lang = True
#             elif ch_lang:
#                 ch_lang = False
#                 lang = argv[k]
#             elif argv[k][0] in '0123456789':
#                 phoneNumbers.append(argv[k])
#
#     last_path = getcwd() # We save the old current directory
#     chdir(path.dirname(argv[0])) # The new current directory is the directory of this program
#
#     use(phoneNumbers, lang)
#
#     chdir(last_path) # We go back to the old current directory