try:
    from src.buscador_adapter import Buscador_adapter
    from src.Breakdown import Breakdown
    from src.condicion import (
        Condicion_de_cuerpo,
        Condicion_de_emisor,
        Condicion_de_receptor,
        Condicion_de_enviado_antes_de,
        Condicion_de_enviado_despues_de,
    )
except ModuleNotFoundError:
    from buscador_adapter import Buscador_adapter
    from Breakdown import Breakdown
    from condicion import (
        Condicion_de_cuerpo,
        Condicion_de_emisor,
        Condicion_de_receptor,
        Condicion_de_enviado_antes_de,
        Condicion_de_enviado_despues_de,
    )

class System_Facade:

    @classmethod
    def login(cls, user, password):
        buscador_por_asunto = Buscador_adapter.login(user, password)
        buscador_por_cuerpo = Buscador_adapter.login(user, password)
        return cls.build(user, buscador_por_asunto, buscador_por_cuerpo)

    @classmethod
    def build(cls, user, buscador, buscador_por_cuerpo=None):
       return cls(user, buscador, buscador_por_cuerpo)

    builde = build

    def __init__(self, user, buscador_por_asunto, buscador_por_cuerpo):
        self.abogado_a_cargo = user
        self.mails_encontrados = []
        self.mails_del_breakdown = []
        self.descripcion_por_mail = {}
        self.minutos_por_mail = {}
        self.buscador_por_asunto = buscador_por_asunto
        self.buscador_por_cuerpo = buscador_por_cuerpo
        self.buscador = buscador_por_asunto
        self.condiciones = []

    def buscar_de_a_partes_por_asunto(self, asunto):
        return self.buscador_por_asunto.encontrar_de_a_partes_por_asunto(asunto, self.condiciones)

    def buscar_de_a_partes_por_cuerpo(self, cuerpo):
        return self.buscador_por_cuerpo.encontrar_de_a_partes_por_cuerpo(cuerpo, self.condiciones)

    def cambiar_carpeta_de_busqueda(self, carpeta):
        buscadores = self._buscadores_activos()
        carpetas_previas = {id(buscador): buscador.carpeta_actual for buscador in buscadores}

        try:
            for buscador in buscadores:
                buscador.cambiar_carpeta(carpeta)
        except Exception:
            for buscador in buscadores:
                carpeta_previa = carpetas_previas[id(buscador)]
                try:
                    buscador.cambiar_carpeta(carpeta_previa)
                except Exception:
                    pass
            raise

    def _buscadores_activos(self):
        buscadores = []
        vistos = set()
        for buscador in (self.buscador_por_asunto, self.buscador_por_cuerpo):
            if id(buscador) in vistos:
                continue
            vistos.add(id(buscador))
            buscadores.append(buscador)
        return buscadores

    def agregar_mail_encontrado(self, mail):
        self.mails_del_breakdown.append(mail)
        self.mails_encontrados.remove(mail)
        self.descripcion_por_mail[mail] = ""
        self.minutos_por_mail[mail] = 0

    def agregar_mails_encontrados(self, mails):
        self.mails_encontrados.extend(mails)
    

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
        self.descripcion_por_mail.pop(mail, None)
        self.minutos_por_mail.pop(mail, None)


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


    def limpiar_condiciones(self):
        self.condiciones = []

    def cambiar_descripcion_de(self, mail, descripcion):
        self.descripcion_por_mail[mail] = descripcion

    def ver_descripcion_de(self, mail):
        return self.descripcion_por_mail.get(mail, "")

    def cambiar_minutos_de(self, mail, minutos):
        self.minutos_por_mail[mail] = minutos

    def ver_minutos_de(self, mail):
        return self.minutos_por_mail.get(mail, 0)

    def crear_breakdown(self, path):
        return Breakdown.con_mails_manejado_por(
            self.mails_del_breakdown, self.abogado_a_cargo, path=path, sistema=self
        ) 

    def cantidad_de_encontrados(self):
        return len(self.mails_encontrados)
