from variablesGlobales import CONFIG_BASE
import sqlite3
from sqlalchemy import exc
class Conexion:
    
    def __init__(self):

        self.path=CONFIG_BASE
        self.conectarse()
        
    def conectarse(self):
        
        self.con=sqlite3.connect(self.path)
        cursor=self.con.cursor()
        cursor.execute("""  CREATE TABLE  IF NOT EXISTS alumnos 
                            (
                                    cedula 	   CHAR(8)      NOT NULL PRIMARY KEY,
                                    nombre 	   VARCHAR(11)  NOT NULL,
                                    apellido   VARCHAR(11)  NOT NULL,
                                    telefono   VARCHAR(15)  NOT NULL,
                                    emailMadre VARCHAR(200)	NULL,
                                    emailPadre VARCHAR(200) NULL
                            );""")

        cursor.execute(""" CREATE TABLE  IF NOT EXISTS clases
                            (
                                    fecha   DATE NOT NULL PRIMARY KEY,
                                    cierre	DATE NULL
                            );""")

        cursor.execute(""" CREATE TABLE  IF NOT EXISTS presente
                            (
                                    cedula	CHAR(8)  NOT NULL REFERENCES alumnos(cedula),
                                    fecha	DATE 	 NOT NULL REFERENCES clase(fecha  ),
                                    PRIMARY KEY(cedula,fecha)
                            );

                       """)
        
    def actualizacion(self,sql,parametros):
        
        cursor=self.con.cursor()
        cursor.execute(sql,parametros)
        self.con.commit()
        

    def consulta(self,sql,parametros):
        
        cursor=self.con.cursor()
        return cursor.execute(sql,parametros)
        
    def scalar(self,sql,parametros):
        cursor=self.con.cursor()
        cursor.execute(sql,parametros)
        return cursor.fetchone()
