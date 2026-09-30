import functools
import io
import operator
import unittest
from contextlib import redirect_stdout

from currying import add3, curry, power
from my_reduce import my_reduce, my_reduce_recursive
from timing import timed
from transforms import (apply_chain, apply_each, filter_even, is_even,
                        map_pairwise)


class TransformsTest(unittest.TestCase):
    def test_filter_even(self):
        self.assertEqual(filter_even([1, 2, 3, 4, 5, 6]), [2, 4, 6])
        self.assertEqual(filter_even([-4, -3, 0]), [-4, 0])
        self.assertEqual(filter_even([]), [])

    def test_is_even(self):
        self.assertTrue(is_even(0))
        self.assertFalse(is_even(7))

    def test_apply_each(self):
        result = apply_each([abs, str], [-1, 2])
        self.assertEqual(result, {"abs": [1, 2], "str": ["-1", "2"]})

    def test_apply_each_with_lambdas(self):
        def square(x):
            return x * x

        result = apply_each([square, float], [1, 2, 3])
        self.assertEqual(result["square"], [1, 4, 9])
        self.assertEqual(result["float"], [1.0, 2.0, 3.0])

    def test_apply_chain(self):
        result = apply_chain([lambda x: x + 1, lambda x: x * 10], [1, 2])
        self.assertEqual(result, [20, 30])

    def test_map_pairwise(self):
        self.assertEqual(map_pairwise(operator.mul, [1, 2, 3], [4, 5, 6]),
                         [4, 10, 18])


class TimedTest(unittest.TestCase):
    def test_result_and_time(self):
        @timed
        def work(n):
            return sum(range(n))

        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(work(1000), 499500)
        self.assertGreaterEqual(work.last_time, 0)
        self.assertIn("work выполнена за", output.getvalue())

    def test_metadata_kept(self):
        @timed
        def documented():
            """Документация."""

        self.assertEqual(documented.__name__, "documented")
        self.assertEqual(documented.__doc__, "Документация.")

    def test_time_measured_on_exception(self):
        @timed
        def broken():
            raise RuntimeError("ошибка")

        with redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError):
                broken()
        self.assertIsNotNone(broken.last_time)


class MyReduceTest(unittest.TestCase):
    cases = [
        (operator.add, [1, 2, 3, 4]),
        (operator.mul, [1, 2, 3, 4, 5]),
        (lambda a, b: a if a > b else b, [3, 9, 2]),
        (lambda acc, s: acc + s.upper(), ["a", "b", "c"]),
    ]

    def test_same_as_functools(self):
        for func, data in self.cases:
            with self.subTest(data=data):
                self.assertEqual(my_reduce(func, data),
                                 functools.reduce(func, data))

    def test_with_initial(self):
        self.assertEqual(my_reduce(operator.add, [1, 2, 3], 10), 16)
        self.assertEqual(my_reduce(operator.add, [], 10), 10)
        self.assertIsNone(my_reduce(operator.add, [], None))

    def test_empty_without_initial(self):
        with self.assertRaises(TypeError):
            my_reduce(operator.add, [])

    def test_works_with_generators(self):
        self.assertEqual(my_reduce(operator.add, (x for x in range(5))), 10)

    def test_order_is_left_to_right(self):
        self.assertEqual(my_reduce(operator.sub, [10, 1, 2]), 7)

    def test_recursive(self):
        self.assertEqual(my_reduce_recursive(operator.add, [1, 2, 3], 0), 6)


class CurryTest(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(curry(add3)(1)(2)(3), 6)

    def test_groups(self):
        self.assertEqual(curry(add3)(1, 2)(3), 6)
        self.assertEqual(curry(add3)(1)(2, 3), 6)
        self.assertEqual(curry(add3)(1, 2, 3), 6)

    def test_partial_reuse(self):
        square = curry(power)  # power(base, exponent)
        two_to = square(2)
        self.assertEqual(two_to(3), 8)
        self.assertEqual(two_to(10), 1024)

    def test_default_arguments_not_required(self):
        def greet(name, greeting="Привет"):
            return f"{greeting}, {name}!"

        self.assertEqual(curry(greet)("Мир"), "Привет, Мир!")

    def test_explicit_arity_for_varargs(self):
        total = curry(lambda *xs: sum(xs), arity=3)
        self.assertEqual(total(1)(2)(3), 6)

    def test_empty_call(self):
        with self.assertRaises(TypeError):
            curry(add3)(1)()


if __name__ == "__main__":
    unittest.main()
