"""Cenários de entrada usados nos benchmarks."""

from collections.abc import Sequence
from enum import Enum
from typing import Any

from src.utils.input_analysis import is_integer_input, is_nearly_sorted, value_range

_TINY_LIST_LIMIT = 32


class Scenario(str, Enum):
    RANDOM_LARGE_KEYS = "aleatorio_chaves_grandes"
    NARROW_RANGE = "faixa_estreita"
    NEARLY_SORTED = "quase_ordenado"
    TINY_LIST = "lista_minuscula"


def classify_scenario(values: Sequence[Any]) -> Scenario:
    if not is_integer_input(values):
        raise ValueError("Os benchmarks salvos suportam apenas entradas inteiras")
    if len(values) <= _TINY_LIST_LIMIT:
        return Scenario.TINY_LIST
    if is_nearly_sorted(values):
        return Scenario.NEARLY_SORTED
    if value_range(values) <= max(64, len(values) // 2):
        return Scenario.NARROW_RANGE
    return Scenario.RANDOM_LARGE_KEYS
