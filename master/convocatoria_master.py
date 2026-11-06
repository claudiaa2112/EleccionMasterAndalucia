from collections.abc import Mapping
from dataclasses import dataclass

from .corte import CorteNumerico
from .master import Master

CIFRAS_CODIGO_MASTER = 6
PESO_MAXIMO_NOTA_MEDIA = 100
PUNTUACION_MAXIMA = 10


@dataclass(eq=False)
class ConvocatoriaMaster:
    identificador: str
    masters: Mapping[str, Master]

    def __post_init__(self) -> None:
        for codigo, master in self.masters.items():
            if len(codigo) != CIFRAS_CODIGO_MASTER or not codigo.isdigit():
                raise ValueError(f"El código del máster debe tener {CIFRAS_CODIGO_MASTER} cifras.")
            if not 0 <= master.ponderacion_nota_media <= PESO_MAXIMO_NOTA_MEDIA:
                raise ValueError(
                    f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
            if isinstance(master.corte, CorteNumerico) and not 0 <= master.corte.puntuacion <= PUNTUACION_MAXIMA:
                raise ValueError(
                    f"La puntuación del último admitido debe estar entre 0 y {PUNTUACION_MAXIMA}.")
