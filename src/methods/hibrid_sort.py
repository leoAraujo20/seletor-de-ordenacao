import random


def _insertion_sort_slice(arr, low, high):
    """Ordenação por inserção para subvetores pequenos."""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _hybrid_sort_helper(arr, low, high, threshold=16):
    while low < high:
        # Quando a partição fica pequena, usa inserção
        if high - low + 1 <= threshold:
            _insertion_sort_slice(arr, low, high)
            break
        else:
            # Pivô aleatório + partição
            pivot_idx = random.randint(low, high)
            arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
            pivot = arr[high]

            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            p = i + 1

            # Chamada recursiva na menor metade para otimizar pilha
            if p - low < high - p:
                _hybrid_sort_helper(arr, low, p - 1, threshold)
                low = p + 1
            else:
                _hybrid_sort_helper(arr, p + 1, high, threshold)
                high = p - 1


def hybrid_sort(arr):
    if len(arr) <= 1:
        return arr
    _hybrid_sort_helper(arr, 0, len(arr) - 1)
    return arr
