import sys

import smtplib
from configparser     import ConfigParser
from logica.Protocolo import Protocolo

class Email:
    def __init__(self):
        config          = ConfigParser()
        config.read("configuracion\\configuracion.cfg")
        self.enviar     = [];
        self.asunto     = config.get("email", "asunto")
        self.cuerpo     = config.get("email", "cuerpo")
        self.protocolo  = Protocolo()
        
    def agregar(self,emailEnviar):
        self.enviar.append(emailEnviar)
    
    def enviarTodos(self):
        try:  
            if len(self.enviar)>0:
                email = """ From: %s 
                            To: %s 
                            MIME-Version: 1.0 
                            Content-type: text/html 
                            Subject: %s 

                            %s
                        """ % ("carlosalesanchez@gmail.com", self.enviar, self.asunto, self.cuerpo) 
                server = smtplib.SMTP(self.protocolo.servidor, self.protocolo.puerto)
                server.ehlo()
                server.login(self.protocolo.usuario, self.protocolo.password)
                server.sendmail(self.protocolo.usuario,self.enviar, email)
                server.close()
                return True
            else:
                print ('Agrege alguien para enviar')
                return False
        except:  
            print (sys.exc_info()[0])
            return False
