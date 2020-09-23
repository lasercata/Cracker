#!/bin/python3
# -*- coding: utf-8 -*-

"""Program including useful arithmetic functions."""

arithmetic__auth = 'Elerias'
arithmetic__last_update = '23.09.2020'
arithmetic__version = '1.0'


##-functions

def extended_gcd(a: int, b: int) -> (int, (int, int)):
    """
    Extended Euclidean algorithm.
    Return great common divisor (gcd) and Bezout coefficients (u, v) for (a, b).
    u*a + v*b = gcd(a, b)
    Return (gcd, (u, v)).
    Source of algorithm : https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm.
    """
    
    (old_r, r) = (a, b)
    (old_u, u) = (1, 0)
    (old_v, v) = (0, 1)

    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q*r)
        (old_u, u) = (u, old_u - q*u)
        (old_v, v) = (v, old_v - q*v)

    return old_r, (old_u, old_v)


def bezout(a: int, b: int) -> (int, int):
    """
    Return Bézout coefficients (u, v) for (a, b).
    u*a + v*b = gcd(a, b)
    """
    
    return extended_gcd(a, b)[1]


def mult_inverse(a: int, n: int) -> int:
    """
    Return multiplicative inverse u of a modulo n.
    u*a = 1 modulo n
    Source of algorithm : https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm.
    """
    
    (old_r, r) = (a, n)
    (old_u, u) = (1, 0)

    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q*r)
        (old_u, u) = (u, old_u - q*u)

    if old_r > 1:
        raise ValueError(str(a) + ' is not inversible in the ring Z/' + str(n) + 'Z.')

    if old_u < 0:
        return old_u + n
    else:
        return old_u
