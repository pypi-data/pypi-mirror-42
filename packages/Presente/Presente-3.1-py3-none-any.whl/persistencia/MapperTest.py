from persistencia.Conexion import Conexion
from logica.Alumno         import Alumno

class MapperTest:
    def __init__(self):
        self.conexion=Conexion()
        self.limpiar()

    def limpiar(self):
        self.conexion.actualizacion(""" DELETE
                                        FROM alumnos""",())
        self.conexion.actualizacion(""" DELETE
                                        FROM clases""",())
        self.conexion.actualizacion(""" DELETE
                                        FROM presente""",())
        
