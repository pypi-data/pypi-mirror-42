
# Cargamos los modulos de Qt necesarios para el programa.
from PyQt5                  import QtCore, QtGui,  uic
from PyQt5.QtWidgets        import *
from logica.QR              import QR
from logica.SistemaPresente import Sistema
from variablesGlobales      import CONFIG_UI
from pygame                 import mixer
import numpy as np
# Cargamos el modulo de OpenCV.
import cv2
import time

from variablesGlobales import CONFIG_SONIDO

class PasarLista:
    def __init__(self):
        
        mixer.init()
        mixer.music.load(CONFIG_SONIDO+"abrirlibreta.mp3")
        mixer.music.play()  

        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"pasarLista.ui")
 
        # Tomamos el dispositivo de captura a partir de la webcam.
        self.webcam = cv2.VideoCapture(0)
 
        # Creamos un temporizador para que cuando se cumpla el tiempo limite tome una captura desde la webcam.
        self.timer = QtCore.QTimer(self.MainWindow);
 
        # Conectamos la señal timeout() que emite nuestro temporizador con la funcion show_frame().
        self.timer.timeout.connect(self.show_frame)
 
        # Tomamos una captura cada 1 mili-segundo.
        self.timer.start(1);
        
        listadoAlumnos=Sistema.listado()
        listado=[]
        for alumno in listadoAlumnos:
            listado.append(alumno.getNombre()+" "+alumno.getApellido())
        self.MainWindow.lstAlumnos.addItems(listado)
        self.fecha=time.strftime("%d/%m/%y")
        
        Sistema.aperturaLista(self.fecha)
        self.alumno=None

    """
    show_frame() -> None
 
    Esta funcion toma una captura desde la webcam y la muestra en una QLabel.
    """
    def show_frame(self):
        # Tomamos una captura desde la webcam.
        ok, imagen = self.webcam.read()
        if not ok:
            return
        
        qr = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
         
        decodedObjects = QR.decodificar(qr)
        font = cv2.FONT_HERSHEY_SIMPLEX
        for decodedObject in decodedObjects: 
            points = decodedObject.polygon
         
            # If the points do not form a quad, find convex hull
            if len(points) > 4 : 
              hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
              hull = list(map(tuple, np.squeeze(hull)))
            else : 
              hull = points;
             
            # Number of points in the convex hull
            n = len(hull)     
            # Draw the convext hull
            for j in range(0,n):
              cv2.line(imagen, hull[j], hull[ (j+1) % n], (255,0,0), 3)
            
            dato=decodedObject.data.decode('ascii')
            cv2.putText(imagen, "Detectado", (decodedObject.rect.left, decodedObject.rect.top), font, 1, (0,255,255), 2, cv2.LINE_AA)
            alumno=Sistema.buscar(dato)
            self.MainWindow.lblDatos.setText(dato)
            if alumno is None:
                self.MainWindow.lblMensaje.setText("No encontrado")
            else:
                if(self.alumno is None or alumno!=self.alumno):
                    self.alumno=alumno
                    fechaGenerado=Sistema.falto(self.fecha)
                    
                    if fechaGenerado.existeAlumno(alumno):
                    
                        Sistema.presente(dato,self.fecha)
                        self.MainWindow.lstAlumnos.clear()
                        
                        listado      = []
                        listadoFecha = fechaGenerado.getListadoAlumnos()
                        fechaGenerado=Sistema.falto(self.fecha)
                        for alumno in listadoFecha:
                            listado.append(alumno.getNombre()+" "+alumno.getApellido())
                        
                        self.MainWindow.lstAlumnos.addItems(listado)
                    
                        self.MainWindow.lblMensaje.setText( str(self.alumno))
                    
                
                    
        image = QtGui.QImage(imagen, imagen.shape[1], imagen.shape[0], imagen.shape[1] * imagen.shape[2], QtGui.QImage.Format_RGB888)
 
        # Creamos un pixmap a partir de la imagen.
        # OpenCV entraga los pixeles de la imagen en formato BGR en lugar del tradicional RGB,
        # por lo tanto tenemos que usar el metodo rgbSwapped() para que nos entregue una imagen con
        # los bytes Rojo y Azul intercambiados, y asi poder mostrar la imagen de forma correcta.
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        
        # Mostramos el QPixmap en la QLabel.
        self.MainWindow.lblWebcam.setPixmap(pixmap)
 