from decimal import Decimal
from pathlib import Path

from master.convocatoria_master import ConvocatoriaMaster

TITULACION = "GRADO EN INGENIERÍA INFORMÁTICA"
NOTA_MEDIA_CLAUDIA = Decimal("7.061")
PAGINAS_DUA = Path(__file__).parent / "paginas_dua"
CODIGOS_CATALOGO = ["102902", "324208", "407908", "492700", "493003", "518302", "803141", "A06400", "807203"]
CATALOGO = (PAGINAS_DUA / "catalogo.html").read_text(encoding="utf-8")
NOTAS_CORTE = (PAGINAS_DUA / "notas_corte.html").read_text(encoding="utf-8")
FICHAS = {codigo: (PAGINAS_DUA / "fichas" / f"ficha_{codigo}.html").read_text(encoding="utf-8")
          for codigo in CODIGOS_CATALOGO}


def crear_convocatoria(fichas=None, catalogo=None, notas_corte=None):
    return ConvocatoriaMaster(fichas or FICHAS, {TITULACION: catalogo or CATALOGO}, notas_corte or NOTAS_CORTE)


CONVOCATORIA = crear_convocatoria()
