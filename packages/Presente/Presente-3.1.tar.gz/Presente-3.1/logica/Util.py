class Util:
    
    @staticmethod
    def cedula(numeroCedula):
        numeroCedula=numeroCedula.replace('.', '')
        numeroCedula=numeroCedula.replace('-', '')
        return int(numeroCedula)