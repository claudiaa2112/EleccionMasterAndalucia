import unittest
from decimal import Decimal

from nose2.tools import params

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import CorteNumerico, EstadoCorte
from master.master import Master
from master.prioridad_carreras import PrioridadCarrera

MASTER = Master(accesos={}, ponderacion_nota_media=100, requisitos_adicionales={},
                corte=EstadoCorte.SIN_ADJUDICACION)


class TestCodigoMaster(unittest.TestCase):
    def test_acepta_un_codigo_de_seis_cifras(self):
        convocatoria = ConvocatoriaMaster("2026-2027", {"492700": MASTER})
        self.assertIn("492700", convocatoria.masters)

    @params("49270", "4927000", "49270A", "")
    def test_rechaza_un_codigo_que_no_tiene_seis_cifras(self, codigo):
        with self.assertRaisesRegex(ValueError, "6 cifras"):
            ConvocatoriaMaster("2026-2027", {codigo: MASTER})


def master_con_peso(peso):
    return Master(accesos={}, ponderacion_nota_media=peso, requisitos_adicionales={},
                  corte=EstadoCorte.SIN_ADJUDICACION)


class TestPesoNotaMedia(unittest.TestCase):
    @params(0, 100)
    def test_acepta_un_peso_en_los_limites(self, peso):
        convocatoria = ConvocatoriaMaster("2026-2027", {"492700": master_con_peso(peso)})
        self.assertIn("492700", convocatoria.masters)

    @params(-1, 101)
    def test_rechaza_un_peso_fuera_de_0_a_100(self, peso):
        with self.assertRaisesRegex(ValueError, "entre 0 y 100"):
            ConvocatoriaMaster("2026-2027", {"492700": master_con_peso(peso)})


def master_con_corte(puntuacion):
    return Master(accesos={}, ponderacion_nota_media=100, requisitos_adicionales={},
                  corte=CorteNumerico(PrioridadCarrera.RESTO, puntuacion))


class TestPuntuacionCorte(unittest.TestCase):
    @params(Decimal("0"), Decimal("10"))
    def test_acepta_una_puntuacion_en_los_limites(self, puntuacion):
        convocatoria = ConvocatoriaMaster("2026-2027", {"492700": master_con_corte(puntuacion)})
        self.assertIn("492700", convocatoria.masters)

    @params(Decimal("-0.01"), Decimal("10.01"))
    def test_rechaza_una_puntuacion_fuera_de_0_a_10(self, puntuacion):
        with self.assertRaisesRegex(ValueError, "entre 0 y 10"):
            ConvocatoriaMaster("2026-2027", {"492700": master_con_corte(puntuacion)})
