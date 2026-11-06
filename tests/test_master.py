import unittest
from decimal import Decimal

from nose2.tools import params

from master.corte import EstadoCorte
from master.master import Master

NOTA_MEDIA = Decimal("7.061")


def master_con_peso(peso):
    return Master(accesos={}, ponderacion_nota_media=peso, requisitos_adicionales={},
                  corte=EstadoCorte.SIN_ADJUDICACION)


class TestPuntuaciones(unittest.TestCase):
    @params((100, "7.061"), (60, "4.2366"), (0, "0"))
    def test_la_minima_solo_cuenta_la_nota_media(self, peso, minima):
        self.assertEqual(master_con_peso(peso).puntuacion_minima(NOTA_MEDIA), Decimal(minima))

    @params((100, "7.061"), (60, "8.2366"), (0, "10"))
    def test_la_maxima_suma_un_10_en_el_resto_de_criterios(self, peso, maxima):
        self.assertEqual(master_con_peso(peso).puntuacion_maxima(NOTA_MEDIA), Decimal(maxima))
