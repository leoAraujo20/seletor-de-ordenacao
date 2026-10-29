# Relatório — Seletor de ordenação

## 1. Comparação dos quatro cenários

Tempos registrados em `results.json`, em milissegundos:

| Cenário                      | Insertion |  Counting |  Radix | Quick | Merge |    Hybrid |
| ---------------------------- | --------: | --------: | -----: | ----: | ----: | --------: |
| Aleatório com chaves grandes |   174,565 |       `∞` | 14,757 | 6,491 | 7,688 | **5,489** |
| Faixa estreita               |   160,405 | **0,672** |  2,734 | 1,533 | 7,506 |    10,536 |
| Quase ordenado               | **0,501** |     0,973 |  5,356 | 5,233 | 5,570 |     3,593 |
| Lista minúscula              | **0,006** |       `∞` |  0,123 | 0,022 | 0,024 |     0,007 |

`∞` significa que o método não foi considerado aplicável. O `counting_sort` é desabilitado quando a faixa numérica ultrapassa 1.000.000 posições.

Os datasets são gerados em `datasets.py`: listas de 2.000 elementos nos três primeiros cenários e uma lista de 12 elementos no cenário minúsculo.

## 2. Vencedor de cada cenário

- **Aleatório com chaves grandes: `hybrid_sort`**  
  Venceu com 5,489 ms. Embora o radix sort seja adequado para inteiros grandes, sua implementação separa negativos e positivos e faz várias passagens pelos dígitos. O híbrido usa particionamento rápido e insertion sort em sublistas pequenas, apresentando menor tempo neste benchmark.

- **Faixa estreita: `counting_sort`**  
  Venceu com 0,672 ms. Existem muitos valores, mas concentrados em uma faixa pequena. Assim, o custo da tabela de contagem é baixo e o algoritmo evita comparações repetidas.

- **Quase ordenado: `insertion_sort`**  
  Venceu com 0,501 ms. O insertion sort trabalha muito bem quando há poucas inversões, pois movimenta apenas os elementos fora de posição.

- **Lista minúscula: `insertion_sort`**  
  Venceu com 0,006 ms. Para apenas 12 elementos, o custo baixo e a simplicidade do insertion sort superam o custo de algoritmos recursivos ou que criam estruturas auxiliares.

## 3. Regras usadas por `choose_algorithm`

As regras estão em `algorithm_selector.py`:

1. Se `len(values) <= 32`, escolhe `insertion_sort`.
2. Se a entrada estiver quase ordenada, escolhe `insertion_sort`.
3. Para inteiros:
   - se a faixa de valores for menor ou igual a 1.000.000 e também menor ou igual a `4 * tamanho`, escolhe `counting_sort`;
   - se o maior valor absoluto ou a faixa forem pelo menos 1.000.000, escolhe `radix_sort`;
   - caso contrário, escolhe `quick_sort`.
4. Para valores não inteiros:
   - até 64 elementos: `merge_sort`;
   - acima disso: `hybrid_sort`.

As análises de tipo, faixa e ordenação estão em `input_analysis.py`.

Essas regras vieram de:

- características dos próprios datasets;
- complexidade esperada dos algoritmos;
- limite prático para evitar tabelas enormes no counting sort;
- testes automatizados em `test_algorithm_selector.py`.

O `choose_algorithm` é heurístico: ele não mede os algoritmos antes de escolher. Já `choose_benchmarked_algorithm` classifica a entrada e consulta os tempos previamente salvos.

## 4. Custo de executar o `choose_algorithm`

O custo é **O(n)** no pior caso.

A função pode fazer algumas passagens lineares pela entrada:

- verificar se está quase ordenada;
- verificar se todos os valores são inteiros;
- calcular a faixa numérica;
- encontrar o maior valor absoluto.

Como o número de passagens é constante, o custo total continua sendo O(n). O uso de memória extra é O(1), desconsiderando a entrada.

Na prática, esse custo é pequeno comparado ao custo de ordenar uma lista grande. Portanto, **compensa**, especialmente quando:

- as entradas são grandes;
- o seletor é usado repetidamente;
- não é desejável medir todos os algoritmos a cada execução.

A alternativa `choose_measured_algorithm` é muito mais cara, pois executa os seis algoritmos e repete as medições.

## 5. Um cenário em que o seletor erra

O seletor erra no cenário **aleatório com chaves grandes**.

Para esse tipo de entrada, a regra:

```python
if max(abs(value) for value in values) >= 1_000_000:
    return radix_sort
```

faz o `choose_algorithm` selecionar `radix_sort`.

Entretanto, no benchmark:

- `radix_sort`: 14,757 ms;
- `hybrid_sort`: **5,489 ms**.

Logo, a heurística escolhe radix sort, mas o vencedor real é o hybrid sort. Isso mostra que complexidade teórica e características gerais da entrada não garantem o melhor desempenho em uma implementação concreta: custos de alocação, tratamento de números negativos e detalhes da linguagem também influenciam.
