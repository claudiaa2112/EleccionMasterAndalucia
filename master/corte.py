from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from .prioridad_carreras import PrioridadCarrera

class EstadoCorte(Enum):
    TODOS_ADMITIDOS = "TODOS_ADMITIDOS"
    SIN_ADJUDICACION = "SIN_ADJUDICACION"

@dataclass(frozen=True)
class CorteNumerico:
    prioridad: PrioridadCarrera
    puntuacion: Decimal
