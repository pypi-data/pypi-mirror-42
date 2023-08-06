import sys
 
from PyQt5                      import QtWidgets, uic
from variablesGlobales          import CONFIG_UI
from grafica.maestra.pasarLista import PasarLista

class Menu:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"menu.ui")

        #Eventos
        self.MainWindow.btnSalir.clicked.connect(self.salir)
        self.MainWindow.btnLista.clicked.connect(self.lista)

    def salir(self):
        sys.exit()

    def lista(self):
        app         = QtWidgets.QApplication(sys.argv)
        pasarLista  = PasarLista()
        pasarLista.MainWindow.show()
        app.exec_()
