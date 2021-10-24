
import unittest


def throttle(f, n):
    """
    Throttle a function ``f`` such that it is only executed every ``n`` calls.
    The returned function will execute on its first call. If passed ``n <= 0``,
    the returned function will be always execute.
    """
    i = n

    def throttled(*args, **kwargs):
        nonlocal i
        i += 1
        if i >= n:
            i = 0
            return f(*args, **kwargs)

    return throttled


class TestFunctional(unittest.TestCase):
    def test_throttle(self):
        def f(x): return 2 * x
        throttled = throttle(f, 4)

        for _ in range(30):
            self.assertEqual(f(3), throttled(3))
            self.assertIsNone(throttled(3))
            self.assertIsNone(throttled(3))
            self.assertIsNone(throttled(3))
