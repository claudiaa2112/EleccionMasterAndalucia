import unittest
from decimal import Decimal

from ejemplos import CODIGOS_CATALOGO, CONVOCATORIA, NOTA_MEDIA_CLAUDIA, TITULACION, crear_convocatoria, leer_fichas, leer_pagina

from master.posibilidad import Posibilidad

CATALOGO = leer_pagina("catalogo.html")
NOTAS_CORTE = leer_pagina("notas_corte.html")
FICHA_492700 = leer_fichas()["492700"]
PESO_492700 = '<td class="text-right">100</td>'
CORTE_492700 = "<b>RESTO</b>-5,00"
CORTE_102902 = "<b>RESTO</b>-5,37"


class TestCodigoMaster(unittest.TestCase):
    def test_acepta_los_codigos_del_catalogo_con_las_dos_formas_que_usa_el_dua(self):
        for codigo in ("492700", "A06400"):
            with self.subTest(codigo=codigo):
                self.assertIn(TITULACION, CONVOCATORIA.masters[codigo].accesos)

    def test_rechaza_un_codigo_que_no_usa_el_dua(self):
        for codigo in ("49270", "4927000", "49270A", "A0640", "B06400", ""):
            with self.subTest(codigo=codigo), self.assertRaisesRegex(ValueError, "6 cifras, o una A y 5 cifras"):
                crear_convocatoria(catalogo=CATALOGO.replace("<td>492700</td>", f"<td>{codigo}</td>"))


class TestFichaDelMaster(unittest.TestCase):
    def test_rechaza_un_master_del_catalogo_sin_ficha(self):
        fichas = leer_fichas()
        del fichas["492700"]
        with self.assertRaisesRegex(ValueError, "Falta la ficha del máster 492700"):
            crear_convocatoria(fichas=fichas)


class TestPesoNotaMedia(unittest.TestCase):
    def test_acepta_un_peso_en_los_limites(self):
        for codigo, peso in (("807203", 0), ("492700", 100)):
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.masters[codigo].ponderacion_nota_media, peso)

    def test_rechaza_un_peso_fuera_de_0_a_100(self):
        for peso in ("-1", "101"):
            with self.subTest(peso=peso), self.assertRaisesRegex(ValueError, "entre 0 y 100"):
                ficha = FICHA_492700.replace(PESO_492700, f'<td class="text-right">{peso}</td>')
                crear_convocatoria(fichas=leer_fichas() | {"492700": ficha})


class TestPuntuacionCorte(unittest.TestCase):
    def test_acepta_una_puntuacion_en_los_limites(self):
        for puntuacion in ("0,00", "10,00"):
            with self.subTest(puntuacion=puntuacion):
                notas_corte = NOTAS_CORTE.replace(CORTE_492700, f"<b>RESTO</b>-{puntuacion}")
                self.assertIn("492700", crear_convocatoria(notas_corte=notas_corte).masters)

    def test_rechaza_una_puntuacion_por_encima_de_10(self):
        with self.assertRaisesRegex(ValueError, "entre 0 y 10"):
            crear_convocatoria(notas_corte=NOTAS_CORTE.replace(CORTE_492700, "<b>RESTO</b>-10,01"))


class TestPuntuaciones(unittest.TestCase):
    def test_la_minima_solo_cuenta_la_nota_media(self):
        for codigo, minima in (("492700", "7.061"), ("518302", "4.2366"), ("807203", "0")):
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.puntuacion_minima(codigo, NOTA_MEDIA_CLAUDIA), Decimal(minima))

    def test_la_maxima_suma_un_10_en_el_resto_de_criterios(self):
        for codigo, maxima in (("492700", "7.061"), ("518302", "8.2366"), ("807203", "10")):
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.puntuacion_maxima(codigo, NOTA_MEDIA_CLAUDIA), Decimal(maxima))


class TestPosibilidad(unittest.TestCase):
    def test_la_prioridad_decide_antes_que_la_puntuacion(self):
        for codigo, esperada in (("492700", Posibilidad.ENTRA_SEGURO), ("407908", Posibilidad.NO_ENTRA)):
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.posibilidad(codigo, TITULACION, NOTA_MEDIA_CLAUDIA), esperada)

    def test_con_la_misma_prioridad_decide_la_puntuacion(self):
        casos = (("4,00", Posibilidad.ENTRA_SEGURO), ("5,37", Posibilidad.DEPENDE), ("9,00", Posibilidad.NO_ENTRA))
        for puntuacion, esperada in casos:
            with self.subTest(puntuacion=puntuacion):
                convocatoria = crear_convocatoria(notas_corte=NOTAS_CORTE.replace(CORTE_102902, f"<b>RESTO</b>-{puntuacion}"))
                self.assertEqual(convocatoria.posibilidad("102902", TITULACION, NOTA_MEDIA_CLAUDIA), esperada)

    def test_responde_aunque_no_haya_puntuacion_de_corte(self):
        for codigo, esperada in (("493003", Posibilidad.ENTRA_SEGURO), ("324208", Posibilidad.NO_SE_SABE)):
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.posibilidad(codigo, TITULACION, NOTA_MEDIA_CLAUDIA), esperada)


class TestPosibilidades(unittest.TestCase):
    def test_claudia_sabe_su_posibilidad_en_cada_master_de_su_catalogo(self):
        esperadas = {"102902": Posibilidad.DEPENDE, "324208": Posibilidad.NO_SE_SABE,
                     "407908": Posibilidad.NO_ENTRA, "492700": Posibilidad.ENTRA_SEGURO,
                     "493003": Posibilidad.ENTRA_SEGURO, "518302": Posibilidad.NO_ENTRA,
                     "803141": Posibilidad.NO_SE_SABE, "807203": Posibilidad.NO_ENTRA,
                     "A06400": Posibilidad.ENTRA_SEGURO}
        self.assertEqual(CONVOCATORIA.posibilidades(TITULACION, NOTA_MEDIA_CLAUDIA), esperadas)

    def test_claudia_sabe_en_que_masteres_su_prioridad_pide_un_requisito_adicional(self):
        self.assertEqual(CONVOCATORIA.con_requisito_adicional(TITULACION), ["407908"])

    def test_acepta_una_nota_media_en_los_limites(self):
        for nota_media in (Decimal("5"), Decimal("10")):
            with self.subTest(nota_media=nota_media):
                self.assertEqual(len(CONVOCATORIA.posibilidades(TITULACION, nota_media)), len(CODIGOS_CATALOGO))

    def test_rechaza_una_nota_media_fuera_de_5_a_10(self):
        for nota_media in (Decimal("4.99"), Decimal("10.01")):
            with self.subTest(nota_media=nota_media), self.assertRaisesRegex(ValueError, "entre 5 y 10"):
                CONVOCATORIA.posibilidades(TITULACION, nota_media)
