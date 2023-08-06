"""Clase Alumno"""
class Alumno:
    
    def __init__(self, nombre,apellido,cedula,telefono,emailPadre,emailMadre):
        """Constructor de Alumno"""
        self.__nombre       = nombre
        self.__apellido     = apellido
        self.__cedula       = cedula
        self.__telefono	    = telefono
        self.__emailPadre	= emailPadre
        self.__emailMadre	= emailMadre
        
    def getNombre(self):
        
        return self.__nombre
    
    def setNombre(self,nombre):
        self.__nombre=nombre
        
    def getApellido(self):
        return self.__apellido
    
    def setApellido(self,apellido):
        self.__Apellido=apellido    
        
    def getCedula(self):
        return self.__cedula
    
    def setCedula(self,cedula):
        self.__cedula=cedula
        
    def getTelefono(self):
        return self.__nombre
    
    def setTelefono(self,telefono):
        self.__telefono=telefono   
        
    def getEmailPadre(self):
        return self.__emailPadre
    
    def setEmailPadre(self,emailPadre):
        self.__emailPadre=emailPadre

    def getEmailMadre(self):
        return self.__emailMadre
    
    def setEmailMadre(self,emailMadre):
        self.__emailMadre=emailMadre
        
    def __repr__(self):

        return "{}-{}".format( self.getApellido(),self.getNombre())

    def __eq__(self, other): 
        return int(self.__cedula) == int(other.getCedula())

    def __cmp__(self, other):
        return int(self.__cedula) - int(other.getCedula())
    