from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera

class EstadoCorte(Enum):
    TODOS_ADMITIDOS = "TODOS_ADMITIDOS"
    SIN_ADJUDICACION = "SIN_ADJUDICACION"


POSIBILIDAD_POR_ESTADO = {
    EstadoCorte.TODOS_ADMITIDOS: Posibilidad.ENTRA_SEGURO,
    EstadoCorte.SIN_ADJUDICACION: Posibilidad.NO_SE_SABE,
}


@dataclass(frozen=True)
class CorteNumerico:
    prioridad: PrioridadCarrera
    puntuacion: Decimal

    def posibilidad(self, prioridad: PrioridadCarrera, minima: Decimal, maxima: Decimal) -> Posibilidad:
        if prioridad.es_mayor_que(self.prioridad):
            return Posibilidad.ENTRA_SEGURO
        if self.prioridad.es_mayor_que(prioridad):
            return Posibilidad.NO_ENTRA
        return self.posibilidad_por_puntuacion(minima, maxima)

    def posibilidad_por_puntuacion(self, minima: Decimal, maxima: Decimal) -> Posibilidad:
        if minima >= self.puntuacion:
            return Posibilidad.ENTRA_SEGURO
        if maxima >= self.puntuacion:
            return Posibilidad.DEPENDE
        return Posibilidad.NO_ENTRA
