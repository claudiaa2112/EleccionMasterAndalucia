import unittest
from decimal import Decimal

from datos_del_dua import CODIGOS_CATALOGO, CONVOCATORIA, TITULACION

from master.corte import CorteNumerico
from master.master import Acceso
from master.prioridad_carreras import PrioridadCarrera


class TestConvocatoriaDesdeLasPaginasDelDua(unittest.TestCase):
    def test_cada_master_del_catalogo_junta_lo_que_dicen_de_el_las_tres_paginas(self):
        casos = (("492700", Acceso(PrioridadCarrera.ALTA, False), 100, CorteNumerico(PrioridadCarrera.RESTO, Decimal("5.00"))),
                 ("A06400", Acceso(PrioridadCarrera.ALTA, False), 80, CorteNumerico(PrioridadCarrera.MEDIA, Decimal("6.01"))))
        for codigo, acceso, peso, corte in casos:
            with self.subTest(codigo=codigo):
                master = CONVOCATORIA.masters[codigo]
                self.assertEqual((master.accesos, master.ponderacion_nota_media, master.corte),
                                 ({TITULACION: acceso}, peso, corte))

    def test_solo_entran_los_masteres_del_catalogo_de_claudia(self):
        self.assertEqual(sorted(CONVOCATORIA.posibilidades(TITULACION, Decimal("5"))), sorted(CODIGOS_CATALOGO))
