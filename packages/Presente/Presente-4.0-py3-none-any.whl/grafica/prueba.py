import sys
 
from PyQt5                      import QtWidgets, uic
from variablesGlobales          import CONFIG_UI


class Prueba:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"probando.ui")

        #Eventos
        self.MainWindow.btnTocar.clicked.connect(self.cambiar)

    def cambiar(self):
        self.MainWindow.lblMensaje.setText("Hola a todos")

app         = QtWidgets.QApplication(sys.argv)
prueba  = Prueba()
prueba.MainWindow.show()
app.exec_()