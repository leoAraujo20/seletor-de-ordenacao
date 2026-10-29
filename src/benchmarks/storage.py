"""Persistência dos resultados dos benchmarks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.benchmarks.scenarios import Scenario

Measurement = dict[str, float]
BenchmarkResults = dict[Scenario, Measurement]
_ALGORITHM_NAMES = {
    "insertion_sort",
    "counting_sort",
    "radix_sort",
    "quick_sort",
    "merge_sort",
    "hybrid_sort",
}


def save_benchmark_results(results: BenchmarkResults, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "scenarios": {
            scenario.value: measurements for scenario, measurements in results.items()
        },
    }
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def load_benchmark_results(path: str | Path) -> BenchmarkResults:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(
            f"Benchmark não encontrado em {source}. Execute benchmark_and_save()."
        )

    payload: dict[str, Any] = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("version") != 1 or set(payload.get("scenarios", {})) != {
        scenario.value for scenario in Scenario
    }:
        raise ValueError(f"Formato de benchmark inválido: {source}")

    results: BenchmarkResults = {}
    for name, measurements in payload["scenarios"].items():
        if set(measurements) != _ALGORITHM_NAMES:
            raise ValueError(f"Algoritmos ausentes no benchmark: {source}")
        results[Scenario(name)] = {
            algorithm: float(time) for algorithm, time in measurements.items()
        }
    return results
