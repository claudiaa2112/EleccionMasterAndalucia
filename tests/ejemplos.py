from master.corte import EstadoCorte
from master.master import Master


def crear_master(peso=100, corte=EstadoCorte.SIN_ADJUDICACION, accesos=None):
    return Master(accesos=accesos or {}, ponderacion_nota_media=peso, corte=corte)


TITULACION = "GRADO EN INGENIERÍA INFORMÁTICA"
