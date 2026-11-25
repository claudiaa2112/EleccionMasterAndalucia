import re
from collections.abc import Mapping
from decimal import Decimal

from .corte import CorteNumerico
from .master import PESO_MAXIMO_NOTA_MEDIA, PUNTUACION_MAXIMA, Acceso, EstadoCorte, Master
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera
from .tablas_html import celdas_de_la_fila, filas_de_la_pagina, texto_de_la_celda

FORMA_CODIGO_MASTER = re.compile(r"\d{6}|A\d{5}")
NOTA_MEDIA_MINIMA = 5
SIN_ADJUDICAR = "AÚN SIN ADJ."
MARCA_TODOS_ADMITIDOS = "**"
CRITERIO_NOTA_MEDIA = "NOTA MEDIA DEL EXPEDIENTE ACADEMICO"
PESO_SIN_NOTA_MEDIA = 0


class ConvocatoriaMaster:
    def __init__(self, fichas: Mapping[str, str], catalogos: Mapping[str, str], notas_corte: str):
        self.masters: dict[str, Master] = {}
        for codigo, ficha in fichas.items():
            self.leer_ficha(codigo, ficha)
        for titulacion, catalogo in catalogos.items():
            self.leer_catalogo(titulacion, catalogo)
        self.leer_notas_corte(notas_corte)
        self.rechazar_datos_imposibles()

    def leer_ficha(self, codigo: str, ficha: str) -> None:
        pesos = [texto_de_la_celda(celdas_de_la_fila(fila)[-1])
                 for fila in filas_de_la_pagina(ficha) if CRITERIO_NOTA_MEDIA in fila]
        self.masters[codigo] = Master(accesos={},
                                      ponderacion_nota_media=int(pesos[0]) if pesos else PESO_SIN_NOTA_MEDIA,
                                      corte=EstadoCorte.SIN_ADJUDICACION)

    def master_con_ficha(self, codigo: str) -> Master:
        if codigo not in self.masters:
            raise ValueError(f"Falta la ficha del máster {codigo}.")
        return self.masters[codigo]

    def leer_catalogo(self, titulacion: str, catalogo: str) -> None:
        for celdas in map(celdas_de_la_fila, filas_de_la_pagina(catalogo)):
            if len(celdas) > 3:
                master = self.master_con_ficha(texto_de_la_celda(celdas[0]))
                if titulacion in master.accesos:
                    raise ValueError(f"Hay un máster repetido en el catálogo de {titulacion}.")
                master.accesos[titulacion] = Acceso(PrioridadCarrera[texto_de_la_celda(celdas[3])],
                                                    "text-danger" in celdas[3])

    def leer_notas_corte(self, notas_corte: str) -> None:
        leidos = set()
        for celdas in map(celdas_de_la_fila, filter(lambda fila: "celda2" in fila, filas_de_la_pagina(notas_corte))):
            codigo = texto_de_la_celda(celdas[0])
            if codigo in leidos:
                raise ValueError("Hay un máster repetido en las notas de corte.")
            leidos.add(codigo)
            prioridad, puntuacion = texto_de_la_celda(celdas[3]).split("-")
            if codigo in self.masters and prioridad != SIN_ADJUDICAR:
                self.masters[codigo].corte = (
                    EstadoCorte.TODOS_ADMITIDOS if puntuacion.startswith(MARCA_TODOS_ADMITIDOS)
                    else CorteNumerico(PrioridadCarrera[prioridad], Decimal(puntuacion.replace(",", "."))))

    def rechazar_datos_imposibles(self) -> None:
        if not all(FORMA_CODIGO_MASTER.fullmatch(codigo) for codigo in self.masters):
            raise ValueError("El código del máster debe tener 6 cifras, o una A y 5 cifras.")
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
