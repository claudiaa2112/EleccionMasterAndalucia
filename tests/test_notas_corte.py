import unittest
from decimal import Decimal
from pathlib import Path

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import CorteNumerico
from master.master import EstadoCorte
from master.prioridad_carreras import PrioridadCarrera

NOTAS_CORTE = (Path(__file__).parent / "paginas_dua" / "notas_corte.html").read_text(encoding="utf-8")


class TestUltimoAdmitidoEnLasNotasDeCorte(unittest.TestCase):
    def test_la_situacion_del_ultimo_admitido_sale_de_las_notas_de_corte(self):
        casos = (("492700", CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.00"))),
                 ("A06400", CorteNumerico(PrioridadCarrera.MEDIA, Decimal("6.01"))),
                 ("493003", EstadoCorte.TODOS_ADMITIDOS),
                 ("324208", EstadoCorte.SIN_ADJUDICACION))
        cortes = ConvocatoriaMaster.cortes_de_las_notas(NOTAS_CORTE)
        for codigo, corte in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(cortes[codigo], corte)

    def test_cada_master_de_las_notas_de_corte_aparece_una_sola_vez(self):
        cortes = ConvocatoriaMaster.cortes_de_las_notas(NOTAS_CORTE)
        self.assertEqual(sorted(cortes), sorted(["102902", "324208", "407908", "492700", "493003", "518302", "A04601", "A06400", "807203"]))
