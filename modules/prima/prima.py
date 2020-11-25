#!/bin/python3
# -*- coding: utf-8 -*-
"""Module dealing with prime numbers."""

prima__auth = 'Elerias'
prima__last_update = '25.11.2020'
prima__version = '3.3'


##-import

import math
from random import randint
from datetime import datetime
from time import time
from os import getcwd, chdir

cracker = False
path = getcwd()
for k in range(3):
    try:
        from modules.base.console.color import color, cl_inp, cl_out, c_output, c_succes, c_wrdlt, c_error, c_prog, c_ascii
        from modules.base.base_functions import use_menu, inp_int
        import modules.base.ini as ini
        from Languages.lang import translate as tr
        cracker = True
    except:
        pass
    chdir('..')
chdir(path)
if not cracker:
    print("~prima_v" + prima__version + ".py in " + getcwd())
    print("Cracker not found")


##-functions

def isPerfectPower(n: int) -> (bool, int, int):
    """Return True, a, b with n = a ** b if n is a perfect power else False, n, 1."""

    for k in range(2, int(math.log2(n)+1)):
        a = n ** (1 / k)
        if a == int(a):
            return (True, int(a), k)
    return (False, n, 1)


##-factorization algorithms


    ##-trial divisions

def trial_division(n: int) -> (bool, list):
    """Decompose the integer n as a product of prime factors by trial division method. Here, the divisors are tested until sqrt(n) and only 2 and odd numbers are tested."""

    if type(n) is not int:
        raise TypeError(tr('n has to be an integer'))
    if n < 0:
        raise ValueError(tr('n cannot be negative'))

    factors = []
    while n > 2 and n % 2 == 0:
        factors.append(2)
        n = n // 2
    d = 3
    s = math.sqrt(n)
    while n > 1 and d <= s:
        while n % d == 0:
            factors.append(d)
            n = n // d
            s = math.sqrt(n)
        d = d + 2

    if n > 1:
        factors.append(n)
    return (len(factors) == 1, factors)


def wheel_factorization(n: int, base=(2, 3, 5, 7)) -> (bool, list):
    """Improvement of trial division : the incrementation isn't 2 anymore, it varies according to the base of prime factors.
    Site : https://en.wikipedia.org/wiki/Wheel_factorization
    """

    if type(n) is not int:
        raise TypeError(tr('n has to be an integer'))
    if n < 0:
        raise ValueError(tr('n cannot be negative'))

    # Generating of inc
    inc = [] # inc is the list of steps
    size = 1 # We calculate the sum of every numbers of inc
    for i in base:
        size = size * i
    L = [x for x in range(base[-1]+1, size+base[-1]+1)]
    for i in base:
        j = 0
        while j < len(L):
            if L[j] % i == 0:
                del L[j] # We delete all the numbers which are not coprimes with the base
            else:
                j = j + 1
    for i in range(j-1): # j is the length of the list
        inc.append(L[i+1] - L[i]) # Every differences constistue a step
    inc.append(size+L[0]-L[-1]) # We add the last step
    l_inc = len(inc)

    # Divisions
    factors = []
    for i in base:
        while n > i and n % i == 0:
            factors.append(i)
            n = n // i
    d = L[0]
    s = math.sqrt(n)
    index = 0 # index of the list of steps inc
    while n > 1 and d <= s:
        while n % d == 0:
            factors.append(d)
            n = n // d
            s = math.sqrt(n)
        d = d + inc[index]
        index = index + 1
        if index == l_inc:
            index = 0

    if n > 1:
        factors.append(n)
    return (len(factors) == 1, factors)


    ##-Congruence of squares

def fermat(n: int) -> int:
    """Return a non trivial factor of n or 1 if he is prime or equals to 1."""

    if n == 0:
        raise ValueError(tr('0 is not factorizable'))
    if n == 2:
        return 1

    x = int(math.sqrt(n))
    y = 0.5
    while int(y) != y:
        x = x + 1
        y = x ** 2 % n
        y = math.sqrt(y)
    return math.gcd(x - int(y), n)

def fermat_factorization(n: int) -> (bool, list):
    """Use the factorization of Fermat to decompose n as a product of prime factors."""

    factors = []
    while n > 1:
        p = fermat(n)
        if p == 1:
            factors.append(n)
            n = 1
        else:
            factors_p = fermat_factorization(p)[1]
            factors.extend(factors_p)
            n = n // p
    return (len(factors) == 1, factors)


    ##-Others

def pollard_rho(n: int) -> int:
    """Return the primality and the factorization of n as a product of prime factors with Pollard's rho algorithm with Brent's cycle finding and Pollard's optimisation of gcd.
    Inspired of https://en.wikipedia.org/wiki/Cycle_detection#Brent.27s_algorithm.
    n must not be a power of a prime number. Return n if n is prime and 1 if n = 1."""

    if n == 1:
        return 1

    a = b = d = 1;
    power=1
    while d == 1:
        for i in range(power):
            b = (b ** 2 + 1) % n
            d = d * (a - b) % n
        d = math.gcd(abs(d), n);
        if d == n:
            b = a  # We begin again but we check d every times
            d = 1
            while d == 1:
                b = (b ** 2 + 1) % n
                d = math.gcd(abs(a-b), n)
        a = b
        power *= 2
    return d

def pollard_rho_decomposition(n: int, primality_test=True) -> (bool, list):
    """Use recursively pollard-rho to decompose n as a product of prime factors"""

    factors = []
    while n > 1 and not(primality_test and miller_rabin(n)):
        b, a, k = isPerfectPower(n)
        if b:
            for i in range(k):
                factors.extend(pollard_rho_decomposition(a)[1])
            return (False, factors)
        p = pollard_rho(n)
        if p == n:
            factors.append(n)
            n = 1
        else:
            factors_p = pollard_rho_decomposition(p)[1]
            factors.extend(factors_p)
            n = n // p
    if n > 1:
        factors.append(n)
    return (len(factors) == 1, factors)

def pollard_pm1(n: int) -> (bool, list) :
    """Find a prime factor of n with the pollard's p - 1 algorithm."""
    if type(n) is not int:
        raise TypeError(tr('n has to be an integer'))
    if n < 0:
        raise ValueError(tr('n cannot be negative'))
    if n == 0 or n == 1:
        return False, n
    if n == 2:
        return True, 2
    if n % 2 == 0:
        return False, 2

    B = int(n ** (1/6)) + 1
    P = segmentation_erathostenes_sieve(B)
    s = 1
    for k in P:
        s = s * k ** int(math.log(B, k)) % n
    x = math.gcd(pow(2, s, n)-1, n)
    if x == n:
        return True, n
    elif x == 1:
        k = B + 1
        while x == 1:
            s = s * k % n
            x = math.gcd(pow(2, s, n)-1, n)
            k = k + 1
    return False, x

def pollard_pm1_decomposition(n: int, primality_test=True) -> (bool, list) :
    """Use recursively pollard_pm1 to decompose n as a product of prime factors"""

    factors = []
    while n > 1 and not(primality_test and miller_rabin(n)):
        pr, p = pollard_pm1(n)
        if pr:
            factors.append(n)
            n = 1
        else:
            factors_p = pollard_pm1_decomposition(p)[1]
            factors.extend(factors_p)
            n = n // p
    if n > 1:
        factors.append(n)
    return (len(factors) == 1, factors)

##-Probabilistic primalities test


# isSurelyPrime from Prime.isprime RSA by Lasercata

def isSurelyPrime(n):
    """
    Check if n is prime. Uses Miller Rabin test.
    If n is prime, return True ;
    return False else.
    """

    if n == 1 or n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False

    if n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        return True

    elif n in (0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20):
        return False

    if n > 1027:
        for d in range(7, 1028, 30) :
            if n % d == 0 or n % (d+4) == 0 or n % (d+6) == 0 or n % (d+10) == 0 or n % (d+12) == 0 or n % (d+16) == 0 or n % (d+22) == 0 or n % (d+24) == 0:
                return False

    return miller_rabin(n, 15)

def fermat_test(n) :
    """Use the Fermat's test a**(p-1) - 1 = 0 if p is prime for k in 2, 3, 5, 7."""

    if n in (2, 3, 5, 7):
        return True
    if n == 0 or n == 1 or n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False
    return not(pow(2, n - 1, n) != 1 or pow(3, n - 1, n) != 1 or pow(5, n - 1, n)!=1 or pow(7, n - 1, n) != 1)

def miller_rabin_witness(a, d, s, n):
    """Return True if a is a Miller-Rabin witness."""

    r = pow(a, d, n)
    if r == 1 or r == n - 1:
        return False
    for k in range(s):
        r = r**2 % n
        if r == n - 1:
            return False
    return True

def miller_rabin(n, k=15) :
    """
    Return the primality of n using the probabilistic test of primality of Miller-Rabin. k is the number of the loops.
    The possible decreases in averages of 75 % by unity if k.

    n : number to determine the primality ;
    k : number of tests (Error = 0.25 ^ number of tests).
    """

    if n in (0, 1):
        return False
    if n == 2:
        return True
    s = 1

    d = n // 2

    while d % 2 == 0:

        s +=  1

        d = d // 2

    for k in range(k) :

        a = randint(2, n - 1)
        if miller_rabin_witness(a, d, s, n):
            return False
    return True


##-sieves

def basic_erathostenes_sieve(end: int) -> list:
    """Inspired of an algorithm of someone else (a student of my father) and of https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes. Find all the prime numbers between 0 and end.
    Let n be end
    Complexity in time : O(n log(log(n)))
    Complexity in space : O(n)."""
    end = end + 1
    L = [True] * end
    L[0] = L[1] = False
    for i in range(int(math.sqrt(end)) + 1):
        if L[i]:
            for k in range(i**2, end, i):
                L[k] = False
    return [x for x in range(end) if L[x]]

def segmentation_erathostenes_sieve(end: int) -> list:
    """http://research.cs.wisc.edu/techreports/1990/TR909.pdf
    Complexity in space : O(sqrt(n))"""
    if end <= 1:
        return []
    end = end + 1
    s = int(math.sqrt(end)) + 1
    P = basic_erathostenes_sieve(s)
    P2 = []
    i = s
    while i < end:
        if i > end - s:
            s = end - i
        L = [True] * s
        for j in P:
            for k in range(-i % j, s, j):
                L[k] = False
        P2.extend([x+i for x in range(s) if L[x]])
        i = i + s
    return P+P2


##-using

def to_str(alg, n, n_tests=15):
    """Return informations extracted from the algorithm name specified."""

    ret = ""

    dct_algo_f = {
            tr('Trial division'): trial_division,
            tr('Wheel factorization'): wheel_factorization,
            tr("Fermat's factorization"): fermat_factorization,
            tr("Pollard's rho"): pollard_rho_decomposition,
            'p - 1': pollard_pm1_decomposition,
            tr("Miller-Rabin's test"): miller_rabin,
            tr("Fermat's test"): fermat_test,
            tr('Sieve of Erathostenes'): basic_erathostenes_sieve,
            tr('Segmented sieve of Erathostenes'): segmentation_erathostenes_sieve
        }

    dct_unicode_exp = {
            '0': '\u2070',
            '1': '\u00B9',
            '2': '\u00B2',
            '3': '\u00B3',
            '4': '\u2074',
            '5': '\u2075',
            '6': '\u2076',
            '7': '\u2077',
            '8': '\u2078',
            '9': '\u2079'
        }

    f = dct_algo_f[alg]

    if alg in ini.prima_algo_list[tr('Decomposition')]:
        primality, dec = f(n)

        if primality:
            txt = tr('Prime')
        else:
            txt = tr('Not prime') + '\n' + str(n) + ' = '

            dec.sort()
            dec2 = []

            k = 0
            while k < len(dec):
                p = dec[k]
                n = k
                while k < len(dec) and dec[k] == p:
                    k += 1
                txt += str(p)
                if (k-n) > 1:
                    l = str(k-n)
                    for j in l:
                        txt += dct_unicode_exp[j]
                txt += ' * '


            txt = txt[:-3]


    elif alg in ini.prima_algo_list[tr('Probabilistic')]:
        if alg == tr("Miller-Rabin's test"):
            primality = f(n, n_tests)

        else:
            primality = f(n)

        if primality:
            txt = tr('Probably prime')

        else:
            txt = tr('Not prime')


    else:
        L = f(n)
        txt = str(len(L)) + ' ' + tr('prime numbers') + ' :\n\n'
        for k in L:
            txt += '\t' + str(k) + '\n'

    return txt


##-console

def parser_use(n, pb=False):
    """Use prima functions with the parser console mode. Lasercata"""

    if not pb:
        p, L = trial_division(n)

    else:
        p = fermat2(n)

    if p and pb:
        return str(n) + ' ' + tr('is likely a prime number')

    elif p:
        return str(n) + ' ' + tr('is a prime number')

    elif pb:
        return str(n) + ' ' + tr('is a composite number')

    else:
        return str(n) + ' ' + tr('is a composite number') + '\n' + tr('List of prime factors : ') + str(L)


def use(cracker=cracker):
    """Use prima fonctions. Beautiful menu thanks to Lasercata"""

    c = ''
    while c not in ('0', 'quit', tr('exit'), 'q'):

        if cracker: color(c_succes)
        print('')
        print('\\'*50)

        if cracker: color(c_prog)
        print('\n' + tr('Prima menu :') + '\n')

        if cracker:
            color(c_error)
            print('    0.' + tr('Main menu'))
        else: print('    0.' + tr('Exit'))

        if cracker: color(c_succes)
        print('    ' + '-'*16)
        if cracker: color(c_wrdlt)

        print('    ' + tr('Decomposition of a number as a product of prime factors'))
        if cracker: color(c_ascii)
        print('        1 : ' + tr('Trial division'))
        print('        2 : ' + tr('Wheel factorization'))
        print('        3 : ' + tr("Fermat's' factorization"))
        print('        4 : ' + tr("Pollard's rho"))
        print('        5 : ' + tr('p - 1'))

        if cracker: color(c_succes)
        print('    ' + '-'*16)
        if cracker: color(c_wrdlt)

        print('    ' + tr("Probabilistic primality's test"))
        if cracker: color(c_ascii)
        print('        6 : ' + tr("Fermat's test"))
        print('        7 : ' + tr("Miller-Rabin's test"))

        if cracker: color(c_succes)
        print('    ' + '-'*16)
        if cracker: color(c_wrdlt)

        print('    ' + tr('Sieves to find prime numbers'))
        if cracker: color(c_ascii)
        print('        8 : ' + tr('Sieve of Erathostenes'))
        print('        9 : ' + tr('Segmented sieve of Erathostenes'))

        c = ''
        if cracker: c = cl_inp('\n' + tr('Your choice : '))
        else: c = input('\n' + tr('Your choice : '))

        if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q'):
            prnt = '"' + c + '" ' + tr('is NOT an option of this menu !')
            if cracker: cl_out(c_error, prnt)
            else: print(prnt)


        if c in ('1', '2', '3', '4', '5', '6', '7'):
            if cracker: n = inp_int(tr('Enter the integer number : '))
            else: n = int(input(tr('Enter the integer number : ')))

        if c != '0':

            t1 = datetime.now()

            dct = {
                '1': tr('Trial division'),
                '2': tr('Wheel factorization'),
                '3': tr("Fermat's factorization"),
                '4': tr("Pollard's rho"),
                '5': 'p - 1',
                '6': tr("Miller-Rabin's test"),
                '7': tr("Fermat's test"),
                '8': tr('Sieve of Erathostenes'),
                '9': tr('Segmented sieve of Erathostenes')
            }

            t1 = datetime.now()

            if c == '7':
                if cracker: nt = inp_int(tr('Number of tests (Error = 0.25 ^ number of tests) : '))
                else: nt = int(input(tr('Number of tests (Error = 0.25 ^ number of tests) : ')))
                txt = to_str(dct['7'], n, nt)
            else:

                if c in ('8', '9'):
                    if cracker: n = inp_int(tr('Limit : '))
                    else: n = int(input(tr('Limit : ')))
                    if c == '8':
                        f = basic_erathostenes_sieve
                    else:
                        f = segmentation_erathostenes_sieve
                    L = f(n)
                    txt = ""
                else:
                    txt = to_str(dct[c], n)

            t = datetime.now() - t1

            print(txt)

            if c in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                if cracker: cl_out(c_succes, tr('Realised in ') + str(t))
                else: print(tr('Realised in ') + str(t))

                if c in ('8', '9'):
                    print(tr('Length of the list :'), len(L))
                    ans = input(tr('Write the prime numbers in a file ? '))
                    if ans in (tr('y'), tr('Y'), tr('yes'), tr('Yes'), tr('YES')):
                        nf = input(tr('Name of the file (a file of the same name will be erase) : '))
                        f = open(nf, 'w')
                        for k in L:
                            f.write(str(k) + "\n")
                        f.close()
                    else:
                        if len(L) < 1000:
                            ans = input(tr('Print the list on the screen ? '))
                            if ans in (tr('y'), tr('Y'), tr('yes'), tr('Yes'), tr('YES')):
                                for k in L:
                                    print(k)
                if cracker: color(c_wrdlt)
                input(tr('---End---'))
                if cracker: color(c_prog)
