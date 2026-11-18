import unittest
from decimal import Decimal

from ejemplos import TITULACION, crear_master

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import CorteNumerico, EstadoCorte
from master.master import Acceso
from master.posibilidad import Posibilidad
from master.prioridad_carreras import PrioridadCarrera


class TestCodigoMaster(unittest.TestCase):
    def test_acepta_un_codigo_de_seis_cifras(self):
        convocatoria = ConvocatoriaMaster("2026-2027", {"492700": crear_master()})
        self.assertIn("492700", convocatoria.masters)

    def test_rechaza_un_codigo_que_no_tiene_seis_cifras(self):
        for codigo in ("49270", "4927000", "49270A", ""):
            with self.subTest(codigo=codigo), self.assertRaisesRegex(ValueError, "6 cifras"):
                ConvocatoriaMaster("2026-2027", {codigo: crear_master()})


class TestPesoNotaMedia(unittest.TestCase):
    def test_acepta_un_peso_en_los_limites(self):
        for peso in (0, 100):
            with self.subTest(peso=peso):
                convocatoria = ConvocatoriaMaster("2026-2027", {"492700": crear_master(peso=peso)})
                self.assertIn("492700", convocatoria.masters)

    def test_rechaza_un_peso_fuera_de_0_a_100(self):
        for peso in (-1, 101):
            with self.subTest(peso=peso), self.assertRaisesRegex(ValueError, "entre 0 y 100"):
                ConvocatoriaMaster("2026-2027", {"492700": crear_master(peso=peso)})


class TestPuntuacionCorte(unittest.TestCase):
    def test_acepta_una_puntuacion_en_los_limites(self):
        for puntuacion in (Decimal("0"), Decimal("10")):
            with self.subTest(puntuacion=puntuacion):
                convocatoria = ConvocatoriaMaster("2026-2027", {"492700": crear_master(corte=CorteNumerico(PrioridadCarrera.RESTO, puntuacion))})
                self.assertIn("492700", convocatoria.masters)

    def test_rechaza_una_puntuacion_fuera_de_0_a_10(self):
        for puntuacion in (Decimal("-0.01"), Decimal("10.01")):
            with self.subTest(puntuacion=puntuacion), self.assertRaisesRegex(ValueError, "entre 0 y 10"):
                ConvocatoriaMaster("2026-2027", {"492700": crear_master(corte=CorteNumerico(PrioridadCarrera.RESTO, puntuacion))})


class TestPosibilidades(unittest.TestCase):
    def test_responde_solo_por_los_masteres_que_admiten_su_titulacion(self):
        admite = crear_master(corte=EstadoCorte.TODOS_ADMITIDOS,
                              accesos={TITULACION: Acceso(PrioridadCarrera.RESTO, False)})
        convocatoria = ConvocatoriaMaster("2026-2027", {"492700": admite, "109908": crear_master()})
        self.assertEqual(convocatoria.posibilidades(TITULACION, Decimal("7.061")),
                         {"492700": Posibilidad.ENTRA_SEGURO})
