def insertion(ls: list[dict], obj: dict, key: str, ascending: bool = True):
    for i in range(len(ls)):
        if (ascending and obj.get(key) < ls[i].get(key)) or (not ascending and obj.get(key) > ls[i].get(key)):
            ls.insert(i, obj)
            return

    ls.append(obj)

def binary_insertion(arr: list[dict], obj: dict, key: str):
    l = 0
    r = len(arr) - 1

    while l < r:
        m = l + (r - l) // 2
        v = arr[m]

        if v.get(key) < obj.get(key):
            l = m + 1
        else:
            r = m - 1

    arr.insert(l, obj)
    return l