import pytest

from ex2.models import Email, Person
from ex2.person_dao import PersonDAO


@pytest.fixture
def dao():
    return PersonDAO()


def pessoa(name="Maria Silva", age=30, emails=None):
    if emails is None:
        emails = [Email(1, "maria@empresa.com")]
    return Person(id=1, name=name, age=age, emails=emails)


# Regra 0 - pessoa totalmente valida nao gera erros
def test_pessoa_valida_nao_gera_erros(dao):
    assert dao.isValidToInclude(pessoa()) == []


# Regra 1 - nome com ao menos 2 partes
def test_nome_com_uma_unica_parte_gera_erro(dao):
    erros = dao.isValidToInclude(pessoa(name="Maria"))
    assert erros == [PersonDAO.ERRO_NOME_PARTES]


def test_nome_com_tres_partes_e_valido(dao):
    assert dao.isValidToInclude(pessoa(name="Maria da Silva")) == []


# Regra 2 - nome composto apenas por letras
def test_nome_com_caractere_nao_alfabetico_gera_erro(dao):
    erros = dao.isValidToInclude(pessoa(name="Maria S1lva"))
    assert erros == [PersonDAO.ERRO_NOME_LETRAS]


def test_nome_com_acentuacao_e_valido(dao):
    assert dao.isValidToInclude(pessoa(name="Jose Conceicao")) == []
    assert dao.isValidToInclude(pessoa(name="José Conceição")) == []


# Regra 3 - idade no intervalo [1, 200]
@pytest.mark.parametrize("idade", [1, 2, 199, 200])
def test_idade_dentro_do_intervalo_e_valida(dao, idade):
    assert dao.isValidToInclude(pessoa(age=idade)) == []


@pytest.mark.parametrize("idade", [-1, 0, 201])
def test_idade_fora_do_intervalo_gera_erro(dao, idade):
    erros = dao.isValidToInclude(pessoa(age=idade))
    assert erros == [PersonDAO.ERRO_IDADE_FORA_DO_INTERVALO]


# Regra 4 - ao menos um Email associado (multiplicidade 1..* do diagrama)
def test_pessoa_sem_email_gera_erro(dao):
    erros = dao.isValidToInclude(pessoa(emails=[]))
    assert erros == [PersonDAO.ERRO_SEM_EMAIL]


# Regra 5 - formato do email
@pytest.mark.parametrize(
    "endereco",
    ["a@b.c", "maria@empresa.com", "maria.silva@empresa.com.br"],
)
def test_email_em_formato_valido(dao, endereco):
    assert dao.isValidToInclude(pessoa(emails=[Email(1, endereco)])) == []


@pytest.mark.parametrize(
    "endereco",
    ["ab.c", "@b.c", "a@.c", "a@b.", "a@b", "", "a b@c.d"],
)
def test_email_em_formato_invalido_gera_erro(dao, endereco):
    erros = dao.isValidToInclude(pessoa(emails=[Email(1, endereco)]))
    assert erros == [PersonDAO.ERRO_EMAIL_FORMATO]


def test_apenas_um_email_invalido_entre_varios_ja_gera_erro(dao):
    emails = [Email(1, "maria@empresa.com"), Email(2, "invalido")]
    erros = dao.isValidToInclude(pessoa(emails=emails))
    assert erros == [PersonDAO.ERRO_EMAIL_FORMATO]


# Regra 6 - a validacao nao para no primeiro erro
def test_pessoa_invalida_em_tudo_acumula_os_tres_erros(dao):
    erros = dao.isValidToInclude(pessoa(name="Maria", age=0, emails=[]))
    assert erros == [
        PersonDAO.ERRO_NOME_PARTES,
        PersonDAO.ERRO_IDADE_FORA_DO_INTERVALO,
        PersonDAO.ERRO_SEM_EMAIL,
    ]


# Regra 7 - save() so persiste pessoas validas
def test_save_persiste_pessoa_valida(dao):
    p = pessoa()
    dao.save(p)
    assert dao.pessoas == [p]


def test_save_rejeita_pessoa_invalida(dao):
    with pytest.raises(ValueError, match=PersonDAO.ERRO_NOME_PARTES):
        dao.save(pessoa(name="Maria"))
    assert dao.pessoas == []
