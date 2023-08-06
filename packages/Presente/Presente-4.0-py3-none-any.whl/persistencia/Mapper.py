from persistencia.Conexion import Conexion
from logica.Alumno         import Alumno
from logica.Fecha          import Fecha

class Mapper:
    def __init__(self,alumno):
        self.conexion = Conexion()
        self.alumno   = alumno

    def guardar(self):
        alumno=self.alumno
        self.conexion.actualizacion(""" INSERT INTO alumnos(nombre,apellido,cedula,telefono,emailPadre,emailMadre)
                                        VALUES(?,?,?,?,?,?);""",(alumno.getNombre(),alumno.getApellido(),alumno.getCedula(),alumno.getTelefono(),alumno.getEmailPadre(),alumno.getEmailMadre()))

    def listado(self):
        listadoAlumnos=self.conexion.consulta("""   SELECT  *
                                                    FROM    alumnos""",())
        listado=[]
        for campo in listadoAlumnos:
            alumno=self.crearAlumno(campo)
            listado.append(alumno)
        return listado 

    def aperturaLista(self,fecha):
        self.conexion.actualizacion(""" INSERT INTO clases(fecha,cierre)
                                        VALUES(?,NULL)""",[fecha])
    
    def presente(self,cedula,fecha):
           
            self.conexion.actualizacion(""" INSERT INTO presente(fecha,cedula)
                                            VALUES(?,?);""",(fecha,cedula))
            
    
    def cierreLista(self,fechaInicial,fecha):
        self.conexion.actualizacion(""" UPDATE clases
                                        SET    cierre= ?
                                        WHERE  fecha = ?""",[fecha,fechaInicial])

    def falto(self,fecha):
        listadoAlumnos=self.conexion.consulta("""   SELECT  * 
                                                    FROM    alumnos
                                                    WHERE   alumnos.cedula NOT IN (SELECT presente.cedula
                                                                                   FROM presente
                                                                                   WHERE  fecha=?)
                                                    ORDER BY apellido,nombre""",[fecha])

        resultado=Fecha()
        resultado.setFecha(fecha)
        for campo in listadoAlumnos:
            alumno=self.crearAlumno(campo)
            resultado.agregar(alumno)

        return resultado

    def buscar(self,cedula):
        laLinea=self.conexion.scalar("""    SELECT  * 
                                            FROM    alumnos
                                            WHERE   alumnos.cedula =?""",[cedula])
        alumno=self.crearAlumno(laLinea)
        return alumno
    
    def crearAlumno(self,linea):
        if linea is None:
            return None
        else:
            return Alumno(linea[1],linea[2],linea[0],linea[3],linea[4],linea[5])
