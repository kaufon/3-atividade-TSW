from dataclasses import dataclass
from decimal import Decimal

from ex3.cargo import Cargo


@dataclass
class Funcionario:
    nome: str
    email: str
    salario_base: Decimal
    cargo: Cargo
