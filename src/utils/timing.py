"""Medição de tempo de funções."""

from collections.abc import Callable
from time import perf_counter_ns
from typing import Any


def measure_milliseconds(
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, float]:
    started_at = perf_counter_ns()
    result = function(*args, **kwargs)
    elapsed = (perf_counter_ns() - started_at) / 1_000_000
    return result, elapsed
