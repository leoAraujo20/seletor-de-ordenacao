"""Gera os datasets usados pelos benchmarks."""

from src.data.datasets import generate_datasets


if __name__ == "__main__":
    for scenario, path in generate_datasets().items():
        print(f"{scenario.value}: {path}")
