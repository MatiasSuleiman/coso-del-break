from functools import partial
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt


class Mostrador_de_mails():

    @classmethod
    def en(self, master ,altura, anchura, x, y, user_interface):
        return self(master ,altura, anchura, x, y, user_interface)


    def __init__(self, master ,altura, anchura, x, y, user_interface):

        self.user_interface = user_interface
        self.mails = []

        area = QScrollArea(master)
        area.setGeometry(x, y, altura, anchura)
        area.setWidgetResizable(True)

        self.contenedor_de_mails = QWidget()

        self.layout = QVBoxLayout(self.contenedor_de_mails)
        self.contenedor_de_mails.setLayout(self.layout)

        area.setWidget(self.contenedor_de_mails)


    def limpiar_mostrador(self):

        while self.layout.count() > 0: 
            item = self.layout.takeAt(0)  
            widget = item.widget()  
            
            if widget:  
                widget.deleteLater()



class Mostrador_de_mails_buscados(Mostrador_de_mails):


    def mostrar(self, mails):
        
        self.limpiar_mostrador()
        for mail in mails:

            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setFixedHeight(100)
            frame.setLineWidth(3)                         

            layout_del_frame = QHBoxLayout(frame)

            layout_del_frame.addWidget(QLabel(parent = frame, text = f"Asunto: {mail.subject}\nDe: {mail.from_}\nFecha: {mail.date.strftime('%d/%m/%y')}"))
            self.layout.addWidget(frame)


            boton_de_visualizacion = QPushButton(text = 'Ver', parent = frame)
            boton_de_visualizacion.clicked.connect(partial(self.user_interface.ver_mail, mail))
            layout_del_frame.addWidget(boton_de_visualizacion)

            boton_de_agregar = QPushButton(text = '+', parent = frame)
            boton_de_agregar.clicked.connect(partial(self.user_interface.agregar_mail, mail))
            layout_del_frame.addWidget(boton_de_agregar)




class Mostrador_de_mails_del_break(Mostrador_de_mails):


    def mostrar(self, mails):

        self.limpiar_mostrador()
        
        for mail in mails:

            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setFixedHeight(100)
            frame.setLineWidth(3)                         

            layout_del_frame = QHBoxLayout(frame)

            layout_del_frame.addWidget(QLabel(parent = frame, text = f"Asunto: {mail.subject}\nDe: {mail.from_}\nFecha: {mail.date.strftime('%d/%m/%y')}"))
            self.layout.addWidget(frame)


            boton_de_visualizacion = QPushButton(text = 'Ver', parent = frame)
            boton_de_visualizacion.clicked.connect(partial(self.user_interface.ver_mail, mail))
            layout_del_frame.addWidget(boton_de_visualizacion)

            boton_de_quitar = QPushButton(text = 'x', parent = frame)
            boton_de_quitar.clicked.connect(partial(self.user_interface.quitar_mail, mail))
            layout_del_frame.addWidget(boton_de_quitar)

