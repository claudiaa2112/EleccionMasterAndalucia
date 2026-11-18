from enum import Enum

class PrioridadCarrera(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3
    RESTO = 4

    def es_mayor_que(self, otra: PrioridadCarrera) -> bool:
        return self.value < otra.value
