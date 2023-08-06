
import qrcode
import pyzbar.pyzbar as pyzbar
from   logica.Alumno     import Alumno
from   variablesGlobales import CONFIG_IMG

class QR:

    @staticmethod
    def generar(alumno):
        img = qrcode.make(alumno.getCedula())
        f = open(CONFIG_IMG, "wb")
        img.save(f)
        f.close()

    @staticmethod
    def decodificar(im):
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(im)
        # Print results
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data,'\n')     
        return decodedObjects
