import re

from ex2.models import Person


class PersonDAO:
    ERRO_NOME_PARTES = "O nome deve ser composto por ao menos 2 partes"
    ERRO_NOME_LETRAS = "O nome deve ser composto apenas por letras"
    ERRO_IDADE_FORA_DO_INTERVALO = "A idade deve estar no intervalo [1, 200]"
    ERRO_SEM_EMAIL = "A pessoa deve ter ao menos um email associado"
    ERRO_EMAIL_FORMATO = "O email deve estar no formato ____@____.____"

    IDADE_MINIMA = 1
    IDADE_MAXIMA = 200

    _FORMATO_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    def __init__(self) -> None:
        self.pessoas: list[Person] = []

    def isValidToInclude(self, p: Person) -> list[str]:
        erros: list[str] = []

        partes = p.name.split()
        if len(partes) < 2:
            erros.append(self.ERRO_NOME_PARTES)
        if not all(parte.isalpha() for parte in partes):
            erros.append(self.ERRO_NOME_LETRAS)

        if not self.IDADE_MINIMA <= p.age <= self.IDADE_MAXIMA:
            erros.append(self.ERRO_IDADE_FORA_DO_INTERVALO)

        if not p.emails:
            erros.append(self.ERRO_SEM_EMAIL)
        elif not all(self._FORMATO_EMAIL.fullmatch(e.name) for e in p.emails):
            erros.append(self.ERRO_EMAIL_FORMATO)

        return erros

    def save(self, p: Person) -> None:
        erros = self.isValidToInclude(p)
        if erros:
            raise ValueError("; ".join(erros))
        self.pessoas.append(p)
