# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import random, time, os, subprocess, numpy, sqlite3, warnings, subprocess
import matplotlib.pyplot as plt
from datetime import datetime

warnings.filterwarnings('ignore')

hafıza = []
figMemory = {"ing": [], "tur": []}
wanted_version = None

class Ui_MainWindow(object):
    def __init__(self):
        if "datas" not in os.listdir():
            os.mkdir("datas")
        
        self.con = sqlite3.connect("datas\\statistics.db")
        self.cursor = self.con.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS data(queue_names TEXT, scoresEng TEXT, scoresTur TEXT)")
        self.con.commit()

        self.cursor.execute("Select * From data")
        self.queueData = {}
        for i in self.cursor.fetchall():
            self.queueData.update({i[0]: {"eng": i[1], "tur": i[2]}})

        try:
            open("Kelimeler.txt", "r")
        except FileNotFoundError:
            open("Kelimeler.txt", "w")

        self.satır_sayısı = 0
        with open("Kelimeler.txt", "r", encoding = "utf-8") as file:
            queue_names_list = []
            texts = file.readlines()
            last_word = ""
            for i in texts:
                if i != "---------------------------------------------------------------------------------------------------------------------------\n":
                    self.satır_sayısı += 1
                    last_word = i.replace(" ", "").rstrip("\n")
                    last_word = (last_word[:3] + "_" + last_word[-3:]).lower()
                else:
                    if self.satır_sayısı != 0:
                        queue_names_list.append(last_word)
        
        for i in queue_names_list:
            if not i in self.queueData:
                self.cursor.execute("Insert into data Values(?, ?, ?)", (i, "['']", "['']"))
                self.con.commit()

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

        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, dark_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, dark_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, dark_gray_brush)
        MainWindow.setPalette(self.palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app_images\\Fatih_Terim.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, light_gray_brush)
        self.label_2.setPalette(self.palette)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setText("\tCopyright @Osman-Kahraman. \n\n\n")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(MainWindow)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, light_gray_brush)
        self.label.setPalette(self.palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, dark_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, dark_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, light_gray_brush)
        self.palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, dark_gray_brush)
        self.lineEdit.setPalette(self.palette)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        R = random.randrange(0, 256)
        G = random.randrange(0, 256)
        B = random.randrange(0, 256)
        self.color(R, G, B)
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
        self.A.addAction(self.actionKonsol)
        self.A.addAction(self.actionYeni_Pencere)
        self.menu_al.addAction(self.action_ngilizce)
        self.menu_al.addAction(self.actionT_rk_e)
        self.menuKelime.addAction(self.actionEkle)
        self.menubar.addAction(self.A.menuAction())
        self.menuKelime.addAction(self.menu_al.menuAction())
        self.menubar.addAction(self.menuKelime.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionKonsol.triggered.connect(self.console)
        self.actionYeni_Pencere.triggered.connect(self.new_tab)
        self.action_ngilizce.triggered.connect(self.studyWords_English)
        self.actionT_rk_e.triggered.connect(self.studyWords_Turkish)
        self.actionEkle.triggered.connect(self.addWords)
        self.pushButton.clicked.connect(self.click)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrolled)

        self.console()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mahmut"))
        self.A.setTitle(_translate("MainWindow", "Aç"))
        self.menuKelime.setTitle(_translate("MainWindow", "Kelime"))
        self.menu_al.setTitle(_translate("MainWindow", "Çalış"))
        self.actionKonsol.setText(_translate("MainWindow", "Konsol"))
        self.actionKonsol.setShortcut(_translate("MainWindow", 'Ctrl+"'))
        self.actionYeni_Pencere.setText(_translate("MainWindow", "Yeni Pencere"))
        self.actionYeni_Pencere.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actionEkle.setText(_translate("MainWindow", "Ekle"))
        self.actionEkle.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.action_ngilizce.setText(_translate("MainWindow", "İngilizce"))
        self.actionT_rk_e.setText(_translate("MainWindow", "Türkçe"))
    
    def scrolled(self):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
    
    def console_text(self, text, assets = True): 
        if assets:
            self.label_2.setText(str(self.label_2.text()) + os.getcwd() + ">>> [" + time.strftime("%H: %M: %S") + "] " + str(text) + "\n")
        else:
            self.label_2.setText(str(self.label_2.text()) + str(text) + "\n")

    def color(self, R, G, B):
        light_brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        light_brush.setStyle(QtCore.Qt.SolidPattern)
        R /= 2
        G /= 2
        B /= 2
        mid_brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        mid_brush.setStyle(QtCore.Qt.SolidPattern)
        R /= 2
        G /= 2
        B /= 2
        dark_brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        dark_brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, light_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, light_brush)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, dark_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, dark_brush)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, mid_brush)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, mid_brush)
        self.line.setPalette(self.palette)

    def addWords(self):
        self.lineEdit.clear()
        
        satır_sayısı_yazı = "Satır sayısı: " + str(self.satır_sayısı)
        if self.pushButton.text() != "Ekle" and self.label.text() != "Ekle? (e/h)":
            self.console_text(str(150 * "+"), assets = False)
            self.console_text(str(25 * " ") + str(100 * "-") + "\n" + (150 - len(satır_sayısı_yazı)) * " " + satır_sayısı_yazı, assets = False)
        elif self.pushButton.text() != "Ekle":
            self.console_text(str(25 * " ") + str(100 * "-") + "\n" + (150 - len(satır_sayısı_yazı)) * " " + satır_sayısı_yazı, assets = False)
        self.label.setText("İngilizcesi:")
        self.pushButton.setText("Ekle")

    def studyWords(self, language):
        self.language = language
        self.label_list = []
        self.lineEdit_list_turkish = []
        self.lineEdit_list_english = []
        self.lineEdit.clear()
        if self.pushButton.text() != "Kontrol Et":
            self.pushButton.setText("Kontrol Et")
            self.console_text(str(150 * "+"), assets = False)

        try:
            with open("Çalışılacak Kelimeler.txt", "r", encoding = "utf-8") as file:
                for i in file.readlines():
                    if i == "---------------------------------------------------------------------------------------------------------------------------\n":
                        continue

                    i = i.lstrip(" ").rstrip("\n").split(" : ")
                    i_e = i[0].split("; ")
                    i_t = i[1].split("; ")
                    
                    english_list = []
                    for j in i_e:
                        j = j.lower().replace(" ", "")
                        english_list.append(j)
                    turkish_list = []
                    for j in i_t:
                        j = j.lower().replace(" ", "")
                        turkish_list.append(j)
                    
                    self.label_list.append(i)
                    self.lineEdit_list_english.append(english_list)
                    self.lineEdit_list_turkish.append(turkish_list)
        except FileNotFoundError:
            open("Çalışılacak Kelimeler.txt", "w")
        try:
            self.rastgele_sayı = random.randrange(start = 0, stop = len(self.label_list))
        
            english_word = self.label_list[self.rastgele_sayı][0].split("; ")
            turkish_word = self.label_list[self.rastgele_sayı][1].split("; ")

            if self.language == "İngilizce":
                self.label.setText(english_word[random.randint(0, len(english_word) - 1)])
            else:
                self.label.setText(turkish_word[random.randint(0, len(turkish_word) - 1)])
        except:
            self.console_text("Çalışılacak Kelimeler.txt'yi okumada başarısız olundu.\nŞunlar sebep olabilir;\n -Dosya boş olabilir.\n -Dosya kaydedilmemiş olabilir.")

    def studyWords_English(self):
        self.studyWords("İngilizce")

    def studyWords_Turkish(self):
        self.studyWords("Türkçe")
    
    def click(self):
        global hafıza, wanted_version
        
        if self.pushButton.text() == "Kontrol Et":
            user_text = self.lineEdit.text().lower().replace(" ", "")
            
            if self.language == "İngilizce":
                if user_text in self.lineEdit_list_turkish[self.rastgele_sayı]:
                    a = self.lineEdit_list_turkish[self.rastgele_sayı].index(user_text)
                    self.console_text("d0ru Cevap")
                    if len(self.lineEdit_list_turkish[self.rastgele_sayı]) >= 2:
                        self.console_text("Diğer anlamları; " + str(self.lineEdit_list_turkish[self.rastgele_sayı][0:a] + self.lineEdit_list_turkish[self.rastgele_sayı][a + 1:]))
                    self.lineEdit.clear()
                    self.studyWords(self.language)
                    figMemory["ing"].append(True)
                else:
                    self.console_text("Yanlış Cevap")
                    figMemory["ing"].append(False)
            else:
                if user_text in self.lineEdit_list_english[self.rastgele_sayı]:
                    a = self.lineEdit_list_english[self.rastgele_sayı].index(user_text)
                    self.console_text("d0ru Cevap")
                    if len(self.lineEdit_list_english[self.rastgele_sayı]) >= 2:
                        self.console_text("Diğer anlamları; " + str(self.lineEdit_list_english[self.rastgele_sayı][0:a] + self.lineEdit_list_english[self.rastgele_sayı][a + 1:]))
                    self.lineEdit.clear()
                    self.studyWords(self.language)
                    figMemory["tur"].append(True)
                else:
                    self.console_text("Yanlış Cevap")
                    figMemory["tur"].append(False)
        elif self.pushButton.text() == "Ekle":
            if self.label.text() == "İngilizcesi:":
                if len(self.lineEdit.text()) in range(1, 76):
                    self.label.setText("Türkçesi:")
                    hafıza.append(self.lineEdit.text())

                    self.console_text("İngilizce kelime: " + self.lineEdit.text())

                    self.lineEdit.clear()
                elif len(self.lineEdit.text()) > 75:
                    self.console_text("Yüksek karakter içeriği, lütfen İngilizce kelimenizin en fazla 75 karakter uzunluğunda olmasına dikkat edin.")
            elif self.label.text() == "Türkçesi:":
                if len(self.lineEdit.text()) in range(1, 76):
                    self.label.setText("İngilizcesi:")
                    hafıza.append(self.lineEdit.text())

                    self.console_text("Türkçe kelime: " + self.lineEdit.text())

                    self.lineEdit.clear()
                elif len(self.lineEdit.text()) > 75:
                    self.console_text("Yüksek karakter içeriği, lütfen Türkçe kelimenizin en fazla 75 karakter uzunluğunda olmasına dikkat edin.")
        else:
            if self.lineEdit.text().lower().rstrip(" ") == "baban kim?":
                self.lineEdit.clear()
                a = int(str(datetime.now())[str(datetime.now()).rfind(".") + 1:])
                
                with open("app_images\\a.txt", "r", encoding="utf-8") as file:
                    liste = []
                    for i in file.readlines():
                        liste.append(i.rstrip("\n"))
                i = 0
                while i < len(liste):
                    if abs(a - int(str(datetime.now())[str(datetime.now()).rfind(".") + 1:])) <= 3000:
                        if i == 0:
                            self.console_text("Osman Kahraman")
                        self.console_text(liste[i], assets = False)
                        i += 1

            elif self.lineEdit.text().lower().endswith(" aç"):
                program = "\"" + str(self.lineEdit.text()).rstrip(" aç") + "\""
                self.console_text(program + " açılıyor.")
                subprocess.Popen("{}\\{}".format(os.getcwd(), self.lineEdit.text().rstrip(" aç")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
                self.lineEdit.clear()
            
            elif self.lineEdit.text().lower().startswith("kd"):
                try:
                    dosya_yolu = self.lineEdit.text().lower().lstrip("kd ")
                    os.chdir(dosya_yolu)
                    self.label.setText(dosya_yolu)
                    self.lineEdit.clear()
                except FileNotFoundError:
                    self.console_text("Dosya yolu bulunamadı.")
            
            elif self.lineEdit.text().lower().startswith("ard"):
                lineEdit_color = list(self.lineEdit.text().lower().lstrip("ard ").replace(" ", "").split(","))
                self.color(int(lineEdit_color[0]), int(lineEdit_color[1]), int(lineEdit_color[2]))
                self.console_text("Renk değişti. " + str(lineEdit_color))
                self.lineEdit.clear()

            elif self.lineEdit.text().lower().startswith("versiyon"):
                self.console_text("v_1_0\n\n+ Mahmut, dünyaya merhaba dedi! \n\n20.03.2021 Perşembe 16:21")
                self.lineEdit.clear()

            elif self.lineEdit.text().lower().startswith("güncelle"):
                wanted_version = self.lineEdit.text().lower().lstrip("güncelle ")

                self.console_text("Güncellenmek istenen sürüm ayarlandı. \nArka plandaki köle robotların yeni sürümü eklemesi için lütfen programı kapatın. ")
                self.lineEdit.clear()
            
        if len(hafıza) == 2:
            self.label.setText("Ekle? (e/h)")
            self.pushButton.setText("↑")
            
            if self.lineEdit.text().lower().replace(" ", "") == "e":
                self.satır_sayısı += 1
                boşluk = " "

                with open("Kelimeler.txt", "a", encoding = "utf-8") as file:
                    boşluk_sayısı = 50
                        
                    boşluk_sayısı = boşluk_sayısı - len(hafıza[0])
                    yazı = (boşluk * boşluk_sayısı) + hafıza[0] + " : " + hafıza[1] + "\n"
                    file.write(yazı)

                    if self.satır_sayısı in range(0, self.satır_sayısı + 1, 40):
                        file.write("---------------------------------------------------------------------------------------------------------------------------\n")

                    file.close()

                self.console_text("Kelime eklendi.")
                hafıza = []
                self.addWords()
            elif self.lineEdit.text().lower().replace(" ", "") == "h":
                self.console_text("Eklemeden vazgeçildi.")
                hafıza = []
                self.addWords()

    def new_tab(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def console(self):
        global figMemory

        self.label.setText(os.getcwd() + ">>> ")

        if figMemory["ing"] and figMemory["tur"]:
            self.cursor.execute("Select * From data")
            self.queueData = {}
            for i in self.cursor.fetchall():
                self.queueData.update({i[0]: {"eng": i[1], "tur": i[2]}})

            queueName = str(self.lineEdit_list_english[-1][0] + ":" + self.lineEdit_list_turkish[-1][-1][-3:])
            queueName = queueName[:3] + "_" + queueName[-3:]
            queueScore_Eng = float("{:.2f}".format(figMemory["ing"].count(True) / len(figMemory["ing"])))
            queueScore_Tur = float("{:.2f}".format(figMemory["tur"].count(True) / len(figMemory["tur"])))
            queueScores_Eng = list(str(self.queueData[queueName]["eng"]).lstrip("[").rstrip("]").replace("'", "").split(","))
            queueScores_Tur = list(str(self.queueData[queueName]["tur"]).lstrip("[").rstrip("]").replace("'", "").split(","))
            
            for i, j in zip(queueScores_Eng, queueScores_Tur):
                if queueScores_Eng.index(i) != 0:
                    queueScores_Eng[queueScores_Eng.index(i)], queueScores_Tur[queueScores_Tur.index(j)] = float(i), float(j)
            queueScores_Eng.append(queueScore_Eng)
            queueScores_Tur.append(queueScore_Tur)

            try:
                self.cursor.execute("Update data set scoresEng = ?, scoresTur = ? where queue_names = ?", (str(queueScores_Eng), str(queueScores_Tur), queueName))
            except:
                self.cursor.execute("Insert into data Values(?, ?, ?)", (queueName, "['', {}]".format(str(queueScores_Eng)), "['', {}]".format(str(queueScores_Tur))))
            self.con.commit()

            queueScores_Eng, queueScores_Tur = queueScores_Eng[1:], queueScores_Tur[1:] 
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
            figMemory["ing"], figMemory["tur"] = [], []

        if self.pushButton.text() != "↑":
            self.pushButton.setText("↑")
            self.console_text(str(150 * "+"), assets = False)

def run():
    if __name__ != "__main__":
        import sys

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()

        return {
            "wanted_version": wanted_version
            }
