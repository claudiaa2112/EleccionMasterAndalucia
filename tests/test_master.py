import unittest
from decimal import Decimal

from ejemplos import NOTA_MEDIA_CLAUDIA, TITULACION, master_real

from master.posibilidad import Posibilidad


class TestPuntuaciones(unittest.TestCase):
    def test_la_minima_solo_cuenta_la_nota_media(self):
        for codigo, minima in (("492700", "7.061"), ("518302", "4.2366"), ("807203", "0")):
            with self.subTest(codigo=codigo):
                self.assertEqual(master_real(codigo).puntuacion_minima(NOTA_MEDIA_CLAUDIA), Decimal(minima))

    def test_la_maxima_suma_un_10_en_el_resto_de_criterios(self):
        for codigo, maxima in (("492700", "7.061"), ("518302", "8.2366"), ("807203", "10")):
            with self.subTest(codigo=codigo):
                self.assertEqual(master_real(codigo).puntuacion_maxima(NOTA_MEDIA_CLAUDIA), Decimal(maxima))


class TestAdmision(unittest.TestCase):
    def test_admite_solo_las_titulaciones_de_su_catalogo(self):
        for titulacion, esperado in ((TITULACION, True), ("GRADO EN FÍSICA", False)):
            with self.subTest(titulacion=titulacion):
                self.assertEqual(master_real("492700").admite(titulacion), esperado)


class TestPosibilidad(unittest.TestCase):
    def test_responde_segun_el_corte_del_master(self):
        casos = (("493003", Posibilidad.ENTRA_SEGURO),
                 ("324208", Posibilidad.NO_SE_SABE),
                 ("102902", Posibilidad.DEPENDE))
        for codigo, esperada in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(master_real(codigo).posibilidad(TITULACION, NOTA_MEDIA_CLAUDIA), esperada)
