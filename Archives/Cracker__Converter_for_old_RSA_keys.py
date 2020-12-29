
from os import chdir, mkdir, getcwd, listdir, rename, remove
from os.path import expanduser, isfile


from modules.base.base_functions import chd #Run this script in Pyzo : run first Cracker, then run this script (to be able to import this)

#---------csv
import csv


#---------chdir
def chd_rsa(path, first=False, interface=None):
    '''
    Change current directory to [cracker]/RSA_keys/[path], where [cracker] is
    the path where cracker is launched.

    If first is True, and if the folder "RSA_keys" don't exist, generate "auto_generated_512" keys.

    If directory "RSA_keys" don't exist, it create it.

    If [path] don't exist, return to last path and raise a FileNotFoundError exeption,
    Return the old path else.
    '''

    old_path = getcwd()

    chd('.') #chdir to cracker's data

    #------cd to 'RSA_keys'
    try:
        chdir('RSA_keys')

    except FileNotFoundError:
        mkdir('RSA_keys')
        print('"RSA_keys" folder created at "{}" !'.format(getcwd()))
        chdir('RSA_keys')

        if first:
            msg1 = 'It seem that it is the first time you launch this application on this computer. New RSA 512 bits keys will be generated, but you should consider to generate yours (at least 2048 bits)'
            msg2 = 'Keys path : {}/RSA_keys'.format(glb.Cracker_data_path)

            if interface == None:
                print(msg1)
                print(msg2)

            elif interface == 'console':
                cl_out(c_output, '{}\n{}'.format(msg1, msg2))

            else:
                QMessageBox.about(None, 'Ciphers info ― Cracker', '<h3>{}</h3>\n<h4>{}</h4>'.format(msg1, msg2))


            RsaKeys('auto_generated_512', interface).generate(512)


    try:
        chdir(path)

    except FileNotFoundError as err:
        chdir(old_path)
        raise FileNotFoundError(err)

    return old_path



#---------rm_lst
def rm_lst(lst, lst_to_rm):
    '''Remove the list "lst_to_rm" from "lst".'''

    for k in lst:
        if k in lst_to_rm:
            lst.remove(k)

    return lst



#---------CSV
class CSV:
    '''Class dealing with csv file.'''

    def __init__(self, fn, delim=','):
        '''Initiate some variables'''

        self.fn = fn
        self.delim = delim

    #------read
    def read(self):
        '''Return a list of dict of the file self.fn.'''

        with open(self.fn) as f_csv:
            table = csv.DictReader(f_csv, delimiter=self.delim)

            lst = []
            for k in table:
                lst.append(k)

        return lst

    #------write
    def write(self, fdnames, row):
        '''Write row in csv file self.fn with fieldnames fdnames.'''

        with open(self.fn, 'w') as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=fdnames)
            writer.writeheader()
            writer.writerow(row)


    #------get_fieldnames
    def get_fdn(self):
        '''Return the fieldnames in a tuple.'''

        with open(self.fn) as f:
            fdn = f.readline()

        return tuple(fdn.strip('\n').split(self.delim))


class RsaKeys:
    '''Class which allow to generate RSA keys, and to manipulate them (saving in files, ...)'''

    def __init__(self, keys_name, interface=None):
        '''
        Initiate the RsaKeys object.

        - keys_name : the set of keys' name (without the extention).
        '''

        if interface not in (None, 'gui', 'console'):
            raise ValueError('The argument "interface" should be None, "gui", \
                or "console", but {} of type {} was found !!!'.format(interface, type(interface)))


        self.k_name = keys_name
        self.interface = interface


    def __repr__(self):
        '''Represent the object.'''

        return "RsaKeys('{}', interface='{}')".format(self.k_name, self.interface)



    def old_show_keys(self, get_stg_md=False):
        '''
        Return the keys and info about them.

        Return :
            (pbk, pvk), (p, q, n, phi, e, d), (n_strth, date_) --- if it's a normal dir ;
            pbk, (n, e), (n_strth, date_, date_exp) --- if it's a pkb file ;
            md_stored ('hexa' or 'dec') --- if get_stg_md is True ;
            -1 --- if the file was not found.

        self.k_name : the keys' name ;
        get_stg_md : If True, return only the way how they are stored, i.e. "hexa" or "dec". Should be True or False.

        The way how the keys are stored is automaticly detected.

        Order of the key finding :
            .1 : RSA full keys, in decimal ;
            .2 : RSA public keys, in decimal ;
            .3 : RSA full keys, in hexa ;
            .4 : RSA public keys, in hexa.
        '''

        if get_stg_md not in (True, False):
            raise ValueError('"get_stg_md" should be True or False, but "' + str(get_stg_md) + '" was found !!!')

        try:
            old_path = chd_rsa('RSA_keys__' + self.k_name)
            md = ('all', 'dec')

        except FileNotFoundError:
            try:
                old_path = chd_rsa('RSA_pbk__' + self.k_name)
                md = ('pbk', 'dec')

            except FileNotFoundError:
                try:
                    old_path = chd_rsa('RSA_hex_keys__' + self.k_name)
                    md = ('all', 'hexa')

                except FileNotFoundError:
                    try:
                        old_path = chd_rsa('RSA_hex_pbk__' + self.k_name)
                        md = ('pbk', 'hexa')

                    except FileNotFoundError:
                        return -1

        if get_stg_md:
            chdir(old_path)
            return md[1]

        if md[0] == 'pbk': #---RSA pbk
            if md[1] == 'dec':
                pb_n = 'RSA_public_key__' + self.k_name
                i_nm = 'RSA_pbk_infos__' + self.k_name + '.csv'

            else:
                pb_n = 'RSA__hex_pbkey__' + self.k_name
                i_nm = 'RSA_hex_pbk_infos__' + self.k_name + '.csv'

            with open(pb_n) as f:
                pbk = f.read()

            infos = CSV(i_nm).read()[0]
            date_, date_exp, n_strth = infos['date'], infos['date_export'], infos['n_strenth']
            n, e = infos['n'], infos['e']

            if md[1] == 'hexa': #convert in decimal
                pbk = pbk.split(',')
                pbk = str(int(pbk[0], 16)) + ',' + str(int(pbk[1], 16))
                n_strth = str(int(n_strth, 16))
                n, e = str(int(n, 16)), str(int(e, 16))

            chdir(old_path)

            return pbk, (n, e), (n_strth, date_, date_exp)


        else: #---RSA_all
            if md[1] == 'dec':
                pb_n = 'RSA_public_key__' + self.k_name
                pv_n = 'RSA_private_key__' + self.k_name
                i_nm = 'RSA_keys_infos__' + self.k_name + '.csv'

            else:
                pb_n = 'RSA_hex_pbkey__' + self.k_name
                pv_n = 'RSA_hex_pvkey__' + self.k_name
                i_nm = 'RSA_hex_kinfos__' + self.k_name + '.csv'

            with open(pb_n) as f:
                pbk = f.read()

            with open(pv_n) as f:
                pvk = f.read()

            infos = CSV(i_nm).read()[0]
            date_, n_strth = infos['date'], infos['n_strenth']
            p, q, n, phi, e, d = infos['p'], infos['q'], infos['n'], infos['phi'], infos['e'], infos['d']

            if md[1] == 'hexa': #convert in decimal
                pbk = pbk.split(',')
                pbk = str(int(pbk[0], 16)) + ',' + str(int(pbk[1], 16))
                pvk = pvk.split(',')
                pvk = str(int(pvk[0], 16)) + ',' + str(int(pvk[1], 16))

                n_strth = str(int(n_strth, 16))
                p, q, n, phi, e, d = str(int(p, 16)), str(int(q, 16)), \
                    str(int(n, 16)), str(int(phi, 16)), str(int(e, 16)), str(int(d, 16))

            chdir(old_path)

            return (pbk, pvk), (p, q, n, phi, e, d), (n_strth, date_)



    def convert(self):
        '''
        Function which convert old RSA keys (in folders) to new RSA keys (in one file).
        '''

        try:
            lst_keys, lst_values, lst_infos = self.old_show_keys()
            stg_md = self.old_show_keys(True)

        except ValueError:
            raise ValueError('Keys not found')


        if len(lst_infos) == 2: #pvk
            v = {
                'p' : lst_values[0],
                'q' : lst_values[1],
                'n' : lst_values[2],
                'phi' : lst_values[3],
                'e' : lst_values[4],
                'd' : lst_values[5],
                'date' : lst_infos[1],
                'n_strenth' : lst_infos[0]
            }

            if stg_md == 'dec':
                fn = str(self.k_name) + '.pvk-d'

            else:
                fn = str(self.k_name) + '.pvk-h'

                for k in v:
                    if k != 'date':
                        v[k] = format(int(v[k]), 'x') #convert numbers to hexadecimal

            pbk = v['e'], v['n']
            pvk = v['d'], v['n']

            #---check if it not already exists
            old_path = chd_rsa('.')

            if isfile(fn):
                chdir(old_path)
                raise ValueError('A file named "{}" already exists !!!\nOr you already converted your old keys, or you made new one under the same name !!!'.format(fn))

            #---make file
            fdn = tuple(v.keys()) #('p', 'q', 'n', 'phi', 'e', 'd', 'date', 'n_strenth')
            row = v
            CSV(fn).write(fdn, row)

            chdir(old_path)

        else: #pbk
            v = {
                'e' : lst_values[1],
                'n' : lst_values[0],
                'date' : lst_infos[1],
                'date_export' : lst_infos[2],
                'n_strenth' : lst_infos[0]
            }
            pbk = v['e'], v['n']

            #---write
            if stg_md == 'dec':
                fn = str(self.k_name) + '.pbk-d'

            else:
                fn = str(self.k_name) + '.pbk-h'

                for k in v:
                    if k not in ('date', 'date_export'):
                        v[k] = format(int(v[k]), 'x') #convert numbers to hexadecimal

            old_path = chd_rsa('.')

            if isfile(fn):
                chdir(old_path)
                raise ValueError('A file named "{}" already exists !!!\nOr you already converted your old keys, or you made new one under the same name !!!'.format(fn))

            fdn = tuple(v.keys()) #('e', 'n', 'date', 'date_export', 'n_strenth')
            row = (v)

            CSV(fn).write(fdn, row)

            chdir(old_path)








#------list_keys
def old_list_keys(mode='any'):
    '''
    Function which lists the existing keys.

    Return six tuples, first is the list of the normal keys (pvk + pbk) without the keys exported,
    the second is the list of the exported (pbk) keys,
    the third is the list of the normal keys in hexadecimal without the hex keys exported,
    the fourth is the list of the exported (pbk) in hexadecimal,
    the fifth is the list of all the key not exported,
    and the sixth is the list of all of them, removing the duplicates.

    mode : what return. Should be "pvk", "pbk", "pvk_hex", "pbk_hex", "pvk_without_pbk", "all", or "any".

    if mode is "any", return :
        pvk, pbk, hex_pvk, hex_pbk, lst_pvk_without_pbk, all

    else return the corresponding value.
    '''

    if mode not in ('pvk', 'pbk', 'pvk_hex', 'pbk_hex', 'pvk_without_pbk', 'all', 'any'):
        raise ValueError('"mode" should be "pvk", "pbk", "pvk_hex", "pbk_hex", "pvk_without_pbk", "all" or "any", but "' + str(mode) + '" was found !!!')

    old_path = chd_rsa('.')
    lst_k = listdir()
    chdir(old_path)

    lst_pvk = []
    lst_pbk = []
    lst_hex_pvk = []
    lst_hex_pbk = []
    lst_all = []

    for k in lst_k:
        if 'RSA_keys__' in k:
            lst_pvk.append(k[10:])
            lst_all.append(k[10:])

        elif 'RSA_pbk__' in k:
            lst_pbk.append(k[9:])
            lst_all.append(k[9:])

        elif 'RSA_hex_keys__' in k:
            lst_hex_pvk.append(k[14:])
            lst_all.append(k[14:])

        elif 'RSA_hex_pbk__' in k:
            lst_hex_pbk.append(k[13:])
            lst_all.append(k[13:])

    #---
    lst_pvk = rm_lst(lst_pvk, lst_pbk)
    lst_hex_pvk = rm_lst(lst_hex_pvk, lst_hex_pbk)

    lst_pvk_without_pbk = rm_lst(lst_pvk + lst_hex_pvk, lst_pbk + lst_hex_pbk)

    lst_all = list(set(lst_all))
    lst_all.sort()

    if mode == 'all':
        return tuple(lst_all)

    elif mode == 'pvk':
        return tuple(lst_pvk)

    elif mode == 'pbk':
        return tuple(lst_pbk)

    elif mode == 'pvk_hex':
        return tuple(lst_hex_pvk)

    elif mode == 'pbk_hex':
        return tuple(lst_hex_pbk)

    elif mode == 'pvk_without_pbk':
        return tuple(lst_pvk_without_pbk)

    return (
        tuple(lst_pvk),
        tuple(lst_pbk),
        tuple(lst_hex_pvk),
        tuple(lst_hex_pbk),
        tuple(lst_pvk_without_pbk),
        tuple(lst_all)
    )


#------list_keys
def list_keys(mode='any'):
    '''
    Function which lists the existing keys.

    Return six tuples, first is the list of the normal keys (pvk + pbk) without the keys exported,
    the second is the list of the exported (pbk) keys,
    the third is the list of the normal keys in hexadecimal without the hex keys exported,
    the fourth is the list of the exported (pbk) in hexadecimal,
    the fifth is the list of all the key not exported,
    and the sixth is the list of all of them, removing the duplicates.

    mode : what return. Should be "pvk", "pbk", "pvk_hex", "pbk_hex", "pvk_without_pbk", "all", or "any".

    if mode is "any", return :
        pvk, pbk, hex_pvk, hex_pbk, lst_pvk_without_pbk, all

    else return the corresponding value.
    '''

    if mode not in ('pvk', 'pbk', 'pvk_hex', 'pbk_hex', 'pvk_without_pbk', 'all', 'any'):
        raise ValueError('"mode" should be "pvk", "pbk", "pvk_hex", "pbk_hex", "pvk_without_pbk", "all" or "any", but "' + str(mode) + '" was found !!!')

    old_path = chd_rsa('.')
    lst_k = listdir()
    chdir(old_path)

    lst_pvk = []
    lst_pbk = []
    lst_hex_pvk = []
    lst_hex_pbk = []
    lst_all = []

    for k in lst_k:
        if '.pvk-d' in k:
            lst_pvk.append(k[:-6])
            lst_all.append(k[:-6])

        elif '.pbk-d' in k:
            lst_pbk.append(k[:-6])
            lst_all.append(k[:-6])

        elif '.pvk-h' in k:
            lst_hex_pvk.append(k[:-6])
            lst_all.append(k[:-6])

        elif '.pbk-h' in k:
            lst_hex_pbk.append(k[:-6])
            lst_all.append(k[:-6])

    #---
    lst_pvk = rm_lst(lst_pvk, lst_pbk)
    lst_hex_pvk = rm_lst(lst_hex_pvk, lst_hex_pbk)

    lst_pvk_without_pbk = rm_lst(lst_pvk + lst_hex_pvk, lst_pbk + lst_hex_pbk)

    lst_all = list(set(lst_all))
    lst_all.sort()

    if mode == 'all':
        return tuple(lst_all)

    elif mode == 'pvk':
        return tuple(lst_pvk)

    elif mode == 'pbk':
        return tuple(lst_pbk)

    elif mode == 'pvk_hex':
        return tuple(lst_hex_pvk)

    elif mode == 'pbk_hex':
        return tuple(lst_hex_pbk)

    elif mode == 'pvk_without_pbk':
        return tuple(lst_pvk_without_pbk)

    return (
        tuple(lst_pvk),
        tuple(lst_pbk),
        tuple(lst_hex_pvk),
        tuple(lst_hex_pbk),
        tuple(lst_pvk_without_pbk),
        tuple(lst_all)
    )

