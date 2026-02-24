from functools import partial
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


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
        self.mails = []

    def ordenar_por_mas_recientes(self, mails):
        return sorted(mails, key=lambda mail: mail.date, reverse=True)

    def cambiar_resumen_de(self, mail):
        ventana_de_resumen = QDialog(self.contenedor_de_mails)
        ventana_de_resumen.setWindowTitle(f"{mail.subject} summary")
        ventana_de_resumen.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()
        lector_de_texto = QTextEdit(ventana_de_resumen)
        lector_de_texto.setPlainText(self.user_interface.ver_resumen_de(mail))
        layout.addWidget(lector_de_texto)

        boton_aplicar_cambios = QPushButton("Apply changes", ventana_de_resumen)
        boton_aplicar_cambios.clicked.connect(
            lambda _, mail=mail, lector=lector_de_texto: self.aplicar_cambios_de_resumen(
                mail, lector.toPlainText(), ventana_de_resumen
            )
        )
        layout.addWidget(boton_aplicar_cambios)

        ventana_de_resumen.setLayout(layout)
        ventana_de_resumen.show()
        ventana_de_resumen.raise_()
        ventana_de_resumen.activateWindow()

    def aplicar_cambios_de_resumen(self, mail, resumen, parent):
        self.user_interface.cambiar_resumen_de(mail, resumen)
        QMessageBox.information(parent, "Summary", "Summary changed successfully")



class Mostrador_de_mails_buscados(Mostrador_de_mails):


    def agregar_mail(self, mail):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFixedHeight(100)
        frame.setLineWidth(3)

        layout_del_frame = QHBoxLayout(frame)
        layout_del_frame.addWidget(
            QLabel(
                parent=frame,
                text=f"Asunto: {mail.subject}\nDe: {mail.from_}\nFecha: {mail.date.strftime('%d/%m/%y')}",
            )
        )
        self.layout.addWidget(frame)

        boton_de_visualizacion = QPushButton(text="Ver", parent=frame)
        boton_de_visualizacion.clicked.connect(partial(self.user_interface.ver_mail, mail))
        layout_del_frame.addWidget(boton_de_visualizacion)

        boton_de_agregar = QPushButton(text="+", parent=frame)
        boton_de_agregar.clicked.connect(partial(self.user_interface.agregar_mail, mail))
        layout_del_frame.addWidget(boton_de_agregar)

    def agregar_mails(self, mails):
        for mail in mails:
            if mail not in self.mails:
                self.mails.append(mail)

        mails_ordenados = self.ordenar_por_mas_recientes(self.mails)
        self.limpiar_mostrador()
        self.mails = list(mails_ordenados)
        for mail in self.mails:
            self.agregar_mail(mail)

    def mostrar(self, mails):
        mails_ordenados = self.ordenar_por_mas_recientes(mails)
        self.limpiar_mostrador()
        self.mails = list(mails_ordenados)
        for mail in self.mails:
            self.agregar_mail(mail)




class Mostrador_de_mails_del_break(Mostrador_de_mails):


    def mostrar(self, mails):
        mails_ordenados = self.ordenar_por_mas_recientes(mails)
        self.limpiar_mostrador()
        self.mails = list(mails_ordenados)
        for mail in self.mails:

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

            boton_de_resumen = QPushButton(text='Summary', parent=frame)
            boton_de_resumen.clicked.connect(lambda _, mail=mail: self.cambiar_resumen_de(mail))
            layout_del_frame.addWidget(boton_de_resumen)

            boton_de_quitar = QPushButton(text = 'x', parent = frame)
            boton_de_quitar.clicked.connect(partial(self.user_interface.quitar_mail, mail))
            layout_del_frame.addWidget(boton_de_quitar)
