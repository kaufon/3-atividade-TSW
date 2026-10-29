from itertools import permutations

import pytest

from ex1.triangulo import TipoTriangulo, Triangulo


@pytest.fixture
def triangulo():
    return Triangulo()


# CT01 - escaleno valido
def test_ct01_escaleno(triangulo):
    assert triangulo.classificar(3, 4, 5) is TipoTriangulo.ESCALENO


# CT02 - isosceles valido
def test_ct02_isosceles(triangulo):
    assert triangulo.classificar(5, 5, 8) is TipoTriangulo.ISOSCELES


# CT03 - equilatero valido
def test_ct03_equilatero(triangulo):
    assert triangulo.classificar(3, 3, 3) is TipoTriangulo.EQUILATERO


# CT04 a CT06 - isosceles com permutacao dos mesmos valores
@pytest.mark.parametrize("lados", [(3, 3, 4), (3, 4, 3), (4, 3, 3)], ids=str)
def test_ct04_ct06_isosceles_permutado(triangulo, lados):
    assert triangulo.classificar(*lados) is TipoTriangulo.ISOSCELES


# CT07 - um valor zero
def test_ct07_um_lado_zero(triangulo):
    with pytest.raises(ValueError, match="positivos"):
        triangulo.classificar(0, 4, 5)


# CT08 - um valor negativo
def test_ct08_um_lado_negativo(triangulo):
    with pytest.raises(ValueError, match="positivos"):
        triangulo.classificar(-1, 4, 5)


# CT09 a CT14 - soma de dois lados igual ao terceiro, uma permutacao por CT
@pytest.mark.parametrize("lados", list(permutations((1, 2, 3))), ids=str)
def test_ct09_ct14_soma_igual_ao_terceiro_lado(triangulo, lados):
    with pytest.raises(ValueError, match="desigualdade"):
        triangulo.classificar(*lados)


# CT15 a CT20 - soma de dois lados menor que o terceiro, uma permutacao por CT
@pytest.mark.parametrize("lados", list(permutations((1, 2, 4))), ids=str)
def test_ct15_ct20_soma_menor_que_o_terceiro_lado(triangulo, lados):
    with pytest.raises(ValueError, match="desigualdade"):
        triangulo.classificar(*lados)


# CT21 - tres valores iguais a zero
def test_ct21_tres_lados_zero(triangulo):
    with pytest.raises(ValueError, match="positivos"):
        triangulo.classificar(0, 0, 0)
