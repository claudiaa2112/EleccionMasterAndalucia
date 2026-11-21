import unittest
from pathlib import Path

from master.convocatoria_master import ConvocatoriaMaster

FICHAS = Path(__file__).parent / "paginas_dua" / "fichas"


def leer_ficha(codigo):
    return (FICHAS / f"ficha_{codigo}.html").read_text(encoding="utf-8")


class TestPesoDeLaNotaMediaEnLaFicha(unittest.TestCase):
    def test_el_peso_de_la_nota_media_sale_de_la_ficha_del_master(self):
        casos = (("492700", 100), ("A06400", 80))
        for codigo, peso in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(ConvocatoriaMaster.peso_de_la_ficha(leer_ficha(codigo)), peso)

    def test_si_la_ficha_no_puntua_la_nota_media_su_peso_es_cero(self):
        self.assertEqual(ConvocatoriaMaster.peso_de_la_ficha(leer_ficha("807203")), 0)
