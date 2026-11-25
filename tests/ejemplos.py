from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from master.convocatoria_master import ConvocatoriaMaster

TITULACION = "GRADO EN INGENIERÍA INFORMÁTICA"
NOTA_MEDIA_CLAUDIA = Decimal("7.061")
PAGINAS_DUA = Path(__file__).parent / "paginas_dua"
CODIGOS_CATALOGO = ["102902", "324208", "407908", "492700", "493003", "518302", "803141", "A06400", "807203"]


def leer_pagina(nombre):
    return (PAGINAS_DUA / nombre).read_text(encoding="utf-8")


def leer_fichas():
    return {codigo: leer_pagina(f"fichas/ficha_{codigo}.html") for codigo in CODIGOS_CATALOGO}


def crear_convocatoria(fichas=None, catalogo=None, notas_corte=None):
    return ConvocatoriaMaster(fichas or leer_fichas(), {TITULACION: catalogo or leer_pagina("catalogo.html")},
                              notas_corte or leer_pagina("notas_corte.html"))


CONVOCATORIA = crear_convocatoria()


def master_real(codigo, **cambios):
    return replace(CONVOCATORIA.masters[codigo], **cambios)
