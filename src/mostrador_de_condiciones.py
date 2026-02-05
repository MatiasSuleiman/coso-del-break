import tkinter as interfaz
from tkinter import ttk

class Mostrador_de_condiciones:

    def __init__(self, altura, anchura, x, y, maestro):

        self.frame = interfaz.Frame(width = anchura, height= altura, master= maestro.ventana)
        self.frame.place(x = x,y = y)
        self.maestro= maestro

        self.inicializar_contenidos_del_frame()



    def inicializar_contenidos_del_frame(self):

        self.frame.rowconfigure(0, weight = 1)
        self.frame.rowconfigure(1, weight = 1)
        self.frame.rowconfigure(2, weight = 1)
        self.frame.rowconfigure(3, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        self.frame.columnconfigure(0, weight = 5)
        self.frame.columnconfigure(1, weight = 5)

        titulo_de_enviado_por = ttk.Label(self.frame, text= "Enviado por:")
        titulo_de_enviado_por.grid(row = 0, column = 0)

        titulo_de_enviado_a = ttk.Label(self.frame, text= "Enviado a:")
        titulo_de_enviado_a.grid(row = 1, column = 0)

        titulo_de_enviado_antes_de = ttk.Label(self.frame, text= "Enviado antes de:")
        titulo_de_enviado_antes_de.grid(row = 2, column = 0)

        titulo_de_enviado_despues_de = ttk.Label(self.frame, text= "Enviado despues de:")
        titulo_de_enviado_despues_de.grid(row = 3, column = 0)

        titulo_de_texto_en_el_cuerpo = ttk.Label(self.frame, text= "Conteniendo:")
        titulo_de_texto_en_el_cuerpo.grid(row = 4, column = 0)
  

        
        self.barra_de_enviado_por = ttk.Entry(self.frame, width = 60)
        self.barra_de_enviado_por.grid(row = 0, column = 1, padx = 3)
 
        self.barra_de_enviado_a = ttk.Entry(self.frame, width = 60)
        self.barra_de_enviado_a.grid(row = 1, column = 1, padx = 3)

        contenedor_de_enviado_antes_de = ttk.Frame(self.frame)
        contenedor_de_enviado_antes_de.grid(row = 2, column = 1, padx = 3)

        self.fecha_de_enviado_antes_de = Entry_de_fecha(contenedor_de_enviado_antes_de)


        contenedor_de_enviado_despues_de = ttk.Frame(self.frame)
        contenedor_de_enviado_despues_de.grid(row = 3, column = 1, padx = 3)

        self.fecha_de_enviado_despues_de = Entry_de_fecha(contenedor_de_enviado_despues_de)

 
        self.barra_de_conteniendo = ttk.Entry(self.frame, width = 60)
        self.barra_de_conteniendo.grid(row = 4, column = 1, padx = 3)
 




class Entry_de_fecha:

    def __init__(self, maestro):
        self.barra_de_dia = ttk.Entry(maestro, width = 5)
        self.barra_de_dia.pack(side = interfaz.LEFT)

        barra_entre_dia_y_mes = interfaz.Label(maestro, text= '/')
        barra_entre_dia_y_mes.pack(side = interfaz.LEFT)


        self.barra_de_mes = ttk.Entry(maestro, width = 5)
        self.barra_de_mes.pack(side = interfaz.LEFT)

        barra_entre_mes_y_año = interfaz.Label(maestro, text= '/')
        barra_entre_mes_y_año.pack(side = interfaz.LEFT)
 
        self.barra_de_año = ttk.Entry(maestro, width = 5)
        self.barra_de_año.pack(side = interfaz.LEFT)

       
