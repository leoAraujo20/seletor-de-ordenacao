# Seletor de ordenação

## Execução

Para executar o fluxo completo em um único comando:

```bash
.venv/bin/python -m src.main
```

O comando gera os datasets, executa os benchmarks, salva os resultados e
exibe o algoritmo vencedor de cada cenário. A quantidade de repetições pode
ser alterada:

```bash
.venv/bin/python -m src.main --repetitions 10
```

Para usar os arquivos já existentes em `src/data`:

```bash
.venv/bin/python -m src.main --skip-generation
```

O módulo antigo continua disponível como compatibilidade:

```bash
.venv/bin/python -m src.benchmarks.run_benchmark
```

Ao final, o `main` mostra a validação da seleção:

```text
Cenário identificado: lista_minuscula
Arquivo consultado: .../src/benchmarks/results.json
Algoritmo selecionado: insertion_sort
Tempo salvo do selecionado: 0.008 ms
Menor tempo salvo no cenário: 0.008 ms
Seleção confirmada: SIM
```

Essa confirmação é feita comparando o tempo do algoritmo retornado por
`choose_benchmarked_algorithm()` com `min()` dos tempos salvos para o cenário.
Se o algoritmo escolhido não for o menor, o programa encerra com erro em vez
de apresentar uma validação falsa.

O seletor oferece duas formas de escolha:

```python
from src.selector import choose_measured_algorithm, sort

dados = [4, 1, 3, 2]
algoritmo = choose_measured_algorithm(dados, repetitions=3)
resultado = sort(dados, measured=True)
```

Para persistir os tempos na pasta `src/benchmarks`, execute:

```bash
python -m src.benchmarks.run_benchmark
```

Esse comando gera ou atualiza quatro entradas em `src/data` e mede os
algoritmos usando esses arquivos:

```text
src/data/
├── aleatorio_chaves_grandes.txt
├── faixa_estreita.txt
├── quase_ordenado.txt
└── lista_minuscula.txt
```

Para gerar somente os dados:

```bash
python -m src.data.generate_data
```

Os arquivos usam um inteiro por linha, o que facilita a inspeção e permite
substituir um cenário por dados próprios. O benchmark pode receber outro
diretório com `measure_data_scenarios(directory)`.

Depois, o algoritmo vencedor pode ser obtido sem medir novamente:

```python
from src.selector import choose_benchmarked_algorithm

algoritmo = choose_benchmarked_algorithm(dados)
resultado = algoritmo(dados)
if resultado is None:
    resultado = dados
```

Ou diretamente pela função unificada:

```python
resultado = sort(dados, use_saved_benchmark=True)
```

O seletor classifica `dados` em um dos quatro cenários e consulta o menor
tempo salvo em `src/benchmarks/results.json`. Se o arquivo não existir, execute
o comando de benchmark antes de chamar `choose_benchmarked_algorithm`.

`choose_algorithm` usa heurísticas e não mede tempo. Para a atividade, use
`measure_data_scenarios()` para medir todos os métodos nos quatro cenários,
usando os arquivos persistidos em `src/data`:

```python
from src.selector import measure_data_scenarios

medicoes = measure_data_scenarios(repetitions=3)
for scenario, algorithms in medicoes.items():
    vencedor = min(algorithms, key=algorithms.get)
    print(scenario.value, vencedor, algorithms[vencedor], "ms")
```

Os cenários são:

- aleatório com chaves grandes;
- faixa estreita;
- quase ordenado;
- lista minúscula.

Um tempo `inf` significa que o algoritmo não é aplicável ao cenário. Por
exemplo, `counting_sort` não é executado em uma faixa numérica grande, pois
isso exigiria uma tabela de contagem potencialmente enorme.