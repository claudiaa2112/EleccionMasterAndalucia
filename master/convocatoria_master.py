import re
from collections.abc import Mapping
from decimal import Decimal

from .corte import CorteNumerico
from .master import PESO_MAXIMO_NOTA_MEDIA, PUNTUACION_MAXIMA, Acceso, EstadoCorte, Master
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera
from .tablas_html import celdas_de_la_fila, esta_en_rojo, filas_de_la_pagina, texto_de_la_celda

FORMA_CODIGO_MASTER = re.compile(r"\d{6}|A\d{5}")
NOTA_MEDIA_MINIMA = 5
SIN_ADJUDICAR = "AÚN SIN ADJ."
MARCA_TODOS_ADMITIDOS = "**"
CRITERIO_NOTA_MEDIA = "NOTA MEDIA DEL EXPEDIENTE ACADEMICO"
PESO_SIN_NOTA_MEDIA = 0


class ConvocatoriaMaster:
    def __init__(self, fichas: Mapping[str, str], catalogos: Mapping[str, str], notas_corte: str):
        self.masters: dict[str, Master] = {}
        for titulacion, catalogo in catalogos.items():
            self.leer_catalogo(titulacion, catalogo, fichas)
        self.leer_notas_corte(notas_corte)
        self.rechazar_datos_imposibles()

    def leer_ficha(self, codigo: str, fichas: Mapping[str, str]) -> None:
        if codigo not in fichas:
            raise ValueError(f"Falta la ficha del máster {codigo}.")
        pesos = [texto_de_la_celda(celdas_de_la_fila(fila)[-1])
                 for fila in filas_de_la_pagina(fichas[codigo]) if CRITERIO_NOTA_MEDIA in fila]
        self.masters[codigo] = Master(accesos={},
                                      ponderacion_nota_media=int(pesos[0]) if pesos else PESO_SIN_NOTA_MEDIA,
                                      corte=EstadoCorte.SIN_ADJUDICACION)

    def leer_catalogo(self, titulacion: str, catalogo: str, fichas: Mapping[str, str]) -> None:
        for celdas in map(celdas_de_la_fila, filas_de_la_pagina(catalogo)):
            if len(celdas) > 3:
                codigo = texto_de_la_celda(celdas[0])
                if not FORMA_CODIGO_MASTER.fullmatch(codigo):
                    raise ValueError("El código del máster debe tener 6 cifras, o una A y 5 cifras.")
                if codigo not in self.masters:
                    self.leer_ficha(codigo, fichas)
                master = self.masters[codigo]
                if titulacion in master.accesos:
                    raise ValueError(f"Hay un máster repetido en el catálogo de {titulacion}.")
                master.accesos[titulacion] = Acceso(PrioridadCarrera[texto_de_la_celda(celdas[3])],
                                                    esta_en_rojo(celdas[3]))

    def leer_notas_corte(self, notas_corte: str) -> None:
        leidos = set()
        for celdas in filter(lambda celdas: len(celdas) > 3, map(celdas_de_la_fila, filas_de_la_pagina(notas_corte))):
            codigo = texto_de_la_celda(celdas[0])
            if codigo not in self.masters:
                continue
            if codigo in leidos:
                raise ValueError("Hay un máster repetido en las notas de corte.")
            leidos.add(codigo)
            prioridad, puntuacion = texto_de_la_celda(celdas[3]).split("-")
            if prioridad != SIN_ADJUDICAR:
                self.masters[codigo].corte = (
                    EstadoCorte.TODOS_ADMITIDOS if puntuacion.startswith(MARCA_TODOS_ADMITIDOS)
                    else CorteNumerico(PrioridadCarrera[prioridad], Decimal(puntuacion.replace(",", "."))))

    def rechazar_datos_imposibles(self) -> None:
        if not all(0 <= master.ponderacion_nota_media <= PESO_MAXIMO_NOTA_MEDIA for master in self.masters.values()):
            raise ValueError(f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
        if not all(0 <= master.corte.puntuacion <= PUNTUACION_MAXIMA
                   for master in self.masters.values() if isinstance(master.corte, CorteNumerico)):
            raise ValueError(f"La puntuación del último admitido debe estar entre 0 y {PUNTUACION_MAXIMA}.")

    def posibilidades(self, titulacion: str, nota_media: Decimal) -> dict[str, Posibilidad]:
        if not NOTA_MEDIA_MINIMA <= nota_media <= PUNTUACION_MAXIMA:
            raise ValueError(f"La nota media debe estar entre {NOTA_MEDIA_MINIMA} y {PUNTUACION_MAXIMA}.")
        return {codigo: master.posibilidad(titulacion, nota_media)
                for codigo, master in self.masters.items() if master.admite(titulacion)}

    def con_requisito_adicional(self, titulacion: str) -> list[str]:
        return [codigo for codigo, master in self.masters.items()
                if master.admite(titulacion) and master.accesos[titulacion].con_requisito_adicional]
