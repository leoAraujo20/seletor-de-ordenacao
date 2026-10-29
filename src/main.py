"""Ponto de entrada para executar e validar o projeto."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.benchmarks.scenarios import Scenario, classify_scenario
from src.data.datasets import DEFAULT_DATA_PATH, generate_datasets, load_datasets
from src.selector import (
    benchmark_and_save,
    choose_benchmarked_algorithm,
    load_benchmark_results,
    sort,
)


def _format_time(time_in_ms: float) -> str:
    return "não aplicável" if time_in_ms == float("inf") else f"{time_in_ms:.3f} ms"


def print_results(results: dict[Scenario, dict[str, float]]) -> None:
    print("\nResultados dos benchmarks")
    print("=" * 72)

    for scenario, measurements in results.items():
        winner = min(measurements, key=measurements.__getitem__)
        print(f"\nCenário: {scenario.value}")
        print(f"Vencedor: {winner} ({_format_time(measurements[winner])})")
        for algorithm, time_in_ms in sorted(
            measurements.items(), key=lambda item: item[1]
        ):
            print(f"  - {algorithm:<16} {_format_time(time_in_ms)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gera datasets, executa benchmarks e valida o seletor."
    )
    parser.add_argument(
        "-r",
        "--repetitions",
        type=int,
        default=5,
        help="quantidade de medições por algoritmo (padrão: 5)",
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="usa os datasets existentes sem gerá-los novamente",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.repetitions < 1:
        raise SystemExit("--repetitions deve ser maior ou igual a 1")

    print("Seletor de ordenação")
    print("-" * 72)

    if not args.skip_generation:
        generated = generate_datasets()
        print(f"Datasets gerados: {len(generated)} arquivos")
    else:
        print(f"Datasets existentes: {Path(DEFAULT_DATA_PATH)}")

    destination = benchmark_and_save(repetitions=args.repetitions)
    print(f"Benchmarks salvos em: {destination}")

    results = load_benchmark_results(destination)
    print_results(results)

    sample = [9, 2, 7, 1, 5]
    original_sample = sample.copy()
    scenario = classify_scenario(sample)
    saved_measurements = results[scenario]
    selected_algorithm = choose_benchmarked_algorithm(
        sample,
        path=destination,
    )
    selected_name = selected_algorithm.__name__
    best_time = min(saved_measurements.values())
    selected_time = saved_measurements[selected_name]
    if selected_time != best_time:
        raise RuntimeError(
            f"O seletor escolheu {selected_name}, mas o menor tempo salvo é "
            f"{best_time:.3f} ms"
        )
    sorted_sample = sort(sample, use_saved_benchmark=True)
    print("\nValidação do seletor")
    print(f"Entrada: {original_sample}")
    print(f"Cenário identificado: {scenario.value}")
    print(f"Arquivo consultado: {destination}")
    print(f"Algoritmo selecionado: {selected_name}")
    print(f"Tempo salvo do selecionado: {_format_time(selected_time)}")
    print(f"Menor tempo salvo no cenário: {_format_time(best_time)}")
    print(f"Seleção confirmada: {'SIM' if selected_time == best_time else 'NÃO'}")
    print(f"Saída:   {sorted_sample}")
    print(f"Datasets carregados: {len(load_datasets())}")
    print("\nExecução concluída com sucesso.")


if __name__ == "__main__":
    main()
