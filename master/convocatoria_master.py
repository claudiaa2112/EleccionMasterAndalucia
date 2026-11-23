import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from html import unescape

from .corte import CorteNumerico
from .master import PESO_MAXIMO_NOTA_MEDIA, PUNTUACION_MAXIMA, Acceso, EstadoCorte, Master
from .posibilidad import Posibilidad
from .prioridad_carreras import PrioridadCarrera

FORMA_CODIGO_MASTER = re.compile(r"\d{6}|A\d{5}")
INICIO_FILA = re.compile(r"<tr\b")
CELDA = re.compile(r"<td\b[^>]*>(.*?)</td>", re.DOTALL)
ETIQUETA = re.compile(r"<[^>]+>")
NOTA_MEDIA_MINIMA = 5
SIN_ADJUDICAR = "AÚN SIN ADJ."
MARCA_TODOS_ADMITIDOS = "**"
CRITERIO_NOTA_MEDIA = "NOTA MEDIA DEL EXPEDIENTE ACADEMICO"
PESO_SIN_NOTA_MEDIA = 0


@dataclass(eq=False)
class ConvocatoriaMaster:
    titulacion: str
    masters: Mapping[str, Master]

    @classmethod
    def comprobar_masters(cls, masters: Mapping[str, Master]) -> None:
        if not all(map(cls.es_codigo_master_valido, masters)):
            raise ValueError("El código del máster debe tener 6 cifras, o una A y 5 cifras.")
        if not all(map(cls.es_peso_valido, masters.values())):
            raise ValueError(f"El peso de la nota media debe estar entre 0 y {PESO_MAXIMO_NOTA_MEDIA}.")
        if not all(map(cls.es_corte_valido, masters.values())):
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
    def filas_de_la_pagina(pagina: str) -> list[str]:
        return INICIO_FILA.split(pagina)[1:]

    @staticmethod
    def celdas_de_la_fila(fila: str) -> list[str]:
        return CELDA.findall(fila)

    @staticmethod
    def texto_de_la_celda(celda: str) -> str:
        return " ".join(unescape(ETIQUETA.sub("", celda)).split())

    @staticmethod
    def por_codigo[T](filas: list[tuple[str, T]], pagina: str) -> dict[str, T]:
        masters = dict(filas)
        if len(masters) < len(filas):
            raise ValueError(f"Hay un máster repetido en {pagina}.")
        return masters

    @classmethod
    def accesos_del_catalogo(cls, catalogo: str) -> dict[str, Acceso]:
        accesos = []
        for celdas in map(cls.celdas_de_la_fila, cls.filas_de_la_pagina(catalogo)):
            if len(celdas) > 3:
                codigo = cls.texto_de_la_celda(celdas[0])
                prioridad = PrioridadCarrera[cls.texto_de_la_celda(celdas[3])]
                con_requisito_adicional = "text-danger" in celdas[3]
                accesos.append((codigo, Acceso(prioridad, con_requisito_adicional)))
        return cls.por_codigo(accesos, "el catálogo")

    @classmethod
    def cortes_de_las_notas(cls, notas_corte: str) -> dict[str, CorteNumerico | EstadoCorte]:
        cortes = []
        for fila in filter(lambda fila: "celda2" in fila, cls.filas_de_la_pagina(notas_corte)):
            celdas = cls.celdas_de_la_fila(fila)
            codigo = cls.texto_de_la_celda(celdas[0])
            prioridad, puntuacion = cls.texto_de_la_celda(celdas[3]).split("-")
            if prioridad == SIN_ADJUDICAR:
                corte = EstadoCorte.SIN_ADJUDICACION
            elif puntuacion.startswith(MARCA_TODOS_ADMITIDOS):
                corte = EstadoCorte.TODOS_ADMITIDOS
            else:
                corte = CorteNumerico(PrioridadCarrera[prioridad], Decimal(puntuacion.replace(",", ".")))
            cortes.append((codigo, corte))
        return cls.por_codigo(cortes, "las notas de corte")

    @classmethod
    def peso_de_la_ficha(cls, ficha: str) -> int:
        pesos = [cls.texto_de_la_celda(cls.celdas_de_la_fila(fila)[-1])
                 for fila in cls.filas_de_la_pagina(ficha) if CRITERIO_NOTA_MEDIA in fila]
        return int(pesos[0]) if pesos else PESO_SIN_NOTA_MEDIA

    @staticmethod
    def ficha_del_master(fichas: Mapping[str, str], codigo: str) -> str:
        if codigo not in fichas:
            raise ValueError(f"Falta la ficha del máster {codigo}.")
        return fichas[codigo]

    @classmethod
    def desde_las_paginas_del_dua(cls, titulacion: str, catalogo: str,
                                  notas_corte: str, fichas: Mapping[str, str]) -> ConvocatoriaMaster:
        cortes = cls.cortes_de_las_notas(notas_corte)
        masters = {codigo: Master(accesos={titulacion: acceso},
                                  ponderacion_nota_media=cls.peso_de_la_ficha(cls.ficha_del_master(fichas, codigo)),
                                  corte=cortes.get(codigo, EstadoCorte.SIN_ADJUDICACION))
                   for codigo, acceso in cls.accesos_del_catalogo(catalogo).items()}
        cls.comprobar_masters(masters)
        return cls(titulacion, masters)

    def posibilidades(self, nota_media: Decimal) -> dict[str, Posibilidad]:
        self.comprobar_nota_media(nota_media)
        return {codigo: master.posibilidad(self.titulacion, nota_media) for codigo, master in self.masters.items()}

    def con_requisito_adicional(self) -> list[str]:
        return [codigo for codigo, master in self.masters.items()
                if master.accesos[self.titulacion].con_requisito_adicional]
