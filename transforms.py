"""Средние задания №10 и №2: map с несколькими функциями и filter чётных."""


def is_even(number):
    return number % 2 == 0


def filter_even(numbers):
    """Задание №2: оставить только чётные числа (через filter)."""
    return list(filter(is_even, numbers))
