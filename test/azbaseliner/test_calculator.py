import unittest
import logging
from azbaseliner.calculator import Calculator


class TestCalculator(unittest.TestCase):

    def test_integer_addition(self) -> None:
        c: Calculator = Calculator()
        a: int = 21
        b: int = 21
        r: int = c.add(a, b)
        logging.info("testing integer calculator")
        self.assertEqual(42, r, "integer addition result is correct")
