import unittest
from decimal import Decimal

from ejemplos import crear_master

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
