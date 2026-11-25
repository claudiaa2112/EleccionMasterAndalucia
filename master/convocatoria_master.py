import re
from collections.abc import Mapping
from dataclasses import replace
from decimal import Decimal

from .corte import CorteNumerico
from .master import Acceso, EstadoCorte, Master
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera
from .tablas_html import celdas_de_la_fila, esta_en_rojo, filas_de_la_pagina, texto_de_la_celda

FORMA_CODIGO_MASTER = re.compile(r"\d{6}|A\d{5}")
NOTA_MEDIA_MINIMA = 5
SIN_ADJUDICAR = "AÚN SIN ADJ."
MARCA_TODOS_ADMITIDOS = "**"
CRITERIO_NOTA_MEDIA = "NOTA MEDIA DEL EXPEDIENTE ACADEMICO"
PESO_SIN_NOTA_MEDIA = 0
PESO_MAXIMO_NOTA_MEDIA = 100
PUNTUACION_MAXIMA = 10
POSIBILIDAD_POR_ESTADO = {
    EstadoCorte.TODOS_ADMITIDOS: Posibilidad.ENTRA_SEGURO,
    EstadoCorte.SIN_ADJUDICACION: Posibilidad.NO_SE_SABE,
}


class ConvocatoriaMaster:
    def __init__(self, fichas: Mapping[str, str], catalogos: Mapping[str, str], notas_corte: str):
        self.masters: dict[str, Master] = {}
        for titulacion, catalogo in catalogos.items():
            self.leer_catalogo(titulacion, catalogo, fichas)
        self.leer_notas_corte(notas_corte)
        self.rechazar_datos_imposibles()

    def leer_ficha(self, codigo: str, fichas: Mapping[str, str], accesos: Mapping[str, Acceso]) -> None:
        if codigo not in fichas:
            raise ValueError(f"Falta la ficha del máster {codigo}.")
        pesos = [texto_de_la_celda(celdas_de_la_fila(fila)[-1])
                 for fila in filas_de_la_pagina(fichas[codigo]) if CRITERIO_NOTA_MEDIA in fila]
        self.masters[codigo] = Master(accesos=accesos,
                                      ponderacion_nota_media=int(pesos[0]) if pesos else PESO_SIN_NOTA_MEDIA,
                                      corte=EstadoCorte.SIN_ADJUDICACION)

    def leer_catalogo(self, titulacion: str, catalogo: str, fichas: Mapping[str, str]) -> None:
        for celdas in map(celdas_de_la_fila, filas_de_la_pagina(catalogo)):
            if len(celdas) > 3:
                codigo = texto_de_la_celda(celdas[0])
                if not FORMA_CODIGO_MASTER.fullmatch(codigo):
                    raise ValueError("El código del máster debe tener 6 cifras, o una A y 5 cifras.")
                acceso = Acceso(PrioridadCarrera[texto_de_la_celda(celdas[3])], esta_en_rojo(celdas[3]))
                if codigo not in self.masters:
                    self.leer_ficha(codigo, fichas, {titulacion: acceso})
                elif titulacion in self.masters[codigo].accesos:
                    raise ValueError(f"Hay un máster repetido en el catálogo de {titulacion}.")
                else:
                    self.masters[codigo] = replace(self.masters[codigo],
                                                   accesos={**self.masters[codigo].accesos, titulacion: acceso})

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
                self.masters[codigo] = replace(self.masters[codigo], corte=(
                    EstadoCorte.TODOS_ADMITIDOS if puntuacion.startswith(MARCA_TODOS_ADMITIDOS)
                    else CorteNumerico(PrioridadCarrera[prioridad], Decimal(puntuacion.replace(",", ".")))))

    def rechazar_datos_imposibles(self) -> None:
        if not all(0 <= master.ponderacion_nota_media <= PESO_MAXIMO_NOTA_MEDIA for master in self.masters.values()):
            raise ValueError(f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
        if not all(0 <= master.corte.puntuacion <= PUNTUACION_MAXIMA
                   for master in self.masters.values() if isinstance(master.corte, CorteNumerico)):
            raise ValueError(f"La puntuación del último admitido debe estar entre 0 y {PUNTUACION_MAXIMA}.")

    def posibilidades(self, titulacion: str, nota_media: Decimal) -> dict[str, Posibilidad]:
        if not NOTA_MEDIA_MINIMA <= nota_media <= PUNTUACION_MAXIMA:
            raise ValueError(f"La nota media debe estar entre {NOTA_MEDIA_MINIMA} y {PUNTUACION_MAXIMA}.")
        return {codigo: self.posibilidad(codigo, titulacion, nota_media)
                for codigo, master in self.masters.items() if titulacion in master.accesos}

    def posibilidad(self, codigo: str, titulacion: str, nota_media: Decimal) -> Posibilidad:
        master = self.masters[codigo]
        if isinstance(master.corte, EstadoCorte):
            return POSIBILIDAD_POR_ESTADO[master.corte]
        prioridad = master.accesos[titulacion].prioridad.value
        if prioridad > master.corte.prioridad.value:
            return Posibilidad.ENTRA_SEGURO
        if prioridad < master.corte.prioridad.value:
            return Posibilidad.NO_ENTRA
        if self.puntuacion_minima(codigo, nota_media) >= master.corte.puntuacion:
            return Posibilidad.ENTRA_SEGURO
        if self.puntuacion_maxima(codigo, nota_media) >= master.corte.puntuacion:
            return Posibilidad.DEPENDE
        return Posibilidad.NO_ENTRA

    def puntuacion_minima(self, codigo: str, nota_media: Decimal) -> Decimal:
        return self.masters[codigo].ponderacion_nota_media * nota_media / PESO_MAXIMO_NOTA_MEDIA

    def puntuacion_maxima(self, codigo: str, nota_media: Decimal) -> Decimal:
        peso_resto = PESO_MAXIMO_NOTA_MEDIA - self.masters[codigo].ponderacion_nota_media
        return self.puntuacion_minima(codigo, nota_media) + Decimal(peso_resto * PUNTUACION_MAXIMA) / PESO_MAXIMO_NOTA_MEDIA

    def con_requisito_adicional(self, titulacion: str) -> list[str]:
        return [codigo for codigo, master in self.masters.items()
                if titulacion in master.accesos and master.accesos[titulacion].con_requisito_adicional]
