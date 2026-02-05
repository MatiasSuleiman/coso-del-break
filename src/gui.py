import pdb
from PyQt6.QtWidgets import QMainWindow, QLabel, QScrollArea, QVBoxLayout, QSplitter, QPushButton, QTextBrowser, QDialog, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt
from src.system_facade import System_Facade
from src.mostrador_de_mails import Mostrador_de_mails, Mostrador_de_mails_buscados, Mostrador_de_mails_del_break
from src.mostrador_de_condiciones import Mostrador_de_condiciones


class Gui:

    def __init__(self):

       self.sistema = System_Facade.login("testinatordelbuscador@gmail.com",'rqxk ugvt yvxg kwjw')
       self.ventana = QMainWindow()
       self.ventana.setWindowTitle("Build n' Breakdown")
       self.ventana.setGeometry(100,100,1600,900)

       texto_de_bienvenida =  QLabel("Bienvenido a Breaking Down,\n elija los mails para comenzar", self.ventana)
       texto_de_bienvenida.setGeometry(720, 10, 280, 30)

       self.mostrador_de_mails_del_break = Mostrador_de_mails_del_break.en(self.ventana, 700, 700, 20, 100, self)

       self.mostrador_de_mails_encontrados = Mostrador_de_mails_buscados.en(self.ventana, 700, 700, 880, 100, self)

       self.boton_de_busqueda = QPushButton("Buscar", self.ventana)
       self.boton_de_busqueda.clicked.connect(self.buscar)
       self.boton_de_busqueda.setGeometry(880, 50, 50, 30)

       self.barra_de_busqueda = QLineEdit(self.ventana)
       self.barra_de_busqueda.setGeometry(970, 50, 500, 30)

       self.boton_de_crear_break = QPushButton("Crear Breakdown", self.ventana)
       self.boton_de_crear_break.clicked.connect(self.crear_breakdown)
       self.boton_de_crear_break.setGeometry(520, 850, 200, 30)



       self.ventana.show()



    def buscar(self):

        self.limpiar_buscados()
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
        


