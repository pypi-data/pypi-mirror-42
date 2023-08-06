from fpdf                    import FPDF
from variablesGlobales       import CONFIG_PATH
from variablesGlobales       import CONFIG_IMG
from variablesGlobales       import CONFIG_PDF
from configparser            import ConfigParser
from logica.QR               import QR
from logica.Alumno           import Alumno

class PDF(FPDF):

    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    
    @staticmethod
    def generar(alumno):
        pdf=PDF()
        config = ConfigParser()
        config.read(CONFIG_PATH)
        tamanio   = int(config.get("pdf", "tamanio"))
        pdf.add_page()
        QR.generar(alumno)
        pdf.image(CONFIG_IMG, 10, 8, tamanio,tamanio)
        pdf.output(CONFIG_PDF+"\\"+str(alumno)+".pdf", 'F') 

alumno=Alumno('m','s','s','s','s','s')
PDF.generar(alumno)