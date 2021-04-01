#!/bin/python3
# -*- coding: utf-8 -*-

calc__auth = 'Elerias'
calc__ver = '1.0'
calc__last_update = '01.04.2021'


##-import

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QLCDNumber, QPushButton


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

        calc_grid = QGridLayout(self)

        self.screen = QLCDNumber(self)
        self.screen.setMinimumSize(200, 45)
        self.screen.setDigitCount(20)

        calc_grid.addWidget(self.screen, 0, 0, 1, 4)

        labels = [
        '7', '8', '9', '+',
        '4', '5', '6', '-',
        '1', '2', '3', '×',
        '0', '.', 'Ent', '÷'
        ]

        buttons = []
        buttons_functions = [
        lambda: self.add('7'), lambda: self.add('8'), lambda: self.add('9'), lambda: self.add('+'),
        lambda: self.add('4'), lambda: self.add('5'), lambda: self.add('6'), lambda: self.add('-'),
        lambda: self.add('1'), lambda: self.add('2'), lambda: self.add('3'), lambda: self.add('×'),
        lambda: self.add('0'), lambda: self.add('.'), lambda: self.add('Ent'), lambda: self.add('÷')
        ]

        for k in range(16):
            buttons.append(QPushButton(labels[k]))
            buttons[k].clicked.connect(buttons_functions[k])
            calc_grid.addWidget(buttons[k], 1 + k // 4, k % 4)

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
        else:
            self.point = False
            self.zeros = 0
            self.n_dec = 0
            if c == 'Ent':
                self.modif = True
                self.stack.append(0)
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


##-main

if __name__ == '__main__':
    monApp=QApplication(sys.argv)
    window = Calc()
    window.show()
    sys.exit(monApp.exec_())

