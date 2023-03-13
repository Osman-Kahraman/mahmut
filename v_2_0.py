# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import random, time, os, numpy, warnings, json, sqlite3, sys
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import check

warnings.filterwarnings('ignore')

wanted_version = None
class Ui_MainWindow(object):
    def __init__(self):
        #-Preparing-----------------------------------------------------------------------------------
        if "datas" not in os.listdir():
            os.mkdir("datas")

        self.ab = 0
        self.de = 0
        self.da = []
        self.ce = 0
        self.word_info_timer = 1
        self.R = 0
        self.G = 0
        self.B = 0
        self.console_text_memory = "\tCopyright @Osman-Kahraman\n\tContact on o_kahraman@outlook.com\n\n\n"
        self.word_memory = list()
        self.fig_memory = {
            "eng": [], 
            "tur": []
            }
        self.words = {"idle": {}}
        self.word_line = 0
        try:
            with open("datas\\memory.json", "r") as file:
                self.words = json.loads(file.read())

                self.word_line = sum([len(self.words[name]) for name in self.words.keys()])
        except FileNotFoundError:
            try:
                with open("Kelimeler.txt", "r", encoding = "utf-8") as file:
                    words_part = []
                    for text in file.readlines():
                        if text != "---------------------------------------------------------------------------------------------------------------------------\n":
                            words_part.append(tuple(text.replace("\n", "").rstrip(" ").lstrip(" ").split(" : ")))
                            self.word_line += 1
                        else:
                            if self.word_line != 0:
                                last_line = "".join(words_part[-1]).replace(" ", "")
                                
                                name = ("{first_third}_{last_third}".format(first_third = last_line[:3], last_third = last_line[-3:])).lower()

                                if not name in self.words.keys():
                                    self.words.update({
                                        name: dict(words_part)
                                        })

                            words_part = []
                    with open("datas\\memory.json", "w") as file:
                        json.dump(self.words, file)

                os.remove("Kelimeler.txt")
                os.remove("Çalışılacak Kelimeler.txt")
                del words_part, last_line
            except FileNotFoundError:
                with open("datas\\memory.json", "w") as file:
                    json.dump(self.words, file)
        else:
            self.con = sqlite3.connect("datas\\statistics.db")
            self.cursor = self.con.cursor()

            try:
                self.cursor.execute("Select * From data")
            except:
                self.words_scores_data = {}
            else:
                self.words_scores_data = dict([(name, {"eng": eng_scores, "tur": tur_scores}) for name, eng_scores, tur_scores in self.cursor.fetchall()])
        #---------------------------------------------------------------------------------------------

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(960, 320)
        MainWindow.setMinimumSize(QtCore.QSize(960, 240))
        self.palette = QtGui.QPalette()
        dark_gray_brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
        dark_gray_brush.setStyle(QtCore.Qt.SolidPattern)
        light_gray_brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        light_gray_brush.setStyle(QtCore.Qt.SolidPattern)

        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Window, 
            dark_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Window, 
            dark_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Window, 
            dark_gray_brush
            )
        MainWindow.setPalette(self.palette)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app_images\\terim.jpg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.95)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 1, 620, 189))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents
            )
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.WindowText, 
            light_gray_brush
            )
        self.label_2.setPalette(self.palette)

        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)

        self.label_2.setFont(font)
        self.label_2.setText("\tCopyright @Osman-Kahraman\n\tContact on o_kahraman@outlook.com\n\n\n")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(MainWindow)

        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.WindowText, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.WindowText, 
            light_gray_brush
            )
        self.label.setPalette(self.palette)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit(MainWindow)

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
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Base, 
            dark_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Text, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Base, 
            dark_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Text, 
            light_gray_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.Base, 
            dark_gray_brush
            )
        self.lineEdit.setPalette(self.palette)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QtWidgets.QFrame(self.centralwidget)

        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(50)
        self.line.setMidLineWidth(50)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.A = QtWidgets.QMenu(self.menubar)
        self.A.setObjectName("menuKonsol")
        self.menuKelime = QtWidgets.QMenu(self.menubar)
        self.menuKelime.setObjectName("menuKelime")
        self.menuYardım = QtWidgets.QMenu(self.menubar)
        self.menuYardım.setObjectName("menuYardım")
        self.menu_al = QtWidgets.QMenu(self.menuKelime)
        self.menu_al.setObjectName("menu_al")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionKonsol = QtWidgets.QAction(MainWindow)
        self.actionKonsol.setObjectName("actionA")
        self.actionYeni_Pencere = QtWidgets.QAction(MainWindow)
        self.actionYeni_Pencere.setObjectName("actioYeni_Sekmede_Aç")
        self.actionEkle = QtWidgets.QAction(MainWindow)
        self.actionEkle.setObjectName("actionEkle")
        self.action_ngilizce = QtWidgets.QAction(MainWindow)
        self.action_ngilizce.setObjectName("action_ngilizce")
        self.actionT_rk_e = QtWidgets.QAction(MainWindow)
        self.actionT_rk_e.setObjectName("actionT_rk_e")
        self.actionKomutlar = QtWidgets.QAction(MainWindow)
        self.actionKomutlar.setObjectName("actionKomutlar")
        self.A.addAction(self.actionKonsol)
        self.A.addAction(self.actionYeni_Pencere)
        self.menu_al.addAction(self.action_ngilizce)
        self.menu_al.addAction(self.actionT_rk_e)
        self.menuKelime.addAction(self.actionEkle)
        self.menuYardım.addAction(self.actionKomutlar)
        self.menubar.addAction(self.A.menuAction())
        self.menuKelime.addAction(self.menu_al.menuAction())
        self.menubar.addAction(self.menuKelime.menuAction())
        self.menubar.addAction(self.menuYardım.menuAction())
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.console_text_prepare)
        self.line_check_timer = QtCore.QTimer(self)
        self.line_check_timer.timeout.connect(self.line_check)
        self.line_check_timer.start(40)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionKonsol.triggered.connect(self.console)
        self.actionYeni_Pencere.triggered.connect(self.new_tab)
        self.action_ngilizce.triggered.connect(self.study_words_eng)
        self.actionT_rk_e.triggered.connect(self.study_words_tur)
        self.actionKomutlar.triggered.connect(self.commands)
        self.actionEkle.triggered.connect(self.addWords)
        self.pushButton.clicked.connect(self.click)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrolled)

        self.console()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "Mahmut"))
        self.A.setTitle(_translate("MainWindow", "Aç"))
        self.menuKelime.setTitle(_translate("MainWindow", "Kelime"))
        self.menuYardım.setTitle(_translate("MainWindow", "Yardım"))
        self.menu_al.setTitle(_translate("MainWindow", "Çalış"))
        self.actionKonsol.setText(_translate("MainWindow", "Konsol"))
        self.actionKonsol.setShortcut(_translate("MainWindow", 'Ctrl+"'))
        self.actionYeni_Pencere.setText(_translate("MainWindow", "Yeni Pencere"))
        self.actionYeni_Pencere.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actionEkle.setText(_translate("MainWindow", "Ekle"))
        self.actionEkle.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.action_ngilizce.setText(_translate("MainWindow", "İngilizce"))
        self.actionT_rk_e.setText(_translate("MainWindow", "Türkçe"))
        self.actionKomutlar.setText(_translate("MainWindow", "Komutlar"))

    def new_tab(self):
        ui = KeyTracker()
        ui.show()

    def line_check(self):
        if self.centralwidget.width() != self.ab:
            text = self.console_text_memory.replace("₺+", int(self.centralwidget.width() * 0.158) * "+").replace("₺-", int(self.centralwidget.width() * 0.1) * "-")
            self.label_2.setText(text)

            del text
            self.ab = self.centralwidget.width()

        time = Qt.QTime.currentTime()
        value = int(time.toString("ss"))

        if self.ce + value > 255:
            self.ce = 0
        else:
            self.ce += 5
        self.color(self.ce + value + self.R, self.ce + value + self.G, self.ce + value + self.B)

    def scrolled(self):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def commands(self):
        self.console_text(
                """
kd <dosya yolu>: Bulunulan dosya konumunu değiştirir.
<dosya> aç: Kelime grubunu açar.
versiyon: Kullanılan sürümle ilgili bilgi verir.
güncelle <versiyon>: İstenilen versiyona günceller.
dışa aktar <kelime grup ismi>: İstenilen kelime grubunu dışarıya aktarır.
dir: Bütün kelime grup isimlerini gösterir.
cls: Geçmişi temizler.
₺+              """, assets = False
                )

    def console_text_prepare(self):
        if self.da:
            try:
                self.console_text_memory += self.da[0][self.de] + "\n"
                self.de += 1

                text = self.console_text_memory.replace("₺+", int(self.centralwidget.width() * 0.158) * "+").replace("₺-", int(self.centralwidget.width() * 0.1) * "-")
                self.label_2.setText(text)
            except IndexError:
                self.da.remove(self.da[0])
                self.de = 0
        else:
            self.timer.stop()

    def console_text(self, text, assets = True):
        template = "{PATH}>>> [{time}] ".format(PATH = os.getcwd(), time = time.strftime("%H: %M: %S")) if assets else ""
        template += str(text)

        self.da.append(template.split("\n"))
        self.timer.start(1)

        del template

    def color(self, R, G, B):
        light_brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        light_brush.setStyle(QtCore.Qt.SolidPattern)

        R /= 1.5
        G /= 1.5
        B /= 1.5

        dark_brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        dark_brush.setStyle(QtCore.Qt.SolidPattern)

        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Light, 
            dark_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Light, 
            dark_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Mid, 
            light_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Mid, 
            light_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Dark, 
            dark_brush
            )
        self.palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Dark, 
            dark_brush
            )
        self.line.setPalette(self.palette)

        del light_brush, dark_brush, R, G, B

    def console(self):
        self.label.setText(os.getcwd() + ">>> ")
        self.R = 0
        self.G = 0
        self.B = 0

        if self.fig_memory["eng"] and self.fig_memory["tur"] and check.run():
            self.cursor.execute("Select * From data")

            queueScore_Eng = float("{:.2f}".format(sum(self.fig_memory["eng"]) / len(self.fig_memory["eng"])))
            queueScore_Tur = float("{:.2f}".format(sum(self.fig_memory["tur"]) / len(self.fig_memory["tur"])))

            try:
                queueScores_Eng = self.words_scores_data[self.name]["eng"].lstrip("[").rstrip("]").split(",")
                queueScores_Tur = self.words_scores_data[self.name]["tur"].lstrip("[").rstrip("]").split(",")

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
                self.cursor.execute("Update data set scoresEng = ?, scoresTur = ? where queue_names = ?", (str(queueScores_Eng), str(queueScores_Tur), self.name))
            except:
                self.cursor.execute("Insert into data Values(?, ?, ?)", (self.name, str(queueScores_Eng), str(queueScores_Tur)))
            self.con.commit()

            if len(queueScores_Eng) > 1:
                fig = plt.figure()
                graphic = fig.add_axes([0.1, 0.1, 0.8, 0.8])

                boolen_values_eng, boolen_values_tur = numpy.array(queueScores_Eng), numpy.array(queueScores_Tur)
                values_len = numpy.array(range(len(queueScores_Eng)))

                graphic.plot(values_len, boolen_values_eng, "blue", marker = "o", label = "İngilizce")
                graphic.plot(values_len, boolen_values_tur, "red", marker = "o", label = "Türkçe")

                graphic.legend()
                graphic.set_ylim(-0.1, 1.1)
                graphic.set_xlabel("Çalışma Sayısı")
                graphic.set_ylabel("Skorlar")
                graphic.set_title("Skor Grafiği")

                plt.show()

                del fig, graphic, boolen_values_eng, boolen_values_tur, values_len

            self.fig_memory["eng"].clear()
            self.fig_memory["tur"].clear()
            del queueScore_Eng, queueScore_Tur, queueScores_Eng, queueScores_Tur

        if self.pushButton.text() != "↑":
            self.pushButton.setText("↑")

    def addWords(self):
        self.lineEdit.clear()
        self.R = 0
        self.G = 0
        self.B = 0

        text = "Satır sayısı: " + str(self.word_line)
        if self.pushButton.text() != "Ekle":
            self.console_text("{gaps}\n{line_number_text}".format(gaps = 25 * " " + "₺-", line_number_text = (150 - len(text)) * " " + text), assets=False)

        self.label.setText("İngilizcesi:")
        self.pushButton.setText("Ekle")

        del text

    def word_info(self):
        s = self.tur_words[0] if self.language == "eng" else self.eng_words[0]

        self.console_text(s[:self.word_info_timer] + (len(s) - (self.word_info_timer)) * "-", assets = False)
        self.word_info_timer += 1

    def study_words_eng(self):
        self.lineEdit.clear()
        self.R = -100
        self.G = -100
        self.B = 0

        if not (self.fig_memory["tur"] or self.fig_memory["eng"]):
            try:
                with open("datas\\memory2.json", "r") as file:
                    data = json.loads(file.read())

                if os.path.isfile(data["file_upload_PATH"]):
                    qm = QtWidgets.QMessageBox
                    ret = qm.question(self, "Halihazırda Bir Kelime Grubu Bulundu", "{} ile mi çalışacaksın?\t\t\t".format(data["file_upload_name"]))

                    if ret == 16384:
                        self.study_words("eng", data["file_upload_name"])
                    else:
                        raise FileNotFoundError
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                self.label.setText("İsim:")
                self.pushButton.setText("İngilizce Başlat")
                self.console_text(
                        "İngilizce kelime çalışmaya başlamak için lütfen çalışmak istediğiniz bölümün ismini giriniz."
                        )
        else:
            self.study_words("eng", self.name)

    def study_words_tur(self):
        self.lineEdit.clear()
        self.R = 0
        self.G = -100
        self.B = -100

        if not (self.fig_memory["tur"] or self.fig_memory["eng"]):
            try:
                with open("datas\\memory2.json", "r") as file:
                    data = json.loads(file.read())

                if os.path.isfile(data["file_upload_PATH"]):
                    qm = QtWidgets.QMessageBox
                    ret = qm.question(self, "Halihazırda Bir Kelime Grubu Bulundu", "{} ile mi çalışacaksın?\t\t\t".format(data["file_upload_name"]))

                    if ret == 16384:
                        self.study_words("tur", data["file_upload_name"])
                    else:
                        raise FileNotFoundError
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                self.label.setText("İsim:")
                self.pushButton.setText("Türkçe Başlat")
                self.console_text(
                        "Türkçe kelime çalışmaya başlamak için lütfen çalışmak istediğiniz bölümün ismini giriniz."
                        )
        else:
            self.study_words("tur", self.name)

    def study_words(self, language, name):
        self.lineEdit.clear()
        self.pushButton.setText("Kontrol Et")

        self.language = language
        self.name = name
        words_to_study = self.words[self.name]

        random_number = random.randrange(start = 0, stop = len(words_to_study.keys()))

        eng_words, tur_words = list(words_to_study.items())[random_number]
        self.eng_words = eng_words.split("; ")
        self.tur_words = tur_words.split("; ")

        text = self.eng_words[random.randint(0, len(self.eng_words) - 1)] if self.language == "eng" else self.tur_words[random.randint(0, len(self.tur_words) - 1)]
        self.label.setText(text)

        del words_to_study, random_number, eng_words, tur_words, text

    def click(self):
        global wanted_version

        if self.pushButton.text() == "Kontrol Et":
            self.console_text(self.lineEdit.text())

            user_text = self.lineEdit.text().lower().replace(" ", "")
            words_to_study = self.tur_words if self.language == "eng" else self.eng_words
            s = self.fig_memory["eng"] if self.language == "eng" else self.fig_memory["tur"]
                
            correct_words = [word.lower().replace(" ", "") for word in words_to_study]

            if user_text in correct_words:
                a = correct_words.index(user_text)
                    
                text = "d0ru Cevap" if len(words_to_study) == 1 else  "d0ru Cevap\nDiğer anlamları; " + str(words_to_study[0:a] + words_to_study[a + 1:])
                    
                self.console_text(text)

                self.study_words(self.language, self.name)

                try:
                    false_ratio = float("{:.2f}".format(1 / (len(words_to_study[0]) // (self.word_info_timer - 1)))) if user_text == correct_words[0] else 0
                except ZeroDivisionError:
                    false_ratio = 0

                s.append(1 - false_ratio)
                self.word_info_timer = 1

                del a
            else:
                self.console_text("Yanlış Cevap")

                s.append(0)

            del user_text, words_to_study, s, correct_words
        elif self.pushButton.text() == "İngilizce Başlat":
            self.console_text("{} açılıyor.".format(self.lineEdit.text()))
            self.console_text(25 * " " + 100 * "-", assets = False)
            self.study_words("eng", self.lineEdit.text())
        elif self.pushButton.text() == "Türkçe Başlat":
            self.console_text("{} açılıyor.".format(self.lineEdit.text()))
            self.console_text(25 * " " + 100 * "-", assets = False)
            self.study_words("tur", self.lineEdit.text())
        elif self.pushButton.text() == "Ekle" and self.lineEdit.text():
            if self.label.text() == "İngilizcesi:":
                self.label.setText("Türkçesi:")

                self.word_memory.append(self.lineEdit.text())

                self.console_text("İngilizce kelime: " + self.lineEdit.text())
            elif self.label.text() == "Türkçesi:":
                self.label.setText("İngilizcesi:")

                self.word_memory.append(self.lineEdit.text())

                self.console_text("Türkçe kelime: " + self.lineEdit.text())

            if len(self.word_memory) == 2:
                self.label.setText("Ekle? (e/h)")
                self.pushButton.setText("↑")
        else:
            self.console_text(self.lineEdit.text())

            if self.lineEdit.text().lower().rstrip(" ") == "baban kim?":
                self.console_text("Osman Kahraman")
                with open("app_images\\a.txt", "r", encoding = "utf-8") as file:
                    image = file.readlines()

                    self.console_text(
                        """
Osman Kahraman

{}
                        """.format("".join(image)), assets = False
                    )
            elif self.lineEdit.text().lower().endswith(" aç"):
                name = str(self.lineEdit.text()).rstrip(" aç").lower()                
                    
                try:
                    self.words[name]
                except KeyError:
                    self.console_text("İsim bulunamadı.")
                else:
                    text = ""
                    for eng, tur in self.words[name].items():
                        gap_amount = 50
                        gap_amount = gap_amount - len(eng)

                        line = "{gap}{eng_word} : {tur_word}\n".format(gap = " " * gap_amount, eng_word = eng, tur_word = tur)

                        text += line
                    else:
                        gap_amount = None
                        line = None

                    self.console_text(
                        """{} açılıyor.
{}
                        """.format(name, text)
                        )

                    del text, gap_amount, line

                del name
            elif self.lineEdit.text().lower().startswith("kd"):
                try:
                    PATH = self.lineEdit.text().lower().lstrip("kd ")
                    self.label.setText(PATH)

                    os.chdir(PATH)

                    del PATH
                except FileNotFoundError:
                    self.console_text("Dosya yolu bulunamadı.")
            elif self.lineEdit.text().lower().startswith("versiyon"):
                self.console_text(
                    """
    v_2_0
₺-
+ Pratiklik sağlayan 'Enter' tuş kısayolu eklendi. (Güzel parmakların yorulmayacak. )
+ Veritabanında performans iyileştirmesi yapıldı. (Bilgisayarın rahat edecek. )
+ Yardım butonu getirildi. (Komut ezberleme zahmetinden kurtuldun. )
+ Çalışılacak Kelimeler.txt'yi ayrıca açmak yerine (eğer yeniysen bilmezsin) program arayüzünde kelimelerin açılması için yeni komutlar getirildi. (Bunun için Yardım butonuna tıklayabilirsin. )
+ Konsol ekranındaki karışıklık düzeltildi. (Ne nerede daha az yorulacaksın. )
+ Yeni gelen dışa aktarma özelliğiyle artık gün içinde de akıllı cihazlarından kelime çalışabilirsin. (Tabi önce dışa aktarılan dosyayı cihaza taşıman gerekiyor. )
+ Artık bilemediğin kelimeler için yardım sistemi geldi. (Yardım sistemini kullanmak için 'Alt + 3' tuş kombinasyonunu kullanman yeterli. )
+ Kelime çalışırken yardım-ceza sistemi getirildi. (Ne kadar yardım, o kadar ceza. )
+ Rastgele kelime sorma sistemi değiştirildi. (Art arda aynı kelimeler artık hiç gelmeyecek, böylece hiç sorulmamış kelimelerin daha fazla söz hakkı olacak.)
+ Çeşitli görsel düzeltmeler yapıldı. 
₺-
21.03.2021 Perşembe 01:23
₺+                  """, assets = False
                    )
            elif self.lineEdit.text().lower().startswith("güncelle"):
                wanted_version = self.lineEdit.text().lower().lstrip("güncelle ")

                self.console_text(
                    "Güncellenmek istenen sürüm ayarlandı.\nArka plandaki köle robotların yeni sürümü eklemesi için lütfen programı kapatın."
                    )
            elif self.lineEdit.text().lower() == "dir":
                self.console_text(
                    """
{dir}
₺+                  """.format(dir = str(list(self.words.keys())[1:]).replace(", ", "\n").lstrip("[").rstrip("]"))
                    )
            elif self.lineEdit.text().lower() == "cls":
                self.console_text_memory = "\tCopyright @Osman-Kahraman\n\tContact on o_kahraman@outlook.com\n\n\n"
                self.console_text("", assets = False)
            elif self.lineEdit.text().lower().startswith("dışa aktar"):
                name = self.lineEdit.text().lower()[10:].replace(" ", "")
                if name:
                    try:
                        self.words[name]
                    except KeyError:
                        self.console_text("'{}' bulunamadı.".format(name), assets = False)
                    else:
                        PATH, _type = QtWidgets.QFileDialog.getSaveFileName(self, "Lütfen dışarı aktarılacak konumu belirleyin.", os.getenv("DESKTOP"), "Yazı dosyası (*.txt);;Resim dosyası (*.png *.jpg)")

                        if PATH:
                            try:
                                with open("datas\\memory2.json", "r") as file:
                                    data = json.loads(file.read())
                            except FileNotFoundError:
                                data = {}

                            text = ""
                            for eng, tur in self.words[name].items():
                                gap_amount = 50
                                gap_amount = gap_amount - len(eng)

                                line = "{gap}{eng_word} : {tur_word}\n".format(gap = " " * gap_amount, eng_word = eng, tur_word = tur)

                                text += line
                                
                            if _type == "Yazı dosyası (*.txt)":
                                PATH = PATH.rstrip(".txt")

                                data.update({"file_upload_PATH": PATH + ".txt"})

                                with open("{}.txt".format(PATH), "w", encoding = "utf-8") as file:
                                        file.write(text)
                            else:
                                PATH = PATH.rstrip(".png")

                                data.update({"file_upload_PATH": PATH + ".png"})

                                text = text.encode("latin-1", errors = "replace")

                                img = Image.new('RGB', (600, 600), color = (255, 255, 255))
        
                                d = ImageDraw.Draw(img)
                                d.text((0, 0), text, fill = (0, 0, 0))

                                img.save('{}.png'.format(PATH))

                            self.console_text("'{}', '{}' konumunda dışarıya aktarıldı.".format(name, PATH), assets = False)

                            data.update({"file_upload_name": name})
                            with open("datas\\memory2.json", "w") as file:
                                json.dump(data, file)

                            del text, PATH
                        else:
                            self.console_text("Dışarı aktarma işlemi iptal edildi.", assets = False)

                        del _type
                else:
                    self.console_text("Lütfen dışarıya aktarmak istediğiniz kelime grubunun ismini yazınız. (Örn. dışa aktar {})".format(list(self.words.keys())[random.randrange(0, len(self.words.keys()))]), assets = False)

                del name
            else:
                if len(self.word_memory) == 2:
                    if self.lineEdit.text().lower().replace(" ", "") == "e":
                        self.word_line += 1

                        self.words["idle"].update({self.word_memory[0]: self.word_memory[1]})

                        if len(self.words["idle"].keys()) == 40:
                            a = list(self.words["idle"].keys())[-1]
                            b = self.words["idle"][a]

                            name = ("{first_third}_{last_third}".format(first_third = a[:3], last_third = b[-3:])).lower()

                            self.words.update({
                                name: self.words["idle"].copy()
                                })

                            self.words["idle"].clear()
                            del a, b, name

                        with open("datas\\memory.json", "w") as file:
                            json.dump(self.words, file)
                        self.console_text("Kelime eklendi.", assets = False)

                        self.word_memory.clear()

                        self.addWords()
                    elif self.lineEdit.text().lower().replace(" ", "") == "h":
                        self.console_text("Eklemeden vazgeçildi.", assets = False)

                        self.word_memory.clear()

                        self.addWords()
                else:
                    self.console_text("GEÇERSİZ KOMUT")

        self.lineEdit.clear()

class KeyTracker(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent = parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == 16777220: #Enter key
            self.click()
        elif e.key() == 94: #Alt + 3 key
            self.word_info()

def run(*args, **kwargs):
    if __name__ != "__main__" and check.run():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Windows')

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
        app.setPalette(palette)

        ui = KeyTracker()
        ui.show()
        
        app.exec_()

        del app, ui
        return {
            "wanted_version": wanted_version
        }
