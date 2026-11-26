import unittest

from ejemplos import CODIGOS_CATALOGO, CONVOCATORIA, TITULACION, crear_convocatoria, leer_pagina

from master.master import Acceso
from master.prioridad_carreras import PrioridadCarrera

CATALOGO = leer_pagina("catalogo.html")


class TestPrioridadDeClaudiaEnElCatalogo(unittest.TestCase):
    def test_la_prioridad_de_claudia_en_cada_master_sale_del_catalogo(self):
        casos = (("492700", Acceso(PrioridadCarrera.ALTA, False)),
                 ("407908", Acceso(PrioridadCarrera.MEDIA, True)),
                 ("A06400", Acceso(PrioridadCarrera.ALTA, False)))
        for codigo, acceso in casos:
            with self.subTest(codigo=codigo):
                self.assertEqual(CONVOCATORIA.masters[codigo].accesos[TITULACION], acceso)

    def test_cada_master_del_catalogo_aparece_una_sola_vez(self):
        admiten = [codigo for codigo, master in CONVOCATORIA.masters.items() if TITULACION in master.accesos]
        self.assertEqual(sorted(admiten), sorted(CODIGOS_CATALOGO))

    def test_no_se_puede_cambiar_la_prioridad_de_un_master(self):
        with self.assertRaises(TypeError):
            CONVOCATORIA.masters["492700"].accesos[TITULACION] = Acceso(PrioridadCarrera.RESTO, False)

    def test_rechaza_un_catalogo_con_un_master_repetido(self):
        with self.assertRaisesRegex(ValueError, "repetido en el catálogo"):
            crear_convocatoria(catalogo=CATALOGO + CATALOGO)
