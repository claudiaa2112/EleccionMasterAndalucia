import re
from html import unescape

INICIO_FILA = re.compile(r"<tr\b")
CELDA = re.compile(r"<td\b[^>]*>(.*?)</td>", re.DOTALL)
ETIQUETA = re.compile(r"<[^>]+>")


def filas_de_la_pagina(pagina: str) -> list[str]:
    antes_de_la_primera_fila, *filas = INICIO_FILA.split(pagina)
    return filas


def celdas_de_la_fila(fila: str) -> list[str]:
    return CELDA.findall(fila)


def texto_de_la_celda(celda: str) -> str:
    return " ".join(unescape(ETIQUETA.sub("", celda)).split())


def esta_en_rojo(celda: str) -> bool:
    return "text-danger" in celda
