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
        lados = (a, b, c)

        if any(lado <= 0 for lado in lados):
            raise ValueError(self.ERRO_LADO_NAO_POSITIVO)

        menor, meio, maior = sorted(lados)
        if menor + meio <= maior:
            raise ValueError(self.ERRO_DESIGUALDADE)

        distintos = len(set(lados))
        if distintos == 1:
            return TipoTriangulo.EQUILATERO
        if distintos == 2:
            return TipoTriangulo.ISOSCELES
        return TipoTriangulo.ESCALENO
