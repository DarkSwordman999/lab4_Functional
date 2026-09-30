"""Средние задания №10 и №2: map с несколькими функциями и filter чётных."""


def is_even(number):
    return number % 2 == 0


def filter_even(numbers):
    """Задание №2: оставить только чётные числа (через filter)."""
    return list(filter(is_even, numbers))


def apply_each(functions, values):
    """Задание №10: применить каждую функцию к списку через map.

    Возвращает словарь {имя функции: список результатов}.
    Пример: apply_each([abs, str], [-1, 2]) -> {'abs': [1, 2],
    'str': ['-1', '2']}.
    """
    return {func.__name__: list(map(func, values)) for func in functions}
