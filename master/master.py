from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from .corte import POSIBILIDAD_POR_ESTADO, CorteNumerico, EstadoCorte
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera

PESO_MAXIMO_NOTA_MEDIA = 100
PUNTUACION_MAXIMA = 10

@dataclass(frozen=True)
class Acceso:
    prioridad: PrioridadCarrera
    con_requisito_adicional: bool

@dataclass(eq=False)
class Master:
    accesos: Mapping[str, Acceso]
    ponderacion_nota_media: int
    requisitos_adicionales: Mapping[str, str]
    corte: CorteNumerico | EstadoCorte

    def admite(self, titulacion: str) -> bool:
        return titulacion in self.accesos

    def posibilidad(self, titulacion: str, nota_media: Decimal) -> Posibilidad:
        if isinstance(self.corte, EstadoCorte):
            return POSIBILIDAD_POR_ESTADO[self.corte]
        return self.corte.posibilidad(self.accesos[titulacion].prioridad,
                                      self.puntuacion_minima(nota_media), self.puntuacion_maxima(nota_media))

    def puntuacion_minima(self, nota_media: Decimal) -> Decimal:
        return self.ponderacion_nota_media * nota_media / PESO_MAXIMO_NOTA_MEDIA

    def puntuacion_maxima(self, nota_media: Decimal) -> Decimal:
        peso_resto = PESO_MAXIMO_NOTA_MEDIA - self.ponderacion_nota_media
        return self.puntuacion_minima(nota_media) + Decimal(peso_resto * PUNTUACION_MAXIMA) / PESO_MAXIMO_NOTA_MEDIA
