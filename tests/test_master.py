import unittest
from decimal import Decimal

from ejemplos import TITULACION, crear_master

from master.corte import CorteNumerico, EstadoCorte
from master.master import Acceso
from master.posibilidad import Posibilidad
from master.prioridad_carreras import PrioridadCarrera

NOTA_MEDIA = Decimal("7.061")


class TestPuntuaciones(unittest.TestCase):
    def test_la_minima_solo_cuenta_la_nota_media(self):
        for peso, minima in ((100, "7.061"), (60, "4.2366"), (0, "0")):
            with self.subTest(peso=peso):
                self.assertEqual(crear_master(peso=peso).puntuacion_minima(NOTA_MEDIA), Decimal(minima))

    def test_la_maxima_suma_un_10_en_el_resto_de_criterios(self):
        for peso, maxima in ((100, "7.061"), (60, "8.2366"), (0, "10")):
            with self.subTest(peso=peso):
                self.assertEqual(crear_master(peso=peso).puntuacion_maxima(NOTA_MEDIA), Decimal(maxima))


class TestAdmision(unittest.TestCase):
    def test_admite_solo_las_titulaciones_de_su_catalogo(self):
        casos = (({TITULACION: Acceso(PrioridadCarrera.RESTO, False)}, True), ({}, False))
        for accesos, esperado in casos:
            with self.subTest(esperado=esperado):
                self.assertEqual(crear_master(accesos=accesos).admite(TITULACION), esperado)


class TestPosibilidad(unittest.TestCase):
    def test_responde_segun_el_corte_del_master(self):
        casos = ((EstadoCorte.TODOS_ADMITIDOS, Posibilidad.ENTRA_SEGURO),
                 (EstadoCorte.SIN_ADJUDICACION, Posibilidad.NO_SE_SABE),
                 (CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.37")), Posibilidad.DEPENDE))
        for corte, esperada in casos:
            with self.subTest(corte=corte):
                master = crear_master(peso=60, corte=corte,
                                      accesos={TITULACION: Acceso(PrioridadCarrera.RESTO, False)})
                self.assertEqual(master.posibilidad(TITULACION, NOTA_MEDIA), esperada)
