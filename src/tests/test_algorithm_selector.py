from src.methods.counting_sort import counting_sort
from src.methods.hibrid_sort import hybrid_sort
from src.methods.insertion_sort import insertion_sort
from src.methods.merge_sort import merge_sort
from src.methods.quick_sort import quick_sort
from src.methods.radix_sort import radix_sort
from src.selector.algorithm_selector import (
    Scenario,
    choose_algorithm,
    choose_benchmarked_algorithm,
    choose_measured_algorithm,
    classify_scenario,
    measure_algorithms,
    save_benchmark_results,
    sort,
)


def test_choose_insertion_for_small_input():
    assert choose_algorithm([3, 1, 2]) is insertion_sort


def test_choose_insertion_for_nearly_sorted_input():
    values = list(range(100))
    values[50], values[51] = values[51], values[50]
    assert choose_algorithm(values) is insertion_sort


def test_choose_counting_for_dense_integer_range():
    values = [5, 2, 4, 3, 1] * 10
    assert choose_algorithm(values) is counting_sort


def test_choose_quick_for_medium_integer_input():
    values = [index * 100 for index in range(5_000)]
    for index in range(0, len(values) - 1, 2):
        values[index], values[index + 1] = values[index + 1], values[index]
    assert choose_algorithm(values) is quick_sort


def test_choose_radix_for_sparse_integer_range():
    values = [10**9, -(10**9), 7] * 20
    assert choose_algorithm(values) is radix_sort


def test_choose_merge_for_small_non_integer_input():
    values = [chr(97 + (index * 7) % 26) for index in range(64)]
    assert choose_algorithm(values) is merge_sort


def test_choose_hybrid_for_large_non_integer_input():
    values = [str(index) for index in range(100, 0, -1)]
    assert choose_algorithm(values) is hybrid_sort


def test_sort_normalizes_in_place_and_new_list_algorithms():
    values = [4, 1, 3, 2]
    result = sort(values)
    assert result == [1, 2, 3, 4]
    assert result is values


def test_datasets_cover_four_scenarios():
    from src.data import load_datasets

    assert list(Scenario) == [
        Scenario.RANDOM_LARGE_KEYS,
        Scenario.NARROW_RANGE,
        Scenario.NEARLY_SORTED,
        Scenario.TINY_LIST,
    ]
    datasets = load_datasets()
    assert set(datasets) == set(Scenario)
    assert len(datasets[Scenario.TINY_LIST]) == 12


def test_measure_algorithms_returns_time_for_every_method():
    measurements = measure_algorithms([3, 1, 2], repetitions=1)

    assert set(measurements) == {
        "insertion_sort",
        "counting_sort",
        "radix_sort",
        "quick_sort",
        "merge_sort",
        "hybrid_sort",
    }
    assert all(time >= 0 for time in measurements.values())


def test_measure_data_scenarios_returns_the_four_required_scenarios():
    from src.selector import measure_data_scenarios

    measurements = measure_data_scenarios(repetitions=1)

    assert set(measurements) == set(Scenario)
    assert all(
        len(scenario_measurements) == 6
        for scenario_measurements in measurements.values()
    )


def test_measured_selection_returns_an_algorithm():
    assert choose_measured_algorithm([3, 1, 2], repetitions=1).__name__ in {
        "insertion_sort",
        "counting_sort",
        "radix_sort",
        "quick_sort",
        "merge_sort",
        "hybrid_sort",
    }


def test_benchmark_results_can_be_saved_and_used(tmp_path):
    path = tmp_path / "results.json"
    results = {
        scenario: {
            "insertion_sort": 10.0,
            "counting_sort": 2.0,
            "radix_sort": 3.0,
            "quick_sort": 4.0,
            "merge_sort": 5.0,
            "hybrid_sort": 6.0,
        }
        for scenario in Scenario
    }

    save_benchmark_results(results, path)

    assert classify_scenario([3, 1, 2]) is Scenario.TINY_LIST
    assert choose_benchmarked_algorithm([3, 1, 2], path).__name__ == "counting_sort"
