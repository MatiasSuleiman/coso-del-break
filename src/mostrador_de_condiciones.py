from datetime import datetime
from PyQt6.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit
from src.condicion import (
    Condicion_de_cuerpo,
    Condicion_de_emisor,
    Condicion_de_receptor,
    Condicion_de_enviado_antes_de,
    Condicion_de_enviado_despues_de,
)




class Mostrador_de_condiciones:


    @classmethod
    def en(self, master, anchura, altura, x, y):
        return self(master, anchura, altura, x, y)



    def __init__(self, master, anchura, altura, x, y):
        self.caja_filtros = QGroupBox("Filtros", master)
        self.caja_filtros.setGeometry(x, y, anchura, altura)
        self.inicializar_contenidos()



    def inicializar_contenidos(self):
        layout = QGridLayout(self.caja_filtros)
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



    def parse_fecha(self, texto):
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



    def obtener_condiciones(self):

        emisor = self.barra_de_emisor.text().strip()
        receptor = self.barra_de_receptor.text().strip()
        cuerpo = self.barra_de_cuerpo.text().strip()
        fecha_antes = self.parse_fecha(self.barra_de_antes.text())
        fecha_despues = self.parse_fecha(self.barra_de_despues.text())

        return [
            Condicion_de_emisor.con_emisor(emisor),
            Condicion_de_receptor.con_receptor(receptor),
            Condicion_de_cuerpo.con_cuerpo(cuerpo),
            Condicion_de_enviado_antes_de.enviado_antes_de(fecha_antes),
            Condicion_de_enviado_despues_de.enviado_despues_de(fecha_despues),
        ]
