"""Análise genérica das entradas de ordenação."""

from collections.abc import Sequence
from typing import Any


def is_integer_input(values: Sequence[Any]) -> bool:
    return all(
        isinstance(value, int) and not isinstance(value, bool) for value in values
    )


def is_nearly_sorted(values: Sequence[Any]) -> bool:
    if len(values) < 2:
        return True

    inversions = sum(
        values[index] > values[index + 1] for index in range(len(values) - 1)
    )
    return inversions <= max(1, len(values) // 20)


def value_range(values: Sequence[int]) -> int:
    if not values:
        return 0
    return max(values) - min(values) + 1
