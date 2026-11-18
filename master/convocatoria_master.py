from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from .corte import CorteNumerico
from .master import PESO_MAXIMO_NOTA_MEDIA, PUNTUACION_MAXIMA, Master
from .posibilidad import Posibilidad

CIFRAS_CODIGO_MASTER = 6


def es_codigo_valido(codigo: str) -> bool:
    return len(codigo) == CIFRAS_CODIGO_MASTER and codigo.isdigit()


def es_peso_valido(master: Master) -> bool:
    return 0 <= master.ponderacion_nota_media <= PESO_MAXIMO_NOTA_MEDIA


def es_corte_valido(master: Master) -> bool:
    return not isinstance(master.corte, CorteNumerico) or 0 <= master.corte.puntuacion <= PUNTUACION_MAXIMA


@dataclass(eq=False)
class ConvocatoriaMaster:
    identificador: str
    masters: Mapping[str, Master]

    def __post_init__(self) -> None:
        if not all(map(es_codigo_valido, self.masters)):
            raise ValueError(f"El código del máster debe tener {CIFRAS_CODIGO_MASTER} cifras.")
        if not all(map(es_peso_valido, self.masters.values())):
            raise ValueError(f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
        if not all(map(es_corte_valido, self.masters.values())):
            raise ValueError(f"La puntuación del último admitido debe estar entre 0 y {PUNTUACION_MAXIMA}.")

    def posibilidades(self, titulacion: str, nota_media: Decimal) -> dict[str, Posibilidad]:
        return {codigo: master.posibilidad(titulacion, nota_media)
                for codigo, master in self.masters.items() if master.admite(titulacion)}
