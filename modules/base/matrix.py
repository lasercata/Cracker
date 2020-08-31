#!/bin/python3
# -*- coding: utf-8 -*-

"""Program including matrice object."""

matrix__auth = 'Elerias'
matrix__last_update = '09.07.2020'
matrix__version = '1.1'


##-functions

def t(M, i, j):
    M2 = []
    for h in M:
        M2.append(list(h))
    del M2[i]
    for k in range(len(M2)):
        del M2[k][j]
    return M2

def modular_inverse(a, n):
    """Return the modular inverse of the integer a in a base n."""

    if a == 1:
        return 1
    n2 = n
    rest = a % n2
    aq = 1
    au = 1
    av = 0
    u = 0
    v = 1
    while rest > 1:
        rest = a % n2
        q = (a-rest) // n2
        nu = au - q*u
        nv = av-  q*v
        aq = q
        au = u
        av = v
        u = nu
        v = nv
        a = n2
        n2 = rest
    i = (u+n) % n
    return i


##-main class

class Matrix:
    """Class defining Matrix object."""

    def __init__(self, L=[]):
        """L is a list composed of m lists representing the lines and composed of n numbers."""

        if type(L) not in (list, tuple, set, Matrix):
            raise ValueError('The argument "L" should be a list, tuple, or a set, but a "{}" was found !!!'.format(type(L)))

        for j, k in enumerate(L):
            if type(k) not in (list, tuple, set, Matrix):
                raise ValueError('Invalid item in the list "L" at position {} : should be a list, tuple, or a set, but a "{}" was found !'.format(j, type(k)))

        self.value = list(L) # Creating a list here to do len(Matrix(c)), with type(c) = Matrix

    def __repr__(self):
        a = ""
        for k in self.value:
            for l in k:
                a = a + str(l) + " "
            a = a[0:-1] + "\n"
        return a[0:-1]

    def __getitem__(self, i):
        return self.value[i]

    def __add__(A, B):
        """Addition of two matrix."""

        vA = A.value
        vB = B.value
        if len(vA) == len(vB) and len(vA[0]) == len(vB[0]):
            vC = []
            for i in range(len(vA)):
                a = []
                for j in range(len(vA[0])):
                    a.append(vA[i][j] + vB[i][j])
                vC.append(a)
            C = Matrix(vC)
            return C
        else:
            return "Undefined"

    def __sub__(A, B):
        """Soustraction of two matrix."""

        vA = A.value
        vB = B.value
        if len(vA) == len(vB) and len(vA[0]) == len(vB[0]):
            vC = []
            for i in range(len(vA)):
                a = []
                for j in range(len(vA[0])):
                    a.append(vA[i][j] - vB[i][j])
                vC.append(a)
            C = Matrix(vC)
            return C
        else:
            return "IndÃƒÆ’Ã‚Â©fini" # 'Undefined' ?

    def __mul__(A, B):
        """Product of two matrix or scalar multiplication of one matrix and one number."""

        if type(A) != Matrix or type(B) != Matrix:
            if type(A) == Matrix:
                A, B = B, A
            vB = B.value #todo: error here ?
            vC = []
            for i in vB:
                a = []
                for j in i:
                    a.append(A * j)
                vC.append(a)
            C = Matrix(vC)
            return C

        vA = A.value
        vB = B.value
        if len(vA[0]) == len(vB):
            vC = []
            for i in range(len(vA)):
                a = []
                for j in range(len(vB[0])):
                    s = 0
                    for k in range(len(vA[0])):
                        s = s + vA[i][k] * vB[k][j]
                    a.append(s)
                vC.append(a)
            C = Matrix(vC)
            return C
        else:
            return "Undefined"

    def __truediv__(A, B):
        """Product of matrix A and inverse of matrix or the number B in base n if specified."""

        if type(B) == Matrix:
            return A * B.inverse()
        return A * (1 / B)

    def __mod__(A, n):
        """Return matrix A in base n."""

        vA = A.value
        vB = []
        for i in vA:
            c = []
            for j in i:
                c.append(j % n)
            vB.append(c)
        return Matrix(vB)

    def __pow__(A, n):
        """Return matrix A raised to the power n."""

        B = A
        for k in range(n-1):
            B = B * A
        return B

    def det(self):
        """Return the determinant of square matrix."""

        M = self.value
        if len(M) == len(M[0]):    # if the matrix is square, return the determinant
            if len(M) == 1:    # calculating for size 1
                return M[0][0]
            if len(M) == 2:    # calculating for size 2
                return M[0][0] * M[1][1] - M[0][1] * M[1][0]
            else:    # calculating for other sizes
                d = 0
                for k in range(len(M)):
                    M2=[]
                    for l in range(len(M)-1):
                        M2.append(M[l+1][0:k] + M[l+1][k+1:len(M)])
                    M2 = Matrix(M2)
                    if k % 2 == 0:
                        d = d + M[0][k] * M2.det()
                    else:
                        d = d - M[0][k] * M2.det()
                return d
        else:
            return "Undefined"

    def transpose(self):
        """Return the transpose of the matrix."""

        M = self.value
        M2 = []
        for j in range(len(M[0])):
            c = []
            for k in range(len(M)):
                c.append(M[k][j])
            M2.append(c)
        return Matrix(M2)

    def comatrice(self):
        """Return the comatrix of the matrix."""

        M = self.value
        C = []
        nl = len(M)
        nc = len(M[0])
        for i in range(nc):
            c = []
            for j in range(nl):
                if (i + j) % 2 == 0:
                    c.append(det(t(M, i, j))) #todo: What is this function ?
                else:
                    c.append(-det(t(M, i, j))) #todo: there is a self.det function, but it does not take other arg than self.
            C.append(c)
        return Matrix(C)

    def inverse(self, n=0):
        """Return the inverse of the matrix and in base n if specified."""

        M = self.value
        if n == 0:
            return self.comatrice().transpose() * (1 / (self.det()))
        else:
            return (self.comatrice().transpose() * modular_inverse(self.det(), n)) % n

    def trace(self):
        """Return the trace of the matrix."""

        t = 0
        M = self.value
        a = len(M[0])
        if len(M) < len(M[0]):
            a = len(M)
        for k in range(a):
            t = t + M[k][k]
        return t