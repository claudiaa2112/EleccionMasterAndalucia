import unittest

from master.prioridad_carreras import PrioridadCarrera


class TestOrdenDePrioridad(unittest.TestCase):
    def test_entra_antes_la_prioridad_mayor(self):
        self.assertTrue(PrioridadCarrera.ALTA.es_mayor_que(PrioridadCarrera.MEDIA))

    def test_no_entra_antes_la_prioridad_menor(self):
        self.assertFalse(PrioridadCarrera.RESTO.es_mayor_que(PrioridadCarrera.BAJA))

    def test_con_la_misma_prioridad_no_entra_antes_ninguna(self):
        self.assertFalse(PrioridadCarrera.MEDIA.es_mayor_que(PrioridadCarrera.MEDIA))
