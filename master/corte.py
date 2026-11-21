from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera

class EstadoCorte(Enum):
    TODOS_ADMITIDOS = "TODOS_ADMITIDOS"
    SIN_ADJUDICACION = "SIN_ADJUDICACION"


@dataclass(frozen=True)
class CorteNumerico:
    prioridad: PrioridadCarrera
    puntuacion: Decimal

    def posibilidad(self, prioridad: PrioridadCarrera, minima: Decimal, maxima: Decimal) -> Posibilidad:
        if prioridad.es_mayor_que(self.prioridad):
            return Posibilidad.ENTRA_SEGURO
        if self.prioridad.es_mayor_que(prioridad):
            return Posibilidad.NO_ENTRA
        if minima >= self.puntuacion:
            return Posibilidad.ENTRA_SEGURO
        if maxima >= self.puntuacion:
            return Posibilidad.DEPENDE
        return Posibilidad.NO_ENTRA
