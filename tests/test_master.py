import unittest
from decimal import Decimal

from ejemplos import crear_master

from master.corte import CorteNumerico
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


TITULACION = "GRADO EN INGENIERÍA INFORMÁTICA"


class TestAdmision(unittest.TestCase):
    def test_admite_una_titulacion_de_su_catalogo(self):
        master = crear_master(accesos={TITULACION: Acceso(PrioridadCarrera.RESTO, False)})
        self.assertTrue(master.admite(TITULACION))

    def test_no_admite_una_titulacion_que_no_esta_en_su_catalogo(self):
        self.assertFalse(crear_master().admite(TITULACION))


class TestPosibilidad(unittest.TestCase):
    def test_junta_la_prioridad_del_catalogo_y_las_puntuaciones(self):
        master = crear_master(peso=60, corte=CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.37")),
                              accesos={TITULACION: Acceso(PrioridadCarrera.RESTO, False)})
        self.assertEqual(master.posibilidad(TITULACION, NOTA_MEDIA), Posibilidad.DEPENDE)
