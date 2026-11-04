from collections.abc import Mapping
from dataclasses import dataclass

from .master import Master

@dataclass(eq=False)
class ConvocatoriaMaster:
    identificador: str
    masters: Mapping[str, Master]
