from src.buscador_adapter import Buscador_adapter
from src.condicion import Condicion, Condicion_de_cuerpo, Condicion_de_emisor, Condicion_de_receptor
from imap_tools import MailBox


password = 'rqxk ugvt yvxg kwjw'
buscador = Buscador_adapter.login('testinatordelbuscador@gmail.com', password)

def test_01_buscador_sin_matches_no_encuentra_nada():
        assert buscador.encontrar("mail_que_no_esta", []) == []


def test_02_buscador_con_una_match_la_encuentra():
        mail = buscador.encontrar("AnasheMalAmigoooo", []) [0]
        assert mail.subject == "AnasheMalAmigoooo"
        assert mail.text == "clanka\r\n"


def test_03_buscador_con_multiples_matches_los_ordena_cronologicamente():
        mails = buscador.encontrar("A", [])

        assert mails[0].subject == "AnasheMalAmigoooo"
        assert mails[0].text == "clanka\r\n"

        assert mails[1].subject == "Asbesto"
        assert mails[1].text == "blud\r\n"


def test_04_buscar_sin_cadena_da_todas_la_matches_que_cumpla_la_condicion():
        condicion = Condicion_de_cuerpo('blud')
        mails = buscador.encontrar("", [condicion])

        assert mails[0].subject == "Asbesto"
        assert mails[0].text == "blud\r\n"

def test_05_buscador_puede_encontrar_segun_quien_envio_el_mail():
        condicion = Condicion_de_emisor('minecraftpocketeditionprogamer@gmail.com')
        mails = buscador.encontrar("", [condicion])

        assert mails[0].subject == "no disparen soy imbeci"
        assert mails[0].text == "a ver demuestralo\r\n"


def test_06_buscador_puede_encontrar_segun_quien_recibio_el_mail():
        condicion = Condicion_de_receptor('matysuleiman@gmail.com')
        mails = buscador.encontrar("", [condicion])

        assert mails[0].subject == "Hola"
        assert mails[1].subject == "Re: Asbesto"

def test_07_buscador_puede_encontrar_por_conjuncion_de_multiples_condiciones():
        condicion1 = Condicion_de_receptor('matysuleiman@gmail.com')
        condicion2 = Condicion_de_cuerpo('chau')
        mails = buscador.encontrar("", [condicion1, condicion2])

        assert mails[0].subject == "Re: Asbesto"

