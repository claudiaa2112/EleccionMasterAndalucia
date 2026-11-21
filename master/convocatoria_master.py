import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from lxml import html

from .corte import CorteNumerico
from .master import PESO_MAXIMO_NOTA_MEDIA, PUNTUACION_MAXIMA, Acceso, EstadoCorte, Master
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera

FORMA_CODIGO_MASTER = re.compile(r"\d{6}|A\d{5}")
NOTA_MEDIA_MINIMA = 5
SIN_ADJUDICAR = "AÚN SIN ADJ."
MARCA_TODOS_ADMITIDOS = "**"
CRITERIO_NOTA_MEDIA = "NOTA MEDIA DEL EXPEDIENTE ACADEMICO"


@dataclass(eq=False)
class ConvocatoriaMaster:
    identificador: str
    masters: Mapping[str, Master]

    def __post_init__(self) -> None:
        if not all(map(self.es_codigo_master_valido, self.masters)):
            raise ValueError("El código del máster debe tener 6 cifras, o una A y 5 cifras.")
        if not all(map(self.es_peso_valido, self.masters.values())):
            raise ValueError(f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
        if not all(map(self.es_corte_valido, self.masters.values())):
            raise ValueError(f"La puntuación del último admitido debe estar entre 0 y {PUNTUACION_MAXIMA}.")

    @staticmethod
    def es_codigo_master_valido(codigo: str) -> bool:
        return FORMA_CODIGO_MASTER.fullmatch(codigo) is not None

    @staticmethod
    def es_peso_valido(master: Master) -> bool:
        return 0 <= master.ponderacion_nota_media <= PESO_MAXIMO_NOTA_MEDIA

    @staticmethod
    def es_corte_valido(master: Master) -> bool:
        return not isinstance(master.corte, CorteNumerico) or 0 <= master.corte.puntuacion <= PUNTUACION_MAXIMA

    @staticmethod
    def comprobar_nota_media(nota_media: Decimal) -> None:
        if nota_media < NOTA_MEDIA_MINIMA or nota_media > PUNTUACION_MAXIMA:
            raise ValueError(f"La nota media debe estar entre {NOTA_MEDIA_MINIMA} y {PUNTUACION_MAXIMA}.")

    @staticmethod
    def accesos_del_catalogo(catalogo: str) -> dict[str, Acceso]:
        accesos = {}
        for fila in html.fromstring(catalogo).xpath("//tr[count(td) > 3]"):
            codigo = fila.xpath("string(td[1])").strip()
            prioridad = PrioridadCarrera[fila.xpath("string(td[4])").strip()]
            en_rojo = bool(fila.xpath("td[4]//*[contains(@class, 'text-danger')]"))
            accesos[codigo] = Acceso(prioridad, en_rojo)
        return accesos

    @staticmethod
    def cortes_de_las_notas(notas_corte: str) -> dict[str, CorteNumerico | EstadoCorte]:
        cortes = {}
        for fila in html.fromstring(notas_corte).xpath("//tr[td[@class='celda2']]"):
            codigo = fila.xpath("string(td[1])").strip()
            prioridad, puntuacion = " ".join(fila.xpath("string(td[4])").split()).split("-")
            if prioridad == SIN_ADJUDICAR:
                cortes[codigo] = EstadoCorte.SIN_ADJUDICACION
            elif puntuacion.startswith(MARCA_TODOS_ADMITIDOS):
                cortes[codigo] = EstadoCorte.TODOS_ADMITIDOS
            else:
                cortes[codigo] = CorteNumerico(PrioridadCarrera[prioridad], Decimal(puntuacion.replace(",", ".")))
        return cortes

    @staticmethod
    def peso_de_la_ficha(ficha: str) -> int:
        pesos = html.fromstring(ficha).xpath(f"//tr[td[contains(., '{CRITERIO_NOTA_MEDIA}')]]/td[last()]/text()")
        return int(pesos[0]) if pesos else 0

    @classmethod
    def desde_las_paginas_del_dua(cls, identificador: str, titulacion: str, catalogo: str,
                                  notas_corte: str, fichas: Mapping[str, str]) -> ConvocatoriaMaster:
        cortes = cls.cortes_de_las_notas(notas_corte)
        masters = {codigo: Master(accesos={titulacion: acceso},
                                  ponderacion_nota_media=cls.peso_de_la_ficha(fichas[codigo]),
                                  corte=cortes[codigo])
                   for codigo, acceso in cls.accesos_del_catalogo(catalogo).items()}
        return cls(identificador, masters)

    def posibilidades(self, titulacion: str, nota_media: Decimal) -> dict[str, Posibilidad]:
        self.comprobar_nota_media(nota_media)
        return {codigo: master.posibilidad(titulacion, nota_media)
                for codigo, master in self.masters.items() if master.admite(titulacion)}
