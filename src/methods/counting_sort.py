def counting_sort(arr):
    if len(arr) <= 1:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    val_range = max_val - min_val + 1

    count = [0] * val_range
    for num in arr:
        count[num - min_val] += 1

    idx = 0
    for i in range(val_range):
        while count[i] > 0:
            arr[idx] = i + min_val
            idx += 1
            count[i] -= 1

    return arr