from decimal import Decimal

from ex3.funcionario import Funcionario


class CalculadoraSalario:
    def calcular(self, funcionario: Funcionario) -> Decimal:
        raise NotImplementedError
