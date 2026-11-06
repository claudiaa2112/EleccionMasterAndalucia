import unittest

from nose2.tools import params

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import EstadoCorte
from master.master import Master

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
