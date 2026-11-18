import unittest

from master.prioridad_carreras import PrioridadCarrera


class TestOrdenDePrioridad(unittest.TestCase):
    def test_entra_antes_solo_la_prioridad_mayor(self):
        casos = ((PrioridadCarrera.ALTA, PrioridadCarrera.MEDIA, True),
                 (PrioridadCarrera.RESTO, PrioridadCarrera.BAJA, False),
                 (PrioridadCarrera.MEDIA, PrioridadCarrera.MEDIA, False))
        for una, otra, esperado in casos:
            with self.subTest(una=una, otra=otra):
                self.assertEqual(una.es_mayor_que(otra), esperado)
