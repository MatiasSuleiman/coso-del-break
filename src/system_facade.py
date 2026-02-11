from src.buscador_adapter import Buscador_adapter
from src.Breakdown import Breakdown
from src.condicion import Condicion_de_cuerpo, Condicion_de_emisor, Condicion_de_receptor, Condicion_de_enviado_antes_de, Condicion_de_enviado_despues_de

class System_Facade:

    @classmethod
    def login(self, user, password):
        return self(user,password)

    def __init__(self, user, password):
        self.abogado_a_cargo = user
        self.mails_encontrados = []
        self.mails_del_breakdown = []
        self.buscador = Buscador_adapter.login(user, password)
        self.condiciones = []

    def buscar(self, asunto):
        self.limpiar_encontrados()
        self.mails_encontrados =  self.buscador.encontrar(asunto, self.condiciones)

    def agregar_mail_encontrado(self, mail):
        self.mails_del_breakdown.append(mail)
        self.mails_encontrados.remove(mail)
    

    def limpiar_encontrados(self):
        self.mails_encontrados = []


    def agregar_todos_los_mails_encontrados(self):
        for mail in list(self.mails_encontrados):
            self.agregar_mail_encontrado(mail)
    

    def ver_mail_encontrado(self, numero):
        return self.mails_encontrados[numero]
     

    def ver_todos_los_mails_encontrados(self):
        return self.mails_encontrados
     

    def quitar_mail_del_breakdown(self, mail):
        self.mails_del_breakdown.remove(mail)
        self.mails_encontrados.append(mail)


    def ver_mail_en_breakdown(self, numero):
        return self.mails_del_breakdown[numero]


    def agregar_condicion_de_cuerpo(self, cuerpo):
        condicion = Condicion_de_cuerpo.con_cuerpo(cuerpo)
        self.condiciones += [condicion]


    def agregar_condicion_de_emisor(self, emisor):
        condicion = Condicion_de_emisor.con_emisor(emisor)
        self.condiciones += [condicion]

    def agregar_condicion_de_receptor(self, receptor):
        condicion = Condicion_de_receptor.con_receptor(receptor)
        self.condiciones += [condicion]

    def agregar_condicion_de_enviado_antes_de(self, fecha):
        condicion = Condicion_de_enviado_antes_de.enviado_antes_de(fecha)
        self.condiciones += [condicion]

    def agregar_condicion_de_enviado_despues_de(self, fecha):
        condicion = Condicion_de_enviado_despues_de.enviado_despues_de(fecha)
        self.condiciones += [condicion]


    def ver_condicion(self, numero):
        return self.condiciones[numero]


    def quitar_condicion(self, condicion):
        self.condiciones.remove(condicion)


    def limpiar_condiciones(self):
        self.condiciones = []

    def establecer_condiciones(self, condiciones):
        self.limpiar_condiciones()
        for condicion in condiciones:
            self.condiciones.append(condicion)


    def crear_breakdown(self, path=None):
        return Breakdown.con_mails_manejado_por(self.mails_del_breakdown, self.abogado_a_cargo, path=path)
