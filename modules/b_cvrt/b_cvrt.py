#!/bin/python3
# -*- coding: utf-8 -*-
'''Module incuding b_cvrt fonctions'''

b_cvrt__auth = 'Lasercata'
b_cvrt__last_update = '26.06.2020'
b_cvrt__version = '3.0'

##-import
#---------Cracker modules
from modules.base.console.color import color, cl_inp, cl_out, c_error, c_output, c_prog, c_succes, c_ascii
from modules.base.base_functions import use_menu

#------others modules
from math import log

##-ini
alf = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_36 = '0123456789abcdefghijklmnopqrstuvwxyz'

##-functions
#---------n_add
def n_add(n, lth, side='left'):
    '''Return n, containing lth characters, with '0' added to the side 'side'.

    n : the number (int or str) to the one add zeros ;
    lth : the final length of n ;
    side : where add the zeros. Should be in ('right', 'left'). Default is "left".
    '''

    if side not in ('right', 'left'):
        raise ValueError('"side" should be "right" or "left", but "' + str(side) + '" was found !!!')

    n = str(n)

    if side == 'left':
        return '0'*(lth - len(n)) + n

    else:
        return n + '0'*(lth - len(n))

#---------insert
def insert(lst, n, k):
    '''This function returns the list lst with n insert at the position k (lst[k])'''

    return lst[:k] + [n] + lst[k:]

#---------lth_standard
def lth_standard(n, NEG=False): #----------------------
    '''Return n with 0 at left to make a 2^x bytes number according to the lenth of n.'''

    n = str(n)
    lth = len(n)

    if NEG:
        lth += 1

    if lth <= 8:
        return n_add(n, 8)

    else:
        for k in range(int(log(lth, 2)) + 1):
            if lth > 2**k and lth <= 2*2**k:
                return n_add(n, 2*2**k)


#---------sapce
#------groups
def sp_grp(n, grp, sep=' ', rev_lst=True):
    '''Base of space. Return n with spaced groups of grp.
    .n : the number / string to space ;
    .grp : the group size ;
    .sep : the separation (default is a space) ;
    .rev_lst : reverse the string or not. Useful to not reverse it with RSA.
    '''

    lth = len(str(n))
    n_lst = list(n)

    if rev_lst:
        n_lst.reverse()

    i = 0
    for k in range(lth):
        if k % grp == 0 and k != 0:
            n_lst.insert(k + i, sep)
            i += 1

    if rev_lst:
        n_lst.reverse()

    ret = ''
    for k in n_lst:
        ret += k

    return ret

#------space standard length
def space_b(n, nb=3):
    '''
    Return n with regular spaces to easilier read the numbers.
    Works with floating numbers.

    n : number to space ;
    nb : number's base.
    '''

    lth = len(str(n))
    n = str(n)
    n_lst = list(n)

    if nb <= 10: # floating
        if int(float(n)) != float(n):
            n_int = str(int(float(n))) #integer

            lst_n_fl = n.split('.') # float
            n_fl = lst_n_fl[1][::-1] #reverse

            return space_b(n_int, nb) + '.' + space_b(n_fl, nb)[::-1]

    if nb == 2:
        return sp_grp(n, 4)


    elif nb == 10:
        return sp_grp(n, 3)

    elif nb == 16:
        return sp_grp(n, 2)

    else:
        return sp_grp(n, 3)


#---------b_cvrt
def b_cvrt(n, nb, b):
    '''
    Function which return the number n, in base nb, converted to the base b.

    n : the number to convert ;
    nb : base of n ;
    b : return's base.
    '''

    if b > len(alf):
        raise ValueError('Impossible to convert in a base bigger than ' + \
            str(len(alf)) + ' (the lenght of the alphabet) !')

    #---convert in base 10
    if nb != 10:
        n_lst = list(str(n))
        n_lst.reverse()
        lst_10 = []

        for i, k in enumerate(n_lst):
            lst_10.append(alf.index(k) * nb**i) #decompose the number (i.g. aef in base 16 = 10*16^2 + 14*16^1 + 15*16^0 in base 10).

        n_10 = 0
        for k in lst_10:
            n_10 += k

        if b == 10:
            return n_10

    else:
        n_10 = int(n)


    #---convert in base b
    if b == 1:
        return '1'*n_10


    lst_b = []
    while n_10 > 0:
        r = n_10 % b
        n_10 = n_10 // b
        lst_b.append(r)

    lst_b.reverse()

    ret = ''
    for k in lst_b:
        ret += str(alf[k])

    return ret


##-main
class BaseConvert:
    '''Class dealing with number convertions'''

    def __init__(self, n, nb, alf=alf):
        '''Create the BaseConvert number.

        n : the number ;
        nb : the number's base ;
        alf : the alphabet used by the number. Default is 0-9, a-z, A-Z (of length 62).
        '''

        #---validity tests
        #-ieee754
        if str(nb).lower() == 'ieee754':
            for k in str(n):
                if k not in (' ', '0', '1'):
                    raise ValueError('Invalid character at position ' + \
                        str(str(n).index(k)) + ' : "' + k + '" is not in (" ", "0", "1") !!!')

            lst_n_ieee754 = n.split(' ')
            if len(lst_n_ieee754) != 3:
                raise ValueError('The number is not encoded in the good IEEE754 format !!! It should be at the format "S EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM" !')

            if len(lst_n_ieee754[0]) != 1 or len(lst_n_ieee754[1]) != 8 or len(lst_n_ieee754[2]) != 23:
                raise ValueError('The number is not encoded in the good IEEE754 format !!! It should be at the format "S EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM" !')

        #-others bases
        else:
            try:
                nb = int(nb)

            except ValueError:
                raise ValueError("The number's base should be an int !!! ('" + \
                    str(nb) + "' of type '" + str(type(nb)) + "' was found !)")

            if nb <= 0 or nb > len(alf):
                raise ValueError('Invalid number base !!! ("' + str(nb) + '" was found)')

            for k in str(n):
                if k not in alf[:nb] and k not in ('-', '.'):
                    raise ValueError('Invalid number for this base !!! ("' + str(k) + '" not in the alphabet !)')


        #-empty
        if n == '':
            raise ValueError('The number should not be empty !!!')


        #---ini
        self.n = n
        self.nb = nb
        self.alf = alf

        #---
        if str(n)[0] == '-': #Negative
            self.neg = True

        else:
            self.neg = False

        #---try if it's an int, float or str
        self.BIG = False

        try:
            n = float(n)

        except ValueError:
            self.INT = False
            self.FL = False

        except OverflowError:
            self.FL = False
            self.INT = True
            self.BIG = True

            self.n = int(n)

        else:
            if int(float(n)) == float(n):
                self.n = int(n)
                self.INT = True
                self.FL = False

            else:
                self.n = float(n)
                self.FL = True


    def __repr__(self):
        '''Represent the BaseConvert object.'''

        return 'BaseConvert("{}", "{}"'.format(self.n, self.nb)


    def convert(self, b, NEG=False):
        '''Function which allow to choose the good funtion to convert.

        NEG : Should be True or False. Indicate if the number is encoded using the two's complement.
        '''

        #---tests
        if NEG not in (True, False):
            raise ValueError('NEG argument should be True or False, but "' + str(NEG) + '" was found !!!')


        if str(b).lower() != 'ieee754':
            try:
                b = int(b)

            except ValueError:
                raise ValueError("The base b should be an int !!! ('" + \
                    str(b) + "' of type '" + str(type(b)) + "' was found !)")


        #---others tests
        if (self.FL or self.INT) and (not self.BIG):
            if float(self.n) < 0 or self.neg:
                neg = True

            else:
                neg = False

        else:
            neg = False

        if self.FL:
            n = float(self.n)
            fl_n = round(n - int(n), len(str(n)) - (len(str(int(n))) + 1))
            number_fl = BaseConvert(abs(fl_n), self.nb, self.alf)
            number_int = BaseConvert(int(n), self.nb, self.alf)

        elif self.INT:
            n = int(self.n)


        #---return
        if str(b).lower() == 'ieee754' or str(self.nb).lower() == 'ieee754':
            return self.ieee754(b)


        elif NEG and self.FL and b == 2:
            if number_fl.floating(b, True):
                return 'Approxiamte value : ' + space_b(float(self.b_cvrt_neg(b)) + number_fl.floating(b), b)

            else:
                return space_b(float(self.b_cvrt_neg(b)) + number_fl.floating(b), b)


        elif NEG and self.FL and b == 10:
            if number_fl.floating(b, True):
                return 'Approxiamte value : ' + space_b(float(number_int.b_cvrt_neg(b)) - number_fl.floating(b), b)

            else:
                return space_b(float(number_int.b_cvrt_neg(b)) - number_fl.floating(b), b)


        elif NEG:
            return space_b(self.b_cvrt_neg(b), b)


        elif self.FL:
            if number_fl.floating(b, True):
                return 'Approxiamte value : ' + space_b(self.floating(b), b)

            else:
                return space_b(self.floating(b), b)


        else:
            if neg:
                return '-' + space_b(self.cvrt(b), b)

            else:
                return space_b(self.cvrt(b), b)


    #---------b_cvrt
    def cvrt(self, b):
        '''
        Function which return the number n, in base nb, converted to the base b.

        b : return's base.

        Return n, in string.
        '''

        if b > len(self.alf):
            raise ValueError('Impossible to convert in a base bigger than ' + \
                str(len(self.alf)) + ' (the lenght of the alphabet) !')

        if self.neg:
            n = str(self.n)[1:]

        else:
            n = str(self.n)


        #---convert in base 10
        if self.nb != 10:
            n_inv = n[::-1] #Reverse n
            lst_10 = []

            for i, k in enumerate(n_inv):
                lst_10.append(self.alf.index(k) * self.nb**i) #decompose the number (i.g. aef in base 16 = 10*16^2 + 14*16^1 + 15*16^0 in base 10).

            n_10 = 0
            for k in lst_10:
                n_10 += k

            if b == 10:
                return n_10

        else:
            try:
                n_10 = int(float(n))

            except OverflowError:
                n_10 = int(n)


        #---convert in base b
        if b == 1:
            return '1'*n_10


        lst_b = []
        while n_10 > 0:
            r = n_10 % b
            n_10 = n_10 // b
            lst_b.append(r)

        lst_b.reverse()

        ret = ''
        for k in lst_b:
            ret += str(self.alf[k])


        #---return
        if ret == '':
            return 0

        return ret


    #---------b_cvrt_neg_2
    def b_cvrt_neg(self, b):
        '''Return n converted in base b, using the two's complement negative standard'''

        if b == 2 and self.nb == 10:
            n_bi = BaseConvert(self.n, self.nb, self.alf).cvrt(2)
            n_dec = int(BaseConvert(self.n, self.nb, self.alf).cvrt(10))
            lth_bi = len(lth_standard(n_bi))

            return BaseConvert(2**lth_bi - abs(n_dec), 10, self.alf).cvrt(2)

        elif b == 10 and self.nb == 2:
            lth_bi = len(str(self.n))

            return -(2**lth_bi - BaseConvert(self.n, 2, self.alf).cvrt(10))


        else:
            raise ValueError("The two's complement can only deal with bases two and ten !!!")


    #---------floating
    def floating(self, b, inf_ask=False, verbose=False):
        '''Convert the float number to the base b.

        inf_ask : If True, return True if decimal is infinite, False else ;
        verbose : If True, return the convertion's steps, without the number.
        '''

        inf = False

        lst_n = []

        if self.nb == 10 and b == 2:
            if int(self.n) == float(self.n):
                return float(self.cvrt(b))

            fl = '0.'
            int_n_2 = int(BaseConvert(int(float(self.n)), 10, self.alf).cvrt(2))
            fl_n = abs(round(self.n - int(self.n), len(str(self.n)) - (len(str(int(self.n))) + 1)))

            while fl_n < 1:
                if verbose:
                    print(fl_n, fl)

                fl_n *= 2
                fl += str(int(fl_n))

                if fl_n > 1 and fl_n != int(fl_n):
                    fl_n -= int(fl_n)
                    fl_n = round(fl_n, 7)

                if fl_n in lst_n:
                    inf = True
                    break

                lst_n.append(fl_n)

            fl = float(fl)
            fl += int_n_2

            if inf_ask:
                if inf:
                    return True

                else:
                    return False

            else:
                return fl


        elif self.nb == 2 and b == 10:
            if inf_ask:
                return False

            int_n_10 = int(BaseConvert(int(self.n), 2, self.alf).cvrt(10))
            fl_n = round(self.n - int(self.n), len(str(self.n)) - (len(str(int(self.n))) + 1))

            lst_fl_n = list(str(fl_n))
            del lst_fl_n[0], lst_fl_n[0] #del '0.'
            lth = len(lst_fl_n)


            lst_ = []
            for k in range(1, lth + 1):
                lst_.append(str(int(lst_fl_n[k - 1], self.nb) * self.nb**(-k)))

            fl_n_10 = 0
            for k in lst_:
                fl_n_10 += float(k)

            ret = float(int_n_10 + fl_n_10)
            return ret

        else:
            raise ValueError('Can only convert float from base 10 in 2, and vice versa !')


    #---------IEEE754
    #------exposant add
    def exp_add(self, exp_10):
        exp_10_shift = exp_10 + 127
        exp_2 = BaseConvert(exp_10_shift, 10, self.alf).cvrt(2)

        return n_add(exp_2, 8)


    #------IEEE754
    def ieee754(self, b='ieee754'):
        '''
        This function return self.n convert in binary, using the standard IEEE 754.
        Form of the IEEE 754 return : 'S EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM'

        self.n : float number to convert ;
        self.nb : base of n ;
        b : base of the returned result. Default is 'ieee754'.
        '''

        if b not in ('ieee754', '10', 10):
            raise ValueError('Invalid base !!! The base should be in ("ieee754", "10", 10), but "' + \
                str(b) + '" was found !!!')


        if b in ('ieee754', '2', 2) and self.nb == 10:

            if self.n < 0:
                bit1 = 1

            else:
                bit1 = 0

            if self.nb == 10:
                n_fl_2 = self.floating(2)

            else:
                n_fl_2 = self.n


            if int(float(n_fl_2)) == 1: #--------------------------------1.01101

                lst_n_fl_2 = str(n_fl_2).split('.')
                mantisse = lst_n_fl_2[1]

                mtse23 = n_add(mantisse, 23, 'right')

                exp_2_8bits = '01111111'


            elif int(float(n_fl_2)) == 0: #----------------------------0.0101101

                lst_fl = str(n_fl_2).split('.')

                a = lst_fl[1]
                b = int(lst_fl[1])

                mantisse = ''
                for i in range(len(str(b))):
                    if i != 0 and str(b)[i] != '.':
                        mantisse += str(b)[i]

                exp_10 = len(str(mantisse)) - len(a) # exposant
                if not -126 < exp_10 < 127:
                    raise ValueError('The number is too large or too small : the exposant is not in [-126 ; 127] !!!')

                exp_2_8bits = self.exp_add(exp_10)

                mtse23 = n_add(mantisse, 23, 'right')


            else: #------------------------------------------------------101.101
                str_n_2 = str(n_fl_2)

                mantisse = '' #mantisse
                for i in range(len(str_n_2)):
                    if i != 0 and str_n_2[i] != '.':
                        mantisse += str_n_2[i]

                mtse23 = n_add(mantisse, 23, 'right') #end mantisse

                lst_int_n_fl = str_n_2.split('.') #exposant

                exp_10 = len(lst_int_n_fl[0]) - 1
                if not -126 < exp_10 < 127:
                    raise ValueError('The number is too large or too small : the exposant is not in [-126 ; 127] !!!')

                exp_2_8bits = self.exp_add(exp_10)


            ret = str(bit1) + ' ' + str(exp_2_8bits) + ' ' + str(mtse23)
            return ret


        elif b == 10 and self.nb in ('ieee754', '2', 2): #-------------------------------
            lst_n = self.n.split(' ')

            S = int(lst_n[0])
            exp_2 = lst_n[1]
            mtse23 = lst_n[2]

            exp_10_shift = BaseConvert(exp_2, 2).cvrt(10)
            exp_10 = int(exp_10_shift) - 127

            mtse_2 = float('1.' + mtse23)
            mtse_10 = BaseConvert(mtse_2, 2, self.alf).floating(10)

            ret = mtse_10 * 2 **exp_10

            if S == 1:
                ret = -ret

            return ret

        else:
            raise ValueError('This program can only convert from base 10 in 2 with the standard IEEE754, and vice-versa.')


