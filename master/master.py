from types import MappingProxyType
from dataclasses import dataclass
from enum import Enum

from .corte import CorteNumerico
from .prioridad_carreras import PrioridadCarrera

class EstadoCorte(Enum):
    TODOS_ADMITIDOS = "TODOS_ADMITIDOS"
    SIN_ADJUDICACION = "SIN_ADJUDICACION"

@dataclass(frozen=True)
class Acceso:
    prioridad: PrioridadCarrera
    con_requisito_adicional: bool

@dataclass(frozen=True)
class Master:
    accesos: MappingProxyType[str, Acceso]
    ponderacion_nota_media: int
    corte: CorteNumerico | EstadoCorte
