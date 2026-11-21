import unittest
from decimal import Decimal
from pathlib import Path

from ejemplos import TITULACION

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import CorteNumerico
from master.master import Acceso
from master.prioridad_carreras import PrioridadCarrera

PAGINAS_DUA = Path(__file__).parent / "paginas_dua"
CODIGOS_CATALOGO = ["324208", "407908", "492700", "493003", "518302", "A06400", "807203"]


def leer_pagina(nombre):
    return (PAGINAS_DUA / nombre).read_text(encoding="utf-8")


def crear_convocatoria():
    fichas = {codigo: leer_pagina(f"fichas/ficha_{codigo}.html") for codigo in CODIGOS_CATALOGO}
    return ConvocatoriaMaster.desde_las_paginas_del_dua("2026-2027", TITULACION, leer_pagina("catalogo.html"),
                                                        leer_pagina("notas_corte.html"), fichas)


class TestConvocatoriaDesdeLasPaginasDelDua(unittest.TestCase):
    def test_cada_master_del_catalogo_junta_lo_que_dicen_de_el_las_tres_paginas(self):
        casos = (("492700", Acceso(PrioridadCarrera.ALTA, False), 100, CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.00"))),
                 ("A06400", Acceso(PrioridadCarrera.ALTA, False), 80, CorteNumerico(PrioridadCarrera.MEDIA, Decimal("6.01"))))
        masters = crear_convocatoria().masters
        for codigo, acceso, peso, corte in casos:
            with self.subTest(codigo=codigo):
                master = masters[codigo]
                self.assertEqual((master.accesos, master.ponderacion_nota_media, master.corte),
                                 ({TITULACION: acceso}, peso, corte))

    def test_solo_entran_los_masteres_del_catalogo_de_claudia(self):
        self.assertEqual(sorted(crear_convocatoria().masters), sorted(CODIGOS_CATALOGO))
