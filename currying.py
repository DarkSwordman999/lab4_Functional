"""Повышенное задание №3: функция-карринг.

curry(f) превращает функцию f(a, b, c) в цепочку функций одного
(или нескольких) аргументов: curry(f)(a)(b)(c) == f(a, b, c).
Аргументы можно передавать и группами: curry(f)(a, b)(c).
"""

import functools
import inspect


def curry(func, arity=None):
    if arity is None:
        params = inspect.signature(func).parameters.values()
        arity = sum(
            1 for p in params
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
            and p.default is p.empty
        )

    def collect(*collected):
        if len(collected) >= arity:
            return func(*collected)

        def next_step(*more):
            if not more:
                raise TypeError("Каррированной функции нужен аргумент")
            return collect(*collected, *more)

        return next_step

    return functools.wraps(func)(lambda *args: collect(*args))


def add3(a, b, c):
    return a + b + c


def power(base, exponent):
    return base ** exponent
