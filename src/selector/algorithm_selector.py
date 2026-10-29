"""Seleção e medição de algoritmos de ordenação."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from statistics import median
from typing import Any

from src.benchmarks.scenarios import (
    Scenario,
    classify_scenario,
)
from src.benchmarks.storage import (
    BenchmarkResults,
)
from src.benchmarks.storage import (
    load_benchmark_results as _load_benchmark_results,
)
from src.benchmarks.storage import (
    save_benchmark_results as _save_benchmark_results,
)
from src.data.datasets import DEFAULT_DATA_PATH, load_datasets
from src.methods.counting_sort import counting_sort
from src.methods.hibrid_sort import hybrid_sort
from src.methods.insertion_sort import insertion_sort
from src.methods.merge_sort import merge_sort
from src.methods.quick_sort import quick_sort
from src.methods.radix_sort import radix_sort
from src.utils.input_analysis import (
    is_integer_input,
    is_nearly_sorted,
    value_range,
)
from src.utils.sorting import apply_sort, ensure_sorted
from src.utils.timing import measure_milliseconds

SortFunction = Callable[[list[Any]], list[Any] | None]
Algorithm = tuple[str, SortFunction]

_MAX_COUNTING_RANGE = 1_000_000
_COUNTING_RANGE_FACTOR = 4
_INSERTION_SIZE_LIMIT = 32
_ALGORITHMS: tuple[Algorithm, ...] = (
    ("insertion_sort", insertion_sort),
    ("counting_sort", counting_sort),
    ("radix_sort", radix_sort),
    ("quick_sort", quick_sort),
    ("merge_sort", merge_sort),
    ("hybrid_sort", hybrid_sort),
)
DEFAULT_BENCHMARK_PATH = (
    Path(__file__).resolve().parents[1] / "benchmarks" / "results.json"
)


def measure_algorithms(values: Sequence[Any], repetitions: int = 3) -> dict[str, float]:
    """Mede todos os algoritmos em milissegundos, sem alterar ``values``."""
    if repetitions < 1:
        raise ValueError("repetitions deve ser maior ou igual a 1")

    expected = sorted(values)
    measurements: dict[str, float] = {}
    for name, algorithm in _ALGORITHMS:
        if not _is_supported_for_measurement(name, values):
            measurements[name] = float("inf")
            continue

        elapsed_times: list[float] = []
        for _ in range(repetitions):
            candidate = list(values)
            result, elapsed = measure_milliseconds(algorithm, candidate)
            elapsed_times.append(elapsed)
            ordered = candidate if result is None else result
            ensure_sorted(name, ordered, expected)
        measurements[name] = median(elapsed_times)
    return measurements


def _is_supported_for_measurement(name: str, values: Sequence[Any]) -> bool:
    if name not in {"counting_sort", "radix_sort"}:
        return True
    if not is_integer_input(values):
        return False
    if not values:
        return True

    return name != "counting_sort" or value_range(values) <= _MAX_COUNTING_RANGE


def measure_data_scenarios(
    directory: str | Path = DEFAULT_DATA_PATH,
    repetitions: int = 3,
) -> dict[Scenario, dict[str, float]]:
    """Mede os algoritmos usando os arquivos persistidos em ``data``."""
    return {
        scenario: measure_algorithms(values, repetitions)
        for scenario, values in load_datasets(directory).items()
    }


def save_benchmark_results(
    results: BenchmarkResults, path: str | Path = DEFAULT_BENCHMARK_PATH
) -> Path:
    return _save_benchmark_results(results, path)


def load_benchmark_results(
    path: str | Path = DEFAULT_BENCHMARK_PATH,
) -> BenchmarkResults:
    return _load_benchmark_results(path)


def benchmark_and_save(
    repetitions: int = 3,
    path: str | Path = DEFAULT_BENCHMARK_PATH,
    data_directory: str | Path = DEFAULT_DATA_PATH,
) -> Path:
    """Mede os datasets persistidos e atualiza o arquivo de resultados."""
    return save_benchmark_results(
        measure_data_scenarios(data_directory, repetitions),
        path,
    )


def choose_benchmarked_algorithm(
    values: Sequence[Any], path: str | Path = DEFAULT_BENCHMARK_PATH
) -> SortFunction:
    """Escolhe o método com menor tempo salvo para o cenário da entrada."""
    scenario = classify_scenario(values)
    measurements = load_benchmark_results(path)[scenario]
    selected_name = min(measurements, key=measurements.__getitem__)
    return dict(_ALGORITHMS)[selected_name]


def choose_measured_algorithm(
    values: Sequence[Any], repetitions: int = 3
) -> SortFunction:
    """Escolhe o algoritmo mais rápido medido para uma entrada."""
    measurements = measure_algorithms(values, repetitions)
    selected_name = min(measurements, key=measurements.__getitem__)
    return dict(_ALGORITHMS)[selected_name]


def choose_algorithm(values: Sequence[Any]) -> SortFunction:
    """Escolhe o método mais adequado para as características de ``values``.

    Esta é a opção rápida, baseada nas características da entrada. Para
    escolher pelo tempo medido, use :func:`choose_measured_algorithm`.
    """
    size = len(values)

    if size <= _INSERTION_SIZE_LIMIT or is_nearly_sorted(values):
        return insertion_sort

    if is_integer_input(values):
        input_range = value_range(values)
        if (
            input_range <= _MAX_COUNTING_RANGE
            and input_range <= size * _COUNTING_RANGE_FACTOR
        ):
            return counting_sort
        if max(abs(value) for value in values) >= 1_000_000 or input_range >= 1_000_000:
            return radix_sort
        return quick_sort

    if size <= 64:
        return merge_sort
    return hybrid_sort


def sort(
    values: list[Any],
    measured: bool = False,
    use_saved_benchmark: bool = False,
) -> list[Any]:
    """Ordena ``values`` usando o algoritmo escolhido automaticamente.

    Os métodos que operam in-place retornam ``None``; os que criam uma nova
    lista retornam essa lista. Esta função oferece uma interface única e
    sempre devolve a lista ordenada.
    """
    if use_saved_benchmark:
        algorithm = choose_benchmarked_algorithm(values)
    elif measured:
        algorithm = choose_measured_algorithm(values)
    else:
        algorithm = choose_algorithm(values)
    return apply_sort(algorithm, values)


__all__ = [
    "DEFAULT_BENCHMARK_PATH",
    "Scenario",
    "benchmark_and_save",
    "classify_scenario",
    "choose_algorithm",
    "choose_benchmarked_algorithm",
    "choose_measured_algorithm",
    "load_benchmark_results",
    "measure_algorithms",
    "measure_data_scenarios",
    "save_benchmark_results",
    "sort",
]
