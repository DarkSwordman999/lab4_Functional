"""Лабораторная работа №4, вариант 10: демонстрация заданий."""

import math
import operator

from currying import add3, curry
from my_reduce import my_reduce
from timing import timed
from transforms import apply_chain, apply_each, filter_even


@timed
def sum_of_squares(n):
    return my_reduce(operator.add, map(lambda x: x * x, range(n)), 0)


def main():
    numbers = list(range(-3, 8))
    print("Исходный список:", numbers)

    print("\n[№2] Чётные числа (filter):", filter_even(numbers))

    print("\n[№10] Несколько функций через map:")
    table = apply_each([abs, float, bin], numbers[:5])
    for name, values in table.items():
        print(f"  {name:>6}: {values}")
    print("  цепочка abs -> sqrt -> round:",
          apply_chain([abs, math.sqrt, lambda x: round(x, 2)], numbers[:5]))

    print("\n[№8] Декоратор замера времени:")
    result = sum_of_squares(200_000)
    print(f"  результат {result}, last_time = {sum_of_squares.last_time:.4f}")

    print("\n[Повыш. №10] Собственный reduce:")
    print("  сумма:", my_reduce(operator.add, numbers))
    print("  произведение 1..6:", my_reduce(operator.mul, range(1, 7)))
    print("  максимум:", my_reduce(lambda a, b: a if a > b else b, numbers))

    print("\n[Повыш. №3] Карринг:")
    curried = curry(add3)
    add_10 = curried(10)
    print("  curry(add3)(1)(2)(3) =", curried(1)(2)(3))
    print("  add_10 = curry(add3)(10); add_10(5)(1) =", add_10(5)(1))
    print("  map с каррированной функцией:",
          list(map(add_10(0), [1, 2, 3])))


if __name__ == "__main__":
    main()
