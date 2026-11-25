from dataclasses import dataclass
from decimal import Decimal

from .prioridad_carreras import PrioridadCarrera

@dataclass(frozen=True)
class CorteNumerico:
    prioridad: PrioridadCarrera
    puntuacion: Decimal
