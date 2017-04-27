from number import Number
import unittest


class TestNumbers(unittest.TestCase):
    one = Number(value=1)
    negative_two = Number(value=-2)
    three = Number(value=3)
    zero = Number(value=0)
    twelve = Number(value=12)

    def test_create_number(self):
        self.assertIsInstance(TestNumbers.three, Number)
        self.assertIsInstance(Number(left=[TestNumbers.negative_two],
                                     right=[TestNumbers.one]),
                              Number)
        self.assertIsInstance(Number(value=3), Number)
        x = TestNumbers.one + TestNumbers.three
        self.assertIsInstance(x, Number)

    def test_simplest_number(self):
        self.assertEqual(Number.simplest_between(TestNumbers.one,
                                                 TestNumbers.three),
                         Number(value=2))
        self.assertEqual(Number.simplest_between(TestNumbers.negative_two,
                                                 TestNumbers.twelve),
                         Number(value=0))


if __name__ == "__main__":
    unittest.main(exit=False)