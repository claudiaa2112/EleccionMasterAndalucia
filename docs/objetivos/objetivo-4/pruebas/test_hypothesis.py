import pytest
from hypothesis import given, strategies as st

from master.convocatoria_master import ConvocatoriaMaster
from master.corte import EstadoCorte
from master.master import Master

MASTER = Master(accesos={}, ponderacion_nota_media=100, requisitos_adicionales={},
                corte=EstadoCorte.SIN_ADJUDICACION)


@given(st.text(alphabet="0123456789", max_size=10).filter(lambda codigo: len(codigo) != 6))
def test_rechaza_cualquier_codigo_que_no_tenga_seis_cifras(codigo):
    with pytest.raises(ValueError, match="seis cifras"):
        ConvocatoriaMaster("2026-2027", {codigo: MASTER})
