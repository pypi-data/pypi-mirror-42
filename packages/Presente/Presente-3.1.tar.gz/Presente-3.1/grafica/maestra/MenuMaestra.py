from logica.Alumno          import Alumno
from logica.SistemaPresente import Sistema
import time

class MenuMaestra:
    
    def mostrarMenu(self):
        from logica.Email import Email
        opcion=1
        while opcion!=0:
            print("*********Menu**************")
            print('* 1 - Listado de alumno   *')
            print('* 2 - Inicia proceso      *')
            print('* 0 - Volver              *')
            print("***************************")
            opcion = int(input('Opcion: '))
            if opcion==1:
                listasAlumnos=Sistema.listado()
                for alumno in listasAlumnos:
                    print(str(alumno))
            else:
                if opcion==2:
                    continuar=True
                    print("Inicio el proceso")
                    ahora = time.strftime("%c")
                    Sistema.aperturaPasada(ahora)
                    while(continuar):
                        codigo=input('Ingreso el id del alumno')
                        Sistema.presente(codigo,ahora)
                        desea=input('Seguira ingresa alumnos? (S)i-(N)o')
                        desea=desea.upper()
                        while(desea!='S' and desea!='N'):
                            print('Ingreso desconocido elija entre N o S')
                            desea=input('Seguira ingresa alumnos? (S)i-(N)o')
                            desea=desea.upper()
                        continuar=(desea=='S')
                    print('Cierre de pase, el sistema empieza enviar email a los padres de los hijos que no vinieron')
                    cierre = time.strftime("%c")
                    Sistema.cierrePasada(ahora,cierre)
                    listado=Sistema.falto(ahora)
                    email=Email()
                    for alumno in listado:
                        email.agregar(alumno.emailPadre)
                    email.enviarTodos()
                else:
                    if opcion==0:
                        print("Volviendo al menu principal")
                    else:
                        print("Opcion desconocida")
