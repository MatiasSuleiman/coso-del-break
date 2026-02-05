from abc import ABC, abstractmethod

def _ymd(fecha):
        if hasattr(fecha, "year") and hasattr(fecha, "month") and hasattr(fecha, "day"):
                return (fecha.year, fecha.month, fecha.day)
        return fecha

class Condicion(ABC):
        @abstractmethod
        def cumple(self,mail):
            raise TypeError("subclass should have overriden!!")

class Condicion_de_cuerpo(Condicion):
        
        def __init__(self,cuerpo):
                self.body = cuerpo
        def cumple(self, mail):
            return self.body in mail.text


class Condicion_de_emisor(Condicion):
        
        def __init__(self,emisor):
                self.emisor = emisor

        def cumple(self, mail):
            return self.emisor == mail.from_

class Condicion_de_receptor(Condicion):
        
        def __init__(self,receptor):
                self.receptor = receptor

        def cumple(self, mail):
            return self.receptor == mail.to[0]


class Condicion_de_enviado_antes_de(Condicion):
        
        def __init__(self,fecha):
                self.fecha_proxima = fecha

        def cumple(self, mail):
            return _ymd(self.fecha_proxima) > _ymd(mail.date)


class Condicion_de_enviado_despues_de(Condicion):
        
        def __init__(self,fecha):
                self.fecha_previa = fecha

        def cumple(self, mail):
            return _ymd(self.fecha_previa) < _ymd(mail.date)
