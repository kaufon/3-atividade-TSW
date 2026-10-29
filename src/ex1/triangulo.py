from enum import Enum


class TipoTriangulo(Enum):
    EQUILATERO = "EQUILATERO"
    ISOSCELES = "ISOSCELES"
    ESCALENO = "ESCALENO"


class Triangulo:
    ERRO_LADO_NAO_POSITIVO = "Todos os lados devem ser valores positivos"
    ERRO_DESIGUALDADE = (
        "A soma de dois lados deve ser maior que o terceiro lado "
        "(desigualdade triangular)"
    )

    def classificar(self, a: int, b: int, c: int) -> TipoTriangulo:
        raise NotImplementedError
