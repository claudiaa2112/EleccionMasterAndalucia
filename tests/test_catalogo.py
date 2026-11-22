import unittest
from pathlib import Path

from master.convocatoria_master import ConvocatoriaMaster
from master.master import Acceso
from master.prioridad_carreras import PrioridadCarrera

CATALOGO = (Path(__file__).parent / "paginas_dua" / "catalogo.html").read_text(encoding="utf-8")


class TestPrioridadDeClaudiaEnElCatalogo(unittest.TestCase):
    def test_la_prioridad_de_claudia_en_cada_master_sale_del_catalogo(self):
        casos = (("492700", Acceso(PrioridadCarrera.ALTA, False)),
                 ("407908", Acceso(PrioridadCarrera.MEDIA, True)),
                 ("A06400", Acceso(PrioridadCarrera.ALTA, False)))
        accesos = ConvocatoriaMaster.accesos_del_catalogo(CATALOGO)
        for codigo, acceso in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(accesos[codigo], acceso)

    def test_cada_master_del_catalogo_aparece_una_sola_vez(self):
        accesos = ConvocatoriaMaster.accesos_del_catalogo(CATALOGO)
        self.assertEqual(sorted(accesos), sorted(["102902", "324208", "407908", "492700", "493003", "518302", "A06400", "807203"]))

    def test_rechaza_un_catalogo_con_un_master_repetido(self):
        with self.assertRaisesRegex(ValueError, "repetido en el catálogo"):
            ConvocatoriaMaster.accesos_del_catalogo(CATALOGO + CATALOGO)
