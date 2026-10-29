from decimal import ROUND_HALF_UP, Decimal

from ex3.cargo import Cargo
from ex3.funcionario import Funcionario


class CalculadoraSalario:
    CENTAVO = Decimal("0.01")

    # cargo -> (salario-limite, desconto a partir do limite, desconto abaixo dele)
    REGRAS = {
        Cargo.DESENVOLVEDOR: (Decimal("3000"), Decimal("0.20"), Decimal("0.10")),
        Cargo.DBA: (Decimal("2000"), Decimal("0.25"), Decimal("0.15")),
        Cargo.TESTADOR: (Decimal("2000"), Decimal("0.25"), Decimal("0.15")),
        Cargo.GERENTE: (Decimal("5000"), Decimal("0.30"), Decimal("0.20")),
    }

    def calcular(self, funcionario: Funcionario) -> Decimal:
        salario = funcionario.salario_base
        limite, desconto_alto, desconto_baixo = self.REGRAS[funcionario.cargo]

        desconto = desconto_alto if salario >= limite else desconto_baixo
        liquido = salario * (Decimal("1") - desconto)

        return liquido.quantize(self.CENTAVO, rounding=ROUND_HALF_UP)
