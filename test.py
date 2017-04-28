from number import Number
from surrealnumber import SurrealNumber
import unittest


class TestNumbers(unittest.TestCase):
    one = SurrealNumber.integer(1)
    negative_two = SurrealNumber.create_integer(-2)
    three = SurrealNumber.integer(3)
    zero = SurrealNumber.integer(0)
    twelve = SurrealNumber.integer(12)
    star = SurrealNumber(left=[zero], right=[0])

    def test_create_number(self):
        self.assertIsInstance(TestNumbers.three, SurrealNumber)
        self.assertIsInstance(SurrealNumber(left=[TestNumbers.negative_two],
                                            right=[TestNumbers.one]),
                              SurrealNumber)
        self.assertIsInstance(SurrealNumber(value=3), SurrealNumber)
        x = TestNumbers.one + TestNumbers.three
        self.assertIsInstance(x, SurrealNumber)

    # def test_simplest_number(self):
    #     self.assertEqual(Number.simplest_between(TestNumbers.one,
    #                                              TestNumbers.three),
    #                      Number(value=2))
    #     self.assertEqual(Number.simplest_between(TestNumbers.negative_two,
    #                                              TestNumbers.twelve),
    #                      Number(value=0))

    def test_number_identification(self):
        self.assertEqual(str(TestNumbers.star), '{ 0 |  0 }')
        self.assertEqual(str(TestNumbers.twelve), '12')
        self.assertEqual(str(TestNumbers.one + TestNumbers.twelve), '13')
        self.assertEqual(str(TestNumbers.one + TestNumbers.star), '{ 1 | 1 }')
        self.assertFalse(TestNumbers.star.is_number())
        self.assertTrue(TestNumbers.twelve.is_number())


    def test_number_summation(self):
        self.assertEqual(TestNumbers.one + TestNumbers.one,
                         SurrealNumber(value=2))
        self.assertEqual(TestNumbers.star+TestNumbers.three,
                         SurrealNumber(left=[TestNumbers.three],
                                       right=[TestNumbers.three]))
        self.assertEqual(TestNumbers.star+TestNumbers.star,TestNumbers.zero)

    def test_number_ordering(self):
        self.assertFalse(TestNumbers.three < TestNumbers.zero)
        self.assertFalse(TestNumbers.star < TestNumbers.zero)
        self.assertTrue(
            SurrealNumber(left=[TestNumbers.zero], right=[]) == TestNumbers.one)


if __name__ == "__main__":
    unittest.main(exit=False)