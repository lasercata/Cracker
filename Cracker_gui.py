#!/bin/python3
# -*- coding: utf-8 -*-

'''Launch Cracker with PyQt5 graphical interface.'''

Cracker_gui__auth = 'Lasercata'
Cracker_gui__last_update = '01.04.2021'
Cracker_gui__version = '1.3.0'


##-import/ini
with open('Data/interface', 'w') as f:
    f.write('gui')


from modules.base.ini import *


##-helpful functions / classes
#---------About
class AboutCracker(QMainWindow):
    '''Create a tab window to show informations on Cracker.'''

    def __init__(self, parent=None):
        '''Create the window'''

        #------ini
        super(AboutCracker, self).__init__(parent)
        self.setWindowTitle(tr('Cracker ― About'))

        main_wid = QWidget()
        main_wid_lay = QGridLayout()
        main_wid.setLayout(main_wid_lay)

        self.m = QTabWidget()
        main_wid_lay.addWidget(self.m, 0, 0)

        self.bt_ok = QPushButton('Ok')
        self.bt_ok.clicked.connect(self.close)
        main_wid_lay.addWidget(self.bt_ok, 1, 0, Qt.AlignRight)

        self.setCentralWidget(main_wid)

        #------about tab
        about_lay = QGridLayout()
        about = QWidget()
        about.setLayout(about_lay)

        self.about_msg = '\n' + tr('Cracker is a software developed and updated by Lasercata and by Elerias. It is written in Python 3 and in C.') + '\n\n\n' + NewLine(100).text_set(tr('This software is a toolbox application that enables you to do many things : you can encrypt securely a secret message using one of the many ciphers present in Cracker (KRIS, AES, RSA, ...), sign it with a hash function, decrypt it.')) + '\n\n' + NewLine(100).text_set(tr('If you have a message without the key, but you need to read the content, you can try to crack it using a wordlist that you made with Cracker, or let the algorithm try to crack it using its wordlist bank.')) + '\n\n' + NewLine(100).text_set(tr("You don't remember which was your favourite wordlist ? Don't worry ! You can analyze them with the wordlist tab to get numerous informations on them.")) + '\n\n' + NewLine(100).text_set(tr('You need to convert a number from binary to hexadecimal ? You need to do a special conversion using your own base alphabet ? Check the "Base convert" tab.')) + '\n\n' + NewLine(100).text_set(tr('As you can see, there is a lot of functions, often about cracking. But Cracker can also help to improve your security : if you need a strong password, hard to be cracked by brute-force, the "P@ssw0rd_Test0r" tab is for you ! It gives a lot of informations about the password you entered, like its entropy.')) + '\n'

        about_lay.addWidget(QLabel(self.about_msg), 0, 0)

        self.m.addTab(about, tr('&About'))

        #------versions tab
        ver = QTextEdit()
        ver.setReadOnly(True)
        if modules_ver != '':
            ver.setPlainText('Cracker : v{}\n{}'.format(cracker_version, modules_ver))

        self.m.addTab(ver, tr('&Version'))

        #------updates tab
        up_lay = QGridLayout()
        up = QWidget()
        up.setLayout(up_lay)

        self.txt = QTextEdit()
        self.txt.setReadOnly(True)
        #self.txt.setMinimumSize(400, 100)
        self.txt.setPlainText(update_notes)
        up_lay.addWidget(self.txt, 0, 0)

        self.m.addTab(up, tr('&Updates'))

        #------authors tab
        auth_lay = QGridLayout()
        auth = QWidget()
        auth.setLayout(auth_lay)

        auth_lay.addWidget(QLabel(tr('By <h3>Lasercata</h3><h3>Elerias</h3>'), alignment=Qt.AlignCenter), 0, 0, Qt.AlignCenter)

        lasercata_logo = QLabel(self)
        lasercata_l_pixmap = QPixmap('Style/lasercata_logo_fly_curve.png')

        lasercata_logo.setPixmap(lasercata_l_pixmap.scaledToHeight(150))
        auth_lay.addWidget(lasercata_logo, 1, 0, alignment=Qt.AlignCenter)

        self.m.addTab(auth, tr('Au&thors'))


    #---------use
    def use(parent=None, main=False):
        '''Launch the window.'''

        if main:
            app_ = QApplication(sys.argv)

        about = AboutCracker(parent)
        about.show()

        if main:
            app_.exec()


#---------Double input
class DoubleInput(QWidget):
    '''Class defining a double input.'''

    def __init__(self, type_=QLineEdit, n=2, parent=None):
        '''
        Initiate the DoubleInput object.

        - type_ : The type of the two widgets. Should be QLineEdit, or QSpinBox ;
        - n : the number of inputs.
        '''

        if type_ not in (QLineEdit, QSpinBox):
            raise ValueError(tr('The arg "type_" should be QLineEdit or QSpinBox, but "{}" was found !!!').format(type_))

        if type(n) != int:
            raise ValueError(tr('The arg "n" should be an int !!!'))

        elif n < 1:
            raise ValueError(tr('The arg "n" should be greater or equal to 1 !!!'))

        #------ini
        super().__init__(parent)

        self.type_ = type_
        self.n = n

        #------widgets
        #---layout
        main_lay = QGridLayout()
        self.setLayout(main_lay)

        #---inputs
        self.inp_lst = []

        if type_ == QLineEdit:
            for k in range(n):
                self.inp_lst.append(QLineEdit())

        elif type_ == QSpinBox:
            for k in range(n):
                self.inp_lst.append(QSpinBox())

        for j, w in enumerate(self.inp_lst):
            main_lay.addWidget(w, 0, j)


    def setStyleSheet(self, style):
        '''Apply the stylesheet 'style'.'''

        for w in self.inp_lst:
            w.setStyleSheet(style)


    def setObjectName(self, name):
        '''Set the object's name.'''

        for w in self.inp_lst:
            w.setObjectName(name)


    def setMinimum(self, n):
        '''Set the minimal number in the QSpinBoxes.'''

        for w in self.inp_lst:
            w.setMinimum(n)


    def setMaximum(self, n):
        '''Set the maximal number in the QSpinBoxes.'''

        for w in self.inp_lst:
            w.setMaximum(n)


    def value(self):
        '''Return the value of the inputs, in a tuple.'''

        if self.type_ == QLineEdit:
            ret = [w.text() for w in self.inp_lst]

        elif self.type_ == QSpinBox:
            ret = [w.value() for w in self.inp_lst]

        return tuple(ret)


    def text(self):
        '''Same as self.value()'''

        return self.value()



##-GUI
class CrackerGui(QMainWindow):
    '''Class defining Cracker's graphical user interface using PyQt5'''

    def __init__(self, parent=None):
        '''Create the window'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Cracker v' + cracker_version)
        self.setWindowIcon(QIcon('Style/Cracker_icon.ico'))

        #---the QTabWidget
        self.app_widget = QTabWidget()
        self.setCentralWidget(self.app_widget)

        self.path_ent = {} #List of all the QLineEdit in paths bar, by tab index (Ig. : {0 : QLineEdit(), 1 : QLineEdit()})
        self.lst_txt = [] #List of all the TextEditor object, used to reload them when changing directory.

        self.lst_wrdlst_opt = {} #List of all the ComboBox selecting the wordlists, by sender text.
        self.lst_selected_wrdlst = {
            tr('Select a wordlist ...') : [],
            tr('Select a location ...') : []
            } #Dict which contain all the selected wordlists, by sender text.
        self.lst_selected_wrdlst[tr('Select a file ...')] = self.lst_selected_wrdlst[tr('Select a wordlist ...')]

        #self.style = style_test
        self.app_style = GuiStyle()
        self.style = self.app_style.style_sheet

        #------create the tabs
        self.tabs = {
            0 : tr('Home'),
            1 : 'Crack',
            2 : tr('Ciphers'),
            3 : 'Wordlists',
            4 : 'Prima',
            5 : 'Base convert',
            6 : 'P@ssw0rd_Test0r',
            7 : 'Anamer0',
            8 : tr('Settings')
        }

        self.create_home()
        self.create_crack()
        self.create_ciphers()
        self.create_wordlists()
        self.create_prima()
        self.create_b_cvrt()
        self.create_pwd_strth()
        self.create_anamer0()
        self.create_settings()

        self.app_widget.currentChanged.connect(self.chk_tab)

        #QCloseEvent.ignore()

        #------show
        self.chk_tab(0) #Resize the window and set a mnimum size.
        self.show()



    #---------create home tab
    def create_home(self):
        '''Create the home tab'''

        #------ini
        tab_home = QWidget()

        tab_home_lay = QGridLayout()
        tab_home_lay.setContentsMargins(5, 5, 5, 5)
        tab_home.setLayout(tab_home_lay)

        #------path bar
        tab_home_lay.addWidget(self.create_path_bar(tab=0), 0, 0, alignment=Qt.AlignTop)

        #------widgets
        logo = QLabel(self)
        l_pixmap = QPixmap('Style/Cracker_ascii_logo.png')
        logo.setPixmap(l_pixmap)
        tab_home_lay.addWidget(logo, 0, 0, alignment=Qt.AlignCenter)

        bt_info = QPushButton(tr('&About ...'))
        bt_info.setObjectName('bt_info')
        bt_info.setStyleSheet(self.style)
        bt_info.setMaximumSize(QSize((len(tr('&About ...'))-1)*13, 35))
        bt_info.clicked.connect(self.show_infos)
        tab_home_lay.addWidget(bt_info, 0, 0, Qt.AlignLeft | Qt.AlignBottom)

        bt_lay = QHBoxLayout()
        tab_home_lay.addLayout(bt_lay, 0, 0, alignment=Qt.AlignRight | Qt.AlignBottom)

        bt_calc = QPushButton('&Calc')
        bt_calc.setObjectName('bt_calc')
        bt_calc.setStyleSheet(self.style)
        bt_calc.setMaximumSize(QSize(52, 35))
        bt_calc.clicked.connect(self.start_calc)
        bt_lay.addWidget(bt_calc)

        bt_lock = QPushButton(tr('&Lock'))
        bt_lock.setObjectName('bt_lock')
        bt_lock.setStyleSheet(self.style)
        bt_lock.setMaximumSize(QSize((len(tr('&Lock'))-1)*13, 35))
        bt_lock.clicked.connect(self.lock)
        bt_lay.addWidget(bt_lock)

        bt_quit = QPushButton(tr('&Quit'))
        bt_quit.setObjectName('bt_quit')
        bt_quit.setStyleSheet(self.style)
        bt_quit.setMaximumSize(QSize((len(tr('&Quit'))-1)*13, 35))
        bt_quit.clicked.connect(self.quit)
        bt_lay.addWidget(bt_quit)


        #------show
        self.app_widget.addTab(tab_home, tr('&Home'))



    #---------create crack tab
    def create_crack(self):
        '''Create the "Crack" tab.'''

        #------ini
        tab_crack = QWidget()

        tab_crack_lay = QGridLayout()
        tab_crack_lay.setContentsMargins(5, 5, 5, 5)
        tab_crack.setLayout(tab_crack_lay)

        #------check functions
        def chk_meth(meth):
            '''Check the selected method and decide to dislable or not the wordlist's selection.'''

            if meth == 'Dictionary attack':
                for wid in crack_wrdlst_lst_wid:
                    wid.setHidden(False)
                    wid.setDisabled(False)

                for wid in crack_wlst_permut_lst:
                    wid.setHidden(True)

            elif meth == 'Brute-force':
                for wid in crack_wlst_permut_lst:
                    wid.setHidden(False)
                    wid.setDisabled(False)

                for wid in crack_wrdlst_lst_wid:
                    wid.setHidden(True)

            else:
                for wid in crack_wrdlst_lst_wid:
                    wid.setDisabled(True)

                for wid in crack_wlst_permut_lst:
                    wid.setDisabled(True)


        def chk_ciph(cipher):
            '''Check the cipher's combo box and dislable or not options in crack method.'''

            if cipher in crypta.broken_ciph:
                self.crack_opt_meth.model().item(5).setEnabled(True)

            else:
                self.crack_opt_meth.model().item(5).setEnabled(False)
                if self.crack_opt_meth.currentText() == 'Code break':
                    self.crack_opt_meth.setCurrentText('-- Select a method --')


            if cipher in (*ciphers_list['hash'], *crypta.ciph_sort['0_key'], 'Unknow', 'Unknow hash'):
                for k in range(2, 5): #2, 3, 4
                    self.crack_opt_meth.model().item(k).setEnabled(True)


            elif cipher in (*crypta.ciph_sort['1_key_str'], *crypta.ciph_sort['1_key_int']):
                self.crack_opt_meth.model().item(2).setEnabled(True)
                self.crack_opt_meth.model().item(3).setEnabled(False)
                self.crack_opt_meth.model().item(4).setEnabled(False)

                if self.crack_opt_meth.currentText() not in ('Code break', 'Brute-force'):
                    self.crack_opt_meth.setCurrentText('-- Select a method --')

            else:
                for k in range(2, 5): #2, 3, 4
                    self.crack_opt_meth.model().item(k).setEnabled(False)

                if self.crack_opt_meth.currentText() != 'Code break':
                    self.crack_opt_meth.setCurrentText('-- Select a method --')


        def clear():
            '''Clear the text return widget.'''

            if self.crack_ret.toPlainText() != '':
                sure = QMessageBox.question(self, 'Sure ?', '<h2>Are you sure ?</h2>', \
                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)

                if sure != QMessageBox.Yes:
                    return None

                self.crack_ret.clear()


        #------path bar
        tab_crack_lay.addWidget(self.create_path_bar(tab=1), 0, 0, 1, 4, alignment=Qt.AlignTop)

        #------widgets
        #---text editor
        self.txt_crack = TextEditor()
        self.lst_txt.append(self.txt_crack) # used to reload when changing directory.
        tab_crack_lay.addWidget(self.txt_crack, 1, 0, 1, 4)

        tab_crack_lay.addWidget(QLabel(''), 2, 0) # blank

        #---combo box cipher
        opt_ciph_lay = QHBoxLayout()
        tab_crack_lay.addLayout(opt_ciph_lay, 3, 0)

        opt_ciph_lay.addWidget(QLabel('Encrypted with :'))

        self.crack_opt_ciph = QComboBox()
        self.crack_opt_ciph.activated[str].connect(chk_ciph)
        opt_ciph_lay.addWidget(self.crack_opt_ciph)
        self.crack_opt_ciph.addItem('-- Select an algorithm --')
        self.crack_opt_ciph.insertSeparator(3)
        self.crack_opt_ciph.addItems(['Unknow', 'Unknow hash'])

        for k in ciphers_list:
            if k not in ('KRIS', 'AES', 'RSA', 'analysis'):
                self.crack_opt_ciph.insertSeparator(500)
                self.crack_opt_ciph.addItems(ciphers_list[k])

        #---combo box method
        opt_meth_lay = QHBoxLayout()
        tab_crack_lay.addLayout(opt_meth_lay, 4, 0)

        opt_meth_lay.addWidget(QLabel('Crack method :'))

        self.crack_opt_meth = QComboBox()
        self.crack_opt_meth.activated[str].connect(chk_meth)
        self.crack_opt_meth.addItem('-- Select a method --')
        self.crack_opt_meth.insertSeparator(3)
        self.crack_opt_meth.addItems(crack_method_list)
        opt_meth_lay.addWidget(self.crack_opt_meth)

        #---wordlist chooser
        crack_wrdlst_lay = QGridLayout()
        tab_crack_lay.addLayout(crack_wrdlst_lay, 3, 1, 2, 1)

        crack_wrdlst_lb = QLabel('Wordlist :')
        crack_wrdlst_lay.addWidget(crack_wrdlst_lb, 0, 0, alignment=Qt.AlignCenter)

        self.crack_bt_wrdlst = QPushButton(tr('Select a wordlist ...'))
        self.crack_bt_wrdlst.clicked.connect(self.select_wrdlst)
        crack_wrdlst_lay.addWidget(self.crack_bt_wrdlst, 0, 1, alignment=Qt.AlignLeft)

        self.crack_opt_wrdlst = QComboBox()
        self.crack_opt_wrdlst.addItem('-- Previously selected wordlists --')
        self.crack_opt_wrdlst.insertSeparator(1)
        self.lst_wrdlst_opt[tr('Select a wordlist ...')] = self.crack_opt_wrdlst
        crack_wrdlst_lay.addWidget(self.crack_opt_wrdlst, 1, 0, 1, 2)

        crack_wrdlst_lst_wid = (crack_wrdlst_lb, self.crack_bt_wrdlst, self.crack_opt_wrdlst) #To dislable or not with chk_meth

        #---wordlist gen (permutations)
        crack_wlst_permut_lay = QGridLayout()
        tab_crack_lay.addLayout(crack_wlst_permut_lay, 3, 1, 2, 1)

        #-spin box
        wlst_sp_lb = QLabel("Words' length :")
        crack_wlst_permut_lay.addWidget(wlst_sp_lb, 0, 0, 1, 2)

        self.crack_wlst_sp = QSpinBox()
        self.crack_wlst_sp.setMaximum(50)
        self.crack_wlst_sp.setMinimum(1)
        self.crack_wlst_sp.setValue(5)
        crack_wlst_permut_lay.addWidget(self.crack_wlst_sp, 0, 0, 1, 2, Qt.AlignCenter)

        #-alphabet
        wlst_alf_lb = QLabel(tr('Alphabet :'))
        crack_wlst_permut_lay.addWidget(wlst_alf_lb, 1, 0)

        self.crack_wlst_alf = QComboBox()
        self.crack_wlst_alf.setMaximumSize(200, 35)
        self.crack_wlst_alf.setEditable(True)
        self.crack_wlst_alf.addItem(tr('-- Select an alphabet --'))
        self.crack_wlst_alf.insertSeparator(1)
        self.crack_wlst_alf.addItems(w_gen.alfs.values())
        crack_wlst_permut_lay.addWidget(self.crack_wlst_alf, 1, 1, Qt.AlignLeft)

        crack_wlst_permut_lst = (wlst_sp_lb, self.crack_wlst_sp, wlst_alf_lb, self.crack_wlst_alf)


        tab_crack_lay.setRowMinimumHeight(5, 15)


        self.crack_ret = QTextEdit()
        self.crack_ret.setReadOnly(True)
        self.crack_ret.setMinimumSize(440, 170)
        self.crack_ret.setStyleSheet(self.style)
        self.crack_ret.setObjectName('orange_border_hover')

        tab_crack_lay.addWidget(self.crack_ret, 2, 2, -1, -1, alignment=Qt.AlignTop)

        #---Crack button
        self.bt_crack = QPushButton('C&rack')
        self.bt_crack.setStyleSheet(self.style)
        self.bt_crack.setObjectName('main_obj')
        tab_crack_lay.addWidget(self.bt_crack, 2, 2, -1, -1, Qt.AlignRight | Qt.AlignBottom)

        #---Clear button
        self.crack_bt_clear = QPushButton('Clear')
        self.crack_bt_clear.setMaximumSize(50, 35)
        self.crack_bt_clear.clicked.connect(clear)
        tab_crack_lay.addWidget(self.crack_bt_clear, 5, 1, Qt.AlignRight)

        #------connection
        use_crack = UseCrackTab(
            self.txt_crack,
            self.crack_opt_ciph,
            self.crack_opt_meth,
            self.crack_wlst_sp,
            self.crack_wlst_alf,
            self.crack_opt_wrdlst,
            self.crack_ret
        )

        self.bt_crack.clicked.connect(lambda: use_crack.crack())


        #------show
        chk_meth('Dictionary attack') #Dislable the wordlist selection.
        chk_meth(None)

        self.app_widget.addTab(tab_crack, '&Crack')



    #---------create cipher tab
    def create_ciphers(self):
        '''Create the "Cipher" tab.'''

        #------ini
        tab_cipher = QWidget()

        tab_cipher_lay = QGridLayout()
        tab_cipher_lay.setColumnStretch(0, 1)
        tab_cipher_lay.setContentsMargins(5, 5, 5, 5)
        tab_cipher.setLayout(tab_cipher_lay)

        #------check functions
        def chk_ciph(cipher):
            '''Check the cipher's combo box and dislable or not some widgets, and change the key's entry.'''

            if cipher in (*ciphers_list['KRIS'], *ciphers_list['RSA']): #RSA
                self.cipher_opt_keys.setHidden(False)
                self.cipher_ledit_keys.setHidden(True)
                self.cipher_nb_key.setHidden(True)
                self.cipher_db_ledit_key.setHidden(True)
                self.cipher_db_nb_key.setHidden(True)

            elif cipher in (*crypta.ciph_sort['1_key_int'], tr('Frequence analysis'), 'SecHash'): #QSpinBox
                self.cipher_nb_key.setHidden(False)
                self.cipher_ledit_keys.setHidden(True)
                self.cipher_opt_keys.setHidden(True)
                self.cipher_db_ledit_key.setHidden(True)
                self.cipher_db_nb_key.setHidden(True)

            elif cipher in crypta.ciph_sort['2_key_str']: #Qouble line edit
                self.cipher_db_ledit_key.setHidden(False)
                self.cipher_opt_keys.setHidden(True)
                self.cipher_ledit_keys.setHidden(True)
                self.cipher_nb_key.setHidden(True)
                self.cipher_db_nb_key.setHidden(True)

            elif cipher in crypta.ciph_sort['2_key_int']: #Qouble QSpinBox
                self.cipher_db_nb_key.setHidden(False)
                self.cipher_opt_keys.setHidden(True)
                self.cipher_ledit_keys.setHidden(True)
                self.cipher_nb_key.setHidden(True)
                self.cipher_db_ledit_key.setHidden(True)

            else: #QLinEdit
                self.cipher_ledit_keys.setHidden(False)
                self.cipher_opt_keys.setHidden(True)
                self.cipher_nb_key.setHidden(True)
                self.cipher_db_ledit_key.setHidden(True)
                self.cipher_db_nb_key.setHidden(True)


            if cipher in ciphers_list[tr('analysis')]:
                self.cipher_bt_enc.setText(tr('Analys&e ↓'))

            elif cipher == 'RSA signature':
                self.cipher_bt_enc.setText(tr('Si&gn ↓'))
                self.cipher_bt_dec.setText(tr('Chec&k'))

            elif cipher in ciphers_list['hash']:
                self.cipher_bt_enc.setText(tr('H&ash ↓'))

            else:
                self.cipher_bt_enc.setText(tr('&Encrypt ↓'))
                self.cipher_bt_dec.setText(tr('&Decrypt ↑'))


            dis = (cipher in (*ciphers_list['hash'][:-1], *ciphers_list[tr('analysis')], *crypta.ciph_sort['0_key'])) ^ (cipher == tr('Frequence analysis'))
            self.cipher_opt_keys.setDisabled(dis)
            self.cipher_ledit_keys.setDisabled(dis)
            self.cipher_nb_key.setDisabled(dis)
            self.cipher_db_ledit_key.setDisabled(dis)
            self.cipher_db_nb_key.setDisabled(dis)

            self.cipher_opt_alf.setDisabled(cipher not in crypta.ciph_sort['alf'])
            self.cipher_bt_dec.setDisabled(cipher in (*ciphers_list['hash'], *ciphers_list[tr('analysis')]))

            if cipher in (tr('Frequence analysis'), 'Scytale', 'Rail fence'):
                self.cipher_nb_key.setMinimum(1)
            elif cipher == 'Gronsfeld':
                self.cipher_nb_key.setRange(0, 10**9)
            else:
                self.cipher_nb_key.setRange(-2**16, 2**16)

            if cipher == tr('Frequence analysis'):
                key_label.setText(tr('Group :'))
            else:
                key_label.setText(tr('Key :'))


        #------path bar
        tab_cipher_lay.addWidget(self.create_path_bar(tab=2, mn_size=610), 0, 0, 1, -1)#, alignment=Qt.AlignTop)

        #------widgets
        #---text editor e
        self.txt_e = TextEditor(txt_height=120)
        self.lst_txt.append(self.txt_e) # used to reload when changing directory.
        tab_cipher_lay.addWidget(self.txt_e, 1, 0)


        #---keys
        keys_grp = QGroupBox()
        keys_lay = QGridLayout()
        keys_grp.setLayout(keys_lay)
        tab_cipher_lay.addWidget(keys_grp, 2, 0, 1, 2, alignment=Qt.AlignCenter)

        key_label = QLabel(tr('Key :'))
        keys_lay.addWidget(key_label, 0, 0)

        #-RSA keys' box
        self.cipher_opt_keys = QComboBox()
        self.cipher_opt_keys.setStyleSheet(self.style)
        self.cipher_opt_keys.setObjectName('sec_obj')
        self.cipher_opt_keys.setMinimumSize(200, 0)
        self.cipher_opt_keys.addItem(tr('-- Select a key --'))
        self.cipher_opt_keys.insertSeparator(1)
        self.cipher_opt_keys.addItems(RSA.list_keys('all'))
        keys_lay.addWidget(self.cipher_opt_keys, 0, 1)#, alignment=Qt.AlignLeft)

        #-Line edit key
        self.cipher_ledit_keys = QLineEdit()
        self.cipher_ledit_keys.setStyleSheet(self.style)
        self.cipher_ledit_keys.setObjectName('sec_obj')
        self.cipher_ledit_keys.setMinimumSize(200, 0)
        self.cipher_ledit_keys.setHidden(True)
        keys_lay.addWidget(self.cipher_ledit_keys, 0, 1)#, alignment=Qt.AlignLeft)

        #-Number key
        self.cipher_nb_key = QSpinBox()
        self.cipher_nb_key.setMinimum(-2**16)
        self.cipher_nb_key.setMaximum(2**16)
        self.cipher_nb_key.setStyleSheet(self.style)
        self.cipher_nb_key.setObjectName('sec_obj')
        self.cipher_nb_key.setMinimumSize(200, 0)
        self.cipher_nb_key.setHidden(True)
        keys_lay.addWidget(self.cipher_nb_key, 0, 1)#, alignment=Qt.AlignLeft)

        #-Double line edit
        self.cipher_db_ledit_key = DoubleInput()
        self.cipher_db_ledit_key.setStyleSheet(self.style)
        self.cipher_db_ledit_key.setObjectName('sec_obj')
        self.cipher_db_ledit_key.setMinimumSize(200, 0)
        self.cipher_db_ledit_key.setHidden(True)
        keys_lay.addWidget(self.cipher_db_ledit_key, 0, 1)#, alignment=Qt.AlignLeft)

        #-Double number key
        self.cipher_db_nb_key = DoubleInput(type_=QSpinBox)
        self.cipher_db_nb_key.setMinimum(-2**16)
        self.cipher_db_nb_key.setMaximum(2**16)
        self.cipher_db_nb_key.setStyleSheet(self.style)
        self.cipher_db_nb_key.setObjectName('sec_obj')
        self.cipher_db_nb_key.setMinimumSize(200, 0)
        self.cipher_db_nb_key.setHidden(True)
        keys_lay.addWidget(self.cipher_db_nb_key, 0, 1)#, alignment=Qt.AlignLeft)

        #-Buttons
        self.cipher_bt_enc = QPushButton('&Encrypt ↓')
        self.cipher_bt_enc.setStyleSheet(self.style)
        self.cipher_bt_enc.setObjectName('main_obj')
        self.cipher_bt_enc.setMaximumSize(90, 40)
        keys_lay.addWidget(self.cipher_bt_enc, 0, 2)#, alignment=Qt.AlignLeft)

        self.cipher_bt_dec = QPushButton('&Decrypt ↑')
        self.cipher_bt_dec.setStyleSheet(self.style)
        self.cipher_bt_dec.setObjectName('main_obj')
        self.cipher_bt_dec.setMaximumSize(90, 40)
        keys_lay.addWidget(self.cipher_bt_dec, 0, 3)#, alignment=Qt.AlignLeft)

        keys_lay.setColumnMinimumWidth(4, 20) #Spacing

        #-Alphabets' box
        self.cipher_opt_alf = QComboBox()
        self.cipher_opt_alf.setEditable(True)
        self.cipher_opt_alf.addItem(tr('-- Select an alphabet --'))
        self.cipher_opt_alf.insertSeparator(1)
        self.cipher_opt_alf.addItems(list(crypta_alf_list.values()))
        keys_lay.addWidget(self.cipher_opt_alf, 0, 5)

        keys_lay.setColumnMinimumWidth(6, 50) #Spacing

        #-Ciphers' box
        self.cipher_opt_ciphs = QComboBox()
        self.cipher_opt_ciphs.activated[str].connect(chk_ciph)
        self.cipher_opt_ciphs.addItem(tr('-- Select a cipher --'))
        for k in ciphers_list:
            self.cipher_opt_ciphs.insertSeparator(500)
            self.cipher_opt_ciphs.addItems(ciphers_list[k])
        keys_lay.addWidget(self.cipher_opt_ciphs, 0, 7)#, alignment=Qt.AlignLeft)


        #---text editor d
        self.txt_d = TextEditor(txt_height=125)
        #self.txt_d.setMaximumSize(10000, 450)
        self.lst_txt.append(self.txt_d) # used to reload when changing directory.
        tab_cipher_lay.addWidget(self.txt_d, 3, 0)


        #---buttons
        bt_lay = QVBoxLayout()
        tab_cipher_lay.addLayout(bt_lay, 1, 1, 1, -1, alignment=Qt.AlignTop)

        bt_lay.addWidget(QLabel('')) # Spacing

        bt_gen = QPushButton(tr('Generate keys'))
        bt_gen.setStyleSheet(self.style)
        bt_gen.setObjectName('orange_border_hover')
        bt_gen.clicked.connect(lambda: GenKeyWin.use(self.style, parent=self))
        bt_lay.addWidget(bt_gen, alignment=Qt.AlignRight)

        bt_exp = QPushButton(tr('Export public keys'))
        bt_exp.setStyleSheet(self.style)
        bt_exp.setObjectName('orange_border_hover')
        bt_exp.clicked.connect(lambda: ExpKeyWin.use(self.style, parent=self))
        bt_lay.addWidget(bt_exp, alignment=Qt.AlignRight)

        bt_info_k = QPushButton(tr('Show info about keys'))
        bt_info_k.setStyleSheet(self.style)
        bt_info_k.setObjectName('orange_border_hover')
        bt_info_k.clicked.connect(lambda: InfoKeyWin.use(self.style, parent=self))
        bt_lay.addWidget(bt_info_k, alignment=Qt.AlignRight)

        bt_rn_k = QPushButton(tr('Rename keys'))
        bt_rn_k.setStyleSheet(self.style)
        bt_rn_k.setObjectName('orange_border_hover')
        bt_rn_k.clicked.connect(lambda: RenKeyWin.use(self.style, parent=self))
        bt_lay.addWidget(bt_rn_k, alignment=Qt.AlignRight)

        bt_rn_k = QPushButton(tr('Convert keys'))
        bt_rn_k.setStyleSheet(self.style)
        bt_rn_k.setObjectName('orange_border_hover')
        bt_rn_k.clicked.connect(lambda: CvrtKeyWin.use(self.style, parent=self))
        bt_lay.addWidget(bt_rn_k, alignment=Qt.AlignRight)


        bt_quit = QPushButton(tr('&Quit'))
        bt_quit.setObjectName('bt_quit')
        bt_quit.setStyleSheet(self.style)
        bt_quit.setMaximumSize(QSize(50, 35))
        bt_quit.clicked.connect(self.quit)

        tab_cipher_lay.addWidget(bt_quit, 3, 1, alignment=Qt.AlignRight | Qt.AlignBottom)

        #------connection
        use_ciph = UseCipherTab(
            self.txt_e,
            self.txt_d,
            self.cipher_opt_keys,
            self.cipher_ledit_keys,
            self.cipher_nb_key,
            self.cipher_db_ledit_key,
            self.cipher_db_nb_key,
            self.cipher_opt_alf,
            self.cipher_opt_ciphs
        )

        self.cipher_bt_enc.clicked.connect(lambda: use_ciph.encrypt())
        self.cipher_bt_dec.clicked.connect(lambda: use_ciph.decrypt())


        #------show
        chk_ciph(tr('-- Select a cipher --'))

        self.app_widget.addTab(tab_cipher, tr('C&ipher'))



    #---------Create Wordlists tab
    def create_wordlists(self):
        '''Create the "Wordlists" tab.'''

        #------ini
        tab_wrdlst = QWidget()

        tab_wrdlst_lay = QGridLayout()
        tab_wrdlst_lay.setColumnStretch(0, 1)
        tab_wrdlst_lay.setContentsMargins(5, 5, 5, 5)
        tab_wrdlst.setLayout(tab_wrdlst_lay)

        #------path bar
        tab_wrdlst_lay.addWidget(self.create_path_bar(tab=3, mn_size=470), 0, 0, 1, -1)#, alignment=Qt.AlignTop)

        #------widgets
        #---generate
        #-ini
        gen_grp = QGroupBox(tr('Generate a wordlist'))
        gen_grp.setMinimumSize(730, 190)
        gen_lay = QGridLayout()
        gen_grp.setLayout(gen_lay)
        tab_wrdlst_lay.addWidget(gen_grp, 1, 0)

        gen_col_1 = QFormLayout()
        gen_col_1.setLabelAlignment(Qt.AlignLeft)
        gen_lay.addLayout(gen_col_1, 0, 0)

        #-spin box
        self.wrdlst_lth_sp = QSpinBox()
        self.wrdlst_lth_sp.setMaximum(50)
        self.wrdlst_lth_sp.setMinimum(1)
        self.wrdlst_lth_sp.setValue(5)
        self.wrdlst_lth_sp.setMaximumSize(50, 30)
        gen_col_1.addRow(tr("Words' length :"), self.wrdlst_lth_sp)

        #-alphabet
        self.wrdlst_alf_opt = QComboBox()
        #self.wrdlst_alf_opt.setMaximumSize(300, 35)
        self.wrdlst_alf_opt.setEditable(True)
        self.wrdlst_alf_opt.addItem(tr('-- Select an alphabet --'))
        self.wrdlst_alf_opt.insertSeparator(1)
        self.wrdlst_alf_opt.addItems(w_gen.alfs.values())
        gen_col_1.addRow(tr('Alphabet :'), self.wrdlst_alf_opt)

        #-filename
        self.wrdlst_fn_ledit = QLineEdit()
        self.wrdlst_fn_ledit.setMinimumSize(150, 0)
        self.wrdlst_fn_ledit.setMaximumSize(300, 35)
        gen_col_1.addRow(tr('Filename :'), self.wrdlst_fn_ledit)

        gen_lay.setColumnMinimumWidth(1, 50) #Spacing
        gen_lay.setColumnStretch(1, -1)

        gen_col_2 = QFormLayout()
        gen_col_2.setLabelAlignment(Qt.AlignLeft)
        gen_lay.addLayout(gen_col_2, 0, 2, Qt.AlignLeft) #todo: this don't work : when full screen, goes right

        #-encoding
        self.wrdlst_encod_opt = QComboBox()
        self.wrdlst_encod_opt.setMaximumSize(150, 30)
        self.wrdlst_encod_opt.addItems(lst_encod)
        gen_col_2.addRow(tr('Encoding :'), self.wrdlst_encod_opt)

        gen_col_2.setVerticalSpacing(40)

        #-save's location
        save_lay = QHBoxLayout()
        save_lay.setStretch(1, 1)

        self.wrdlst_dir_bt = QPushButton(tr('Select a location ...'))
        self.wrdlst_dir_bt.setMaximumSize(140, 32)
        self.wrdlst_dir_bt.clicked.connect(self.select_wrdlst)
        save_lay.addWidget(self.wrdlst_dir_bt)

        self.wrdlst_dir_opt = QComboBox()
        self.lst_wrdlst_opt[tr('Select a location ...')] = self.wrdlst_dir_opt
        self.wrdlst_dir_opt.addItem(tr('-- Previous locations --'))
        self.wrdlst_dir_opt.insertSeparator(1)
        save_lay.addWidget(self.wrdlst_dir_opt)

        gen_col_2.addRow(tr('Save in folder :'), save_lay)

        #-gen bt
        self.wrdlst_gen_bt = QPushButton(tr('&Generate'))
        self.wrdlst_gen_bt.setStyleSheet(self.style)
        self.wrdlst_gen_bt.setObjectName('main_obj')
        self.wrdlst_gen_bt.setMaximumSize(140, 32)
        gen_lay.addWidget(self.wrdlst_gen_bt, 1, 2, Qt.AlignRight | Qt.AlignBottom)


        #-Connection
        use_gen = UseWordlistsGenTab(
            self.wrdlst_lth_sp,
            self.wrdlst_alf_opt,
            self.wrdlst_fn_ledit,
            self.wrdlst_encod_opt,
            self.wrdlst_dir_opt
        )

        self.wrdlst_gen_bt.clicked.connect(lambda: use_gen.generate())

        self.wrdlst_lth_sp.valueChanged.connect(lambda: use_gen.set_name())
        self.wrdlst_alf_opt.activated[str].connect(lambda alf: use_gen.set_name(alf))

        #---Analyze
        #-ini
        ana_grp = QGroupBox(tr('Analyze a wordlist'))
        #ana_grp.setMinimumSize(730, 150)
        ana_lay = QGridLayout()
        ana_grp.setLayout(ana_lay)
        tab_wrdlst_lay.addWidget(ana_grp, 2, 0)

        select_lay = QHBoxLayout()
        ana_lay.addLayout(select_lay, 0, 0, 1, 3)

        #-bt select
        self.wrdlst_ana_select_bt = QPushButton(tr('Select a file ...'))
        self.wrdlst_ana_select_bt.setMaximumSize(110, 32)
        self.wrdlst_ana_select_bt.clicked.connect(self.select_wrdlst)
        select_lay.addWidget(self.wrdlst_ana_select_bt)

        #-opt previous loc
        self.wrdlst_ana_opt = QComboBox()
        self.lst_wrdlst_opt[tr('Select a file ...')] = self.wrdlst_ana_opt
        self.wrdlst_ana_opt.addItem(tr('-- Previous locations --'))
        self.wrdlst_ana_opt.insertSeparator(1)
        select_lay.addWidget(self.wrdlst_ana_opt)

        #-bt ana
        self.wrdlst_ana_bt = QPushButton(tr('&Analyze'))
        self.wrdlst_ana_bt.setStyleSheet(self.style)
        self.wrdlst_ana_bt.setObjectName('main_obj')
        self.wrdlst_ana_bt.setMaximumSize(110, 32)
        ana_lay.addWidget(self.wrdlst_ana_bt, 1, 2, Qt.AlignRight)

        #-lth spin box
        ana_lay.addWidget(QLabel(tr('Number of head / bottom lines :')), 1, 1, Qt.AlignLeft)

        self.wrdlst_ana_sp = QSpinBox()
        self.wrdlst_ana_sp.setMaximum(20) #todo: set this from the wordlist len / 2 if len/2 <= 20, 20 else.
        self.wrdlst_ana_sp.setMinimum(1)
        self.wrdlst_ana_sp.setValue(5)
        #self.wrdlst_ana_sp.setMaximumSize(50, 30)
        ana_lay.addWidget(self.wrdlst_ana_sp, 1, 1, Qt.AlignRight)

        #-txt ret
        self.wrdlst_ana_txt_ret = QTextEdit()
        self.wrdlst_ana_txt_ret.setReadOnly(True)
        self.wrdlst_ana_txt_ret.setMinimumSize(300, 150)
        self.wrdlst_ana_txt_ret.setMaximumSize(450, 10**6)
        self.wrdlst_ana_txt_ret.setStyleSheet(self.style)
        self.wrdlst_ana_txt_ret.setObjectName('orange_border_hover')
        ana_lay.addWidget(self.wrdlst_ana_txt_ret, 1, 0, 2, 1)

        #-txt show
        self.wrdlst_ana_txt_show = QTextEdit()
        self.wrdlst_ana_txt_show.setReadOnly(True)
        self.wrdlst_ana_txt_show.setMinimumSize(500, 150)
        self.wrdlst_ana_txt_show.setStyleSheet(self.style)
        self.wrdlst_ana_txt_show.setObjectName('orange_border_hover')
        ana_lay.addWidget(self.wrdlst_ana_txt_show, 2, 1, 1, 2)


        #-Connection
        use_ana = UseWordlistsAnaTab(
            self.wrdlst_ana_opt,
            self.wrdlst_ana_sp,
            self.wrdlst_ana_txt_ret,
            self.wrdlst_ana_txt_show
        )

        self.wrdlst_ana_bt.clicked.connect(lambda: use_ana.show())
        self.wrdlst_ana_sp.valueChanged.connect(lambda: use_ana.actualyze_ln())



        #------show
        self.app_widget.addTab(tab_wrdlst, '&Wordlists')



    #---------create prima tab
    def create_prima(self):
        '''Create the "Prima" tab.'''

        #------ini
        tab_prima = QWidget()

        tab_prima_lay = QGridLayout()
        tab_prima_lay.setColumnStretch(0, 1)
        tab_prima_lay.setContentsMargins(5, 5, 5, 5)
        tab_prima.setLayout(tab_prima_lay)

        #------path bar
        tab_prima_lay.addWidget(self.create_path_bar(tab=4, mn_size=550), 0, 0, 1, -1)

        #------widgets
        #---number
        self.prima_nb = TextEditor(820, 100, tr('Number :'))
        self.lst_txt.append(self.prima_nb) # used to reload when changing directory.
        tab_prima_lay.addWidget(self.prima_nb, 1, 0, 1, -1)

        tab_prima_lay.setRowMinimumHeight(2, 20) #Spacing

        #---algo
        algo_lay = QHBoxLayout()
        tab_prima_lay.addLayout(algo_lay, 3, 0)

        algo_lay.addWidget(QLabel(tr('Algorithm :')))

        self.prima_algo_opt = QComboBox()
        self.prima_algo_opt.setMaximumSize(400, 35)
        self.prima_algo_opt.addItem(tr('-- Select an algorithm --'))
        for k in prima_algo_list:
            self.prima_algo_opt.insertSeparator(500)
            self.prima_algo_opt.addItems(prima_algo_list[k])
        algo_lay.addWidget(self.prima_algo_opt, Qt.AlignLeft)

        #-calc bt
        self.prima_calc_bt = QPushButton(tr('C&alculate'))
        self.prima_calc_bt.setStyleSheet(self.style)
        self.prima_calc_bt.setObjectName('main_obj')
        tab_prima_lay.addWidget(self.prima_calc_bt, 4, 2)

        #-ret
        tab_prima_lay.setColumnStretch(3, 1)

        self.prima_ret = QTextEdit()
        self.prima_ret.setReadOnly(True)
        self.prima_ret.setMinimumSize(500, 150)
        self.prima_ret.setStyleSheet(self.style)
        self.prima_ret.setObjectName('orange_border_hover')
        tab_prima_lay.addWidget(self.prima_ret, 3, 3, 3, -1)


        #------connection
        use_prima = UsePrimaTab(self.prima_nb, self.prima_algo_opt, self.prima_ret)
        self.prima_calc_bt.clicked.connect(lambda: use_prima.calc())



        #------show
        self.app_widget.addTab(tab_prima, '&Prima')



    #---------create b_cvrt tab
    def create_b_cvrt(self):
        '''Create the "Base convert" tab.'''

        #------ini
        tab_b_cvrt = QWidget()

        tab_b_cvrt_lay = QGridLayout()
        tab_b_cvrt_lay.setColumnStretch(0, 1)
        tab_b_cvrt_lay.setContentsMargins(5, 5, 5, 5)
        tab_b_cvrt.setLayout(tab_b_cvrt_lay)

        #------check functions
        def chk_nb(nb):
            self.b_cvrt_n.setDisplayIntegerBase(nb)
            chk_ieee754()

        def chk_big_n():
            self.b_cvrt_n.setDisabled(self.b_cvrt_n_big_chk.isChecked())
            self.b_cvrt_n_big.setDisabled(not self.b_cvrt_n_big_chk.isChecked())

        def chk_alf(alf):
            '''Activated when alf is changed. Change the maximum of nb and b.'''

            spin_box = {'nb': self.b_cvrt_nb, 'b': self.b_cvrt_b}[self.sender().objectName()]
            spin_box.setMaximum(len(alf)) #Choose the spin box that correspond to the alphabet selector..

            if len(alf) > 36:
                if alf[:36] != b_cvrt_alf_list['alf_base36']:
                    self.b_cvrt_n_big_chk.setDisabled(True)
                    self.b_cvrt_n_big_chk.setChecked(True)
                    chk_big_n()

            else:
                self.b_cvrt_n_big_chk.setDisabled(False)
                self.b_cvrt_n_big_chk.setChecked(False)
                chk_big_n()

        def chk_ieee754():
            '''Check if the IEEE754 check box is checked, and activate or not n or n_big.'''

            if self.b_cvrt_ieee754.isChecked() and self.b_cvrt_nb.value() == 2:
                self.b_cvrt_n_big_chk.setDisabled(True)
                self.b_cvrt_n_big_chk.setChecked(True)
                chk_big_n()

            else:
                self.b_cvrt_n_big_chk.setDisabled(False)
                chk_big_n()


        alf_count = 7
        def chk_alf_share(index):
            '''
            Activated when alf combo box's index change.
            Check if there is a new item, and if so, add it to the other combo box.
            '''

            nonlocal alf_count

            sender = self.sender()

            if sender.count() > alf_count:
                alf_count = sender.count()

                try:
                    if sender is self.b_cvrt_opt_alf:
                        self.b_cvrt_opt_alf_b.addItem(sender.itemText(alf_count - 1))

                    else:
                        self.b_cvrt_opt_alf.addItem(sender.itemText(alf_count - 1))

                except AttributeError:
                    pass


        #------widgets
        #---auto convert
        self.b_cvrt_chk_auto = QCheckBox('Auto convert')
        tab_b_cvrt_lay.addWidget(self.b_cvrt_chk_auto, 0, 0, Qt.AlignRight | Qt.AlignTop)

        #---nb
        nb_lay = QFormLayout()
        nb_lay.setLabelAlignment(Qt.AlignLeft)
        tab_b_cvrt_lay.addLayout(nb_lay, 0, 0)

        #-n
        self.b_cvrt_n = QSpinBox()
        self.b_cvrt_n.setMinimumSize(280, 0)
        self.b_cvrt_n.setMinimum(-(2**31-1))
        self.b_cvrt_n.setMaximum(2**31-1)
        nb_lay.addRow('Number to convert :', self.b_cvrt_n)


        big_n_lay = QHBoxLayout()
        self.b_cvrt_n_big = QLineEdit()
        self.b_cvrt_n_big.setText('0')
        big_n_lay.addWidget(self.b_cvrt_n_big)

        self.b_cvrt_n_big_chk = QCheckBox('Number bigger than 2^31-1, smaller than -(2^31-1), or floating')
        self.b_cvrt_n_big_chk.toggled.connect(chk_big_n)
        big_n_lay.addWidget(self.b_cvrt_n_big_chk)

        nb_lay.addRow('', big_n_lay)

        #-nb and alf
        nb_alf_lay = QHBoxLayout()
        nb_lay.addRow("Number's base :", nb_alf_lay)

        #nb
        self.b_cvrt_nb = QSpinBox()
        self.b_cvrt_nb.setMaximumSize(55, 35)
        self.b_cvrt_nb.setMinimum(1)
        self.b_cvrt_nb.setMaximum(10)
        self.b_cvrt_nb.setValue(10)
        self.b_cvrt_nb.valueChanged.connect(chk_nb)
        nb_alf_lay.addWidget(self.b_cvrt_nb)
        nb_alf_lay.addWidget(QLabel(' '*5))

        #alf (in the same row that nb, but align right)
        self.b_cvrt_opt_alf = QComboBox()
        self.b_cvrt_opt_alf.setObjectName('nb')
        self.b_cvrt_opt_alf.setEditable(True)
        self.b_cvrt_opt_alf.activated[str].connect(chk_alf)
        self.b_cvrt_opt_alf.currentIndexChanged.connect(chk_alf_share)
        #self.b_cvrt_opt_alf.currentIndexChanged.connect(lambda x: print(x, self.b_cvrt_opt_alf.itemText(x)))
        self.b_cvrt_opt_alf.addItems([alf for alf in list(b_cvrt_alf_list.values())])
        nb_alf_lay.addWidget(self.b_cvrt_opt_alf, Qt.AlignRight)

        #-b and alf_b
        nb_alf_b_lay = QHBoxLayout()
        nb_lay.addRow("Return base :", nb_alf_b_lay)

        #-b
        self.b_cvrt_b = QSpinBox()
        self.b_cvrt_b.setMaximumSize(55, 35)
        self.b_cvrt_b.setMinimum(1)
        self.b_cvrt_b.setMaximum(10)
        self.b_cvrt_b.setValue(2)
        nb_alf_b_lay.addWidget(self.b_cvrt_b)
        nb_alf_b_lay.addWidget(QLabel(' '*5))

        #alf_b
        self.b_cvrt_opt_alf_b = QComboBox()
        self.b_cvrt_opt_alf_b.setObjectName('b')
        self.b_cvrt_opt_alf_b.setEditable(True)
        self.b_cvrt_opt_alf_b.activated[str].connect(chk_alf)
        self.b_cvrt_opt_alf_b.currentIndexChanged.connect(chk_alf_share)
        self.b_cvrt_opt_alf_b.addItems([alf for alf in list(b_cvrt_alf_list.values())])
        nb_alf_b_lay.addWidget(self.b_cvrt_opt_alf_b, Qt.AlignRight)

        #---check boxes
        chk_box_lay = QVBoxLayout()
        tab_b_cvrt_lay.addLayout(chk_box_lay, 1, 0, Qt.AlignCenter)

        self.b_cvrt_2_2 = QCheckBox("Encoded negatively with the two's complement standard")
        chk_box_lay.addWidget(self.b_cvrt_2_2, Qt.AlignLeft)

        self.b_cvrt_ieee754 = QCheckBox('Encoded with the standard IEEE754')
        self.b_cvrt_ieee754.toggled.connect(chk_ieee754)
        chk_box_lay.addWidget(self.b_cvrt_ieee754, Qt.AlignLeft)

        #---ret
        self.b_cvrt_ret = QTextEdit()
        self.b_cvrt_ret.setReadOnly(True)
        self.b_cvrt_ret.setMinimumSize(400, 100)
        self.b_cvrt_ret.setStyleSheet(self.style)
        self.b_cvrt_ret.setObjectName('orange_border_hover')
        tab_b_cvrt_lay.addWidget(self.b_cvrt_ret, 3, 0)

        #---Convert button
        self.b_cvrt_bt_c = QPushButton('Convert')
        self.b_cvrt_bt_c.setStyleSheet(self.style)
        self.b_cvrt_bt_c.setObjectName('main_obj')
        tab_b_cvrt_lay.addWidget(self.b_cvrt_bt_c, 3, 0, -1, -1, Qt.AlignRight | Qt.AlignBottom)


        #------connection
        use_b_cvrt = UseBaseConvertTab(self.b_cvrt_n, self.b_cvrt_n_big, \
            self.b_cvrt_nb, self.b_cvrt_b, self.b_cvrt_opt_alf, self.b_cvrt_opt_alf_b, self.b_cvrt_2_2, \
            self.b_cvrt_ieee754, self.b_cvrt_n_big_chk, self.b_cvrt_chk_auto, self.b_cvrt_ret)

        self.b_cvrt_bt_c.clicked.connect(lambda: use_b_cvrt.convert(sender='bt'))

        self.b_cvrt_n.valueChanged.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_n_big.textChanged.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_n_big_chk.toggled.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_nb.valueChanged.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_b.valueChanged.connect(lambda: use_b_cvrt.convert())

        self.b_cvrt_opt_alf.currentIndexChanged.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_opt_alf_b.currentIndexChanged.connect(lambda: use_b_cvrt.convert())

        self.b_cvrt_2_2.toggled.connect(lambda: use_b_cvrt.convert())
        self.b_cvrt_ieee754.toggled.connect(lambda: use_b_cvrt.convert())


        #------show
        chk_big_n()
        self.app_widget.addTab(tab_b_cvrt, '&Base convert')



    def create_pwd_strth(self):
        '''Create the "P@ssw0rd_Test0r" tab.'''

        #------ini
        tab_pwd_t = QWidget()

        tab_pwd_t_lay = QGridLayout()
        tab_pwd_t_lay.setContentsMargins(5, 5, 5, 5)
        tab_pwd_t.setLayout(tab_pwd_t_lay)

        #------functions
        #---chk
        def chk_show():
            if self.pwd_t_show.isChecked():
                self.pwd_t_inp.setEchoMode(QLineEdit.Normal)

            else:
                self.pwd_t_inp.setEchoMode(QLineEdit.Password)

        #---get_strth_
        def get_sth_():
            if self.pwd_t_inp.text() == '':
                self.pwd_t_ret.setPlainText('')

            elif self.pwd_t_show.isChecked():
                self.pwd_t_ret.setPlainText(tr('Return for') + ' "' + \
                    self.pwd_t_inp.text() + '"\n' + pwd_testor.get_sth(self.pwd_t_inp.text()))

            else:
                self.pwd_t_ret.setPlainText(tr('Return for') + ' "' + \
                    '*'*len(self.pwd_t_inp.text()) + '"\n' + pwd_testor.get_sth(self.pwd_t_inp.text()))

        #------widgets
        #---label
        tab_pwd_t_lay.addWidget(QLabel(tr('Enter the password to try :')), 0, 0)

        #---pwd_entry
        self.pwd_t_inp = QLineEdit()
        self.pwd_t_inp.setMinimumSize(300, 0)
        self.pwd_t_inp.setEchoMode(QLineEdit.Password) # don't print pwd
        self.pwd_t_inp.returnPressed.connect(get_sth_) # Don't need to press the button : press <enter>
        tab_pwd_t_lay.addWidget(self.pwd_t_inp, 0, 1)

        #---check box
        self.pwd_t_show = QCheckBox(tr('Show password'))
        self.pwd_t_show.toggled.connect(chk_show)
        tab_pwd_t_lay.addWidget(self.pwd_t_show, 1, 0, 1, 2, Qt.AlignCenter | Qt.AlignTop)

        #---button
        self.pwd_t_bt_get = QPushButton(tr('Get strenth'))
        self.pwd_t_bt_get.setStyleSheet(self.style)
        self.pwd_t_bt_get.setObjectName('main_obj')
        self.pwd_t_bt_get.clicked.connect(get_sth_)
        tab_pwd_t_lay.addWidget(self.pwd_t_bt_get, 0, 2)

        #---ret
        self.pwd_t_ret = QTextEdit()
        self.pwd_t_ret.setReadOnly(True)
        self.pwd_t_ret.setMinimumSize(400, 100)
        self.pwd_t_ret.setStyleSheet(self.style)
        self.pwd_t_ret.setObjectName('orange_border_hover')
        tab_pwd_t_lay.addWidget(self.pwd_t_ret, 2, 0, -1, -1)



        #------show
        self.app_widget.addTab(tab_pwd_t, 'P@&ssw0rd_Test0r')



    def create_anamer0(self):
        '''Create the "Anamer0" tab.'''

        #------ini
        tab_anamer0 = QWidget()

        tab_anamer0_lay = QGridLayout()
        tab_anamer0_lay.setContentsMargins(5, 5, 5, 5)
        tab_anamer0.setLayout(tab_anamer0_lay)

        #------functions
        #---get_strth_
        def get_info():
            if self.anamer0_inp.text() == '':
                self.anamer0_ret.setPlainText('')

            else:
                self.anamer0_ret.setPlainText(
                    anamer0.use(self.anamer0_inp.text().split(','))
                )

        #------widgets
        #---label
        tab_anamer0_lay.addWidget(QLabel(tr('Enter french phone number(s) ("," between) :')), 0, 0)

        #---pwd_entry
        self.anamer0_inp = QLineEdit()
        self.anamer0_inp.setMinimumSize(300, 0)
        self.anamer0_inp.returnPressed.connect(get_info) # Don't need to press the button : press <enter>
        tab_anamer0_lay.addWidget(self.anamer0_inp, 0, 1)

        #---button
        self.anamer0_bt_get = QPushButton(tr('Get infos'))
        self.anamer0_bt_get.setStyleSheet(self.style)
        self.anamer0_bt_get.setObjectName('main_obj')
        self.anamer0_bt_get.clicked.connect(get_info)
        tab_anamer0_lay.addWidget(self.anamer0_bt_get, 0, 2)

        #---ret
        self.anamer0_ret = QTextEdit()
        self.anamer0_ret.setReadOnly(True)
        self.anamer0_ret.setMinimumSize(400, 100)
        self.anamer0_ret.setStyleSheet(self.style)
        self.anamer0_ret.setObjectName('orange_border_hover')
        tab_anamer0_lay.addWidget(self.anamer0_ret, 2, 0, -1, -1)



        #------show
        self.app_widget.addTab(tab_anamer0, 'Ana&mer0')



    def create_settings(self):
        '''Create the "Settings" tab.'''

        #------ini
        tab_stng = QWidget()

        tab_stng_lay = QGridLayout()
        tab_stng_lay.setContentsMargins(5, 5, 5, 5)
        tab_stng.setLayout(tab_stng_lay)

        #------widgets
        #---main style
        #-ini
        self.style_grp = QGroupBox('Syle')
        self.style_grp.setMaximumSize(500, 100)
        #self.style_grp.setMinimumSize(500, 200)
        main_style_lay = QHBoxLayout()
        self.style_grp.setLayout(main_style_lay)
        tab_stng_lay.addWidget(self.style_grp, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        self.main_style_palette = QApplication.palette()

        #-combo box
        main_style_lay.addWidget(QLabel('Style :'))

        self.stng_main_style_opt = QComboBox()
        self.stng_main_style_opt.addItems(self.app_style.main_styles)
        self.stng_main_style_opt.activated[str].connect(
            lambda s: self.app_style.set_style(s, self.main_style_std_chkb.isChecked())
        )
        self.stng_main_style_opt.setCurrentText(self.app_style.main_style_name)
        main_style_lay.addWidget(self.stng_main_style_opt)

        #-check box
        self.main_style_std_chkb = QCheckBox("&Use style's standard palette")
        self.main_style_std_chkb.setChecked(True)
        self.main_style_std_chkb.toggled.connect(
            lambda: self.app_style.set_style(
                self.stng_main_style_opt.currentText(),
                self.main_style_std_chkb.isChecked()
            )
        )
        main_style_lay.addWidget(self.main_style_std_chkb)


        #---change password
        #-chk function
        def chk_pwd_shown():
            '''Actualise if the password needs to be shown.'''

            for k in dct_cb:
                if k.isChecked():
                    dct_cb[k].setEchoMode(QLineEdit.Normal)

                else:
                    dct_cb[k].setEchoMode(QLineEdit.Password)

        #-ini
        self.stng_pwd_grp = QGroupBox('Change password')
        self.stng_pwd_grp.setMaximumSize(600, 200)
        self.stng_pwd_grp.setMinimumSize(500, 200)
        stng_pwd_lay = QGridLayout()
        self.stng_pwd_grp.setLayout(stng_pwd_lay)

        tab_stng_lay.addWidget(self.stng_pwd_grp, 0, 1, 2, 1)#, Qt.AlignRight)

        #-form widgets (ask for pwd)
        stng_pwd_form_lay = QFormLayout()
        stng_pwd_lay.addLayout(stng_pwd_form_lay, 0, 0)

        self.stng_old_pwd = QLineEdit()
        self.stng_old_pwd.setMinimumSize(250, 0)
        self.stng_old_pwd.setEchoMode(QLineEdit.Password) # don't print pwd
        stng_pwd_form_lay.addRow('Old password :', self.stng_old_pwd)

        self.stng_pwd1 = QLineEdit()
        self.stng_pwd1.setMinimumSize(250, 0)
        self.stng_pwd1.setEchoMode(QLineEdit.Password) # don't print pwd
        stng_pwd_form_lay.addRow('New password :', self.stng_pwd1)

        self.stng_pwd2 = QLineEdit()
        self.stng_pwd2.setMinimumSize(250, 0)
        self.stng_pwd2.setEchoMode(QLineEdit.Password) # don't print pwd
        stng_pwd_form_lay.addRow('Verify :', self.stng_pwd2)

        #-checkbox widgets (show pwd)
        stng_pwd_cb_lay = QVBoxLayout()
        stng_pwd_cb_lay.setSpacing(15)
        stng_pwd_lay.addLayout(stng_pwd_cb_lay, 0, 1)

        self.stng_old_pwd_cb = QCheckBox()
        stng_pwd_cb_lay.addWidget(self.stng_old_pwd_cb)
        self.stng_old_pwd_cb.toggled.connect(chk_pwd_shown)

        self.stng_pwd1_cb = QCheckBox()
        stng_pwd_cb_lay.addWidget(self.stng_pwd1_cb)
        self.stng_pwd1_cb.toggled.connect(chk_pwd_shown)

        self.stng_pwd2_cb = QCheckBox()
        stng_pwd_cb_lay.addWidget(self.stng_pwd2_cb)
        self.stng_pwd2_cb.toggled.connect(chk_pwd_shown)

        dct_cb = {
            self.stng_old_pwd_cb: self.stng_old_pwd,
            self.stng_pwd1_cb: self.stng_pwd1,
            self.stng_pwd2_cb: self.stng_pwd2
        }

        #-button
        self.stng_pwd_bt = QPushButton('Change password')
        stng_pwd_lay.addWidget(self.stng_pwd_bt, 1, 1, Qt.AlignRight)

        #-connection
        use_c_pwd = UseSettingsTab(self.stng_old_pwd, self.stng_pwd1, self.stng_pwd2)

        self.stng_pwd_bt.clicked.connect(lambda: use_c_pwd.change_pwd())
        self.stng_pwd2.returnPressed.connect(lambda: use_c_pwd.change_pwd())


        #---Change language
        #-function
        def chg_lang():
            '''
            Changing the language (in the text file). The user need to
            close the app and relaunch it manually to apply the new lang.
            '''

            new_lang = self.stng_lang_box.currentText()

            #---test
            if new_lang == lang:
                return -3

            #---write
            with open('Data/lang.txt', 'w') as f:
                f.write(new_lang)

            #---close
            rep = QMessageBox.question(
                None, 'Done !',
                '<h2>The new lang will apply the next time you launch Cracker.</h2>\n<h2>Quit now ?</h2>',
                QMessageBox.No | QMessageBox.Yes,
                QMessageBox.Yes
            )

            if rep == QMessageBox.Yes:
                self.quit()


        #-ini
        self.stng_lang_grp = QGroupBox('Change Language')
        self.stng_lang_grp.setMaximumSize(200, 130)
        # self.stng_lang_grp.setMinimumSize(500, 200)
        stng_lang_lay = QGridLayout()
        self.stng_lang_grp.setLayout(stng_lang_lay)

        tab_stng_lay.addWidget(self.stng_lang_grp, 1, 0)#, Qt.AlignRight)

        #-Langs combo box
        self.stng_lang_box = QComboBox()
        self.stng_lang_box.setMaximumWidth(50)
        self.stng_lang_box.addItems(langs_lst)
        self.stng_lang_box.setCurrentText(lang)
        stng_lang_lay.addWidget(self.stng_lang_box, 0, 0, Qt.AlignLeft)

        #-Button
        self.stng_lang_bt = QPushButton('Apply')
        stng_lang_lay.addWidget(self.stng_lang_bt, 1, 0, Qt.AlignRight)
        self.stng_lang_bt.clicked.connect(chg_lang)

        #------show
        self.app_widget.addTab(tab_stng, 'Setti&ngs')



    #---------Path bar
    def create_path_bar(self, tab, mn_size=700):
        '''Return a QWidget containing a path bar.

        tab : the tab containing the bar 's index.
        '''

        #------ini
        path_bar = QGroupBox()
        path_bar.setObjectName('path_grp')
        path_bar.setStyleSheet(self.style)
        path_bar.setMaximumSize(QSize(7000, 60))

        path_bar_lay = QGridLayout()
        path_bar_lay.setContentsMargins(5, 5, 5, 5)
        path_bar.setLayout(path_bar_lay)

        #------widgets
        path_bar_lay.addWidget(QLabel(tr('Current directory :')), 0 ,0)

        self.path_ent[tab] = QLineEdit()
        self.path_ent[tab].setObjectName('path_entry')
        self.path_ent[tab].setStyleSheet(self.style)
        self.path_ent[tab].setMinimumSize(QSize(mn_size, 20))
        self.path_ent[tab].setText(getcwd())
        self.path_ent[tab].returnPressed.connect(self.change_dir) # Don't need to press the button : press <enter>
        path_bar_lay.addWidget(self.path_ent[tab], 0, 1)

        bt_up = QPushButton('↑')
        bt_up.setMaximumSize(QSize(40, 50))
        bt_up.clicked.connect(self.change_dir_up)
        bt_up.setObjectName('path_bt')
        bt_up.setStyleSheet(self.style)
        path_bar_lay.addWidget(bt_up, 0, 2)

        bt_apply = QPushButton(tr('Apply'))
        bt_apply.clicked.connect(self.change_dir)
        bt_apply.setObjectName('path_bt')
        bt_apply.setStyleSheet(self.style)
        path_bar_lay.addWidget(bt_apply, 0, 3)

        bt_gui = QPushButton(tr('Search'))
        bt_gui.clicked.connect(self.change_dir)
        bt_gui.setObjectName('path_bt')
        bt_gui.setStyleSheet(self.style)
        bt_gui.clicked.connect(self.change_dir_gui)
        path_bar_lay.addWidget(bt_gui, 0, 4)

        return path_bar

    #---------chdir
    def change_dir(self):
        '''Change the current directory according to the path bar'''

        new_dir = self.path_ent[self.app_widget.currentIndex()].text()

        try:
            chdir(new_dir)

        except FileNotFoundError:
            self.path_ent[self.app_widget.currentIndex()].setText(getcwd())
            QMessageBox.about(QWidget(), tr('!!! Directory error !!!'), tr('The directory was NOT found !!!'))
            return False

        for tab in range(5):
            self.path_ent[tab].setText(getcwd()) #actualise every path bar.

        for text_editor in self.lst_txt:
            text_editor.reload() #Reload TextEditors' ComboBox.

        self.reload_keys()


    def change_dir_up(self):
        '''Change the current directory up'''

        chdir('..')
        for tab in range(5):
            self.path_ent[tab].setText(getcwd()) #actualise every path bar.

        for text_editor in self.lst_txt:
            text_editor.reload() #Reload TextEditors' ComboBox.

        self.reload_keys()


    def change_dir_gui(self):
        '''Change the current directory by asking to the user with a popup'''


        new_dir = QFileDialog.getExistingDirectory(self, tr('Select directory'))

        if new_dir:
            try:
                chdir(new_dir)

            except FileNotFoundError:
                self.path_ent[self.app_widget.currentIndex()].setText(getcwd())
                QMessageBox.about(QWidget(), tr('!!! Directory error !!!'), tr('The directory was NOT found !!!'))
                return False

            for tab in range(5):
                self.path_ent[tab].setText(getcwd()) #actualise every path bar.

            for text_editor in self.lst_txt:
                text_editor.reload() #Reload TextEditors' ComboBox.

            self.reload_keys()



    def reload_keys(self):
        '''Reload the RSA keys's box, in the cipher tab.'''

        old_key = self.cipher_opt_keys.currentText()

        keys_list = RSA.list_keys('all')

        self.cipher_opt_keys.clear()

        self.cipher_opt_keys.addItem(tr('-- Select a key --'))
        self.cipher_opt_keys.insertSeparator(1)
        self.cipher_opt_keys.addItems(keys_list)

        if old_key in keys_list:
            self.cipher_opt_keys.setCurrentText(old_key)



    #---------select wordlist
    def select_wrdlst(self):
        '''Open a popup asking for a wordlist file.'''

        tab = self.app_widget.currentIndex()
        sender = self.sender().text()

        if sender in (tr('Select a wordlist ...'), tr('Select a file ...')): #Crack, Wordlists ana
            fn = QFileDialog.getOpenFileName(self, tr('Open file'), getcwd())[0]

        elif sender == tr('Select a location ...'): #Wordlists gen
            fn = QFileDialog.getExistingDirectory(self, tr('Select directory'))


        if fn in ((), ''):
            return -3 # Canceled

        if fn not in self.lst_selected_wrdlst[sender]:
            self.lst_selected_wrdlst[sender].append(fn)

            if sender == tr('Select a location ...'):
                self.lst_wrdlst_opt[sender].addItem(fn)

            else:
                for k in (tr('Select a wordlist ...'), tr('Select a file ...')):
                    self.lst_wrdlst_opt[k].addItem(fn)

        self.lst_wrdlst_opt[sender].setCurrentText(fn)



    #---------chk_tab
    def chk_tab(self, tab):
        '''Resize the window according to the tab.'''

        self.current_tab = tab

        if tab == 0: #Home
            self.setMinimumSize(1090, 400)
            self.resize(1090, 400)

        elif tab == 1: #Crack
            self.setMinimumSize(1090, 600)
            self.resize(1090, 600)

        elif tab == 2: #Cipher
            self.setMinimumSize(1030, 730)
            self.resize(1030, 730)
            self.reload_keys()

        elif tab == 3: #Wordlists
            self.setMinimumSize(900, 560)
            self.resize(900, 560)

        elif tab == 4: #Prima
            self.setMinimumSize(950, 500)
            self.resize(950, 500)

        elif tab == 5: #Base convert
            self.setMinimumSize(800, 400)
            self.resize(750, 350)

        elif tab == 6: #P@ssw0rd_Test0r
            self.setMinimumSize(800, 500)
            self.resize(800, 500)

        elif tab == 7: #Anamer0
            self.setMinimumSize(800, 500)
            self.resize(800, 500)

        elif tab == 8: #Settings
            self.setMinimumSize(900, 250)
            self.resize(900, 250)


    #---------start_calc
    def start_calc(self):
        '''Start a calculator program.'''

        self.calc = Calc()
        self.calc.show()



    #---------infos
    def show_infos(self):
        '''Show information about this program using a popup.'''

        AboutCracker.use(parent=self)



    #---------lock
    def lock(self, tries=5):
        '''Dislable the widgets and ask for the password.'''

        if tries == False:
            tries = 5

        def chk_lock():
            if not self.locker.is_locked():
                self.setDisabled(False)

                global RSA_keys_pwd
                RSA_keys_pwd = self.locker.get_RSA_keys_pwd()

                RSA.SecureRsaKeys(RSA_keys_pwd, interface='gui').decrypt()

        self.locker = Lock(pwd, pwd_h, pwd_loop, tries)

        self.setDisabled(True)
        self.locker.show()

        self.locker.connect(chk_lock)



    #---------quit
    def quit(self, event=None):
        '''Quit the application. Check if there is text somewhere, and ask confirmation if there is.'''

        global app

        txt_ = False
        txt_tab = []
        if self.txt_crack.getText(silent=True, from_='text') != '':
            txt_ = True
            txt_tab.append('Crack')

        if self.txt_e.getText(silent=True, from_='text') != '':
            txt_ = True
            txt_tab.append('Cipher (encrypt)')

        if self.txt_d.getText(silent=True, from_='text') != '':
            txt_ = True
            txt_tab.append('Cipher (decrypt)')

        if self.prima_nb.getText(silent=True, from_='text') != '':
            txt_ = True
            txt_tab.append('Prima')


        if txt_:
            if len(txt_tab) == 1:
                title = '!!! There is text in ' + set_prompt(txt_tab) + ' tab !!!'
                msg = '<h2>The text widget in the ' + set_prompt(txt_tab) + \
                ' tab is not empty !</h2>\n<h4>Your text will be lose if not saved !</h4>\nQuit anyway ?'

            else:
                title = '!!! There is text in some tabs !!!'
                msg = '<h2>The text widgets in the ' + set_prompt(txt_tab) + \
                ' tabs is not empty !</h2>\n<h4>Your text will be lose if not saved !</h4>\nQuit anyway ?'


            sure = QMessageBox.question(self, title, msg, \
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if sure == QMessageBox.No:
                if event not in (None, True, False):
                    event.ignore()
                return -3

        if event not in (None, True, False):
            RSA.SecureRsaKeys(RSA_keys_pwd, 'gui').rm_clear()
            event.accept()

        else:
            RSA.SecureRsaKeys(RSA_keys_pwd, 'gui').rm_clear()
            app.quit()
            #todo: use app.close() ? what differences ?


    def closeEvent(self, event=None):
        self.quit(event)



    #---------use
    def use(lock=True):
        '''Launch the application.'''

        global app, win

        app = QApplication(sys.argv)
        win = CrackerGui()

        #-lock
        if lock:
            win.lock(3)

        #app.setPalette(CrackerGuiStyle.dark_style(None))
        #app.aboutToQuit.connect(win.quit)

        sys.exit(app.exec_())



##-Ciphers' keys management
#---------Generate RSA keys
class GenKeyWin(QMainWindow):
    '''Class which define a window which allow to generate RSA keys.'''

    def __init__(self, style, parent=None):
        '''Initiate the GenKeyWin window.'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Generate RSA keys — Cracker')

        #---Central widget
        self.main_wid = QWidget()
        self.setCentralWidget(self.main_wid)

        main_lay = QGridLayout()
        self.main_wid.setLayout(main_lay)

        #------Main chooser
        self.cipher_box = QComboBox()
        self.cipher_box.setMaximumSize(150, 35)
        self.cipher_box.activated[str].connect(self._chk)
        self.cipher_box.addItems([tr('-- Select a cipher --'), 'RSA', 'AES-256', 'AES-192', 'AES-128'])
        self.cipher_box.insertSeparator(1)
        self.cipher_box.insertSeparator(3)
        for k in (
        crypta.ciph_sort['1_key_str'],
        crypta.ciph_sort['1_key_int'],
        crypta.ciph_sort['1_key_list'],
        crypta.ciph_sort['2_key_int'],
        crypta.ciph_sort['2_key_str']
        ):
            self.cipher_box.insertSeparator(500)
            self.cipher_box.addItems(k)
        main_lay.addWidget(self.cipher_box, 0, 0)

        #------RSA keys
        self.RSA_wid = QWidget() #QGroupBox('Generate RSA keys')
        main_lay.addWidget(self.RSA_wid, 1, 0)

        RSA_lay = QGridLayout()
        self.RSA_wid.setLayout(RSA_lay)

        #---label
        RSA_lay.addWidget(QLabel("Keys' size :"), 0, 0)

        #---Slider
        self.slider_sz = QSlider(Qt.Horizontal)
        self.slider_sz.setMinimumSize(250, 0)
        self.slider_sz.setMinimum(512)
        self.slider_sz.setMaximum(5120)
        self.slider_sz.setSingleStep(512)
        self.slider_sz.setTickInterval(512)
        self.slider_sz.setTickPosition(QSlider.TicksBelow)

        self.slider_sz.setValue(2048)

        RSA_lay.addWidget(self.slider_sz, 0, 1)

        #---QSpinBox
        self.sb = QSpinBox()
        self.sb.setMaximumSize(70, 35)
        self.sb.setMinimum(512)
        self.sb.setMaximum(5120)
        self.sb.setSingleStep(512)
        self.sb.setValue(2048)

        RSA_lay.addWidget(self.sb, 0, 2)

        #-connection
        self.slider_sz.valueChanged.connect(lambda v: self.sb.setValue(v))
        self.sb.valueChanged.connect(lambda v: self.slider_sz.setValue(v))

        #---name label
        RSA_lay.addWidget(QLabel("Keys' name :"), 1, 0)

        #---line edit
        self.ledt = QLineEdit()
        self.ledt.setMinimumSize(250, 0)
        self.ledt.returnPressed.connect(self.gen)
        RSA_lay.addWidget(self.ledt, 1, 1)

        #---check box hexa
        self.chbt_h = QCheckBox('Store in hexadecimal')
        self.chbt_h.setChecked(True)
        RSA_lay.addWidget(self.chbt_h, 1, 2)


        #------One int arg (Label - QSpinBox)
        #---ini
        self.sp_wid = QWidget() #QGroupBox('Generate string key')
        main_lay.addWidget(self.sp_wid, 1, 0)

        sp_lay = QGridLayout()
        self.sp_wid.setLayout(sp_lay)

        #---widgets
        self.sp_lb = QLabel("Key's length :")
        sp_lay.addWidget(self.sp_lb, 0, 0)

        self.str1_lth = QSpinBox()
        self.str1_lth.setValue(15)
        self.str1_lth.setMinimumSize(150, 35)
        sp_lay.addWidget(self.str1_lth, 0, 1)


        #------Two int args
        #---ini
        self.int2_wid = QWidget() #QGroupBox('Generate string key')
        main_lay.addWidget(self.int2_wid, 1, 0)

        int2_lay = QGridLayout()
        self.int2_wid.setLayout(int2_lay)

        #---widgets
        self.int2_lb1 = QLabel('Minimum :')
        int2_lay.addWidget(self.int2_lb1, 0, 0)

        self.int2_sp1 = QSpinBox()
        self.int2_sp1.setMinimumSize(150, 35)
        int2_lay.addWidget(self.int2_sp1, 0, 1)

        self.int2_lb2 = QLabel('Maximum :')
        int2_lay.addWidget(self.int2_lb2, 1, 0)

        self.int2_sp2 = QSpinBox()
        self.int2_sp2.setMinimumSize(150, 35)
        int2_lay.addWidget(self.int2_sp2, 1, 1)


        #------buttons
        self.bt_cancel = QPushButton('Cancel')
        self.bt_cancel.setMaximumSize(55, 35)
        self.bt_cancel.clicked.connect(self.close)
        main_lay.addWidget(self.bt_cancel, 2, 0, Qt.AlignRight)

        self.bt_gen = QPushButton('Generate')
        self.bt_gen.setMinimumSize(0, 35)
        self.bt_gen.setStyleSheet(style)
        self.bt_gen.setObjectName('main_obj')
        self.bt_gen.clicked.connect(self.gen)
        main_lay.addWidget(self.bt_gen, 2, 1)


        self.w_lst = (self.RSA_wid, self.sp_wid, self.int2_wid)
        self._chk('RSA')
        self._chk(tr('-- Select a cipher --'))


    def _chk(self, ciph):
        '''Changes the generation box.'''

        if ciph == tr('-- Select a cipher --'):
            for w in self.w_lst:
                w.setDisabled(True)

        else:
            self.setWindowTitle('Generate {} keys — Cracker'.format(ciph))

            for w in self.w_lst:
                w.setDisabled(False)


        if ciph == 'RSA':
            for w in self.w_lst:
                w.hide()
            self.RSA_wid.show()

        elif 'AES' in ciph:
            for w in self.w_lst:
                w.hide()
            self.sp_wid.show()
            self.sp_lb.setText("Key's size :")

        elif ciph in crypta.ciph_sort['1_key_str']:
            for w in self.w_lst:
                w.hide()
            self.sp_wid.show()
            self.sp_lb.setText("Key's length :")

        elif ciph in ('Scytale', 'Rail fence'):
            for w in self.w_lst:
                w.hide()
            self.sp_wid.show()
            self.sp_lb.setText("Text's length :")

        elif ciph in ('Fleissner', 'Hill'):
            for w in self.w_lst:
                w.hide()
            self.sp_wid.show()
            self.sp_lb.setText("List's size :")

        elif ciph in ('Gronsfeld',):
            for w in self.w_lst:
                w.hide()
            self.int2_wid.show()
            self.int2_lb1.setText('Minimum :')
            self.int2_lb2.setText('Maximum :')

        elif ciph in crypta.ciph_sort['2_key_str']:
            for w in self.w_lst:
                w.hide()
            self.int2_wid.show()
            self.int2_lb1.setText("First key's length :")
            self.int2_lb2.setText("Second key's length :")

        elif ciph in ('Caesar', 'Affine'):
            for w in self.w_lst:
                w.setDisabled(True)



    def gen(self):
        '''Redirect to the good gen method.'''

        ciph = self.cipher_box.currentText()

        if ciph == tr('-- Select a cipher --'):
            QMessageBox.critical(None, '!!! No cipher selected !!!', '<h2>Please select a cipher !!!</h2>')
            return -3

        if ciph == 'RSA':
            ret = self.gen_RSA()

        elif 'AES' in ciph:
            try:
                ret = self._show_key(ciph, KRIS.AES_rnd_key_gen(self.str1_lth.value(), int(ciph[-3:])))

            except ValueError as err:
                QMessageBox.warning(None, 'Key size error', '<h2>{}</h2>'.format(err))
                return -3

        elif ciph == 'Caesar':
            ret = self._show_key('Caesar', str(crypta.Caesar().gen_key()))

        elif ciph == 'Affine':
            ret = self._show_key('Affine', str(crypta.Affine().gen_key()))

        elif ciph in (*crypta.ciph_sort['1_key_str'], 'Scytale', 'Rail fence', 'Fleissner', 'Hill'):
            ret = self.gen_1_arg()

        elif ciph in ('Gronsfeld', *crypta.ciph_sort['2_key_str']):
            ret = self.gen_2_int_arg()


        if ret != -3:
            self.close()

        return ret


    def gen_RSA(self):
        '''Collect the infos and give it to RsaKeys to generate the keys.'''

        global win

        name = self.ledt.text()
        if name == '':
            QMessageBox.critical(None, '!!! No name !!!', '<h2>Please enter a name for the RSA keys !!!</h2>')
            return -3 #Abort

        size = self.slider_sz.value()
        md_st = ('dec', 'hexa')[self.chbt_h.isChecked()]

        val = RSA.RsaKeys(name, 'gui').generate(size, md_stored=md_st)

        if val == -2: #The set of keys already exists
            rep = QMessageBox.question(
                None,
                'File error !',
                '<h2>A set of keys named "{}" already exist !</h2>\n<h2>Overwite it !?</h2>\n<h3>This action can NOT be undone !!!</h3>'.format(name),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if rep == QMessageBox.Yes:
                val = RSA.RsaKeys(name, 'gui').generate(size, md_stored=md_st, overwrite=True)

            else:
                return -2

        win.reload_keys()

        global RSA_keys_pwd
        RSA.RsaKeys(name, 'gui').encrypt(RSA_keys_pwd)


        QMessageBox.about(None, 'Done !', '<h2>Your brand new RSA keys "{}" are ready !</h2>\n<h3>`n` size : {} bits</h3>'.format(name, val[2]))


    def gen_1_arg(self):
        '''Collect infos and gen a key.'''

        ciph = self.cipher_box.currentText()
        lth = self.str1_lth.value()

        key = crypta.crypta_ciphers[ciph]().gen_key(lth)

        self._show_key(ciph, key)


    def gen_2_int_arg(self):
        '''Collect infos and gen a key.'''

        ciph = self.cipher_box.currentText()
        mn = self.int2_sp1.value()
        mx = self.int2_sp2.value()

        if mn > mx and ciph == 'Gronsfeld':
            QMessageBox.critical(None, '!!! Error !!!', '<h2>The maximum can not be smaller than the minimum !!!</h2>')
            return -3

        key = crypta.crypta_ciphers[ciph]().gen_key(mn, mx)

        self._show_key(ciph, key)



    def _show_key(self, ciph, key):
        '''Show the key using Popup.'''

        Popup('{} key — Cracker'.format(ciph), str(key), parent=self)


    def use(style, parent=None):
        '''Function which launch this window.'''

        gen_win = GenKeyWin(style, parent)
        gen_win.show()


#---------export RSA keys
class ExpKeyWin(QMainWindow):
    '''Class which define a window which allow to export RSA keys.'''

    def __init__(self, style, parent=None):
        '''Initiate the ExpKeyWin window.'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Export RSA keys — Cracker')

        #---Central widget
        self.main_wid = QWidget()
        self.setCentralWidget(self.main_wid)

        main_lay = QGridLayout()
        self.main_wid.setLayout(main_lay)

        #------Widgets
        #---label
        main_lay.addWidget(QLabel("Keys' name :"), 0, 0)

        #---Keys combo box
        self.keys_opt = QComboBox()
        self.keys_opt.setStyleSheet(style)
        self.keys_opt.setObjectName('sec_obj')
        self.keys_opt.setMinimumSize(200, 0)
        self.keys_opt.addItem(tr('-- Select a key --'))
        self.keys_opt.insertSeparator(1)
        self.keys_opt.addItems(RSA.list_keys('pvk_without_pbk'))
        main_lay.addWidget(self.keys_opt, 0, 1)

        #---check box hexa
        self.chbt_h = QCheckBox('Store in hexadecimal')
        self.chbt_h.setChecked(True)
        main_lay.addWidget(self.chbt_h, 1, 2)

        #---buttons
        self.bt_cancel = QPushButton('Cancel')
        self.bt_cancel.setMaximumSize(55, 35)
        self.bt_cancel.clicked.connect(self.close)
        main_lay.addWidget(self.bt_cancel, 2, 2, Qt.AlignRight)

        self.bt_gen = QPushButton('Export')
        self.bt_gen.setStyleSheet(style)
        self.bt_gen.setObjectName('main_obj')
        self.bt_gen.clicked.connect(self.exp)
        main_lay.addWidget(self.bt_gen, 2, 3)


    def exp(self):
        '''Collect the info and export the public RSA keys.'''

        global win

        k_name = self.keys_opt.currentText()
        md_st = ('dec', 'hexa')[self.chbt_h.isChecked()]

        if k_name == tr('-- Select a key --'):
            QMessageBox.critical(None, '!!! No selected key !!!', '<h2>Please select a key !!!</h2>')
            return -3

        ret = RSA.RsaKeys(k_name, 'gui').export(md_st)

        if ret == -1:
            QMessageBox.critical(None, '!!! Key not found !!!', '<h2>The keys were NOT found !!!</h2>')
            return -1

        QMessageBox.about(None, 'Done !', '<h2>The keys "{}" have been be exported.</h2>'.format(k_name))

        self.close()
        win.reload_keys()


    def use(style, parent=None):
        '''Function which launch this window.'''

        exp_win = ExpKeyWin(style, parent)
        exp_win.show()


#---------RSA keys infos
class InfoKeyWin(QMainWindow):
    '''Class which define a window which allow to get info on RSA keys.'''

    def __init__(self, style, parent=None):
        '''Initiate the InfoKeyWin window.'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Infos on RSA keys — Cracker')

        #---Central widget
        self.main_wid = QWidget()
        self.setCentralWidget(self.main_wid)

        main_lay = QGridLayout()
        self.main_wid.setLayout(main_lay)

        #------Widgets
        #---label
        main_lay.addWidget(QLabel("Keys' name :"), 0, 0)

        #---Keys combo box
        self.keys_opt = QComboBox()
        self.keys_opt.setStyleSheet(style)
        self.keys_opt.setObjectName('sec_obj')
        self.keys_opt.setMinimumSize(200, 0)
        self.keys_opt.addItem(tr('-- Select a key --'))
        self.keys_opt.insertSeparator(1)
        self.keys_opt.addItems(RSA.list_keys('all'))
        main_lay.addWidget(self.keys_opt, 0, 1)

        #---buttons
        self.bt_cancel = QPushButton('Close')
        self.bt_cancel.setMaximumSize(55, 35)
        self.bt_cancel.clicked.connect(self.close)
        main_lay.addWidget(self.bt_cancel, 1, 1, Qt.AlignRight)

        self.bt_info = QPushButton('Get infos')
        self.bt_info.setMinimumSize(0, 35)
        self.bt_info.setStyleSheet(style)
        self.bt_info.setObjectName('main_obj')
        self.bt_info.clicked.connect(self.info)
        main_lay.addWidget(self.bt_info, 1, 2)


    def info(self):
        '''Collect the infos and get infos on RSA keys.'''

        k_name = self.keys_opt.currentText()
        if k_name == tr('-- Select a key --'):
            QMessageBox.critical(None, '!!! No selected key !!!', '<h2>Please select a key !!!</h2>')
            return -3

        keys = RSA.RsaKeys(k_name, 'gui')

        md_stg = keys.show_keys(get_stg_md=True)

        if md_stg == -1:
            return -1 #File not found

        lst_keys, lst_values, lst_infos = keys.show_keys()

        if len(lst_infos) == 2: #Full keys
            (pbk, pvk), (p, q, n, phi, e, d), (n_strth, date_) = lst_keys, lst_values, lst_infos

            prnt = 'The keys were created the ' + date_
            prnt += '\nThe n\'s strenth : ' + n_strth + ' bytes ;\n'

            prnt += '\n\nValues :\n\tp : ' + str(p) + ' ;\n\tq : ' + str(q) + ' ;\n\tn : ' + str(n)
            prnt += ' ;\n\tphi : ' + str(phi) + ' ;\n\te : ' + str(e) + ' ;\n\td : ' + str(d) + ' ;\n'

            prnt += '\n\tPublic key : ' + str(pbk) + ' ;'
            prnt += '\n\tPrivate key : ' + str(pvk) + '.'

        else: #Public keys
            pbk, (n, e), (n_strth, date_, date_exp) = lst_keys, lst_values, lst_infos

            prnt = 'The keys were created the ' + date_ + '\nAnd exported the ' + date_exp
            prnt += '\nThe n\'s strenth : ' + n_strth + ' bytes ;\n'

            prnt += '\n\nValues :\n\tn : ' + str(n) + ' ;\n\te : ' + str(e) + ' ;\n'

            prnt += '\n\tPublic key : ' + str(pbk) + '.'

        Popup('Info on {}'.format(k_name), prnt, parent=self)


    def use(style, parent=None):
        '''Function which launch this window.'''

        info_win = InfoKeyWin(style, parent)
        info_win.show()


#---------Rename RSA keys
class RenKeyWin(QMainWindow):
    '''Class which define a window which allow to rename RSA keys.'''

    def __init__(self, style, parent=None):
        '''Initiate the RenKeyWin window.'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Rename RSA keys — Cracker')

        #---Central widget
        self.main_wid = QWidget()
        self.setCentralWidget(self.main_wid)

        main_lay = QGridLayout()
        self.main_wid.setLayout(main_lay)

        #------Widgets
        #---label
        main_lay.addWidget(QLabel("Keys' name :"), 0, 0)

        #---Keys combo box
        self.keys_opt = QComboBox()
        self.keys_opt.setStyleSheet(style)
        self.keys_opt.setObjectName('sec_obj')
        self.keys_opt.setMinimumSize(200, 0)
        self.keys_opt.addItem(tr('-- Select a key --'))
        self.keys_opt.insertSeparator(1)
        self.keys_opt.addItems(RSA.list_keys('all'))
        main_lay.addWidget(self.keys_opt, 0, 1)

        #---Rename box
        main_lay.addWidget(QLabel('New name :'), 1, 0)

        self.ledit = QLineEdit()
        self.ledit.setMinimumSize(150, 35)
        main_lay.addWidget(self.ledit, 1, 1)

        #---buttons
        self.bt_cancel = QPushButton('Cancel')
        self.bt_cancel.setMaximumSize(55, 35)
        self.bt_cancel.clicked.connect(self.close)
        main_lay.addWidget(self.bt_cancel, 2, 1, Qt.AlignRight)

        self.bt_rn = QPushButton('Rename')
        self.bt_rn.setMinimumSize(0, 35)
        self.bt_rn.setStyleSheet(style)
        self.bt_rn.setObjectName('main_obj')
        self.bt_rn.clicked.connect(self.rn)
        main_lay.addWidget(self.bt_rn, 2, 2)


    def rn(self):
        '''Collect the infos and rename RSA keys.'''

        global win

        k_name = self.keys_opt.currentText()
        new_name = self.ledit.text()

        if k_name == tr('-- Select a key --'):
            QMessageBox.critical(None, '!!! No selected key !!!', '<h2>Please select a key !!!</h2>')
            return -3

        if new_name == '':
            QMessageBox.critical(None, '!!! No name !!!', '<h2>Please enter a new name !</h2>')
            return -3


        keys = RSA.RsaKeys(k_name, 'gui')
        out = keys.rename(new_name)

        if out == -1:
            QMessageBox.critical(None, '!!! Keys not found !!!', '<h2>The set of keys was NOT found !!!</h2>')
            return -1

        QMessageBox.about(None, 'Done !', '<h2>Your keys "{}" have been be renamed "{}" !</h2>'.format(k_name, new_name))

        self.close()
        win.reload_keys()


    def use(style, parent=None):
        '''Function which launch this window.'''

        rn_win = RenKeyWin(style, parent)
        rn_win.show()


#---------Convert RSA keys
class CvrtKeyWin(QMainWindow):
    '''Class which define a window which allow to convert RSA keys.'''

    def __init__(self, style, parent=None):
        '''Initiate the CvrtKeyWin window.'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('Convert RSA keys — Cracker')

        #---Central widget
        self.main_wid = QWidget()
        self.setCentralWidget(self.main_wid)

        main_lay = QGridLayout()
        self.main_wid.setLayout(main_lay)

        #------Widgets
        #---Radio buttons
        main_lay.addWidget(QLabel("Keys' type :"), 0, 0)

        self.rb_dec = QRadioButton('Decimal')
        self.rb_dec.setChecked(True)
        self.rb_dec.toggled.connect(self._chk)
        main_lay.addWidget(self.rb_dec, 0, 1)

        self.rb_hex = QRadioButton('Hexadecimal')
        self.rb_hex.toggled.connect(self._chk)
        main_lay.addWidget(self.rb_hex, 0, 2)

        #---label
        main_lay.addWidget(QLabel("Keys' name :"), 1, 0)

        #---Keys combo box
        keys_lst = (*RSA.list_keys('pvk'), *RSA.list_keys('pbk'))

        self.keys_opt = QComboBox()
        self.keys_opt.setStyleSheet(style)
        self.keys_opt.setObjectName('sec_obj')
        self.keys_opt.setMinimumSize(200, 0)
        self.keys_opt.addItem(tr('-- Select a key --'))
        self.keys_opt.insertSeparator(1)
        self.keys_opt.addItems(keys_lst)
        main_lay.addWidget(self.keys_opt, 1, 1)

        #---buttons
        self.bt_cancel = QPushButton('Cancel')
        self.bt_cancel.setMaximumSize(55, 35)
        self.bt_cancel.clicked.connect(self.close)
        main_lay.addWidget(self.bt_cancel, 2, 1, Qt.AlignRight)

        self.bt_cvrt = QPushButton('Convert in hexa')
        self.bt_cvrt.setMinimumSize(0, 35)
        self.bt_cvrt.setStyleSheet(style)
        self.bt_cvrt.setObjectName('main_obj')
        self.bt_cvrt.clicked.connect(self.cvrt)
        main_lay.addWidget(self.bt_cvrt, 2, 2)


    def _chk(self):
        '''Check the checked radio button, and actualise the keys combo box.'''

        if self.rb_dec.isChecked():
            keys_lst = (*RSA.list_keys('pvk'), *RSA.list_keys('pbk'))
            self.bt_cvrt.setText('Convert in hexa')

        else:
            keys_lst = (*RSA.list_keys('pvk_hex'), *RSA.list_keys('pbk_hex'))
            self.bt_cvrt.setText('Convert in decimal')

        self.keys_opt.clear()
        self.keys_opt.addItem(tr('-- Select a key --'))
        self.keys_opt.insertSeparator(1)
        self.keys_opt.addItems(keys_lst)


    def cvrt(self):
        '''Collect the infos and convert RSA keys.'''

        k_name = self.keys_opt.currentText()
        exp = ('decimal', 'hexadecimal')[self.rb_dec.isChecked()]

        if k_name == tr('-- Select a key --'):
            QMessageBox.critical(None, '!!! No selected key !!!', '<h2>Please select a key !!!</h2>')
            return -3

        out = RSA.RsaKeys(k_name, 'gui').convert()

        if out == -1:
            QMessageBox.critical(None, '!!! Keys not found !!!', '<h2>The keys were NOT found !!!</h2>')
            return -1

        elif out == -2:
            QMessageBox.critical(None, '!!! Keys already exist !!!', '<h2>The set of keys already exist !!!</h2>\n<h3>You may already have converted them.</h3>')
            return -2

        QMessageBox.about(None, 'Done !', '<h2>Your set of keys has been be converted in "{}" !</h2>'.format(exp))
        self.close()


    def use(style, parent=None):
        '''Function which launch this window.'''

        cvrt_win = CvrtKeyWin(style, parent)
        cvrt_win.show()



##-Classes to use the GUI
#---------Crack
class UseCrackTab:
    '''Class which allow to use the Crack tab.'''

    # use_crack = UseCrackTab(args)
    # ...
    # bt_crack.clicked.connect(use_crack.crack)

    def __init__(self, txt, opt_algo, opt_meth, wlst_sp, wlst_alf, wrdlst, txt_ret):
        '''Create the UseCrackTab object.'''

        self.txt = txt
        self.opt_algo = opt_algo
        self.opt_meth = opt_meth
        self.wlst_sp = wlst_sp
        self.wlst_alf = wlst_alf
        self.wrdlst = wrdlst
        self.txt_ret = txt_ret


    def _verify(self):
        '''Check if everything is filled, raise a popup and return -3 else.'''

        if self.opt_algo.currentText() == '-- Select an algorithm --':
            QMessageBox.critical(None, '!!! No algo selected !!!', '<h2>Please select an algorithm !!!</h2>')
            return -3

        if self.opt_meth.currentText() == '-- Select a method --':
            QMessageBox.critical(None, '!!! No method selected !!!', '<h2>Please select a crack method !!!</h2>')
            return -3


        if self.opt_meth.currentText() == 'Brute-force' and self.wlst_alf.currentText() == tr('-- Select an alphabet --'):
            QMessageBox.critical(None, '!!! No alphabet selected !!!', '<h2>Please select an alphabet !!!</h2>')
            return -3

        if self.opt_meth.currentText() == 'Dictionary attack' and self.wrdlst.currentText() == '-- Previously selected wordlists --':
            QMessageBox.critical(None, '!!! No wordlist selected !!!', '<h2>Please select a wordlist !!!</h2>')
            return -3


    def _ret_append(self, txt, algo=None):
        '''Append 'txt' to the ret QTextEdit, adding some info behind.'''

        meth = self.opt_meth.currentText()
        if algo == None:
            algo = self.opt_algo.currentText()

        sep = ('\n' + '―'*20 + '\n', '')[self.txt_ret.toPlainText() == '']

        self.txt_ret.append(
            '{}{} - {} on {} : {}\n'.format(
                sep,
                str(dt.now())[:-7],
                meth,
                algo,
                txt
            )
        )


    def _crack(self, C, msg_f, prnt, t0, algo=None, f_verbose=True):
        '''Try to crack the text.'''

        txt = self.txt.getText()
        meth = self.opt_meth.currentText()
        wlst_lth = self.wlst_sp.value()
        wlst_alf = self.wlst_alf.currentText()
        wrdlst = self.wrdlst.currentText()

        if algo == None:
            algo = self.opt_algo.currentText()

        pwd = False

        if meth == 'Brute-force':
            if algo in ciphers_list['hash'] + crypta.ciph_sort['0_key']:
                pwd = crack.SmartBruteForce(
                    C,
                    interface='gui'
                ).permutation(txt, wlst_lth, wlst_alf)

            elif algo in crypta.ciph_sort['1_key_str']:
                #------check the alphabet, to know if there is numbers in
                for k in wlst_alf:
                    if k in '0123456789':
                        QMessageBox.warning(None, 'Useless !', '<h2>There is at least one number in your alphabet, but that\'s useless since the cipher only takes string keys.</h2>')
                        return -3

                brk = crack.SmartBruteForce(C, interface='gui').brute_force_str(wlst_lth, wlst_alf, str, ldm=True)

                self._ret_append(brk, algo)

            elif algo in crypta.ciph_sort['1_key_int']:
                #------check the alphabet
                for k in wlst_alf:
                    if k not in '0123456789':
                        QMessageBox.warning(None, 'Useless !', '<h2>There is at least one character which is not a number in your alphabet, so that\'s useless since the cipher only takes numbers keys.</h2>')
                        return -3

                brk = crack.SmartBruteForce(C, interface='gui').brute_force_str(wlst_lth, wlst_alf, int, ldm=True)

                self._ret_append(brk, algo)

        elif meth == 'Dictionary attack':
            pwd = crack.BruteForce(C, wrdlst, interface='gui').crack(txt)

        elif meth == 'Advanced brute-force':
            pwd = crack.SmartBruteForce(C, interface='gui').crack(txt)


        if pwd == False:
            pass

        elif pwd == None:
            self._ret_append(msg_f, algo)
            if f_verbose:
                QMessageBox.about(
                    None, 'Not found !',
                    '<h2>The clear text has not be found !!!</h2>\n<h3>Try with an other {}, method, or dictionary.</h3>'.format(prnt)
                )

        else:
            self._ret_append('\n\t{}.'.format(NewLine(c='\n\t').set('{} ===> {}'.format(pwd, txt))), algo)
            QMessageBox.about(
                None, '{} cracked !!!'.format(prnt),
                '<h2>The {} has been be cracked in {}s !<h2>\n<h2>result :</h2><h1>{}</h1>'.format(
                    prnt,
                    dt.now() - t0,
                    pwd
                )
            )

            return pwd


    def crack(self):
        '''Method which use the Crack tab, when "Crack" button is pressed.'''

        if self._verify() == -3:
            return -3 #Abort

        txt = self.txt.getText()
        algo = self.opt_algo.currentText()
        meth = self.opt_meth.currentText()
        wlst_lth = self.wlst_sp.value()
        wlst_alf = self.wlst_alf.currentText()
        wrdlst = self.wrdlst.currentText()

        msg_f = '\n\tThe clear text has not be found.' #Message False (not found)

        t0 = dt.now()

        if algo not in ('Unknow', 'Unknow hash'):
            #------get the encryption function
            if algo in ciphers_list['hash']:
                C = hasher.Hasher(algo).hash
                prnt = 'hash'

            elif algo in crypta.ciph_sort['0_key']:
                C = crypta.make_ciph(algo, interface='gui').encrypt
                prnt = 'cipher'

            elif algo in (*crypta.ciph_sort['1_key_int'], *crypta.ciph_sort['1_key_str']):
                C = lambda key: crypta.crypta_ciphers[algo](key).decrypt(txt)
                prnt = 'cipher'


            if meth in ('Brute-force', 'Dictionary attack', 'Advanced brute-force'):
                ret = self._crack(C, msg_f, prnt, t0)
                if ret == -3:
                    return -3


            elif meth == 'Code break':
                C = crypta.make_ciph(algo, interface='gui')

                if algo in crypta.broken_ciph_dict['break_']:
                    try:
                        brk = C.break_(txt)

                    except Exception as ept:
                        QMessageBox.critical(None, '!!! Error !!!', '<h2>{}</h2>'.format(ept))
                        return -3

                    self._ret_append('\n\t{}'.format(NewLine(c='\n\t').set('{} ===> {}'.format(brk, txt))))

                else:
                    brk = C.brute_force(txt)
                    m = C.meaning(txt, brk)

                    if m[0] == False:
                        answer = QMessageBox.question(
                            None, 'Maybe not found',
                            '<h2>The list of broken word does not seem to contain something which makes sense.</h2>\n<h2>Show the list anyway ?</h2>',
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )

                        if answer == QMessageBox.Yes:
                            ret = 'Possible decryptions (key - decryption) :'
                            for k in brk:
                                ret += '\n\t{} - {}'.format(k, brk[k])

                            self._ret_append(ret)

                        else:
                            self._ret_append(msg_f)

                    else:
                        self._ret_append('\n\t{}'.format(NewLine(c='\n\t').set('{} ===> {}'.format(m, txt)))) #todo: improve this return : it just show the list (True, txt_c, [key, [alf]])


        elif algo == 'Unknow':
            pos_algo = crack.deter(txt)

            if pos_algo == ():
                QMessageBox.critical(None, 'Cipher not found !!!', '<h2>It is impossible to identify the cipher !!!</h2>')
                return -3

            self._ret_append('\nPossibles used algorithms :' + set_lst(pos_algo))

            rep = QMessageBox.question(None, 'Crack ?', '<h2>Try to crack these ciphers ?</h2>', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if rep == QMessageBox.No:
                return -3

            for k in pos_algo:
                if k in ciphers_list['hash']:
                    C = hasher.Hasher(k).hash
                    prnt = 'hash'

                elif k in crypta.ciph_sort['0_key']:
                    C = crypta.make_ciph(k, interface='gui').encrypt
                    prnt = 'cipher'

                elif k in (*crypta.ciph_sort['1_key_int'], *crypta.ciph_sort['1_key_str']):
                    C = lambda key: crypta.crypta_ciphers[k](key).decrypt(txt)
                    prnt = 'cipher'

                else:
                    C = None
                    prnt = None
                    print('Not trying to crack with the {} cipher.'.format(k))


                if C != None:
                    print(k)
                    ret = self._crack(C, msg_f, prnt, t0, algo=k, f_verbose=False)

                    if ret not in (-3, None):
                        break


        else: #algo == 'Unknow hash'
            pos_hash = crack.deter(txt, only_hash=True)

            if pos_hash == ():
                QMessageBox.critical(None, 'Hash not found !!!', '<h2>It is impossible to identify the hash !!!</h2>')
                return -3

            self._ret_append('\nPossibles used hashes :' + set_lst(pos_hash))

            rep = QMessageBox.question(None, 'Crack ?', '<h2>Try to crack these hashes ?</h2>', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if rep == QMessageBox.No:
                return -3

            for k in pos_hash:
                print(k)
                C = hasher.Hasher(k).hash
                ret = self._crack(C, msg_f, 'hash', t0, algo=k, f_verbose=False)

                if ret not in (-3, None):
                    break



#---------Ciphers
class UseCipherTab:
    '''Class which allow to use the Cipher tab.'''

    def __init__(self, txt_e, txt_d, key_opt, key_ledit, key_nb, key_2_str, key_2_nb, alf, cipher):
        '''Create the UseCipherTab object.'''

        self.txt_e = txt_e
        self.txt_d = txt_d
        self.key_opt = key_opt
        self.key_ledit = key_ledit
        self.key_nb = key_nb
        self.key_2_str = key_2_str
        self.key_2_nb = key_2_nb
        self.alf = alf
        self.cipher = cipher


    def _verify(self, md):
        '''
        Verify if the infos are good, warn the user else.
        md : 0 - encrypt : 1 - decrypt.

        Return :
            -3 if  not good ;
            0 otherwise.
        '''

        if md not in (0, 1):
            raise ValueError('"md" not in (0, 1) !!!')

        ciph = self.cipher.currentText()

        if ciph == tr('-- Select a cipher --'):
            QMessageBox.critical(None, 'No cipher selected !!!', '<h2>Please select a cipher !</h2>')
            return -3

        if ciph in (*ciphers_list['KRIS'], *ciphers_list['RSA']):
            if self.key_opt.currentText() == tr('-- Select a key --'):
                QMessageBox.critical(None, 'No key selected !!!', '<h2>Please select a key !</h2>')
                return -3

        elif ciph not in (
            *ciphers_list['hash'],
            *ciphers_list[tr('analysis')],
            *crypta.ciph_sort['0_key']
        ):
            key = self._get_key(md)
            err = False
            if ciph in (*crypta.ciph_sort['2_key_str'], *crypta.ciph_sort['2_key_int']):
                if '' in key:
                    err = True

            elif key == '':
                err = True

            if err:
                QMessageBox.critical(None, 'No key entered !!!', '<h2>Please enter a key !</h2>')
                return -3

        if ciph in crypta.ciph_sort['alf'] and self.alf.currentText() == tr('-- Select an alphabet --'):
            QMessageBox.critical(None, 'No alphabet selected !!!', '<h2>Please select an alphabet !<h2>')
            return -3

        if ciph in crypta.ciph_sort['1_key_list']:
            try:
                key = Matrix(literal_eval(self.key_ledit.text()))

            except ValueError:
                QMessageBox.critical(None, '!!! Bad key form !!!', '<h2>The key should be a list of lists !</h2>\n<h2>It should be of the form "[[0, 1], [2, 3]]"</h2>\n\n<h3>Try the generate button to generate a {} key.</h3>'.format(ciph))
                return -3

        return 0 #Everything is fine


    def _get_key(self, md):
        '''
        Return the usable key.
        md : 0 - encrypt : 1 - decrypt.

        Return :
            -3 if an error occured (with an RSA key) ;
            the key otherwise.
        '''

        if md not in (0, 1):
            raise ValueError('"md" not in (0, 1) !!!')

        ciph = self.cipher.currentText()

        if ciph in (*ciphers_list['KRIS'], *ciphers_list['RSA']):
            try:
                key = RSA.RsaKeys(self.key_opt.currentText(), interface='gui').read(md)

            except Exception as err:
                QMessageBox.critical(None, '!!! Error !!!', '<h2>{}</h2>'.format(err))
                return -3 #Abort

        elif ciph in (*crypta.ciph_sort['1_key_int'], 'Frequence analysis', 'SecHash'):
            key = self.key_nb.value()

        elif ciph in crypta.ciph_sort['2_key_str']:
            key = self.key_2_str.value()

        elif ciph in crypta.ciph_sort['2_key_int']:
            key = self.key_2_nb.value()

        else:
            key = self.key_ledit.text()


        return key


    def encrypt(self):
        '''Encrypt the text, using the informations given in init.'''

        #------check
        if self._verify(0) == -3:
            return -3 #Abort

        #------ini
        txt = self.txt_e.getText()
        if txt in (-1, -2, -3):
            return txt #Abort

        ciph = self.cipher.currentText()
        encod = self.txt_d.get_encod()
        bytes_md = self.txt_d.get_bytes()

        if ciph != 'RSA signature':
            key = self._get_key(0)

        else:
            key = self._get_key(1)

        if key == -3:
            return -3 #Abort


        #------encrypt with the good cipher
        if ciph in ciphers_list['KRIS']:
            AES_md = (256, 192, 128)[ciphers_list['KRIS'].index(ciph)]

            C = KRIS.Kris((key, None), AES_md, encod, bytes_md, interface='gui')
            msg_c = C.encrypt(txt)

            msg_c = '{} {}'.format(msg_c[0], msg_c[1])


        elif ciph == 'RSA':
            C = RSA.RSA((key, None), interface='gui')
            msg_c = C.encrypt(txt)


        elif ciph == 'RSA signature':
            C = RSA.RsaSign((None, key), interface='gui')
            msg_c = C.str_sign(txt)


        elif  ciph in ciphers_list['AES']:
            AES_md = (256, 192, 128)[ciphers_list['AES'].index(ciph)]
            md = {'t' : 'str', 'b' : 'bytes'}[bytes_md]

            try:
                C = AES.AES(AES_md, key, False, encod)

            except ValueError as err:
                QMessageBox.critical(None, '!!! Value error !!!', '<h2>{}</h2>'.format(err))
                return -3

            msg_c = C.encryptText(txt, encoding=encod, mode_c='hexa', mode=md)


        elif ciph in ciphers_list['hash'][:-1]:
            try:
                C = hasher.Hasher(ciph)

            except ValueError:
                QMessageBox.critical(None, '!!! Unknown hash !!!', '<h2>The hash "{}" is unknown !!!</h2>'.format(ciph))
                return -3

            msg_c = C.hash(txt)


        elif ciph == 'SecHash':
            try:
                msg_c = hasher.SecHash(txt, key)

            except RecursionError:
                QMessageBox.critical(None, '!!! Too big loop !!!', '<h2>The number of loops is too big !!!</h2>')
                return -3


        elif ciph in ciphers_list['Crypta']:
            key2 = None

            if ciph in crypta.ciph_sort['1_key_list']:
                key = literal_eval(key)

            elif ciph in (*crypta.ciph_sort['2_key_str'], *crypta.ciph_sort['2_key_int']):
                key2 = key[1]
                key = key[0]

            try:
                C = crypta.make_ciph(ciph, key, key2=key2, alf=self.alf.currentText(), interface='gui')

            except Exception as ept:
                QMessageBox.critical(None, '!!! Error !!!', '<h2>{}</h2>'.format(ept))
                return -3

            msg_c = C.encrypt(txt)


        elif ciph in ciphers_list[tr('analysis')]:
            if ciph == 'Frequence analysis':
                msg_c = crypta.freqana_str(txt, True, n=key)

            elif ciph == 'Index of coincidence':
                msg_c = str(crypta.Ic(wprocess=True).calc(txt))

            elif ciph == 'Kasiki examination':
                msg_c = crypta.Kasiki(wprocess=True).analyse(txt)

            elif ciph == "Friedman's test":
                msg_c = crypta.Friedman(wprocess=True).analyse(txt)

            elif ciph == 'Text analysis':
                msg_c = crypta.textana(txt, True)


        self.txt_d.setText(msg_c)


    def decrypt(self):
        '''Decrypt the text, using the informations given in init.'''

        #------check
        if self._verify(1) == -3:
            return -3 #Abort

        #------ini
        txt = self.txt_d.getText()
        if txt in (-1, -2, -3):
            return txt #Abort

        ciph = self.cipher.currentText()
        encod = self.txt_e.get_encod()
        bytes_md = self.txt_e.get_bytes()
        bytes_md_d = self.txt_d.get_bytes()

        if ciph != 'RSA signature':
            key = self._get_key(1)

        else:
            key = self._get_key(0)

        if key == -3:
            return -3 #Abort


        #------decrypt using the good cipher
        if ciph in ciphers_list['KRIS']:
            AES_md = (256, 192, 128)[ciphers_list['KRIS'].index(ciph)]

            C = KRIS.Kris((None, key), AES_md, encod, bytes_md, interface='gui')

            try:
                if bytes_md_d == 't':
                    msg_d = C.decrypt(txt.split(' '))
                else:
                    msg_d = C.decrypt(txt.split(b' '))

            except ValueError:
                return -3 #The error message is printed in Kris.


        elif ciph == 'RSA':
            C = RSA.RSA((None, key), interface='gui')
            msg_d = C.decrypt(txt)


        elif ciph == 'RSA signature':
            C = RSA.RsaSign((key, None), interface='gui')
            if C.str_check(txt):
                QMessageBox.about(None, 'Signature result', '<h2>The signature match to the message.</h2>')

            else:
                QMessageBox.about(None, 'Signature result', '<h2>The signature does not match to the message !</h2>\n<h3>You may not have selected the right RSA key, or the message was modified before you received it !!!</h3>')

            return None


        elif  ciph in ciphers_list['AES']:
            AES_md = (256, 192, 128)[ciphers_list['AES'].index(ciph)]
            md = {'t' : 'str', 'b' : 'bytes'}[bytes_md]

            C = AES.AES(AES_md, key, False, encod)
            msg_d = C.decryptText(txt, encoding=encod, mode_c='hexa', mode=md)


        elif ciph in ciphers_list['Crypta']:
            key2 = None

            if ciph in crypta.ciph_sort['1_key_list']:
                key = literal_eval(key)

            elif ciph in (*crypta.ciph_sort['2_key_str'], *crypta.ciph_sort['2_key_int']):
                key2 = key[1]
                key = key[0]

            try:
                C = crypta.make_ciph(ciph, key, key2=key2, alf=self.alf.currentText(), interface='gui')

            except Exception as ept:
                QMessageBox.critical(None, '!!! Error !!!', '<h2>{}</h2>'.format(ept))
                return -3

            msg_d = C.decrypt(txt)

        self.txt_e.setText(msg_d)



#---------Wordlist generator
class UseWordlistsGenTab:
    '''Class which allow to use the Wordlists tab.'''

    def __init__(self, lth, alf, fn, encod, loc_opt):
        '''Create the UseWordlistsGenTab object.'''

        self.lth = lth
        self.alf = alf
        self.fn = fn
        self.encod = encod
        self.loc_opt = loc_opt


    def generate(self):
        '''Generate a wordlist using the form informations.'''

        if self.alf.currentText() == tr('-- Select an alphabet --'):
            QMessageBox.critical(None, '!!! No alphabet !!!', '<h2>Please select an alphabet !!!</h2>')
            return -3 #Abort

        elif self.fn.text() == '':
            QMessageBox.critical(None, '!!! No file name !!!', '<h2>Please select a filename !!!</h2>')
            return -3 #Abort

        elif self.loc_opt.currentText() == tr('-- Previous locations --'):
            QMessageBox.critical(None, '!!! No location !!!', '<h2>Please select a location !!!</h2>')
            return -3 #Abort


        filepath = self.loc_opt.currentText() + '/' + self.fn.text()

        try:
            self.generator = w_gen.WordlistGenerator(
                filepath,
                self.lth.value(),
                self.alf.currentText(),
                encod=self.encod.currentText(),
                interface='gui'
            )

        except FileExistsError:
            return -3 #Abort

        self.generator.generate()


    def set_name(self, alf=None):
        '''Dynamicly set the name, if the alf is in a known one.'''

        lth = self.lth.value()


        if alf == None:
            alf = self.alf.currentText()

        if alf == tr('-- Select an alphabet --'):
            return -3 #Abort


        mk = {
            '0-1' : '_01', '0-9' : '_09', 'a-z' : 'az', 'A-Z' : 'AZ',
            'a-z, 0-9' : 'az09', 'A-Z, 0-9' : 'AZ09', 'a-z, A-Z' : 'azAZ',
            'a-z, A-Z, 0-9' : 'azAZ09',
            'hex' : 'hex', 'spe' : 'spe', 'all' : 'all'
        }

        if alf in w_gen.alfs.values():
            for k in mk:
                if alf == w_gen.alfs[k]:
                    name = 'w{}{}'.format(lth, mk[k])

        else:
            if alf[0] in w_gen.alfs['0-9']:
                name = 'w{}_{}{}'.format(lth, alf[0], alf[-1])

            else:
                name = 'w{}{}{}'.format(lth, alf[0], alf[-1])


        self.fn.setText(name)




#---------Wordlist analyser
class UseWordlistsAnaTab:
    '''Class which allow to use the Wordlists tab.'''

    def __init__(self, opt, nb_show, txt_ret, txt_lines):
        '''Create the UseWordlistsAnaTab object.'''

        self.opt = opt
        self.nb_show = nb_show
        self.txt_ret = txt_ret
        self.txt_lines = txt_lines

        self.analyser = None


    def show(self):
        '''Show informations about a wordlist, using the informations given in init.'''

        self.fn = self.opt.currentText()

        if self.verify_fn() == -3:
            return -3 #Abort

        self.analyser = WordlistAnalyzer(self.fn, interface='gui')

        if self.analyser in (-1, -2):
            self.analyser = None
            return -3 #Abort

        print('Processing ...')
        t0 = dt.now()
        self.lines = self.analyser.show_lines()
        #self.lines['bottom'].reverse()
        print('Step 1/2 done in {} s'.format(dt.now() - t0))

        print('Analysing ...')
        str_ret = str(self.analyser)
        self.analysis = self.analyser.analysis

        self.txt_ret.setPlainText(str_ret)
        self.actualyze_ln()

        print('Done !')


    def actualyze_ln(self):
        '''Show the head and bottom lines of the wordlist.'''

        if self.analyser == None:
            return -3 #Abort

        head = bottom = ''

        nb_show = self.nb_show.value()

        for k in self.lines['head'][:nb_show]:
            head += '{}\n'.format(k)

        for k in self.lines['bottom'][-nb_show:]:
            bottom += '{}\n'.format(k)

        nb_lines = self.analysis[2]['nb_lines'] - 2*nb_show

        ret = '{1}{0}\n[...] {2} lines fold\n{0}\n{3}'.format('-'*32, head, space(nb_lines), bottom)

        self.txt_lines.setPlainText(ret)



    def verify_fn(self):
        '''Check if there is a file is selected. Raise an error popup if not.'''

        if self.fn == tr('-- Previous locations --'):
            QMessageBox.warning(None, '!!! No file selected !!!', '<h2>Please select a file !</h2>')
            return -3



#---------Prima
class UsePrimaTab:
    '''Class which allow to use the Prima tab.'''

    def __init__(self, txt, algo, txt_ret):
        '''Create the UsePrimaTab object.'''

        self.txt = txt
        self.algo = algo
        self.txt_ret = txt_ret


    def calc(self):
        '''Use Prima according to the informations given in init.'''

        if self.verify_nb() == -3:
            return -3 #Aborted.

        elif self.verify_algo() == -3:
            return -3 #Aborted.

        alg = self.algo.currentText()

        t0 = dt.now()

        if alg in ('Sieve of Erathostenes', 'Segmented sieve of Erathostenes'):
            if self.nb >= 2**24: #Abritrary value
                sure = QMessageBox.question(None, 'Are you sure !?', \
                    '<h2>Are you sure !?</h2>\n<h3>This may take some time and slow you computer !</h3>', \
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if sure == QMessageBox.No:
                    return -3 #Cancel

        txt = prima.to_str(alg, self.nb)

        t1 = dt.now() - t0

        self.txt_ret.setPlainText(txt)
        QMessageBox.about(None, 'Done !', '<h2>Done in ' + str(t1) + 's !</h2>')


    def verify_nb(self):
        '''Check if the input is a number. Raise an error popup if not'''

        if self.txt.getText() == -3:
            return -3

        try:
            nb = int(self.txt.getText())
            self.nb = nb

        except ValueError:
            QMessageBox.warning(None, '!!! Not a number !!!', '<h2>Please enter a correct number !!!</h2>')
            return -3


    def verify_algo(self):
        '''Check if there is an algorithm is selected. Raise an error popup if not.'''

        if self.algo.currentText() == '-- Select an algorithm --':
            QMessageBox.warning(None, '!!! No algorithm selected !!!', '<h2>Please select an algorithm !</h2>')
            return -3



#---------Base convert
class UseBaseConvertTab:
    '''Class which allow to use the Base convert tab.'''

    def __init__(self, n, n_big, nb, b, alf, alf_b, chk_2_std, chk_ieee754, chk_n_big, chk_auto, ret):
        '''Create the UseBaseConvertTab object.'''

        self.n = n
        self.n_big = n_big
        self.nb = nb
        self.b = b
        self.alf = alf
        self.alf_b = alf_b
        self.chk_2_std = chk_2_std
        self.chk_ieee754 = chk_ieee754
        self.chk_n_big = chk_n_big
        self.chk_auto = chk_auto
        self.ret = ret


    def convert(self, sender=None):
        '''Use b_cvrt according to the informations given in init.'''

        #---check if auto convert or not
        if not self.chk_auto.isChecked():
            if sender != 'bt':
                return -3 #Abort if the button was not pressed.

        #---tests
        if self.chk_ieee754.isChecked():
            if self.nb.value() not in (10, 2) or self.b.value() not in (10, 2):
                QMessageBox.critical(None, '!!! IEEE754 error !!!', \
                    '<h2>The IEEE754 only deals with bases 10 and 2 !!!</h2>')
                return -3

        #---define the BaseConvert object
        if self.chk_ieee754.isChecked() and self.nb.value() == 2:
            number = self.try_nb(self.n_big.text(), 'ieee754')

        elif self.chk_n_big.isChecked():
            number = self.try_nb(self.n_big.text(), self.nb.value())

        else:
            number = self.try_nb(self.n.cleanText(), self.nb.value())

        if number == -3:
            return -3

        #---define return base
        if self.b.value() == 2 and self.chk_ieee754.isChecked():
            b = 'ieee754'

        else:
            b = self.b.value()

        #---convert
        try:
            ret = number.convert(b, self.chk_2_std.isChecked(), self.alf_b.currentText())

        except ValueError as err:
            QMessageBox.critical(None, '!!! Number error !!!', '<h2>' + str(err) + '</h2>')
            return -3

        except OverflowError as err:
            QMessageBox.critical(None, '!!! Overflow error !!!', '<h2>' + str(err) + '</h2>')
            return -3

        except MemoryError as err:
            QMessageBox.critical(None, '!!! Memory error !!!', '<h2>Memory error !!!</h2>')
            return -3

        else:
            self.ret.setPlainText(str(ret))


        #todo: chk if IEEE754 chked and if not b in (10, 2), same for 2's complement.


    def try_nb(self, n, nb):
        '''Try to create a BaseConvert number with n, nb, and self.alf.
        Return the BaseConvert number if no problem, -3 else.
        '''

        try:
            number = BaseConvert(n, nb, self.alf.currentText())

        except ValueError as err:
            QMessageBox.critical(None, '!!! Number error !!!', '<h2>' + str(err) + '</h2>')
            return -3

        return number



#---------Settings
class UseSettingsTab:
    '''Class which allow to use the Settings tab.'''

    def __init__(self, old_pwd, new_pwd1, new_pwd2):
        '''Create the UseBaseConvertTab object.'''

        self.old_pwd = old_pwd
        self.pwd1 = new_pwd1
        self.pwd2 = new_pwd2


    def change_pwd(self):
        '''Change the password which allow to launch Cracker.'''

        global pwd

        old_pwd = self.old_pwd.text()
        pwd1 = self.pwd1.text()
        pwd2 = self.pwd2.text()
        entro = pwd_testor.get_sth(pwd1, True)

        if '' in (old_pwd, pwd1, pwd2):
            QMessageBox.critical(None, '!!! Fields empty !!!', '<h2>Please fill the three fields !</h2>')
            return -3

        elif hasher.SecHash(old_pwd) != pwd:
            QMessageBox.critical(None, '!!! Bad password !!!', '<h2>The old password is wrong !</h2>')
            return -3

        elif pwd1 != pwd2:
            QMessageBox.critical(None, '!!! Passwords does not correspond !!!', '<h2>The passwords does not correspond !</h2>')
            return -3

        elif entro < 40:
            QMessageBox.critical(None, '!!! Password too much weak !!!', '<h2>Your new password is too much weak !</h2>\n<h2>It should have an entropy of 40 bits at least, but it has an entropy of {} bits !!!</h2>'.format(round(entro)))
            return -3

        #-good
        pwd = hasher.SecHash(pwd1)
        new_RSA_keys_pwd = hasher.Hasher('sha256').hash(pwd1)[:32]

        try:
            with open('Data/pwd', 'w') as f:
                f.write(pwd)

        except Exception as err:
            QMessageBox.critical(None, '!!! Error !!!', '<h2>{}</h2>'.format(err))
            return -1

        else:
            QMessageBox.about(None, 'Done !', '<h2>Your password has been be changed.</h2>\n<h3>It has an entropy of {} bits.</h3>'.format(round(entro)))

            self.old_pwd.clear()
            self.pwd1.clear()
            self.pwd2.clear()

            global RSA_keys_pwd
            RSA.SecureRsaKeys(new_RSA_keys_pwd, RSA_keys_pwd, 'gui').rm_enc()
            RSA.SecureRsaKeys(new_RSA_keys_pwd, interface='gui').encrypt()



##-run
if __name__ == '__main__':
    color(c_prog)

    #------If first time launched, introduce RSA keys
    chdir(RSA.chd_rsa('.', first=True, interface='gui'))

    #------Launch the GUI
    CrackerGui.use()
