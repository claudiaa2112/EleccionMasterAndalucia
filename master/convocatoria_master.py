from collections.abc import Mapping
from dataclasses import dataclass

from .master import Master

CIFRAS_CODIGO_MASTER = 6
PESO_MAXIMO_NOTA_MEDIA = 100


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
