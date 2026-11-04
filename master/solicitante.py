from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

@dataclass(eq=False)
class Solicitante:
    titulacion: str
    nota_media: Decimal
    idiomas: Mapping[str, str]
