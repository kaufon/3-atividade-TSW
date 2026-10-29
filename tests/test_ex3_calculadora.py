from decimal import Decimal

import pytest

from ex3.calculadora_salario import CalculadoraSalario
from ex3.cargo import Cargo
from ex3.funcionario import Funcionario


@pytest.fixture
def calculadora():
    return CalculadoraSalario()


def funcionario(cargo, salario_base):
    return Funcionario(
        nome="Maria Silva",
        email="maria@empresa.com",
        salario_base=Decimal(salario_base),
        cargo=cargo,
    )


# DESENVOLVEDOR - 20% a partir de 3.000,00, senao 10%
def test_desenvolvedor_acima_do_limite_desconta_20(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.DESENVOLVEDOR, "5000.00"))
    assert str(resultado) == "4000.00"


def test_desenvolvedor_abaixo_do_limite_desconta_10(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.DESENVOLVEDOR, "1000.00"))
    assert str(resultado) == "900.00"


# DBA - 25% a partir de 2.000,00, senao 15%
def test_dba_acima_do_limite_desconta_25(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.DBA, "3000.00"))
    assert str(resultado) == "2250.00"


def test_dba_abaixo_do_limite_desconta_15(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.DBA, "1000.00"))
    assert str(resultado) == "850.00"


# TESTADOR - mesma regra do DBA
def test_testador_acima_do_limite_desconta_25(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.TESTADOR, "3000.00"))
    assert str(resultado) == "2250.00"


def test_testador_abaixo_do_limite_desconta_15(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.TESTADOR, "1000.00"))
    assert str(resultado) == "850.00"


# GERENTE - 30% a partir de 5.000,00, senao 20%
def test_gerente_acima_do_limite_desconta_30(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.GERENTE, "6000.00"))
    assert str(resultado) == "4200.00"


def test_gerente_abaixo_do_limite_desconta_20(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.GERENTE, "4000.00"))
    assert str(resultado) == "3200.00"


# Valores-limite: exatamente no limite ja usa o desconto maior
@pytest.mark.parametrize(
    "cargo, salario_base, esperado",
    [
        (Cargo.DESENVOLVEDOR, "3000.00", "2400.00"),
        (Cargo.DBA, "2000.00", "1500.00"),
        (Cargo.TESTADOR, "2000.00", "1500.00"),
        (Cargo.GERENTE, "5000.00", "3500.00"),
    ],
    ids=lambda v: str(v),
)
def test_salario_exatamente_no_limite_usa_desconto_maior(
    calculadora, cargo, salario_base, esperado
):
    assert str(calculadora.calcular(funcionario(cargo, salario_base))) == esperado


@pytest.mark.parametrize(
    "cargo, salario_base, esperado",
    [
        (Cargo.DESENVOLVEDOR, "2999.99", "2699.99"),
        (Cargo.DBA, "1999.99", "1699.99"),
        (Cargo.TESTADOR, "1999.99", "1699.99"),
        (Cargo.GERENTE, "4999.99", "3999.99"),
    ],
    ids=lambda v: str(v),
)
def test_um_centavo_abaixo_do_limite_usa_desconto_menor(
    calculadora, cargo, salario_base, esperado
):
    assert str(calculadora.calcular(funcionario(cargo, salario_base))) == esperado


def test_resultado_sempre_com_duas_casas_decimais(calculadora):
    resultado = calculadora.calcular(funcionario(Cargo.DESENVOLVEDOR, "1234.567"))
    assert str(resultado) == "1111.11"
