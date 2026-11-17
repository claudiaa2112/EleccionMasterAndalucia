from master.corte import EstadoCorte
from master.master import Master


def crear_master(peso=100, corte=EstadoCorte.SIN_ADJUDICACION, accesos={}):
    return Master(accesos=accesos, ponderacion_nota_media=peso, requisitos_adicionales={}, corte=corte)
