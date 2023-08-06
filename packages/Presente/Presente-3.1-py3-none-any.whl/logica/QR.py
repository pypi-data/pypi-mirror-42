from variablesGlobales import CONFIG_IMG
import qrcode
from logica.Alumno import Alumno
class QR:

    @staticmethod
    def generar(alumno):
        img = qrcode.make(alumno.getCedula())
        f = open(CONFIG_IMG, "wb")
        img.save(f)
        f.close()
    
alumno1=Alumno(1,'Carlos',123,'099','carlosalesanchez@gmail.com','carlosalesanchez@gmail.com')
QR.generar(alumno1)
