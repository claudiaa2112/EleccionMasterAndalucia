from collections.abc import Mapping
from dataclasses import dataclass

from .master import Master

CIFRAS_CODIGO_MASTER = 6


@dataclass(eq=False)
class ConvocatoriaMaster:
    identificador: str
    masters: Mapping[str, Master]

    def __post_init__(self) -> None:
        for codigo in self.masters:
            if len(codigo) != CIFRAS_CODIGO_MASTER or not codigo.isdigit():
                raise ValueError(f"El código del máster debe tener {CIFRAS_CODIGO_MASTER} cifras.")
