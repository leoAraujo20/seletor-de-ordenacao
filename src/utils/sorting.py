"""Operações comuns aos algoritmos de ordenação."""

from collections.abc import Callable, Sequence
from typing import Any

SortFunction = Callable[[list[Any]], list[Any] | None]


def apply_sort(algorithm: SortFunction, values: list[Any]) -> list[Any]:
    result = algorithm(values)
    return values if result is None else result


def ensure_sorted(
    algorithm_name: str,
    result: Sequence[Any],
    expected: Sequence[Any],
) -> None:
    if result != expected:
        raise RuntimeError(f"{algorithm_name} não ordenou a entrada corretamente")
