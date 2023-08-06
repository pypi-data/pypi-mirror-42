
from configparser import ConfigParser

class Protocolo:
     def __init__(self):
        config = ConfigParser()
        config.read("configuracion\\configuracion.cfg")
        self.usuario  = config.get("protocolo", "user")
        self.password = config.get("protocolo", "password")
        self.servidor = config.get("protocolo","SMTP")
        self.puerto   = config.get("protocolo","puerto")