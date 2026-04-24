from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from system_facade import System_Facade


class FakeBuscador:
    def __init__(self, nombre="fake"):
        self.nombre = nombre
        self.carpeta_actual = "INBOX"
        self.user = "lawyer@example.com"
        self.password = "secret"
        self.sesion_google = None

    def encontrar_de_a_partes_por_asunto(self, asunto, condiciones):
        return (self.nombre, asunto, condiciones)

    def encontrar_de_a_partes_por_cuerpo(self, cuerpo, condiciones):
        return (self.nombre, cuerpo, condiciones)

    def cambiar_carpeta(self, carpeta):
        self.carpeta_actual = carpeta


def test_build_usa_un_buscador_ya_autenticado():
    buscador = FakeBuscador("asunto")
    buscador_cuerpo = FakeBuscador("cuerpo")

    sistema = System_Facade.build("lawyer@example.com", buscador, buscador_cuerpo)

    assert sistema.abogado_a_cargo == "lawyer@example.com"
    assert sistema.buscador is buscador
    assert sistema.buscador_por_asunto is buscador
    assert sistema.buscador_por_cuerpo is buscador_cuerpo


def test_login_delega_en_build(monkeypatch):
    buscadores = [FakeBuscador("asunto"), FakeBuscador("cuerpo")]
    llamadas = []

    def fake_login(user, password, folder="INBOX"):
        llamadas.append((user, password, folder))
        return buscadores.pop(0)

    monkeypatch.setattr("system_facade.Buscador_adapter.login", fake_login)

    sistema = System_Facade.login("lawyer@example.com", "secret")

    assert llamadas == [
        ("lawyer@example.com", "secret", "INBOX"),
        ("lawyer@example.com", "secret", "INBOX"),
    ]
    assert sistema.buscador_por_asunto.nombre == "asunto"
    assert sistema.buscador_por_cuerpo.nombre == "cuerpo"


def test_builde_es_alias_de_build():
    buscador = FakeBuscador("asunto")
    buscador_cuerpo = FakeBuscador("cuerpo")

    sistema = System_Facade.builde("lawyer@example.com", buscador, buscador_cuerpo)

    assert sistema.buscador is buscador


def test_agregar_mail_inicializa_los_minutos_en_cero():
    buscador = FakeBuscador()
    mail = object()
    sistema = System_Facade.build("lawyer@example.com", buscador)
    sistema.agregar_mails_encontrados([mail])

    sistema.agregar_mail_encontrado(mail)

    assert sistema.ver_minutos_de(mail) == 0


def test_cambiar_minutos_actualiza_el_valor_guardado():
    buscador = FakeBuscador()
    mail = object()
    sistema = System_Facade.build("lawyer@example.com", buscador)
    sistema.agregar_mails_encontrados([mail])
    sistema.agregar_mail_encontrado(mail)

    sistema.cambiar_minutos_de(mail, 135)

    assert sistema.ver_minutos_de(mail) == 135


def test_quitar_mail_del_breakdown_descarta_los_minutos():
    buscador = FakeBuscador()
    mail = object()
    sistema = System_Facade.build("lawyer@example.com", buscador)
    sistema.agregar_mails_encontrados([mail])
    sistema.agregar_mail_encontrado(mail)
    sistema.cambiar_minutos_de(mail, 80)

    sistema.quitar_mail_del_breakdown(mail)

    assert sistema.ver_minutos_de(mail) == 0


def test_reagregar_mail_reinicia_los_minutos_en_cero():
    buscador = FakeBuscador()
    mail = object()
    sistema = System_Facade.build("lawyer@example.com", buscador)
    sistema.agregar_mails_encontrados([mail])
    sistema.agregar_mail_encontrado(mail)
    sistema.cambiar_minutos_de(mail, 80)
    sistema.quitar_mail_del_breakdown(mail)

    sistema.agregar_mail_encontrado(mail)

    assert sistema.ver_minutos_de(mail) == 0


def test_buscar_de_a_partes_por_asunto_delega_en_el_buscador():
    sistema = System_Facade.build(
        "lawyer@example.com",
        FakeBuscador("asunto"),
        FakeBuscador("cuerpo"),
    )

    assert sistema.buscar_de_a_partes_por_asunto("invoice") == ("asunto", "invoice", [])


def test_buscar_de_a_partes_por_cuerpo_delega_en_el_buscador():
    sistema = System_Facade.build(
        "lawyer@example.com",
        FakeBuscador("asunto"),
        FakeBuscador("cuerpo"),
    )

    assert sistema.buscar_de_a_partes_por_cuerpo("invoice") == ("cuerpo", "invoice", [])


def test_cambiar_carpeta_de_busqueda_sincroniza_ambos_buscadores():
    buscador_por_asunto = FakeBuscador("asunto")
    buscador_por_cuerpo = FakeBuscador("cuerpo")
    sistema = System_Facade.build("lawyer@example.com", buscador_por_asunto, buscador_por_cuerpo)

    sistema.cambiar_carpeta_de_busqueda("[Gmail]/Sent Mail")

    assert buscador_por_asunto.carpeta_actual == "[Gmail]/Sent Mail"
    assert buscador_por_cuerpo.carpeta_actual == "[Gmail]/Sent Mail"
