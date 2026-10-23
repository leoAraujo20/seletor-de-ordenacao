def _counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if len(arr) <= 1:
        return arr

    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    if positives:
        max_pos = max(positives)
        exp = 1
        while max_pos // exp > 0:
            _counting_sort_for_radix(positives, exp)
            exp *= 10

    if negatives:
        max_neg = max(negatives)
        exp = 1
        while max_neg // exp > 0:
            _counting_sort_for_radix(negatives, exp)
            exp *= 10

    result = [-x for x in reversed(negatives)] + positives
    for i in range(len(arr)):
        arr[i] = result[i]

    return arr