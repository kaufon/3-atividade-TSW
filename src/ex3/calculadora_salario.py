from decimal import ROUND_HALF_UP, Decimal

from ex3.cargo import Cargo
from ex3.funcionario import Funcionario


class CalculadoraSalario:
    CENTAVO = Decimal("0.01")

    def calcular(self, funcionario: Funcionario) -> Decimal:
        salario = funcionario.salario_base

        if funcionario.cargo is Cargo.DESENVOLVEDOR:
            desconto = Decimal("0.20") if salario >= Decimal("3000") else Decimal("0.10")
        elif funcionario.cargo is Cargo.DBA:
            desconto = Decimal("0.25") if salario >= Decimal("2000") else Decimal("0.15")
        elif funcionario.cargo is Cargo.TESTADOR:
            desconto = Decimal("0.25") if salario >= Decimal("2000") else Decimal("0.15")
        else:
            desconto = Decimal("0.30") if salario >= Decimal("5000") else Decimal("0.20")

        liquido = salario * (Decimal("1") - desconto)
        return liquido.quantize(self.CENTAVO, rounding=ROUND_HALF_UP)
