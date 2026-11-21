import unittest
from decimal import Decimal

from master.corte import CorteNumerico
from master.posibilidad import Posibilidad
from master.prioridad_carreras import PrioridadCarrera


def crear_corte(puntuacion):
    return CorteNumerico(PrioridadCarrera.RESTO, Decimal(puntuacion))


class TestPosibilidadPorPuntuacion(unittest.TestCase):
    def test_entra_seguro_depende_o_no_entra_segun_la_puntuacion(self):
        casos = (("5.00", "7.061", "7.061", Posibilidad.ENTRA_SEGURO),
                 ("7.06", "7.06", "9", Posibilidad.ENTRA_SEGURO),
                 ("5.37", "4.2366", "8.2366", Posibilidad.DEPENDE),
                 ("9.83", "7.061", "7.061", Posibilidad.NO_ENTRA))
        for corte, minima, maxima, esperada in casos:
            with self.subTest(corte=corte, minima=minima):
                posibilidad = crear_corte(corte).posibilidad(PrioridadCarrera.RESTO, Decimal(minima), Decimal(maxima))
                self.assertEqual(posibilidad, esperada)


class TestPosibilidadPorPrioridad(unittest.TestCase):
    def test_la_prioridad_decide_antes_que_la_puntuacion(self):
        casos = ((PrioridadCarrera.MEDIA, "7.90", PrioridadCarrera.ALTA, Posibilidad.ENTRA_SEGURO),
                 (PrioridadCarrera.ALTA, "5.00", PrioridadCarrera.RESTO, Posibilidad.NO_ENTRA))
        for prioridad_corte, puntuacion, prioridad, esperada in casos:
            with self.subTest(prioridad=prioridad):
                corte = CorteNumerico(prioridad_corte, Decimal(puntuacion))
                self.assertEqual(corte.posibilidad(prioridad, Decimal("7.061"), Decimal("7.061")), esperada)
