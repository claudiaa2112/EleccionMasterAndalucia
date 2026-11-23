import unittest
from decimal import Decimal

from ejemplos import (CODIGOS_CATALOGO, NOTA_MEDIA_CLAUDIA, TITULACION, crear_convocatoria, leer_pagina,
                      master_real)

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import CorteNumerico
from master.posibilidad import Posibilidad
from master.prioridad_carreras import PrioridadCarrera


class TestCodigoMaster(unittest.TestCase):
    def test_acepta_los_codigos_que_usa_el_dua(self):
        for codigo in ("492700", "A06400"):
            with self.subTest(codigo=codigo):
                self.assertIn(codigo, crear_convocatoria().masters)

    def test_rechaza_un_codigo_que_no_usa_el_dua(self):
        for codigo in ("49270", "4927000", "49270A", "A0640", "B06400", ""):
            with self.subTest(codigo=codigo), self.assertRaisesRegex(ValueError, "6 cifras, o una A y 5 cifras"):
                ConvocatoriaMaster.comprobar_masters({codigo: master_real("492700")})


class TestFichaDelMaster(unittest.TestCase):
    def test_rechaza_un_master_del_catalogo_sin_ficha(self):
        fichas = {codigo: leer_pagina(f"fichas/ficha_{codigo}.html") for codigo in CODIGOS_CATALOGO if codigo != "492700"}
        with self.assertRaisesRegex(ValueError, "Falta la ficha del máster 492700"):
            ConvocatoriaMaster.desde_las_paginas_del_dua(TITULACION, leer_pagina("catalogo.html"),
                                                         leer_pagina("notas_corte.html"), fichas)


class TestPesoNotaMedia(unittest.TestCase):
    def test_acepta_un_peso_en_los_limites(self):
        for codigo, peso in (("807203", 0), ("492700", 100)):
            with self.subTest(codigo=codigo):
                self.assertEqual(crear_convocatoria().masters[codigo].ponderacion_nota_media, peso)

    def test_rechaza_un_peso_fuera_de_0_a_100(self):
        for peso in (-1, 101):
            with self.subTest(peso=peso), self.assertRaisesRegex(ValueError, "entre 0 y 100"):
                ConvocatoriaMaster.comprobar_masters({"492700": master_real("492700", ponderacion_nota_media=peso)})


class TestPuntuacionCorte(unittest.TestCase):
    def test_acepta_una_puntuacion_en_los_limites(self):
        for puntuacion in (Decimal("0"), Decimal("10")):
            with self.subTest(puntuacion=puntuacion):
                master = master_real("492700", corte=CorteNumerico(PrioridadCarrera.RESTO, puntuacion))
                ConvocatoriaMaster.comprobar_masters({"492700": master})

    def test_rechaza_una_puntuacion_fuera_de_0_a_10(self):
        for puntuacion in (Decimal("-0.01"), Decimal("10.01")):
            with self.subTest(puntuacion=puntuacion), self.assertRaisesRegex(ValueError, "entre 0 y 10"):
                master = master_real("492700", corte=CorteNumerico(PrioridadCarrera.RESTO, puntuacion))
                ConvocatoriaMaster.comprobar_masters({"492700": master})


class TestPosibilidades(unittest.TestCase):
    def test_claudia_sabe_su_posibilidad_en_cada_master_de_su_catalogo(self):
        esperadas = {"102902": Posibilidad.DEPENDE, "324208": Posibilidad.NO_SE_SABE,
                     "407908": Posibilidad.NO_ENTRA, "492700": Posibilidad.ENTRA_SEGURO,
                     "493003": Posibilidad.ENTRA_SEGURO, "518302": Posibilidad.NO_ENTRA,
                     "803141": Posibilidad.NO_SE_SABE, "807203": Posibilidad.NO_ENTRA,
                     "A06400": Posibilidad.ENTRA_SEGURO}
        self.assertEqual(crear_convocatoria().posibilidades(NOTA_MEDIA_CLAUDIA), esperadas)

    def test_acepta_una_nota_media_en_los_limites(self):
        for nota_media in (Decimal("5"), Decimal("10")):
            with self.subTest(nota_media=nota_media):
                self.assertEqual(len(crear_convocatoria().posibilidades(nota_media)), len(CODIGOS_CATALOGO))

    def test_rechaza_una_nota_media_fuera_de_5_a_10(self):
        for nota_media in (Decimal("4.99"), Decimal("10.01")):
            with self.subTest(nota_media=nota_media), self.assertRaisesRegex(ValueError, "entre 5 y 10"):
                crear_convocatoria().posibilidades(nota_media)
