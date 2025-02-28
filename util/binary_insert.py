def binary_insertion(arr: list[dict], obj: dict, key: str):
    l = 0
    r = len(arr) - 1

    while l < r:
        m = (l + (r - l)) // 2
        v = arr[m]

        if obj.get(key) > arr[m].get(key):
            l = m + 1
        else:
            r = m

    arr.insert(l, obj)
