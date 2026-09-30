"""Повышенное задание №10: собственная реализация reduce.

Поведение совпадает с functools.reduce:
    my_reduce(f, [a, b, c])       == f(f(a, b), c)
    my_reduce(f, [a, b, c], init) == f(f(f(init, a), b), c)
Для пустой последовательности без начального значения — TypeError.
"""

_NO_INITIAL = object()  # маркер «начальное значение не передано»


def my_reduce(function, iterable, initial=_NO_INITIAL):
    iterator = iter(iterable)

    if initial is _NO_INITIAL:
        try:
            accumulator = next(iterator)
        except StopIteration:
            raise TypeError(
                "my_reduce() of empty iterable with no initial value"
            ) from None
    else:
        accumulator = initial

    for element in iterator:
        accumulator = function(accumulator, element)
    return accumulator


def my_reduce_recursive(function, items, initial):
    """Рекурсивный вариант (для списков): свёртка слева направо."""
    if not items:
        return initial
    return my_reduce_recursive(function, items[1:],
                               function(initial, items[0]))
