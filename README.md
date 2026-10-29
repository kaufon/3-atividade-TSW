# Atividade — JUnit e TDD

Resolução dos três exercícios de testes de unidade e TDD em **Python 3** com **pytest** e **pytest-cov**.

| Exercício | Tema | Testes | Cobertura (linhas / branches) |
| --------- | ---- | ------ | ----------------------------- |
| 1 | Classificação de triângulos | 21 | 100% / 100% |
| 2 | `PersonDAO.isValidToInclude()` | 27 | 100% / 100% |
| 3 | Calculadora de salário líquido | 17 | 100% / 100% |
| **Total** | | **65** | **100% / 100%** |

## Estrutura

```
├── src/ex1/   triangulo.py
├── src/ex2/   models.py, person_dao.py
├── src/ex3/   cargo.py, funcionario.py, calculadora_salario.py
├── tests/     test_ex1_triangulo.py, test_ex2_person_dao.py, test_ex3_calculadora.py
├── pyproject.toml
└── requirements.txt
```

## Build

Em Python, o "build" é a preparação do ambiente virtual com as dependências.

```bash
# Linux / macOS / WSL
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# dependências (pytest e pytest-cov)
pip install -r requirements.txt
```

## Execução dos testes

```bash
pytest -v
```

Saída resumida:

```
65 passed
```

## Evidências de cobertura

Um comando por exercício, com cobertura de **linhas e de branches**:

### Exercício 1 — Triângulo

```bash
pytest tests/test_ex1_triangulo.py --cov=src/ex1 --cov-branch --cov-report=term-missing
```

```
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
src/ex1/__init__.py        0      0      0      0   100%
src/ex1/triangulo.py      21      0      8      0   100%
------------------------------------------------------------------
TOTAL                     21      0      8      0   100%
============================== 21 passed in 0.06s ==============================
```

### Exercício 2 — isValidToInclude

```bash
pytest tests/test_ex2_person_dao.py --cov=src/ex2 --cov-branch --cov-report=term-missing
```

```
Name                    Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------
src/ex2/__init__.py         0      0      0      0   100%
src/ex2/models.py          11      0      0      0   100%
src/ex2/person_dao.py      32      0     12      0   100%
-------------------------------------------------------------------
TOTAL                      43      0     12      0   100%
============================== 27 passed in 0.06s ==============================
```

### Exercício 3 — Calculadora de salário

```bash
pytest tests/test_ex3_calculadora.py --cov=src/ex3 --cov-branch --cov-report=term-missing
```

```
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
src/ex3/__init__.py                  0      0      0      0   100%
src/ex3/calculadora_salario.py      12      0      0      0   100%
src/ex3/cargo.py                     6      0      0      0   100%
src/ex3/funcionario.py               9      0      0      0   100%
----------------------------------------------------------------------------
TOTAL                               27      0      0      0   100%
============================== 17 passed in 0.05s ==============================
```

Relatório HTML navegável (opcional):

```bash
pytest --cov=src --cov-branch --cov-report=html
# abre htmlcov/index.html
```

---

## Exercício 1 — Triângulo

`Triangulo.classificar(a, b, c)` devolve um `TipoTriangulo` (`EQUILATERO`, `ISOSCELES`, `ESCALENO`) ou lança `ValueError`.

**Decisões de projeto**

- **Ordem das validações:** primeiro os lados positivos, depois a desigualdade triangular, por último a classificação. Se a desigualdade viesse antes, a checagem de positivos ficaria inalcançável — a comparação estrita já barra zero e negativo — e a cobertura de branches não fecharia.
- **Ordenação dos lados:** com `sorted()`, a condição `menor + meio <= maior` cobre todas as permutações numa única comparação, cobrindo tanto "soma igual" quanto "soma menor".
- **Mensagens distintas por erro,** usadas com `match=` nos testes, para que cada CT prove que caiu na regra certa e não em outra que também lançaria `ValueError`.

**Casos de teste**

| CT      | Situação                       | Entrada                        | Esperado     |
| ------- | ------------------------------ | ------------------------------ | ------------ |
| 01      | Escaleno válido                | (3, 4, 5)                      | `ESCALENO`   |
| 02      | Isósceles válido               | (5, 5, 8)                      | `ISOSCELES`  |
| 03      | Equilátero válido              | (3, 3, 3)                      | `EQUILATERO` |
| 04–06   | Isósceles — permutações        | (3,3,4) · (3,4,3) · (4,3,3)    | `ISOSCELES`  |
| 07      | Um valor zero                  | (0, 4, 5)                      | `ValueError` |
| 08      | Um valor negativo              | (−1, 4, 5)                     | `ValueError` |
| 09–14   | Soma de 2 lados = 3º lado      | 6 permutações de (1, 2, 3)     | `ValueError` |
| 15–20   | Soma de 2 lados < 3º lado      | 6 permutações de (1, 2, 4)     | `ValueError` |
| 21      | Três valores iguais a zero     | (0, 0, 0)                      | `ValueError` |

As permutações dos CTs 09–20 são geradas com `itertools.permutations` e `@pytest.mark.parametrize`, de modo que **cada permutação é um caso de teste independente** no relatório do pytest.

## Exercício 2 — `isValidToInclude()`

Implementa o diagrama de classes (`Person 1 — 1..* Email`, `PersonDAO`). O método devolve uma **lista de erros** (vazia quando a pessoa é válida).

Regras validadas:

1. Nome com ao menos 2 partes;
2. Nome composto apenas por letras;
3. Idade no intervalo `[1, 200]`;
4. Ao menos um `Email` associado (multiplicidade `1..*`);
5. Email no formato `____@____.____`, com ao menos um caractere em cada parte.

**Decisões de projeto**

- O nome `isValidToInclude` foi mantido em camelCase, como no diagrama, mesmo fora da convenção PEP 8.
- `name.split()` sem argumento: `split(" ")` produziria partes vazias em caso de espaço duplo, o que faria `"Maria  Silva"` falhar por um motivo errado.
- `str.isalpha()` em vez de um regex `[A-Za-z]`, porque aceita acentuação — `"José Conceição"` é um nome válido.
- `re.fullmatch` em vez de `re.match` com `$`, porque `$` também casa antes de um `\n` final e aceitaria `"a@b.c\n"`.
- A validação **não interrompe no primeiro erro**: há um teste em que nome, idade e email são inválidos ao mesmo tempo e os três erros são devolvidos.
- As mensagens são constantes de classe, reaproveitadas nas asserções dos testes.
- `save()` também é coberto: persiste em memória e lança `ValueError` quando a validação falha.

## Exercício 3 — Calculadora de salário

`CalculadoraSalario.calcular(funcionario)` aplica o desconto conforme o cargo:

| Cargo         | Desconto ≥ limite | Desconto < limite | Limite     |
| ------------- | ----------------- | ----------------- | ---------- |
| DESENVOLVEDOR | 20%               | 10%               | 3.000,00   |
| DBA           | 25%               | 15%               | 2.000,00   |
| TESTADOR      | 25%               | 15%               | 2.000,00   |
| GERENTE       | 30%               | 20%               | 5.000,00   |

**Decisões de projeto**

- Valores monetários em `Decimal` criado **a partir de string** e arredondados com `quantize(Decimal("0.01"), ROUND_HALF_UP)`. `float` tem erro de representação e tornaria o arredondamento imprevisível em casos como `2999.99`.
- Após os testes de DBA e TESTADOR ficarem verdes (regras idênticas), a cadeia de `if`/`elif` foi substituída por uma tabela `Cargo → (limite, desconto_alto, desconto_baixo)`. Esse é o passo de **refactor** do ciclo TDD: comportamento inalterado, testes verdes antes e depois.

**Testes de valor-limite** (onde o "maior ou igual" costuma quebrar):

| Cargo         | No limite           | 1 centavo abaixo    |
| ------------- | ------------------- | ------------------- |
| DESENVOLVEDOR | 3.000,00 → 2.400,00 | 2.999,99 → 2.699,99 |
| DBA           | 2.000,00 → 1.500,00 | 1.999,99 → 1.699,99 |
| TESTADOR      | 2.000,00 → 1.500,00 | 1.999,99 → 1.699,99 |
| GERENTE       | 5.000,00 → 3.500,00 | 4.999,99 → 3.999,99 |

---

## Evidência do TDD

O ciclo **vermelho → verde → refactor** está registrado no histórico de commits: os testes de cada regra foram commitados antes da implementação correspondente.

[Ver histórico de commits](../../commits/main)
