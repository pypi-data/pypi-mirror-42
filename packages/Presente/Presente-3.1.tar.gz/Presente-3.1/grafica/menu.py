# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Menu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnLista = QtWidgets.QPushButton(self.centralwidget)
        self.btnLista.setGeometry(QtCore.QRect(170, 130, 75, 23))
        self.btnLista.setObjectName("btnLista")
        self.btnAdministracion = QtWidgets.QPushButton(self.centralwidget)
        self.btnAdministracion.setGeometry(QtCore.QRect(420, 130, 91, 23))
        self.btnAdministracion.setObjectName("btnAdministracion")
        self.btnConsulta = QtWidgets.QPushButton(self.centralwidget)
        self.btnConsulta.setGeometry(QtCore.QRect(170, 220, 75, 23))
        self.btnConsulta.setObjectName("btnConsulta")
        self.btnSalir = QtWidgets.QPushButton(self.centralwidget)
        self.btnSalir.setGeometry(QtCore.QRect(430, 220, 75, 23))
        self.btnSalir.setObjectName("btnSalir")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Eventos
        self.btnSalir.clicked.connect(self.salir)
    def salir(self):
        sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Presente"))
        self.btnLista.setText(_translate("MainWindow", "Pasar la lista"))
        self.btnAdministracion.setText(_translate("MainWindow", "Administracion"))
        self.btnConsulta.setText(_translate("MainWindow", "Consulta"))
        self.btnSalir.setText(_translate("MainWindow", "Salir"))




