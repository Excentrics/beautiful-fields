# -*- coding: utf-8 -*-


def space125(value):
    s125 = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1e3, 2e3, 5e3,
            1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7, 5e7, 1e8, 2e8, 5e8, 1e9, 2e9, 5e9]
    result = value
    fv = round(value, 3)
    for v in s125:
        result = v
        if result >= fv:
            break
    return result


def beautifulRound(value):
    value = round(value, 3)
    if value:
        s125 = space125(value)
        rate = round(value / s125, 1)
        return rate * s125
    else:
        return 0


def beautifulCeil(value):
    value = round(value, 3)
    if value:
        s125 = space125(value)
        rate = round(value / s125, 1)
        result = rate * s125
        if result < value:
            result += s125 * 0.1
        return result
    else:
        return 0


def beautifulFloor(value):
    value = round(value, 3)
    if value:
        s125 = space125(value)
        rate = round(value / s125, 1)
        result = rate * s125
        if result > value:
            result -= s125 * 0.1
        return result
    else:
        return 0