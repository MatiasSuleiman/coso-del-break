import pytest
import os
from src.system_facade import System_Facade
from tests.date_mock import Date_Mock

@pytest.fixture
def common_setup():
    password = 'rqxk ugvt yvxg kwjw'
    sistema = System_Facade.login('testinatordelbuscador@gmail.com', password)
    return sistema


def test_01_facade_permite_tener_a_mano_los_mails_encontrados(common_setup):

    sistema = common_setup
    sistema.buscar("Asbesto")

    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "Asbesto"
    assert mail.text == "blud\r\n"


def test_02_facade_permite_sumar_al_breakdown_los_mails_encontrados_y_visualizarlos_previamente(common_setup):

    sistema = common_setup
    sistema.buscar("Asbesto")

    sistema.agregar_mail_encontrado(0)

    mail = sistema.ver_mail_en_breakdown(0)

    assert mail.subject == "Asbesto"
    assert mail.text == "blud\r\n"


def test_03_facade_permite_sumar_al_breakdown_todos_los_mails_encontrados_de_una(common_setup):

    sistema = common_setup
    sistema.buscar("A")

    sistema.agregar_todos_los_mails_encontrados()

    mail1 = sistema.ver_mail_en_breakdown(0)
    mail2 = sistema.ver_mail_en_breakdown(1)


    assert mail1.subject == "AnasheMalAmigoooo"
    assert mail1.text == "clanka\r\n"


    assert mail2.subject == "Asbesto"
    assert mail2.text == "blud\r\n"


def test_04_facade_limpia_los_buscados_al_buscar_otra_vez(common_setup):

    sistema = common_setup
    sistema.buscar("a")

    sistema.buscar("no")
    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "no disparen soy imbeci"
    assert mail.text == "a ver demuestralo\r\n"


def test_05_facade_permite_agregar_condicion_de_texto_en_el_cuerpo(common_setup):

    sistema = common_setup
    sistema.agregar_condicion_de_cuerpo("chau")

    sistema.buscar("")
    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "Re: Asbesto"
    assert 'chau1' in mail.text


def test_06_facade_permite_agregar_condicion_de_emisor(common_setup):

    sistema = common_setup
    sistema.agregar_condicion_de_emisor("minecraftpocketeditionprogamer@gmail.com")

    sistema.buscar("")
    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "no disparen soy imbeci"
    assert mail.text == "a ver demuestralo\r\n"


def test_07_facade_permite_agregar_condicion_de_receptor(common_setup):

    sistema = common_setup
    sistema.agregar_condicion_de_receptor("minecraftpocketeditionprogamer@gmail.com")

    sistema.buscar("A")
    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "Ashtor"
    assert mail.text == "por demacia\r\n"


def test_08_facade_permite_agregar_condicion_de_enviado_antes_de(common_setup):

    sistema = common_setup
    fecha = Date_Mock.day_month_year(18, 12, 2025)

    sistema.agregar_condicion_de_enviado_antes_de(fecha)

    sistema.buscar("A")
    mail1 = sistema.ver_mail_encontrado(0)
    mail2 = sistema.ver_mail_encontrado(1)

    assert mail1.subject == "AnasheMalAmigoooo"
    assert mail1.text == "clanka\r\n"

    assert mail2.subject == "Asbesto"
    assert mail2.text == "blud\r\n"


def test_09_facade_permite_agregar_condicion_de_enviado_despues_de(common_setup):

    sistema = common_setup
    fecha = Date_Mock.day_month_year(18, 12, 2025)

    sistema.agregar_condicion_de_enviado_despues_de(fecha)

    sistema.buscar("A")
    mail = sistema.ver_mail_encontrado(0)

    assert mail.subject == "Ashtor"
    assert mail.text == "por demacia\r\n"


def test_10_facade_permite_quitar_cualquier_condicion_agregada_a_la_busqueda_antes_de_buscar(common_setup):

    sistema = common_setup
    fecha = Date_Mock.day_month_year(18, 12, 2025)

    sistema.agregar_condicion_de_enviado_antes_de(fecha)
    condicion = sistema.ver_condicion(0)
    sistema.quitar_condicion(condicion)


    sistema.buscar("A")
    mail1 = sistema.ver_mail_encontrado(0)
    mail2 = sistema.ver_mail_encontrado(1)
    mail3 = sistema.ver_mail_encontrado(2)
    mail4 = sistema.ver_mail_encontrado(3)


    assert mail1.subject == "AnasheMalAmigoooo"
    assert mail1.text == "clanka\r\n"

    assert mail2.subject == "Asbesto"
    assert mail2.text == "blud\r\n"

    assert mail3.subject == "Re: Asbesto"

    assert mail4.subject == "Ashtor"
    assert mail4.text == "por demacia\r\n"


def test_11_facade_permite_mandar_a_crear_el_breakdown_una_vez_decididos_los_mails(common_setup):

    sistema = common_setup

    sistema.buscar("An")
    sistema.agregar_todos_los_mails_encontrados()

    breakdown = sistema.crear_breakdown()

    assert breakdown.tiene_en("A1", "Date")
    assert breakdown.tiene_en("B1", "Description")
    assert breakdown.tiene_en("C1", "Minutes")
    assert breakdown.tiene_en("D1", "Hours")
 
    assert breakdown.tiene_en("A2", "12/12/2025")
    assert breakdown.tiene_en("B2", "Recieved mail from matysuleiman@gmail.com")



    assert os.path.exists("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")


    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")
