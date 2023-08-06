from persistencia.Mapper     import Mapper
from logica.PDF              import PDF


class Sistema:
    @staticmethod
    def guardar(alumno):
        mapper=Mapper(alumno)
        mapper.guardar()
    
    @staticmethod
    def listado():
        mapper=Mapper(None)
        return mapper.listado()
  
    @staticmethod
    def aperturaLista(fecha):
        mapper=Mapper(None)
        return mapper.aperturaLista(fecha)

    @staticmethod
    def presente(codigo,fecha):
        try:  
            mapper=Mapper(None)
            return mapper.presente(int(codigo),fecha)
        except exec.IntegrityError: 
            pass
        

    @staticmethod
    def cierreLista(fecha,cierre):
        mapper=Mapper(None)
        return mapper.cierreLista(fecha,cierre)

    @staticmethod
    def falto(fecha):
        mapper=Mapper(None)
        return mapper.falto(fecha)

    
    @staticmethod
    def generarQR(cedula):
        mapper=Mapper(None)
        alumno=mapper.buscar(cedula)
        PDF.generar(alumno)
               
    
    @staticmethod
    def buscar(cedula):
        if cedula.isnumeric():
            mapper=Mapper(None)
            return mapper.buscar(int(cedula))
        else:
            return None