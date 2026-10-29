# Plano — Atividade JUnit e TDD

**Entrega:** 29/10/2026 até as 23h, somente via Moodle: URL do repositório Git + `README.md` com build, execução dos testes e evidências de cobertura de cada exercício.

**Meta:** fechar tudo até 22:45, pra sobrar folga antes do Moodle fechar.

**Stack:** Python + pytest + pytest-cov. O setup é mais curto que o de TS (sem tsconfig nem ts-jest), é a linguagem que você mais usa e a cobertura sai com uma flag.

## 1. Setup · 19:45–20:00

```
tdd-atividade/
├── src/ex1/          triangulo.py
├── src/ex2/          models.py, person_dao.py
├── src/ex3/          cargo.py, funcionario.py, calculadora_salario.py
├── tests/            test_ex1_triangulo.py, test_ex2_person_dao.py, test_ex3_calculadora.py
├── pyproject.toml    # [tool.pytest.ini_options] pythonpath = ["src"], testpaths = ["tests"]
├── requirements.txt  # pytest, pytest-cov
└── .gitignore        # .venv, __pycache__, .pytest_cache, .coverage, htmlcov
```

- Crie o repo **público** no GitHub. Se for privado, o link não abre pro professor.
- Coloque um `__init__.py` em cada `src/exN/`.
- Não crie um arquivo `email.py`. Ele conflita com o módulo `email` da stdlib e gera um `ImportError` confuso. Por isso as classes ficam em `models.py`.
- O professor só enxerga o TDD pelo histórico de commits. Commite cada ciclo: `test(ex2): ...` (vermelho), depois `feat(ex2): ...` (verde), depois `refactor(...)`.

## 2. Ex. 1 – Triângulo · 20:00–20:35

O esqueleto é um Enum `TipoTriangulo` (EQUILATERO, ISOSCELES, ESCALENO) e o método `Triangulo.classificar(a, b, c)`, que retorna o tipo ou lança `ValueError`. Commite primeiro o esqueleto com `raise NotImplementedError` junto dos testes. A implementação vem no commit seguinte.

| CT    | Situação            | Entrada                     | Esperado   |
| ----- | ------------------- | --------------------------- | ---------- |
| 01    | Escaleno            | (3, 4, 5)                   | ESCALENO   |
| 02    | Isósceles           | (5, 5, 8)                   | ISOSCELES  |
| 03    | Equilátero          | (3, 3, 3)                   | EQUILATERO |
| 04–06 | Isósceles permutado | (3,3,4) · (3,4,3) · (4,3,3) | ISOSCELES  |
| 07    | Um zero             | (0, 4, 5)                   | ValueError |
| 08    | Um negativo         | (−1, 4, 5)                  | ValueError |
| 09–14 | Soma = 3º lado      | permutações de (1, 2, 3)    | ValueError |
| 15–20 | Soma < 3º lado      | permutações de (1, 2, 4)    | ValueError |
| 21    | Três zeros          | (0, 0, 0)                   | ValueError |

```python
@pytest.mark.parametrize("lados", list(permutations((1, 2, 3))), ids=str)
def test_soma_igual_ao_terceiro_lado(lados):
    with pytest.raises(ValueError, match="desigualdade"):
        Triangulo().classificar(*lados)
```

- **Ordem das checagens:** primeiro lados ≤ 0, depois a desigualdade, por último a classificação. Se a desigualdade vier antes, a checagem de positivo nunca executa, porque a desigualdade estrita já barra zero e negativo. Aí a cobertura não fecha 100%.
- **Truque da ordenação:** ordene os lados e teste `menor + meio <= maior`. Uma comparação cobre todas as permutações.
- **Mensagens:** use uma mensagem diferente pra cada erro e `match=` no teste. Assim cada CT prova que caiu na regra certa.

## 3. Ex. 2 – isValidToInclude · 20:35–21:30

Use `@dataclass` para `Person` e `Email`, com `emails: list[Email] = field(default_factory=list)`. Mantenha o nome `isValidToInclude` igual ao do diagrama, mesmo fora do PEP 8, porque é por ele que o professor vai procurar. Defina as mensagens de erro como constantes e reaproveite nos testes.

Faça um ciclo por regra, nesta ordem:

1. Pessoa válida retorna `[]`. A implementação mínima é `return []`.
2. Nome de uma parte só (`"Maria"`) gera erro. Use `split()` sem argumento, porque `split(" ")` cria uma parte vazia quando há espaço duplo.
3. Nome com algo que não é letra (`"Maria S1lva"`) gera erro, e `"José Conceição"` é válido. `str.isalpha()` aceita acento; um regex `[A-Za-z]` reprovaria.
4. Idade nos limites: 0 ✗ · 1 ✓ · 200 ✓ · 201 ✗.
5. Pessoa sem email gera erro. É a multiplicidade `1..*` do diagrama.
6. Formato do email, com parametrize: `a@b.c` é válido; `ab.c`, `@b.c`, `a@.c`, `a@b.`, `a@b` e `""` são inválidos. Use `re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", ...)`, porque `re.match` com `$` aceita um `\n` no final.
7. Nome, idade e email inválidos ao mesmo tempo devolvem os 3 erros na lista. Isso prova que a validação não para no primeiro erro.
8. `save()` está no diagrama, e código sem teste derruba a cobertura. Implemente em memória, lançando erro se a validação falhar, com 2 testes.

## 4. Ex. 3 – Salários · 21:30–22:10

As classes são `Cargo` (Enum), `Funcionario` (dataclass com nome, email, salario_base e cargo) e `CalculadoraSalario.calcular(funcionario)`. Guarde dinheiro em `Decimal` criado a partir de string e arredonde com `quantize(Decimal("0.01"), ROUND_HALF_UP)`. Float tem erro de representação e deixa o arredondamento imprevisível.

1. DESENVOLVEDOR com 5.000 dá 4.000.
2. DESENVOLVEDOR com 1.000 dá 900. É aqui que o `if` aparece.
3. DBA acima e abaixo de 2.000.
4. TESTADOR tem a mesma regra do DBA. Esse é o momento do **refactor**: com tudo verde, troque os `if`s por uma tabela `Cargo → (limite, desconto se ≥, desconto se <)`, num commit `refactor` separado.
5. GERENTE acima e abaixo de 5.000.
6. Valores-limite, onde o "maior ou igual" costuma quebrar:

| Cargo         | No limite           | 1 centavo abaixo    |
| ------------- | ------------------- | ------------------- |
| DESENVOLVEDOR | 3.000,00 → 2.400,00 | 2.999,99 → 2.699,99 |
| DBA           | 2.000,00 → 1.500,00 | 1.999,99 → 1.699,99 |
| TESTADOR      | 2.000,00 → 1.500,00 | 1.999,99 → 1.699,99 |
| GERENTE       | 5.000,00 → 3.500,00 | 4.999,99 → 3.999,99 |

## 5. README e cobertura · 22:10–22:35

Em Python, "build" significa preparar o ambiente. Deixe isso explícito no README:

```bash
# build (Linux/macOS/WSL)
python3 -m venv .venv && source .venv/bin/activate
# build (Windows PowerShell)
python -m venv .venv; .venv\Scripts\Activate.ps1

pip install -r requirements.txt

# testes
pytest -v

# cobertura por exercício (cole cada saída no README)
pytest tests/test_ex1_triangulo.py --cov=src/ex1 --cov-branch --cov-report=term-missing
pytest tests/test_ex2_person_dao.py --cov=src/ex2 --cov-branch --cov-report=term-missing
pytest tests/test_ex3_calculadora.py --cov=src/ex3 --cov-branch --cov-report=term-missing
```

Estruture o README assim: build, testes, depois uma seção por exercício (resumo, decisões, a tabela de CTs no Ex. 1 e a saída de cobertura num bloco de código). No final, um link pro histórico de commits como evidência do TDD.

A meta é 100% de linhas e branches. A coluna `Missing` aponta a linha exata que falta testar. Um print do relatório HTML (`--cov-report=html`) é opcional.

## 6. Envio · 22:35–22:45

- Abra o link do repo numa aba anônima pra confirmar que está público.
- Clone o repo numa pasta nova e siga o README ao pé da letra. Se algum passo falhar ali, vai falhar pro professor também.
- Mande a URL no Moodle e não mexa mais no repo.
