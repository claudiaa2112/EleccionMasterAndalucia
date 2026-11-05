from collections.abc import Mapping
from dataclasses import dataclass

from .corte import CorteNumerico, EstadoCorte
from .prioridad_carreras import PrioridadCarrera

@dataclass(frozen=True)
class RequisitoAdicional:
    descripcion: str
    obligatorio: bool

@dataclass(frozen=True)
class Acceso:
    prioridad: PrioridadCarrera
    codigos_requisitos: frozenset[str]

@dataclass(eq=False)
class Master:
    accesos: Mapping[str, Acceso]
    ponderacion_nota_media: int
    requisitos_adicionales: Mapping[str, RequisitoAdicional]
    corte: CorteNumerico | EstadoCorte
