from openpyxl import Workbook
from openpyxl.styles import Font

class Breakdown:
    @classmethod
    def con_mails_manejado_por(self, mails, abogado, path, sistema):
        return self(mails, abogado, path=path, sistema=sistema)
    
    def __init__(self, mails, abogado, path, sistema):
        self.workbook = Workbook()
        self.excel = self.workbook.active
        self.initialize_excel_file(mails, abogado, path=path, sistema=sistema)


    def initialize_excel_file(self, mails, abogado, path, sistema):
        self.excel['A1'] = "Date"
        self.excel['B1'] = "Description"
        self.excel['C1'] = "Minutes"
        self.excel['D1'] = "Hours"
        self.excel['E1'] = "Summary"

        self.excel['A1'].font = Font(size=14)
        self.excel['B1'].font = Font(size=14)
        self.excel['C1'].font = Font(size=14)
        self.excel['D1'].font = Font(size=14)
        self.excel['E1'].font = Font(size=14)

        for i in range(len(mails)):
            mail = mails[i]
            self.excel[f"A{i+2}"] = mail.date.strftime("%d/%m/%Y")
            if mail.from_ == abogado:
                self.excel[f"B{i+2}"] = "Mail to " + mail.to[0]
            else:
                self.excel[f"B{i+2}"] = "Recieved mail from " + mail.from_

        for i in range(len(mails)):
           mail = mails[i]
           self.excel[f"C{i+2}"] = 0
           self.excel[f"D{i+2}"] = f"=C{i+2} / 60"
           self.excel[f"E{i+2}"] = sistema.ver_resumen_de(mail)

        self.workbook.save(path)


    def tiene_en(self, casilla, string):
        return self.excel[casilla].value == string


    def casilla_tiene_fuente_tamanio(self, casilla, tamanio):
        return self.excel[casilla].font.size == tamanio
