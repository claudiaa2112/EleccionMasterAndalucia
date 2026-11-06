import pytest

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import EstadoCorte
from master.master import Master

MASTER = Master(accesos={}, ponderacion_nota_media=100, requisitos_adicionales={},
                corte=EstadoCorte.SIN_ADJUDICACION)


def test_acepta_codigo_de_seis_cifras():
    convocatoria = ConvocatoriaMaster("2026-2027", {"492700": MASTER})
    assert list(convocatoria.masters) == ["492700"]


def test_rechaza_codigo_de_cinco_cifras():
    with pytest.raises(ValueError, match="seis cifras"):
        ConvocatoriaMaster("2026-2027", {"49270": MASTER})
