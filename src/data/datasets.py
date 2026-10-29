"""Geração e leitura dos datasets de benchmark."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from random import Random

from src.benchmarks.scenarios import Scenario

DEFAULT_DATA_PATH = Path(__file__).resolve().parent


def _dataset_path(scenario: Scenario, directory: str | Path) -> Path:
    return Path(directory) / f"{scenario.value}.txt"


def write_dataset(
    values: Iterable[int], scenario: Scenario, directory: str | Path = DEFAULT_DATA_PATH
) -> Path:
    destination = _dataset_path(scenario, directory)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "\n".join(str(value) for value in values) + "\n",
        encoding="utf-8",
    )
    return destination


def load_dataset(
    scenario: Scenario, directory: str | Path = DEFAULT_DATA_PATH
) -> list[int]:
    source = _dataset_path(scenario, directory)
    if not source.is_file():
        raise FileNotFoundError(
            f"Dataset não encontrado em {source}. Execute generate_datasets()."
        )

    values: list[int] = []
    for line_number, line in enumerate(
        source.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            values.append(int(line))
        except ValueError as error:
            raise ValueError(
                f"Valor inválido em {source}, linha {line_number}: {line!r}"
            ) from error
    return values


def load_datasets(
    directory: str | Path = DEFAULT_DATA_PATH,
) -> dict[Scenario, list[int]]:
    return {scenario: load_dataset(scenario, directory) for scenario in Scenario}


def generate_datasets(
    directory: str | Path = DEFAULT_DATA_PATH,
    seed: int = 42,
) -> dict[Scenario, Path]:
    random = Random(seed)
    datasets: dict[Scenario, list[int]] = {
        Scenario.RANDOM_LARGE_KEYS: [
            random.randint(-10**9, 10**9) for _ in range(2_000)
        ],
        Scenario.NARROW_RANGE: [random.randint(0, 50) for _ in range(2_000)],
        Scenario.NEARLY_SORTED: list(range(2_000)),
        Scenario.TINY_LIST: [random.randint(-10**9, 10**9) for _ in range(12)],
    }

    nearly_sorted = datasets[Scenario.NEARLY_SORTED]
    for _ in range(20):
        first = random.randrange(len(nearly_sorted) - 1)
        nearly_sorted[first], nearly_sorted[first + 1] = (
            nearly_sorted[first + 1],
            nearly_sorted[first],
        )

    return {
        scenario: write_dataset(values, scenario, directory)
        for scenario, values in datasets.items()
    }
