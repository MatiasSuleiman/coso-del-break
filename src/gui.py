from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QTextBrowser, QDialog, QLineEdit, QFileDialog, QGroupBox, QGridLayout
from PyQt6.QtCore import Qt
from src.system_facade import System_Facade
from src.mostrador_de_mails import Mostrador_de_mails_buscados, Mostrador_de_mails_del_break


class Gui:

    def __init__(self):

       self.sistema = System_Facade.login("testinatordelbuscador@gmail.com",'rqxk ugvt yvxg kwjw')
       self.ventana = QMainWindow()
       self.ventana.setWindowTitle("Build n' Breakdown")
       self.ventana.setGeometry(100,100,1600,900)

       texto_de_bienvenida =  QLabel("Bienvenido a Breaking Down,\n elija los mails para comenzar", self.ventana)
       texto_de_bienvenida.setGeometry(720, 10, 280, 30)

       self._crear_filtros()

       self.mostrador_de_mails_del_break = Mostrador_de_mails_del_break.en(self.ventana, 700, 650, 20, 140, self)

       self.mostrador_de_mails_encontrados = Mostrador_de_mails_buscados.en(self.ventana, 700, 650, 880, 140, self)

       self.boton_de_busqueda = QPushButton("Buscar", self.ventana)
       self.boton_de_busqueda.clicked.connect(self.buscar)
       self.boton_de_busqueda.setGeometry(880, 50, 50, 30)

       self.barra_de_busqueda = QLineEdit(self.ventana)
       self.barra_de_busqueda.setPlaceholderText("Buscar por asunto")
       self.barra_de_busqueda.returnPressed.connect(self.buscar)
       self.barra_de_busqueda.setGeometry(970, 50, 500, 30)

       self.boton_de_crear_break = QPushButton("Crear Breakdown", self.ventana)
       self.boton_de_crear_break.clicked.connect(self.crear_breakdown)
       self.boton_de_crear_break.setGeometry(520, 830, 200, 30)



       self.ventana.show()



    def _crear_filtros(self):
        caja_filtros = QGroupBox("Filtros", self.ventana)
        caja_filtros.setGeometry(20, 10, 700, 120)

        layout = QGridLayout(caja_filtros)
        layout.setContentsMargins(10, 20, 10, 10)

        layout.addWidget(QLabel("Enviado por:"), 0, 0)
        self.barra_de_emisor = QLineEdit()
        layout.addWidget(self.barra_de_emisor, 0, 1)

        layout.addWidget(QLabel("Enviado a:"), 0, 2)
        self.barra_de_receptor = QLineEdit()
        layout.addWidget(self.barra_de_receptor, 0, 3)

        layout.addWidget(QLabel("Enviado antes de:"), 1, 0)
        self.barra_de_antes = QLineEdit()
        self.barra_de_antes.setInputMask("00/00/0000")
        self.barra_de_antes.setPlaceholderText("DD/MM/AAAA")
        layout.addWidget(self.barra_de_antes, 1, 1)

        layout.addWidget(QLabel("Enviado despues de:"), 1, 2)
        self.barra_de_despues = QLineEdit()
        self.barra_de_despues.setInputMask("00/00/0000")
        self.barra_de_despues.setPlaceholderText("DD/MM/AAAA")
        layout.addWidget(self.barra_de_despues, 1, 3)

        layout.addWidget(QLabel("Conteniendo:"), 2, 0)
        self.barra_de_cuerpo = QLineEdit()
        layout.addWidget(self.barra_de_cuerpo, 2, 1, 1, 3)


    def _parse_fecha(self, texto):
        texto = texto.strip()
        if not texto or "_" in texto:
            return None
        partes = texto.split("/")
        if len(partes) != 3:
            return None
        try:
            dia, mes, anio = [int(p) for p in partes]
            return datetime(anio, mes, dia)
        except ValueError:
            return None


    def _actualizar_condiciones(self):
        self.sistema.limpiar_condiciones()

        emisor = self.barra_de_emisor.text().strip()
        receptor = self.barra_de_receptor.text().strip()
        cuerpo = self.barra_de_cuerpo.text().strip()
        fecha_antes = self._parse_fecha(self.barra_de_antes.text())
        fecha_despues = self._parse_fecha(self.barra_de_despues.text())

        if emisor:
            self.sistema.agregar_condicion_de_emisor(emisor)
        if receptor:
            self.sistema.agregar_condicion_de_receptor(receptor)
        if cuerpo:
            self.sistema.agregar_condicion_de_cuerpo(cuerpo)
        if fecha_antes:
            self.sistema.agregar_condicion_de_enviado_antes_de(fecha_antes)
        if fecha_despues:
            self.sistema.agregar_condicion_de_enviado_despues_de(fecha_despues)


    def buscar(self):

        self.limpiar_buscados()
        self._actualizar_condiciones()
        asunto = self.barra_de_busqueda.text()
        self.sistema.buscar(asunto)
        mails = self.sistema.ver_todos_los_mails_encontrados()
        self.mostrador_de_mails_encontrados.mostrar(mails)


    def ver_mail(self, mail):

        ventana_del_mail = QDialog(self.ventana)
        ventana_del_mail.setWindowTitle(mail.subject)
        ventana_del_mail.setGeometry(100,100,600,400)

        layout = QVBoxLayout()

        caja_de_texto = QTextBrowser(ventana_del_mail)
        caja_de_texto.setPlainText( f"{mail.subject}\n\t{mail.text}")
        layout.addWidget(caja_de_texto)

        ventana_del_mail.setLayout(layout)
        ventana_del_mail.show()
        ventana_del_mail.raise_()
        ventana_del_mail.activateWindow()



    def agregar_mail(self,mail):
       
        self.sistema.agregar_mail_encontrado(mail)

        self.mostrador_de_mails_del_break.mostrar(self.sistema.mails_del_breakdown)
        self.mostrador_de_mails_encontrados.mostrar(self.sistema.ver_todos_los_mails_encontrados())


    def quitar_mail(self, mail):
        self.sistema.quitar_mail_del_breakdown(mail)

        self.mostrador_de_mails_del_break.mostrar(self.sistema.mails_del_breakdown)
        self.mostrador_de_mails_encontrados.mostrar(self.sistema.ver_todos_los_mails_encontrados())

 
    def limpiar_buscados(self):
        self.mostrador_de_mails_encontrados.limpiar_mostrador()


    def crear_breakdown(self):
        path, _ = QFileDialog.getSaveFileName(self.ventana, "Guardar Breakdown", "", "Excel files (*.xlsx)")
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path = f"{path}.xlsx"
        self.sistema.crear_breakdown(path=path)

