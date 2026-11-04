from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from .corte import CorteNumerico, EstadoCorte
from .prioridad_carreras import PrioridadCarrera

@dataclass(frozen=True)
class Requisito:
    descripcion: str
    obligatorio: bool

@dataclass(frozen=True)
class Criterio:
    ponderacion: Decimal
    calculable: bool

@dataclass(frozen=True)
class Acceso:
    prioridad: PrioridadCarrera
    codigos_requisitos: frozenset[str]

@dataclass(eq=False)
class Master:
    accesos: Mapping[str, Acceso]
    criterios: Mapping[str, Criterio]
    requisitos: Mapping[str, Requisito]
    corte: CorteNumerico | EstadoCorte
