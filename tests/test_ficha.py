import unittest

from ejemplos import CONVOCATORIA


class TestPesoDeLaNotaMediaEnLaFicha(unittest.TestCase):
    def test_el_peso_de_la_nota_media_sale_de_la_ficha_del_master(self):
        casos = (("492700", 100), ("A06400", 80))
        for codigo, peso in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.masters[codigo].ponderacion_nota_media, peso)

    def test_si_la_ficha_no_puntua_la_nota_media_su_peso_es_cero(self):
        self.assertEqual(CONVOCATORIA.masters["807203"].ponderacion_nota_media, 0)
