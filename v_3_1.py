# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import random, time, os, numpy, warnings, json, sqlite3, sys, requests, check
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings('ignore')

wanted_version = None
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        #-Preparing-----------------------------------------------------------------------------------
        if 'datas' not in os.listdir():
            os.mkdir('datas')

        self.console_text_iter_final = ''
        self.ab = 0
        self.console_text_iter = []
        self.ce = 0
        self.weights = []
        self.word_info_timer = 1
        self.console_text = '\n'
        self.word_memory = list()
        self.fig_memory = {
            'eng': [], 
            'tur': []
            }
        self.words = {'idle': {}}
        self.word_line = 0
        try:
            with open('datas\\memory.json', 'r') as file:
                self.words = json.loads(file.read())

                self.word_line = sum([len(self.words[name]) for name in self.words.keys()])
            
            with open('datas\\memory2.json', 'r') as file:
                self.data = json.loads(file.read())
        except FileNotFoundError:
            try:
                with open('Kelimeler.txt', 'r', encoding = 'utf-8') as file:
                    words_part = []
                    for text in file.readlines():
                        if text != '---------------------------------------------------------------------------------------------------------------------------\n':
                            words_part.append(tuple(text.replace('\n', '').rstrip(' ').lstrip(' ').split(' : ')))
                            self.word_line += 1
                        else:
                            if self.word_line != 0:
                                last_line = ''.join(words_part[-1]).replace(' ', '')
                                
                                name = ('{first_third}_{last_third}'.format(first_third = last_line[:3], last_third = last_line[-3:])).lower()

                                if not name in self.words.keys():
                                    self.words.update({
                                        name: dict(words_part)
                                        })

                            words_part = []
                    with open('datas\\memory.json', 'w') as file:
                        json.dump(self.words, file)

                os.remove('Kelimeler.txt')
                os.remove('Çalışılacak Kelimeler.txt')
                del words_part
            except FileNotFoundError:
                with open('datas\\memory.json', 'w') as file:
                    json.dump(self.words, file)

        else:
            self.con = sqlite3.connect('datas\\statistics.db')
            self.cursor = self.con.cursor()

            try:
                self.cursor.execute('Select * From data')
            except:
                self.words_scores_data = {}
            else:
                self.words_scores_data = dict([(name, {'eng': eng_scores, 'tur': tur_scores}) for name, eng_scores, tur_scores in self.cursor.fetchall()])
        
        self.window_color = self.data['window_color']
        self.line_color = self.data['line_color']
        self.text_color = self.data['text_color']
        self.font_ = self.data['font']
        self.words_splitter = self.data['split']
        #---------------------------------------------------------------------------------------------
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setEnabled(True)
        MainWindow.resize(960, 460)
        MainWindow.setMinimumSize(QtCore.QSize(960, 240))
        font = QtGui.QFont()
        font.setFamily(self.font_)
        MainWindow.setFont(font)
        self.palette = QtGui.QPalette()
        R, G, B = self.window_color
        brush_2 = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush_2.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setColor(QtGui.QPalette.Button, QtGui.QColor(R, G, B))
        R, G, B = self.text_color
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(R, G, B))
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Window, 
            brush_2
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Window, 
            brush_2
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Window, 
            brush_2
            )
        MainWindow.setPalette(self.palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('app_images\\terim.jpg'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.95)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName('verticalLayout')
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 1, 620, 189))
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setOpenExternalLinks(True)
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.label_2.setPalette(self.palette)
        self.label_2.setFont(font)
        self.label_2.setObjectName('label_2')
        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.label = QtWidgets.QLabel(MainWindow)
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.label.setPalette(self.palette)
        self.label.setFont(font)
        self.label.setObjectName('label')
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit_(MainWindow)
        self.command_names = {
            "cd": "Changes the current file location.", 
            "open": "Opens the word group.",
            "version": "Show version of application.", 
            "update": "Updates to given version.", 
            "export": "Exports a word group.", 
            "import": "Imports given word group to database.", 
            "dir": "Shows every word group.", 
            "cls": "Clears the terminal output.", 
            "new window": "Opens new window.", 
            "settings": "Opens the settings.", 
            "edit word": "Edits saved word.", 
            "find word": "Finds the words.", 
            "add word": "Adds new word to database.", 
            "study english word": "Opens study page for English words.", 
            "study persian word": "Opens study page for Persian words.", 
            "commands": "Shows commands.", 
            "about": "Gives information about Mahmut.", 
            "exit": "Closes Mahmut."
                 }
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Fixed
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit.setSizePolicy(sizePolicy)
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Text, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Base, 
            brush_2
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Text, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Base, 
            brush_2
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Text, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Base, 
            brush_2
            )
        self.lineEdit.setPalette(self.palette)
        self.lineEdit.setObjectName('lineEdit')
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setObjectName('pushButton')
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(QtWidgets.QLabel(MainWindow))
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(50)
        self.line.setMidLineWidth(50)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName('line')
        self.verticalLayout.addWidget(self.line)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName('menubar')
        self.A = QtWidgets.QMenu(self.menubar)
        self.A.setObjectName('menuKonsol')
        self.menuKelime = QtWidgets.QMenu(self.menubar)
        self.menuKelime.setObjectName('menuKelime')
        self.menuYard_m = QtWidgets.QMenu(self.menubar)
        self.menuYard_m.setObjectName('menuYardım')
        self.menu_al = QtWidgets.QMenu(self.menuKelime)
        self.menu_al.setObjectName('menu_al')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)
        self.actionKonsol = QtWidgets.QAction(MainWindow)
        self.actionKonsol.setObjectName('actionA')
        self.actionYeni_Pencere = QtWidgets.QAction(MainWindow)
        self.actionYeni_Pencere.setObjectName('actioYeni_Sekmede_Aç')
        self.actionAyarlar = QtWidgets.QAction(MainWindow)
        self.actionAyarlar.setObjectName('actionAyarlar')
        self.actionD_zelt = QtWidgets.QAction(MainWindow)
        self.actionD_zelt.setObjectName('actionD_zelt')
        self.actionBul = QtWidgets.QAction(MainWindow)
        self.actionBul.setObjectName("actionBul")
        self.actionEkle = QtWidgets.QAction(MainWindow)
        self.actionEkle.setObjectName('actionEkle')
        self.action_ngilizce = QtWidgets.QAction(MainWindow)
        self.action_ngilizce.setObjectName('action_ngilizce')
        self.actionT_rk_e = QtWidgets.QAction(MainWindow)
        self.actionT_rk_e.setObjectName('actionT_rk_e')
        self.actionKomutlar = QtWidgets.QAction(MainWindow)
        self.actionKomutlar.setObjectName('actionKomutlar')
        self.actionHakk_nda = QtWidgets.QAction(MainWindow)
        self.actionHakk_nda.setObjectName('actionHakk_nda')
        self.A.addAction(self.actionKonsol)
        self.A.addAction(self.actionYeni_Pencere)
        self.A.addAction(self.actionAyarlar)
        self.menu_al.addAction(self.action_ngilizce)
        self.menu_al.addAction(self.actionT_rk_e)
        self.menuKelime.addAction(self.actionD_zelt)
        self.menuKelime.addAction(self.actionBul)
        self.menuKelime.addAction(self.actionEkle)
        self.menuYard_m.addAction(self.actionKomutlar)
        self.menuYard_m.addAction(self.actionHakk_nda)
        self.menubar.addAction(self.A.menuAction())
        self.menuKelime.addAction(self.menu_al.menuAction())
        self.menubar.addAction(self.menuKelime.menuAction())
        self.menubar.addAction(self.menuYard_m.menuAction())
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.console_write(None))
        self.line_check_timer = QtCore.QTimer()
        self.line_check_timer.timeout.connect(self.line_check)
        self.line_check_timer.start(50)
        R, G, B = self.text_color
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(R, G, B))
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.label_2.setPalette(self.palette)
        self.setPalette(self.palette)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionKonsol.triggered.connect(self.console)
        self.actionYeni_Pencere.triggered.connect(self.new_tab)
        self.actionAyarlar.triggered.connect(self.settings)
        self.action_ngilizce.triggered.connect(lambda: self.word_study_find('English'))
        self.actionT_rk_e.triggered.connect(lambda: self.word_study_find('Persian'))
        self.actionKomutlar.triggered.connect(self.commands)
        self.actionHakk_nda.triggered.connect(self.about)
        self.actionD_zelt.triggered.connect(self.word_edit)
        self.actionBul.triggered.connect(self.word_find)
        self.actionEkle.triggered.connect(self.add_words)
        self.pushButton.clicked.connect(self.click)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrolled)

        self.news()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate('MainWindow', 'Mahmut'))
        self.A.setTitle(_translate('MainWindow', 'Open'))
        self.menuKelime.setTitle(_translate('MainWindow', 'Word'))
        self.menuYard_m.setTitle(_translate('MainWindow', 'Help'))
        self.menu_al.setTitle(_translate('MainWindow', 'Study'))
        self.actionKonsol.setText(_translate('MainWindow', 'Console'))
        self.actionKonsol.setShortcut(_translate('MainWindow', 'Ctrl+"'))
        self.actionYeni_Pencere.setText(_translate('MainWindow', 'New Window'))
        self.actionYeni_Pencere.setShortcut(_translate('MainWindow', 'Ctrl+Shift+N'))
        self.actionD_zelt.setText(_translate('MainWindow', 'Edit'))
        self.actionD_zelt.setShortcut(_translate('MainWindow', 'Ctrl+Shift+E'))
        self.actionBul.setText(_translate('MainWindow', 'Find'))
        self.actionBul.setShortcut(_translate('MainWindow', 'Ctrl+Shift+F'))
        self.actionEkle.setText(_translate('MainWindow', 'Add'))
        self.actionEkle.setShortcut(_translate('MainWindow', 'Ctrl+Shift+A'))
        self.action_ngilizce.setText(_translate('MainWindow', 'English'))
        self.actionT_rk_e.setText(_translate('MainWindow', 'Persian'))
        self.actionKomutlar.setText(_translate('MainWindow', 'Commmands'))
        self.actionHakk_nda.setText(_translate('MainWindow', 'About'))
        self.actionAyarlar.setText(_translate('MainWindow', 'Settings'))
        self.lineEdit.setPlaceholderText("You can write your commands here")

    def keyPressEvent(self, e):
        if e.key() == 16777220: #Enter key
            self.click()
        elif e.key() == 94: #Alt + 3 key
            self.word_info()
    
    def line_check(self):
        if self.centralwidget.width() != self.ab:
            text = self.console_text.replace('₺+', int(self.centralwidget.width() * 0.158) * '+').replace('₺-', int(self.centralwidget.width() * 0.1) * '-')
            self.label_2.setText(text)

            del text
            self.ab = self.centralwidget.width()

        R, G, B = self.line_color
        R = R - self.ce if R - self.ce > 0 else 0
        G = G - self.ce if G - self.ce > 0 else 0
        B = B - self.ce if B - self.ce > 0 else 0
        self.ce = 0 if self.ce > 255 else self.ce + 5

        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Light, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Light, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Mid, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Mid, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Dark, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Dark, 
            brush
            )
        self.line.setPalette(self.palette)

        del brush, R, G, B

    def scrolled(self):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def console_write(self, text, assets = True):
        if text:
            template = '{time} | {PATH} > '.format(PATH = os.getcwd(), time = time.strftime('%H: %M: %S')) if assets else ''
            template += str(text)

            self.console_text_iter.append(iter(template.split('\n')))
            self.console_text_iter_final = '<br>' * self.console_text.count('\n')
            self.timer.start(1)

            del template
        else:
            if self.console_text_iter:
                try:
                    self.console_text_iter_final += next(self.console_text_iter[0]) + '<br>'
                    self.label_2.setText(self.console_text_iter_final)
                except StopIteration:
                    self.console_text_iter.remove(self.console_text_iter[0])
            else:
                self.console_text += self.console_text_iter_final.lstrip('\n' * self.console_text.count('\n'))
                self.console_text_iter_final = ''
                self.label_2.setText(self.console_text)
                self.timer.stop()
    
    def word_study_find(self, language: str):
        self.lineEdit.clear()
        self.line_color = (0, 0, 127) if language == 'English' else (170, 0, 0)

        if not (self.fig_memory['tur'] or self.fig_memory['eng']):
            try:
                with open('datas\\memory2.json', 'r') as file:
                    self.data = json.loads(file.read())

                if os.path.isfile(self.data['file_upload_PATH']):
                    qm = QtWidgets.QMessageBox
                    ret = qm.question(self, 'Found an Opened Word Group', 'Will you study with {}?\t\t\t'.format(self.data['file_upload_name']))

                    if ret == 16384:
                        self.word_study(language, self.data['file_upload_name'])
                    else:
                        raise FileNotFoundError
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                self.label.setText('Name:')
                self.pushButton.setText('{} Start'.format(language))
                self.console_write(
                        'Please write the word name for studying {}.'.format(language), 
                        assets = False
                        )
        else:
            self.word_study(language, self.name)

    def new_tab(self):
        self.ui = Ui_MainWindow()
        self.ui.show()

    def settings(self):
        self.Dialog_ = QtWidgets.QDialog()
        self.settings_ui = Ui_Dialog()
        self.settings_ui.setupUi(self.Dialog_, self)
        self.Dialog_.show()

    def commands(self):
        foo = ["{}: {}".format(name, info) for name, info in self.command_names.items()]
        foo = '\n'.join(foo)
        self.console_write(foo, assets = False)

    def about(self):
        self.console_write(
            '''--MAHMUT----------------------------------------------------------------------------------------------------------------------------------------

    The Mahmut Project is a Python-based toolkit designed to streamline automation and data management tasks. 
It integrates various functionalities such as graphical user interfaces (GUI), data visualization, and automated 
processes. (https://github.com/Osman-Kahraman/mahmut)

Versions;
- v_1_0
- v_1_1
- v_2_0
- v_2_1
- v_2_2
- v_2_3
- v_2_4
- v_2_5
- v_2_6
- v_2_7
- v_2_8
- v_2_9
- v_2_10
- v_3_0
- v_3_1

Contributors;
- Talha Gözütok (<a href='https://github.com/tgztk'>https://github.com/tgztk</a>)

Copyright @Osman-Kahraman''', assets = False
            )

        """self.label_2.setText("<b>five</b> ")"""

    def news(self):
        main_r = requests.get(
            'https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/master/news.txt'.format(owner = 'Osman-Kahraman', repo = 'mahmut'),
        )

        self.console_write(main_r.text, assets = False)
        self.console()

    def console(self):
        self.label.clear()
        self.line_color = self.data['line_color']
        completer = QtWidgets.QCompleter(self.command_names.keys())
        self.lineEdit.setCompleter(completer)

        if self.fig_memory['eng'] and self.fig_memory['tur'] and check.run():
            self.cursor.execute('Select * From data')

            queueScore_Eng = float('{:.2f}'.format(sum(self.fig_memory['eng']) / len(self.fig_memory['eng'])))
            queueScore_Tur = float('{:.2f}'.format(sum(self.fig_memory['tur']) / len(self.fig_memory['tur'])))

            try:
                queueScores_Eng = self.words_scores_data[self.name]['eng'].lstrip('[').rstrip(']').split(',')
                queueScores_Tur = self.words_scores_data[self.name]['tur'].lstrip('[').rstrip(']').split(',')

                try:
                    float(queueScores_Eng[0])
                except ValueError:
                    queueScores_Eng, queueScores_Tur = queueScores_Eng[1:], queueScores_Tur[1:]

                for i, j in zip(queueScores_Eng, queueScores_Tur):
                    queueScores_Eng[queueScores_Eng.index(i)], queueScores_Tur[queueScores_Tur.index(j)] = float(i), float(j)
            except KeyError:
                queueScores_Eng = []
                queueScores_Tur = []

            queueScores_Eng.append(queueScore_Eng)
            queueScores_Tur.append(queueScore_Tur)

            try:
                self.words_scores_data[self.name]
                self.cursor.execute('Update data set scoresEng = ?, scoresTur = ? where queue_names = ?', (str(queueScores_Eng), str(queueScores_Tur), self.name))
            except:
                self.cursor.execute('Insert into data Values(?, ?, ?)', (self.name, str(queueScores_Eng), str(queueScores_Tur)))
            self.con.commit()

            if len(queueScores_Eng) > 1:
                fig = plt.figure()
                graphic = fig.add_axes([0.1, 0.1, 0.8, 0.8])

                boolen_values_eng, boolen_values_tur = numpy.array(queueScores_Eng), numpy.array(queueScores_Tur)
                values_len = numpy.array(range(len(queueScores_Eng)))

                graphic.plot(values_len, boolen_values_eng, 'blue', marker = 'o', label = 'English')
                graphic.plot(values_len, boolen_values_tur, 'red', marker = 'o', label = 'Persian')

                graphic.legend()
                graphic.set_ylim(-0.1, 1.1)
                graphic.set_xlabel('Studying Time')
                graphic.set_ylabel('Scores')
                graphic.set_title('Score Graph')

                plt.show()

                del fig, graphic, boolen_values_eng, boolen_values_tur, values_len

            self.fig_memory['eng'].clear()
            self.fig_memory['tur'].clear()
            self.weights = []
            del queueScore_Eng, queueScore_Tur, queueScores_Eng, queueScores_Tur

        if self.pushButton.text() != '↑':
            self.pushButton.setText('↑')

    def game(self):
        self.lineEdit.clear()
        completer = QtWidgets.QCompleter([])
        self.lineEdit.setCompleter(completer)

        self.label.setText('Number? (1-9) = ')
        self.pushButton.setText('Put') 
        self.console_write(self.connect_4.playground(), assets = False)

    def add_words(self):
        self.lineEdit.clear()
        self.line_color = self.data['line_color']
        completer = QtWidgets.QCompleter([])
        self.lineEdit.setCompleter(completer)

        text = 'Line number: ' + str(self.word_line)
        if self.pushButton.text() != 'Add':
            self.console_write('{gaps}\n{line_number_text}'.format(gaps = 25 * ' ' + '₺-', line_number_text = (150 - len(text)) * ' ' + text), assets=False)

        self.label.setText('English:')
        self.pushButton.setText('Add')

        del text

    def word_info(self):
        if self.pushButton.text() == 'Check':
            s = self.tur_words[0] if self.language == 'eng' else self.eng_words[0]
            s = s.strip(' ')

            self.console_write(s[:self.word_info_timer] + (len(s) - (self.word_info_timer)) * '-', assets = False)
            self.word_info_timer += 1
    
    def word_edit(self):
        self.lineEdit.clear()
        self.line_color = self.data['line_color']

        if self.pushButton.text() != 'Add':
            self.console_write('{gaps}'.format(gaps = 25 * ' ' + '₺-'), assets=False)

        self.label.setText('English:')
        self.pushButton.setText('Change') 

    def word_find(self, word: str):
        self.lineEdit.clear()

        if word:
            found = [name for name, w_dict in self.words.items() if word in w_dict.keys()]

            if found:
                self.console_write('It found {} times in these word groups.\n\nFound;\n{}'.format(len(found), found), assets = False)
            else:
                self.console_write('The word is not found.', assets = False)

            return found
        else:
            self.label.setText('Word:')
            self.pushButton.setText('Find') 

    def word_study(self, language, name):
        try:
            words_to_study = self.words[name]
        except KeyError:
            self.console_write('Not found the word group.')
        else:
            if self.pushButton.text().startswith('Start'):
                self.console_write(25 * ' ' + 100 * '-', assets = False)
            
            self.lineEdit.clear()
            self.pushButton.setText('Check')
            completer = QtWidgets.QCompleter([])
            self.lineEdit.setCompleter(completer)
            
            self.word_info_timer = 1
            self.language = language
            self.name = name

            if not self.weights:
                self.weights = [1000 for weight in range(len(words_to_study.keys()))]
                
            eng_words, tur_words = random.choices(list(words_to_study.items()), self.weights)[0]
            
            self.weights[list(words_to_study.keys()).index(eng_words)] -= 1
            
            self.eng_words = [word.strip(' ') for word in eng_words.split(self.words_splitter)]
            self.tur_words = [word.strip(' ') for word in tur_words.split(self.words_splitter)]

            text = self.eng_words[random.randint(0, len(self.eng_words) - 1)] if self.language == 'eng' else self.tur_words[random.randint(0, len(self.tur_words) - 1)]
            self.label.setText(text)

            del words_to_study, eng_words, tur_words, text

    def click(self):
        global wanted_version

        if self.pushButton.text() == 'Check':
            self.console_write(self.lineEdit.text())

            user_text = self.lineEdit.text().replace('İ', 'i').lower().replace(' ', '')
            words_to_study = self.tur_words if self.language == 'eng' else self.eng_words
            s = self.fig_memory['eng'] if self.language == 'eng' else self.fig_memory['tur']
                
            correct_words = [word.replace('İ', 'i').lower().replace(' ', '') for word in words_to_study]

            if user_text in correct_words:
                a = correct_words.index(user_text)
                    
                text = 'Correct Answer' if len(words_to_study) == 1 else  'Correct Answer\nOther meanings; ' + str(words_to_study[0:a] + words_to_study[a + 1:])
                    
                self.console_write(text, assets = False)

                self.word_study(self.language, self.name)

                try:
                    false_ratio = float('{:.2f}'.format(1 / (len(words_to_study[0]) // (self.word_info_timer - 1)))) if user_text == correct_words[0] else 0
                except ZeroDivisionError:
                    false_ratio = 0

                s.append(1 - false_ratio)
                self.word_info_timer = 1

                del a
            else:
                self.console_write('Wrong Answer', assets = False)

                s.append(0)

            del user_text, words_to_study, s, correct_words
        elif self.pushButton.text() == 'Start English':
            self.word_study('eng', self.lineEdit.text())
        elif self.pushButton.text() == 'Start Persian':
            self.word_study('tur', self.lineEdit.text())
        elif self.pushButton.text() == 'Put' and self.lineEdit.text():
            disp_bfr = self.connect_4.playground()
            self.connect_4.input(self.lineEdit.text())
            disp = self.connect_4.playground()
            self.console_text = self.console_text.replace(disp_bfr, disp)
            self.label_2.setText(self.console_text)
            if disp[-2] == "-":
                self.console()
        elif self.pushButton.text() == 'Add' and self.lineEdit.text():
            if self.label.text() == 'English:':
                self.label.setText('Persian:')

                self.word_memory.append(self.lineEdit.text())

                self.console_write('English word: ' + self.lineEdit.text(), assets = False)
            elif self.label.text() == 'Persian:':
                self.label.setText('English:')

                self.word_memory.append(self.lineEdit.text())

                self.console_write('Persian word: ' + self.lineEdit.text(), assets = False)

            if len(self.word_memory) == 2:
                self.label.setText('Add? (y/n)')
                self.pushButton.setText('↑')
        elif self.pushButton.text() == 'Find':
            self.word_find(self.lineEdit.text())
        elif self.pushButton.text() == 'Change' and self.lineEdit.text():
            if self.label.text() == "English:":
                self.label.setText('Persian:')

                self.word_memory.append(self.lineEdit.text())

                self.console_write('English word: ' + self.lineEdit.text(), assets = False)
            elif self.label.text() == 'Persian:':
                self.label.setText('English:')
                
                self.word_memory.append(self.lineEdit.text())

                self.console_write('Persian Word: ' + self.lineEdit.text(), assets = False)
            
            if len(self.word_memory) >= 2:
                self.label.setText('Change? (y/n)')
                self.pushButton.setText('↑')
        else:
            self.console_write(self.lineEdit.text())
            if len(self.word_memory) >= 2:
                if self.lineEdit.text().lower().replace(' ', '') == 'y':
                    if self.label.text() == "Change? (y/n)":
                        for i in range(0, len(self.word_memory), 2):
                            found = self.word_find(self.word_memory[i])

                            for name in found:
                                self.words[name][self.word_memory[i]] = self.word_memory[i + 1]
                            
                            if found:
                                self.console_write('\nWord changed.', assets = False)

                        self.word_edit()
                    elif self.label.text() == 'Add? (y/n)':
                        self.word_line += 1

                        self.words['idle'].update({self.word_memory[0]: self.word_memory[1]})

                        if len(self.words['idle'].keys()) == 40:
                            a = list(self.words['idle'].keys())[-1]
                            b = self.words['idle'][a]

                            name = ('{first_third}_{last_third}'.format(first_third = a[:3], last_third = b[-3:])).lower()

                            self.words.update({
                                name: self.words['idle'].copy()
                                })

                            self.words['idle'].clear()
                            del a, b, name

                        self.console_write('Word added.', assets = False)

                        self.add_words()
                        
                    with open('datas\\memory.json', 'w') as file:
                            json.dump(self.words, file)
                        
                    self.word_memory.clear()
                elif self.lineEdit.text().lower().replace(' ', '') == 'n':
                    if self.label.text() == "Change? (y/n)":
                        self.console_write('Change cancelled.', assets = False)

                        self.word_edit()
                    elif self.label.text() == "Add? (y/n)":
                        self.console_write('Add cancelled.', assets = False)

                        self.add_words()

                    self.word_memory.clear()
            elif self.lineEdit.text().lower() == 'study english word':
                self.word_study_find('İngilizce')
            elif self.lineEdit.text().lower() == 'study persian word':
                self.word_study_find('Türkçe')
            elif self.lineEdit.text().lower() == 'who is your father':
                with open('app_images\\a.txt', 'r', encoding = 'utf-8') as file:
                    image = file.readlines()

                    self.console_write(
                        '''{}\n\nOsman Kahraman'''.format(''.join(image)), assets = False
                    )
            elif self.lineEdit.text().lower() == 'edit word':
                self.word_edit()
            elif self.lineEdit.text().lower() == 'add word':
                self.add_words()
            elif self.lineEdit.text().lower() == 'cls':
                self.console_text = ''
                self.console_write('', assets = False)
            elif self.lineEdit.text().lower() == 'exit':
                self.close()
            elif self.lineEdit.text().lower() == "connect 4":
                self.connect_4 = Connect_4()
                self.game()
            elif self.lineEdit.text().lower() == 'about':
                self.about()
            elif self.lineEdit.text().lower() == 'commands':
                self.commands()
            elif self.lineEdit.text().lower() == 'new window':
                self.new_tab()
            elif self.lineEdit.text().lower() == 'settings':
                self.settings()
            elif self.lineEdit.text().lower() == 'open':
                self.console_write('To use that command, you should define a word group. (Exp. osm_kah open)', assets = False)
            elif self.lineEdit.text().lower().endswith(' open'):
                name = str(self.lineEdit.text()).rstrip(' open').lower()                
                        
                try:
                    self.words[name]
                except KeyError:
                    self.console_write('The word group is missing.', assets = False)
                else:
                    text = ''
                    for eng, tur in self.words[name].items():
                        gap_amount = 50
                        gap_amount -= len(eng)

                        line = '{gap}{eng_word} : {tur_word}\n'.format(gap = ' ' * gap_amount, eng_word = eng, tur_word = tur)

                        text += line
                    else:
                        gap_amount = None
                        line = None

                    self.console_write(text, assets = False)

                    del text, gap_amount, line

                del name
            elif self.lineEdit.text().lower().startswith('cd'):
                try:
                    PATH = self.lineEdit.text().lower().lstrip('cd ')

                    os.chdir(PATH)

                    del PATH
                except FileNotFoundError:
                    self.console_write('There is no PATH.')
            elif self.lineEdit.text().lower().startswith('version'):
                self.console_write(
                    '''
        v_3_1
    + app language transfered to english
    16.01.2025 Thursday 12:52 AM
                    ''', assets = False
                    )
            elif self.lineEdit.text().lower().startswith('update'):
                try: 
                    requests.get('https://www.python.org')
                except requests.exceptions.ConnectionError:
                    self.console_write(
                        'There is an error about internet connection, check it budy.', 
                        assets = False
                        )
                else:
                    wanted_version = self.lineEdit.text().lower().lstrip('update ')
                    self.close()
            elif self.lineEdit.text().lower() == 'dir':
                self.console_write(
                    '{dir}'.format(dir = str(list(self.words.keys())[1:]).replace(', ', '\n').lstrip('[').rstrip(']')), 
                    assets = False
                        )
            elif self.lineEdit.text().lower().startswith('export'):
                name = self.lineEdit.text().lower()[6:].replace(' ', '')
                if name:
                    try:
                        self.words[name]
                    except KeyError:
                        self.console_write("'{}' not found.".format(name), assets = False)
                    else:
                        PATH, _type = QtWidgets.QFileDialog.getSaveFileName(self, 'Please provide the export PATH.', os.getenv('DESKTOP'), 'Text file (*.txt);;Image file (*.png *.jpg)')

                        if PATH:
                            with open('datas\\memory2.json', 'r') as file:
                                self.data = json.loads(file.read())

                            text = ''
                            width = 0
                            for eng, tur in self.words[name].items():
                                gap_amount = 50
                                gap_amount = gap_amount - len(eng)

                                line = '{gap}{eng_word} : {tur_word}\n'.format(gap = ' ' * gap_amount, eng_word = eng, tur_word = tur)

                                if len(line) > width:
                                    width = len(line)

                                text += line
                                    
                            if _type == 'Text file (*.txt)':
                                PATH_ = PATH.rstrip('.txt')

                                self.data.update({'file_upload_PATH': PATH_ + '.txt'})

                                with open('{}.txt'.format(PATH_), 'w', encoding = 'utf-8') as file:
                                        file.write(text)
                            else:
                                PATH_ = PATH.rstrip('.png')

                                self.data.update({'file_upload_PATH': PATH_ + '.png'})

                                img = Image.new('RGB', (width * 10, 800), color = (255, 255, 255))
            
                                font = ImageFont.truetype(r'C:\\Windows\\Fonts\\Calibri\\calibri.ttf', 20) 
                                    
                                d = ImageDraw.Draw(img)
                                d.text((0, 20), text, font = font, fill = (0, 0, 0))

                                img.save('{}.png'.format(PATH_))

                            self.console_write("'{}', exported '{}'.".format(name, PATH), assets = False)

                            self.data.update({'file_upload_name': name})
                            with open('datas\\memory2.json', 'w') as file:
                                json.dump(self.data, file)

                            del text, PATH, PATH_
                        else:
                            self.console_write('Export cancelled.', assets = False)

                        del _type
                else:
                    self.console_write('Please provide a word group that you want to export. (Exp. export {})'.format(list(self.words.keys())[random.randrange(0, len(self.words.keys()))]), assets = False)

                del name
            elif self.lineEdit.text().lower().startswith('import'):
                PATH = self.lineEdit.text()[9:].strip(' ')
                if not PATH:
                    PATH, _type = QtWidgets.QFileDialog.getOpenFileName(self, 'Please provide the import PATH.', os.getenv('DESKTOP'), 'Text file (*.txt)')
                else:
                    PATH = PATH.replace("'", '')
                    PATH = PATH.replace('"', '')

                try:
                    with open(PATH, 'r', encoding = 'utf-8') as file:
                        words = file.read().split('\n')
                        
                        errors = ''
                        for word in words:
                            try:
                                eng_word, tur_word = word.split(':') if word.find(':') != -1 else word.split('-')
                            except ValueError:
                                gap_amount = 50
                                gap_amount -= len(word) // 2
                                errors += gap_amount * ' ' + word + '\n'

                                del gap_amount
                                continue

                            self.words['idle'].update({eng_word.strip(' '): tur_word.strip(' ')})

                            self.word_line += 1

                            if len(self.words['idle'].keys()) == 40:
                                a = list(self.words['idle'].keys())[-1]
                                b = self.words['idle'][a]

                                name = ('{first_third}_{last_third}'.format(first_third = a[:3], last_third = b[-3:])).lower()

                                self.words.update({
                                    name: self.words['idle'].copy()
                                    })

                                self.words['idle'].clear()
                                del a, b, name

                        with open('datas\\memory.json', 'w') as file:
                            json.dump(self.words, file)

                        text = 'Added {} words.'.format(len(words) - errors.count('\n'))

                        if errors:
                            text += '\n\nNot added words;\n{}'.format(errors)

                            with open('{}/errors.txt'.format(PATH[:-PATH[::-1].find('/')]), 'w', encoding = 'utf-8') as file:
                                file.write(errors)

                        self.console_write(text, assets = False)

                        del words, errors, text
                except FileNotFoundError:
                    self.console_write('You should provide a PATH for importing the words.', assets = False)
                del PATH
            else:
                self.console_write('WRONG COMMAND!', assets = False)

        self.lineEdit.clear()

class Ui_Dialog(object):
    def __init__(self) -> None:
        self.window_color_def = (25, 25, 25)
        self.line_color_def = (0, 0, 0)
        self.text_color_def = (232, 232, 232)
        self.font_def = 'Consolas,8,-1,5,75,0,0,0,0,0,Bold'
        self.words_splitter_def = ';'
        self.window_color = self.window_color_def
        self.line_color = self.line_color_def
        self.text_color = self.text_color_def
        self.font_ = self.font_def
        self.words_splitter = self.words_splitter_def

    def setupUi(self, Dialog, MainWindow):
        self.MainWindow_ = MainWindow
        self.Dialog_ = Dialog

        self.window_color = self.MainWindow_.window_color
        self.line_color = self.MainWindow_.line_color
        self.text_color = self.MainWindow_.text_color
        self.font_ = self.MainWindow_.font_
        self.words_splitter = self.MainWindow_.words_splitter

        self.Dialog_.setObjectName('Dialog')
        self.Dialog_.resize(284, 263)
        font = QtGui.QFont()
        font.setFamily(self.font_)
        self.Dialog_.setFont(font)
        self.palette = QtGui.QPalette()
        R, G, B = self.MainWindow_.window_color
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setColor(QtGui.QPalette.Button, QtGui.QColor(R, G, B))
        R, G, B = self.MainWindow_.text_color
        self.palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(R, G, B))
        self.palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(R, G, B))
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Window, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Window, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Window, 
            brush
            )
        self.Dialog_.setPalette(self.palette)

        self.Dialog_.setWindowOpacity(0.95)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName('tabWidget')
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName('tab')
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName('groupBox')
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName('widget')
        self.horizontalLayout_3.addWidget(self.widget)
        self.toolButton = QtWidgets.QToolButton(self.groupBox)
        self.toolButton.setObjectName('toolButton')
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.verticalLayout_10.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName('groupBox_2')
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.widget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_2.setObjectName('widget_2')
        self.horizontalLayout_4.addWidget(self.widget_2)
        self.toolButton_2 = QtWidgets.QToolButton(self.groupBox_2)
        self.toolButton_2.setObjectName('toolButton_2')
        self.horizontalLayout_4.addWidget(self.toolButton_2)
        self.verticalLayout_10.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, '')
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName('tab_2')
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName('groupBox_4')
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.widget_3 = QtWidgets.QWidget(self.groupBox_4)
        self.widget_3.setObjectName('widget_3')
        self.horizontalLayout_2.addWidget(self.widget_3)
        self.toolButton_4 = QtWidgets.QToolButton(self.groupBox_4)
        self.toolButton_4.setObjectName('toolButton_4')
        self.horizontalLayout_2.addWidget(self.toolButton_4)
        self.verticalLayout_5.addWidget(self.groupBox_4)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName('groupBox_3')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName('label')
        self.horizontalLayout.addWidget(self.label)
        self.toolButton_3 = QtWidgets.QToolButton(self.groupBox_3)
        self.toolButton_3.setObjectName('toolButton_3')
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_2, '')
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName('tab_3')
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName('groupBox_5')
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_5)
        self.horizontalSlider.setProperty('value', 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalLayout_4.addWidget(self.horizontalSlider)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_6.setObjectName('groupBox_6')
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.label_2 = QtWidgets.QLabel(self.groupBox_6)
        self.label_2.setObjectName('label_2')
        self.horizontalLayout_5.addWidget(self.label_2)
        self.toolButton_5 = QtWidgets.QToolButton(self.groupBox_6)
        self.toolButton_5.setObjectName('toolButton_5')
        self.horizontalLayout_5.addWidget(self.toolButton_5)
        self.verticalLayout_6.addWidget(self.groupBox_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_3, '')
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName('tab_4')
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName('groupBox_7')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName('verticalLayout')
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton.setObjectName('radioButton')
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton_2.setObjectName('radioButton_2')
        if self.words_splitter == ';':
            self.radioButton.setChecked(True)
        elif self.words_splitter == ':':
            self.radioButton_2.setChecked(True)
        self.verticalLayout.addWidget(self.radioButton_2)
        self.keySequenceEdit = QtWidgets.QKeySequenceEdit(self.groupBox_7)
        self.keySequenceEdit.setObjectName('keySequenceEdit')
        self.verticalLayout.addWidget(self.keySequenceEdit)
        self.verticalLayout_9.addWidget(self.groupBox_7)
        self.verticalLayout_3.addLayout(self.verticalLayout_9)
        spacerItem3 = QtWidgets.QSpacerItem(20, 153, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.tabWidget.addTab(self.tab_4, '')
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName('buttonBox')
        self.verticalLayout_2.addWidget(self.buttonBox)

        R, G, B = self.text_color
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(R, G, B))
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText, 
            brush
            )
        self.groupBox.setPalette(self.palette)
        self.groupBox_2.setPalette(self.palette)
        self.groupBox_3.setPalette(self.palette)
        self.groupBox_4.setPalette(self.palette)
        self.groupBox_5.setPalette(self.palette)
        self.groupBox_6.setPalette(self.palette)
        self.groupBox_7.setPalette(self.palette)
        self.Dialog_.setPalette(self.palette)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.accept_)
        self.buttonBox.rejected.connect(self.reject_)
        self.toolButton.clicked.connect(lambda: self.color('window_color'))
        self.toolButton_2.clicked.connect(lambda: self.color('line_color'))
        self.toolButton_3.clicked.connect(self.font)
        self.toolButton_4.clicked.connect(lambda: self.color('text_color'))
        self.radioButton.clicked.connect(self.radio_butt)
        self.radioButton_2.clicked.connect(self.radio_butt)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog_.setWindowTitle(_translate('Dialog', 'Settings'))
        self.groupBox.setWhatsThis(_translate('Dialog', 'It customizes the window color.'))
        self.groupBox.setTitle(_translate('Dialog', 'Color'))
        self.toolButton.setText(_translate('Dialog', 'Choose'))
        self.groupBox_2.setWhatsThis(_translate('Dialog', 'It customizes the line color from bottom side of the window.'))
        self.groupBox_2.setTitle(_translate('Dialog', 'Line color'))
        self.toolButton_2.setText(_translate('Dialog', 'Choose'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate('Dialog', 'Window'))
        self.groupBox_4.setWhatsThis(_translate('Dialog', 'It changes the text color.'))
        self.groupBox_4.setTitle(_translate('Dialog', 'Color'))
        self.toolButton_4.setText(_translate('Dialog', 'Choose'))
        self.groupBox_3.setWhatsThis(_translate('Dialog', 'It changes the font style.'))
        self.groupBox_3.setTitle(_translate('Dialog', 'Font'))
        self.label.setText(_translate('Dialog', self.font_))
        self.toolButton_3.setText(_translate('Dialog', 'Choose'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate('Dialog', 'Font style'))
        self.groupBox_5.setWhatsThis(_translate('Dialog', 'Changes volume.'))
        self.groupBox_5.setTitle(_translate('Dialog', 'Volume level'))
        self.groupBox_6.setWhatsThis(_translate('Dialog', 'It customizes the keyboard sound.'))
        self.groupBox_6.setTitle(_translate('Dialog', 'Keyboard sound'))
        self.label_2.setText(_translate('Dialog', '#sound.mp3'))
        self.toolButton_5.setText(_translate('Dialog', 'Seç'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate('Dialog', 'Volume'))
        self.groupBox_7.setWhatsThis(_translate('Dialog', 'It changes seperator character of the words.'))
        self.groupBox_7.setTitle(_translate('Dialog', 'Word seperator'))
        self.radioButton.setText(_translate('Dialog', ';'))
        self.radioButton_2.setText(_translate('Dialog', ':'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate('Dialog', 'Other'))
    
    def accept_(self):
        self.MainWindow_.data.update({
            'window_color': self.window_color,
            'line_color': self.line_color,
            'text_color': self.text_color,
            'font': self.font_,
            'split': self.words_splitter})

        with open('datas\\memory2.json', 'w') as file:
            json.dump(self.MainWindow_.data, file)
        self.Dialog_.accept()

    def reject_(self):
        with open('datas\\memory2.json', 'r') as file:
            data = json.loads(file.read())
        
        self.color('window_color', data['window_color'])
        self.color('line_color', data['line_color'])
        self.color('text_color', data['text_color'])
        self.font(self, data['font'])

        self.Dialog_.reject()
    
    def reset(self):
        self.color('window_color', self.window_color_def)
        self.color('line_color', self.line_color_def)
        self.color('text_color', self.text_color_def)
        self.font(self, self.font_def)

    def color(self, button: str, RGB: list or tuple = None):
        if RGB == None:
            picked_color = QtWidgets.QColorDialog.getColor()
            R, G, B, A = picked_color.getRgb()
        else:
            R, G, B = RGB

        if button == 'window_color':
            self.window_color = (R, G, B)
            self.MainWindow_.window_color = (R, G, B)

            brush = QtGui.QBrush(QtGui.QColor(R, G, B))
            brush.setStyle(QtCore.Qt.SolidPattern)
            self.palette.setBrush(
                QtGui.QPalette.Active,
                QtGui.QPalette.Window, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Inactive,
                QtGui.QPalette.Window, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Disabled,
                QtGui.QPalette.Window, 
                brush
                )
            self.palette.setColor(QtGui.QPalette.Button, QtGui.QColor(R, G, B))
            self.palette.setBrush(
                QtGui.QPalette.Active,
                QtGui.QPalette.Text, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Active,
                QtGui.QPalette.Base, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Active,
                QtGui.QPalette.Highlight, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Inactive,
                QtGui.QPalette.Text, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Inactive,
                QtGui.QPalette.Base, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Inactive,
                QtGui.QPalette.Highlight, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Disabled,
                QtGui.QPalette.Text, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Disabled,
                QtGui.QPalette.Base, 
                brush
                )
            self.MainWindow_.setPalette(self.palette)
            self.Dialog_.setPalette(self.palette)
            self.groupBox.setPalette(self.palette)
            self.groupBox_2.setPalette(self.palette)
            self.groupBox_3.setPalette(self.palette)
            self.groupBox_4.setPalette(self.palette)
            self.groupBox_5.setPalette(self.palette)
            self.groupBox_6.setPalette(self.palette)
            self.groupBox_7.setPalette(self.palette)
        elif button == 'line_color':
            self.line_color = (R, G, B)
            self.MainWindow_.line_color = self.line_color
        elif button == 'text_color':
            self.text_color = (R, G, B)
            self.MainWindow_.text_color = (R, G, B)
            
            brush = QtGui.QBrush(QtGui.QColor(R, G, B))
            brush.setStyle(QtCore.Qt.SolidPattern)
            
            self.palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(R, G, B))
            self.palette.setBrush(
                QtGui.QPalette.Active,
                QtGui.QPalette.WindowText, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Inactive,
                QtGui.QPalette.WindowText, 
                brush
                )
            self.palette.setBrush(
                QtGui.QPalette.Disabled,
                QtGui.QPalette.WindowText, 
                brush
                )
            self.MainWindow_.label.setPalette(self.palette)
            self.MainWindow_.label_2.setPalette(self.palette)
            self.MainWindow_.setPalette(self.palette)
            self.Dialog_.setPalette(self.palette)
            self.groupBox.setPalette(self.palette)
            self.groupBox_2.setPalette(self.palette)
            self.groupBox_3.setPalette(self.palette)
            self.groupBox_4.setPalette(self.palette)
            self.groupBox_5.setPalette(self.palette)
            self.groupBox_6.setPalette(self.palette)
            self.groupBox_7.setPalette(self.palette)

    def font(self, foo, a = None):
        if a == None:
            font, valid = QtWidgets.QFontDialog.getFont()
        else:
            font = QtGui.QFont()
            font.setFamily(a)
            self.Dialog_.setFont(font)
            self.palette = QtGui.QPalette()
            valid = True

        if valid:
            self.font_ = font.toString()
            self.MainWindow_.font_ = self.font_
            self.MainWindow_.label.setFont(font)
            self.MainWindow_.label_2.setFont(font)
            self.MainWindow_.setFont(font)
            self.Dialog_.setFont(font)

            self.label.setText(self.font_)
    
    def radio_butt(self):
        if self.radioButton.isChecked():
            self.words_splitter = ';'
            self.MainWindow_.words_splitter = ';'
        elif self.radioButton_2.isChecked():
            self.words_splitter = ':'
            self.MainWindow_.words_splitter = ':'

class QLineEdit_(QtWidgets.QLineEdit):
    def __init__(self, window, *args, **kwargs):
        QtWidgets.QLineEdit.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.window = window

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == 94:
            return True
        else:
            if self.window.lineEdit.text() in self.window.command_names.keys():
                self.window.lineEdit.setStatusTip(self.window.command_names[self.window.lineEdit.text()])
            else:
                self.window.lineEdit.setStatusTip(" ")
            return QtWidgets.QLineEdit.event(self, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text().lstrip('file:///')
        if self.window.pushButton.text() == 'Change':
            with open(text, "r", encoding = 'utf-8') as file:
                words = file.read().split('\n')

                for word in words:
                    eng_word, tur_word = word.split(':') if word.find(':') != -1 else word.split('-')

                    self.window.word_memory.append(eng_word)
                    self.window.word_memory.append(tur_word)
            self.window.label.setText('Change? (y/n)')
            self.window.pushButton.setText('↑')
        else:
            self.setText('import {}'.format(text))
        event.acceptProposedAction()

class Connect_4(object):
    def __init__(self) -> None:
        self.col_codex = 'abcdefghi'
        self.ln_codex = range(1, 10)

        self.place = ''

        self.memory, self.turn = {col + str(ln): ' ' for col in self.col_codex for ln in self.ln_codex}, 'X'
        self.over = False

    def ui(func):
        def wrapper(*args, **kwargs):
            logo = """
       ______                            __     ______                
      / ____/___  ____  ____  ___  _____/ /_   / ____/___  __  _______
     / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/  / /_  / __ \/ / / / ___/
    / /___/ /_/ / / / / / / /  __/ /__/ /_   / __/ / /_/ / /_/ / /    
    \____/\____/_/ /_/_/ /_/\___/\___/\__/  /_/    \____/\__,_/_/     \n\n\n
"""
            foo = func(*args, **kwargs)
            new = ''
            for i in foo.split('\n'):
                new += '\t\t\t\t{}\n'.format(i)

            return logo + new
        return wrapper
    
    @ui
    def playground(self) -> str:
        if self.over:
            return self.celebration(self.turn)
        else:
            sidewalls = 'Π'
            for key, value in self.memory.items():
                sidewalls += value

                if key[1] == '9':
                    if key[0] == 'i':
                        sidewalls += 'Π\n'
                    elif key[0] == 'd':
                        sidewalls += "Π\t{}'s turn\nΠ".format(self.turn)
                    else:
                        sidewalls += 'Π\nΠ'
            ground = 'Ξ' * 11

            return sidewalls + ground
    
    def celebration(self, winner: str):
        fireworks = """               *    *
   *         '       *       .  *   '     .           * *
                                                               '
   *                     *'          *          *        '
   .         *                 |               /
               '.         |    |        '     |    '      *
                 \*        \   \             / 
       '          \    '*  |    |    *      |*                  *  *
            *      `.       \   |      *     /      *      '
  .                  \      |   \          /                *
     *'  *     '      \      \   '.       |
        -._            `                  /            *
  ' '      ``._   *                           '          .      '
   *           *\*          * .   .      *
*  '        *    `-._                       .         _..:='          *
             .  '      *       *    *   .       _.:--'
    *                  . The END, {} won!-'              *
   .               '             . '   *           *         .
  *       ___.-=--..-._     *                '               '
                                  *       *
            *           _.'  .'       `.        '   *              *
    *            *  _.-'   .'            `.               *
                   .'                       `._             *  '
   '       '                        .       .  `.     .
       .                    *                    `
               *        '             '                          .
     .                         *          .           *  *
         *          .                                    '-""".format(winner)
        
        self.memory, self.turn = {col + str(ln): ' ' for col in self.col_codex for ln in self.ln_codex}, 'X'

        return fireworks

    def input(self, move: int) -> None:
        try:
            if int(move) in range(1, 10):
                self.brain(move)
        except ValueError:
            pass

    def brain(self, input):
        def check(place: str) -> bool:
            col, ln = place

            col_ = self.col_codex.find(col)
            ln_ = int(ln)
            horizontal_check = ''
            vertical_check = ''
            cross_check_1 = ''
            cross_check_2 = ''
            for h, v, nh in zip(range(ln_ - 3, ln_ + 4), range(col_ - 3, col_ + 4), range(ln_ + 4, ln_ - 3, -1)):
                try:
                    horizontal_check += self.memory[col + str(h)] #Horizontal
                except:
                    pass
                try:
                    vertical_check += self.memory[self.col_codex[v] + ln] #Vertical
                except:
                    pass
                try:
                    cross_check_1 += self.memory[self.col_codex[v] + str(h)] #Left to right cross
                except:
                    pass
                try:
                    cross_check_2 += self.memory[self.col_codex[v] + str(nh)] #Right to left cross
                except:
                    pass

            con = self.turn * 4
            if horizontal_check.find(con) != -1 or vertical_check.find(con) != -1 or cross_check_1.find(con) != -1 or cross_check_2.find(con) != -1:
                return True

            return False
        
        queue = -1
        while True:
            try:
                self.col_codex[queue]
            except IndexError:
                break
            else:
                if self.memory[self.col_codex[queue] + input] == ' ':
                    self.memory[self.col_codex[queue] + input] = self.turn
                    self.place = self.col_codex[queue] + input

                    if check(self.col_codex[queue] + input):
                        self.over = True
                    else:
                        self.turn = 'O' if self.turn == 'X' else 'X'

                    break
                else:
                    queue -= 1

def run(*args, **kwargs):
    if __name__ != '__main__' and check.run():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')

        ui = Ui_MainWindow()
        ui.show()

        app.exec_()

        del app, ui
        return {
            'wanted_version': wanted_version
        }
