import os
from src.Breakdown import Breakdown
from tests.mail_mock import Mail_Mock
from tests.date_mock import Date_Mock

def test_01_breakdown_crea_excel_al_inicializarse():
    mails = []

    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")

    assert os.path.exists("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")
 
    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

def test_02_breakdown_sin_mails_pone_la_parte_de_arriba_del_cuadro_en_la_primer_fila():

    mails = []

    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")

    assert os.path.exists("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")
    assert breakdown.tiene_en("A1", "Date")
    assert breakdown.tiene_en("B1", "Description")
    assert breakdown.tiene_en("C1", "Minutes")
    assert breakdown.tiene_en("D1", "Hours")
 
    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

def test_03_breakdown_con__mails_los_pone_abajo_del_cuadro_de_arriba():
    date1 = Date_Mock.day_month_year(23, 10, 2026)
    mail1 = Mail_Mock.con("El pepe", "ete Sech", "Teto", "brouder", date1)
    mails = [mail1]

    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")

    assert os.path.exists("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

    assert breakdown.tiene_en("A1", "Date")
    assert breakdown.tiene_en("B1", "Description")
    assert breakdown.tiene_en("C1", "Minutes")
    assert breakdown.tiene_en("D1", "Hours")
 
    assert breakdown.tiene_en("A2", "23/10/2026")
    assert breakdown.tiene_en("B2", "Mail to ete Sech")

    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

def test_04_breakdown_con_multiples_mails_los_pone_en_orden():

    date1 = Date_Mock.day_month_year(10, 11 ,2026)
    date2 = Date_Mock.day_month_year(11, 11 ,2026)
    mail1 = Mail_Mock.con("El pepe", "ete Sech", "Teto", "brouder", date1)
    mail2 = Mail_Mock.con("El pepe", "El papu misterioso", "nashe", "instardo", date2)
    mails = [mail1, mail2]

    
    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")

    assert breakdown.tiene_en("A2", "10/11/2026")
    assert breakdown.tiene_en("B2", "Mail to ete Sech")

    assert breakdown.tiene_en("A3", "11/11/2026")
    assert breakdown.tiene_en("B3", "Mail to El papu misterioso")
    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

def test_05_breakdown_con_mail_recibido_lo_describe_correctamente():
    
    date1 = Date_Mock.day_month_year(10, 11 ,2026)
    mail1 = Mail_Mock.con("ete Sech", "El Pepe", "Teto", "Re: brouder", date1)
    mails = [mail1]

    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")

    assert breakdown.tiene_en("A2", "10/11/2026")
    assert breakdown.tiene_en("B2", "Recieved mail from ete Sech")

    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")

def test_06_breakdown_pone_el_techo_del_cuadro_en_letra_mas_grande():

    date1 = Date_Mock.day_month_year(10, 11 ,2026)
    mail1 = Mail_Mock.con("El pepe", "ete Sech", "Teto", "brouder", date1)
    mail2 = Mail_Mock.con("ete Sech", "El Pepe", "Teto", "Re: brouder", date1)
    mails = [mail1, mail2]

    
    breakdown = Breakdown.con_mails_manejado_por(mails, "El pepe")


    assert breakdown.casilla_tiene_fuente_tamanio("A1", 14)
    assert breakdown.casilla_tiene_fuente_tamanio("B1", 14)
    assert breakdown.casilla_tiene_fuente_tamanio("C1", 14)
    assert breakdown.casilla_tiene_fuente_tamanio("D1", 14)
   
    assert breakdown.casilla_tiene_fuente_tamanio("A2", 11)
    assert breakdown.casilla_tiene_fuente_tamanio("B2", 11)

    assert breakdown.casilla_tiene_fuente_tamanio("A3", 11)
    assert breakdown.casilla_tiene_fuente_tamanio("B3", 11)
   

    os.remove("/home/matias/Prototipo/tests/breakdowns/Unnamed_Breakdown.xlsx")



