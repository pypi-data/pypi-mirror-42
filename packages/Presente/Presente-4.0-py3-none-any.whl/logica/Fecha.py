import time

class Fecha:
    def __init__(self):
        self.__fecha          = time.strftime("%d/%m/%y")
        self.__listadoAlumnos = []

        
    def getFecha(self):
        return self.__fecha
    
    def setFecha(self,fecha):
        self.__fecha=fecha
             
    def getListadoAlumnos(self):
        return self.__listadoAlumnos

    def existeAlumno(self,alumno):
        return alumno in self.__listadoAlumnos

    def agregar(self,alumno):
        self.__listadoAlumnos.append(alumno)
     
    def __repr__(self):

        return " Fecha : {} Listado de Alumnos {}".format( self.__fecha,self.__listadoAlumnos)

    def __eq__(self, other): 
        encontre=True
        if self.__fecha == other.getFecha():
            cantidad = len(other.getListadoAlumnos())
            if len(self.__listadoAlumnos)==cantidad:
                listadoOtro = other.getListadoAlumnos()
                for i in range(0,cantidad):
                    alumnoOtro  = listadoOtro[i]
                    alumno      = self.__listadoAlumnos[i]
                    if alumno!=alumnoOtro:
                        encontre=False
            else:
                encontre=False
        else:
           encontre=False
        return encontre
