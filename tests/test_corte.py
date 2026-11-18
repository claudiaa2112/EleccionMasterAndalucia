import unittest
from decimal import Decimal

from master.corte import CorteNumerico
from master.posibilidad import Posibilidad
from master.prioridad_carreras import PrioridadCarrera


def crear_corte(puntuacion):
    return CorteNumerico(PrioridadCarrera.RESTO, Decimal(puntuacion))


class TestPosibilidadPorPuntuacion(unittest.TestCase):
    def test_entra_seguro_si_la_minima_llega_al_corte(self):
        posibilidad = crear_corte("5.00").posibilidad(Decimal("7.061"), Decimal("7.061"))
        self.assertEqual(posibilidad, Posibilidad.ENTRA_SEGURO)

    def test_empatar_con_el_ultimo_admitido_cuenta_como_entrar(self):
        posibilidad = crear_corte("7.06").posibilidad(Decimal("7.06"), Decimal("9"))
        self.assertEqual(posibilidad, Posibilidad.ENTRA_SEGURO)

    def test_depende_si_solo_llega_la_maxima(self):
        posibilidad = crear_corte("5.37").posibilidad(Decimal("4.2366"), Decimal("8.2366"))
        self.assertEqual(posibilidad, Posibilidad.DEPENDE)

    def test_no_entra_si_ni_la_maxima_llega(self):
        posibilidad = crear_corte("9.83").posibilidad(Decimal("7.061"), Decimal("7.061"))
        self.assertEqual(posibilidad, Posibilidad.NO_ENTRA)
