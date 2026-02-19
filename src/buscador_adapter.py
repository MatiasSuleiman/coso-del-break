import socket
import time
import imaplib
from functools import reduce

from imap_tools import MailBox, AND
from imap_tools.errors import UnexpectedCommandStatusError

from src.errores import CredencialesInvalidasError


def cumple_todo(mail, condiciones):
    return reduce(lambda x, y: x and y.cumple(mail), condiciones, True)


def concatenacion_de_todos_los_elementos_de(data):
    partes = []
    for item in data:
        if isinstance(item, (bytes, bytearray)):
            partes.append(bytes(item))
        else:
            partes.append(str(item).encode("utf-8", errors="ignore"))
    return b" ".join(partes).decode("utf-8", errors="ignore")


def es_error_de_autenticacion(error):
    if hasattr(error, "command_result"):
        try:
            command_result = error.command_result
            data = command_result[1]
            if isinstance(data, (list, tuple)):
                detalle = concatenacion_de_todos_los_elementos_de(data).upper()
                return "AUTHENTICATIONFAILED" in detalle
        except Exception:
            pass
    return "AUTHENTICATIONFAILED" in str(error).upper()


class Buscador_adapter:
    def __init__(self, mailbox, user, password):
        self.mailbox = mailbox
        self.user = user
        self.password = password

    @classmethod
    def login(cls, user, password, retries=3, delay_s=1, folder="INBOX"):
        last_error = None
        for _ in range(retries):
            try:
                mailbox = MailBox("imap.gmail.com").login(user, password, folder)
                return cls(mailbox, user, password)
            except (UnexpectedCommandStatusError, imaplib.IMAP4.error) as error:
                if es_error_de_autenticacion(error):
                    raise CredencialesInvalidasError() from error
                raise
            except socket.gaierror as error:
                last_error = error
                time.sleep(delay_s)
        raise last_error

    def relogin_en(self, folder):
        nuevo_buscador = self.__class__.login(self.user, self.password, folder=folder)
        self.mailbox = nuevo_buscador.mailbox

    def seleccionar_carpeta_de_busqueda(self):
        try:
            self.mailbox.folder.set("[Gmail]/All Mail", readonly=True)
        except UnexpectedCommandStatusError:
            self.relogin_en("[Gmail]/Todos")

    def encontrar_de_a_partes(self, asunto, condiciones):
        self.seleccionar_carpeta_de_busqueda()
        asunto = asunto or ""
        for mail in self.mailbox.fetch(AND(subject=asunto), bulk=50, reverse=True):
            if cumple_todo(mail, condiciones):
                yield mail
