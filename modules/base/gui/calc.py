#!/bin/python3
# -*- coding: utf-8 -*-

calc__auth = 'Elerias'
calc__ver = '1.2'
calc__last_update = '02.04.2021'


##-import

import sys
import math
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QLCDNumber, QPushButton, QShortcut
from PyQt5.QtGui import QKeySequence


##-class

class Calc(QWidget):

    def __init__(self):
        super().__init__()

        self.stack = [0]
        self.point = False
        self.n_dec = 0
        self.zeros = 0
        self.modif = True

        self.create_gui()

    def create_gui(self):

        self.setWindowTitle('Cracker calc')

        calc_grid = QGridLayout(self)

        self.screen = QLCDNumber(self)
        self.screen.setMinimumSize(350, 45)
        self.screen.setDigitCount(20)

        calc_grid.addWidget(self.screen, 1, 0, 1, 4)

        self.little_screen = QLCDNumber(self)
        self.little_screen.setMaximumSize(175, 20)
        self.little_screen.setDigitCount(20)

        calc_grid.addWidget(self.little_screen, 0, 2, 1, 2)

        labels = [
        'C', 'CE', '√',   'x²',
        '7', '8',  '9',   '÷',
        '4', '5',  '6',   '×',
        '1', '2',  '3',   '-',
        '0', '.',  'Ent', '+'
        ]

        buttons = []
        buttons_functions = [
        lambda: self.reset(), lambda: self.add('CE'), lambda: self.add('√'), lambda: self.add('x²'),
        lambda: self.add('7'), lambda: self.add('8'), lambda: self.add('9'), lambda: self.add('÷'),
        lambda: self.add('4'), lambda: self.add('5'), lambda: self.add('6'), lambda: self.add('×'),
        lambda: self.add('1'), lambda: self.add('2'), lambda: self.add('3'), lambda: self.add('-'),
        lambda: self.add('0'), lambda: self.add('.'), lambda: self.add('Ent'), lambda: self.add('+')
        ]
        QShortcut(QKeySequence('Delete'), self).activated.connect(buttons_functions[0])
        QShortcut(QKeySequence('Backspace'), self).activated.connect(buttons_functions[1])
        QShortcut(QKeySequence('s'), self).activated.connect(buttons_functions[2])
        QShortcut(QKeySequence('²'), self).activated.connect(buttons_functions[3])
        QShortcut(QKeySequence('7'), self).activated.connect(buttons_functions[4])
        QShortcut(QKeySequence('8'), self).activated.connect(buttons_functions[5])
        QShortcut(QKeySequence('9'), self).activated.connect(buttons_functions[6])
        QShortcut(QKeySequence('/'), self).activated.connect(buttons_functions[7])
        QShortcut(QKeySequence('4'), self).activated.connect(buttons_functions[8])
        QShortcut(QKeySequence('5'), self).activated.connect(buttons_functions[9])
        QShortcut(QKeySequence('6'), self).activated.connect(buttons_functions[10])
        QShortcut(QKeySequence('*'), self).activated.connect(buttons_functions[11])
        QShortcut(QKeySequence('1'), self).activated.connect(buttons_functions[12])
        QShortcut(QKeySequence('2'), self).activated.connect(buttons_functions[13])
        QShortcut(QKeySequence('3'), self).activated.connect(buttons_functions[14])
        QShortcut(QKeySequence('-'), self).activated.connect(buttons_functions[15])
        QShortcut(QKeySequence('0'), self).activated.connect(buttons_functions[16])
        QShortcut(QKeySequence('.'), self).activated.connect(buttons_functions[17])
        QShortcut(QKeySequence('Return'), self).activated.connect(buttons_functions[18])
        QShortcut(QKeySequence('+'), self).activated.connect(buttons_functions[19])


        for k in range(20):
            buttons.append(QPushButton(labels[k]))
            buttons[k].clicked.connect(buttons_functions[k])
            calc_grid.addWidget(buttons[k], 2 + k // 4, k % 4)

        self.display()

    def add(self, c):
        if c in '0123456789':
            if not self.modif:
                self.stack.append(0)
                self.modif = True
            self.addNumeral(int(c))
        elif c == '.':
            if not self.modif:
                self.stack.append(0)
                self.modif = True
            self.point = True
        elif c == 'CE' and self.modif:
            self.stack[-1] = 0
            self.point = False
            self.zeros = 0
            self.n_dec = 0
        else:
            self.point = False
            self.zeros = 0
            self.n_dec = 0
            if c == 'Ent':
                self.modif = True
                self.stack.append(0)
            elif c in ('√', 'x²'):
                if c == '√' and self.stack[-1] >= 0:
                    self.stack[-1] = math.sqrt(self.stack[-1])
                    self.modif = False
                else:
                    self.stack[-1] = self.stack[-1] ** 2
                    self.modif = False
            elif c in '+-×÷':
                if len(self.stack) >= 2:
                    if c == '+':
                        self.stack[-2] = self.stack[-2] + self.stack[-1]
                        del self.stack[-1]
                        self.modif = False
                    elif c == '-':
                        self.stack[-2] = self.stack[-2] - self.stack[-1]
                        del self.stack[-1]
                        self.modif = False
                    elif c == '×':
                        self.stack[-2] = self.stack[-2] * self.stack[-1]
                        del self.stack[-1]
                        self.modif = False
                    elif self.stack[-1] != 0:
                        self.stack[-2] = self.stack[-2] /self.stack[-1]
                        del self.stack[-1]
                        self.modif = False
        self.display()


    def addNumeral(self, n):
        if self.point:
            self.n_dec += 1
            if n != 0:
                self.stack[-1] += n/10**self.n_dec
                self.zeros = 0
            else:
                self.zeros += 1
        else:
            self.stack[-1] = self.stack[-1] * 10 + n

    def display(self):
        if self.point and self.stack[-1] == int(self.stack[-1]):
            self.screen.display(str(self.stack[-1]) + '.' + self.zeros*'0')
        else:
            self.screen.display(str(self.stack[-1]) + self.zeros*'0')
        if len(self.stack) > 1:
            self.little_screen.display(self.stack[-2])
        else:
            self.little_screen.display("")

    def reset(self):
        self.stack = [0]
        self.point = False
        self.n_dec = 0
        self.zeros = 0
        self.modif = True
        self.display()



##-main

if __name__ == '__main__':
    monApp=QApplication(sys.argv)
    window = Calc()
    window.show()
    sys.exit(monApp.exec_())

