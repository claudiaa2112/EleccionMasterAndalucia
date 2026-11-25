import unittest
from decimal import Decimal

from ejemplos import CONVOCATORIA, crear_convocatoria, leer_pagina

from master.corte import CorteNumerico
from master.master import EstadoCorte
from master.prioridad_carreras import PrioridadCarrera

NOTAS_CORTE = leer_pagina("notas_corte.html")


class TestUltimoAdmitidoEnLasNotasDeCorte(unittest.TestCase):
    def test_la_situacion_del_ultimo_admitido_sale_de_las_notas_de_corte(self):
        casos = (("492700", CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.00"))),
                 ("A06400", CorteNumerico(PrioridadCarrera.MEDIA, Decimal("6.01"))),
                 ("493003", EstadoCorte.TODOS_ADMITIDOS),
                 ("324208", EstadoCorte.SIN_ADJUDICACION))
        for codigo, corte in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.masters[codigo].corte, corte)

    def test_rechaza_unas_notas_de_corte_con_un_master_repetido(self):
        with self.assertRaisesRegex(ValueError, "repetido en las notas de corte"):
            crear_convocatoria(notas_corte=NOTAS_CORTE + NOTAS_CORTE)
