from ex2.models import Person


class PersonDAO:
    ERRO_NOME_PARTES = "O nome deve ser composto por ao menos 2 partes"
    ERRO_NOME_LETRAS = "O nome deve ser composto apenas por letras"
    ERRO_IDADE_FORA_DO_INTERVALO = "A idade deve estar no intervalo [1, 200]"
    ERRO_SEM_EMAIL = "A pessoa deve ter ao menos um email associado"
    ERRO_EMAIL_FORMATO = "O email deve estar no formato ____@____.____"

    def __init__(self) -> None:
        self.pessoas: list[Person] = []

    def isValidToInclude(self, p: Person) -> list[str]:
        raise NotImplementedError

    def save(self, p: Person) -> None:
        raise NotImplementedError
