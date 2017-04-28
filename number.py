import surrealnumber
from fractions import Fraction


class Number(surrealnumber.SurrealNumber):
    '''A class that represents a standard number within the surreal numbers.
    Right now we will focus on numbers that were born on a finite day.

    Attributes:
        left: (list) a list of the surreal numbers that are possible moves for
                    left.
        right: (list) a list fo the surreal numbers that are a possible move for
                right.

    Start with support for numbers, nimbers, and switches.
    '''

    def __init__(self, **kwargs):
        if 'value' in kwargs.keys():
            n = kwargs['value']
            if n == int(n):
                if n == 0:
                    kwargs['left'] = []
                    kwargs['right'] = []
                if n > 0:
                    kwargs['left'] = [Number(value=n - 1)]
                    kwargs['right'] = []
                if n < 0:
                    kwargs['left'] = []
                    kwargs['right'] = [Number(value=n + 1)]
            else:
                raise ValueError('no non-integers yet.')
        super().__init__(**kwargs)

    def __add__(self, other):
        if isinstance(other, Number):
            new_value = self.value + other.value
            return Number(value=new_value)

    def __repr__(self):
        try:
            return str(self.value)
        except AttributeError:
            return str(super().__repr__())


    def __le__(self, other):
        if isinstance(other, Number):
            return self.value < other.value
        else:
            return super().__le__(other)

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value > other.value
        else:
            return super().__ge__(other)

    def __eq__(self, other):
        if isinstance(other, Number):
            try:
                return self.value == other.value
            except AttributeError:
                return self.find_value() == other.find_value()
            finally:
                raise SyntaxError ("something went wrong in finding the value of these numbers")
        else:
            return super().__eq__(other)

    @classmethod
    def create_number(cls, left, right):
        pass

    def find_value(self):
        self.simplify()
        if len(self.left) == 0 and len(self.right) == 0:
            return 0
        elif len(self.left) == 1 and len(self.right) == 0:
            try:
                n = self.left[0].find_value
            except Exception as e:
                print(e)
                return None
            if n >= 0:
                return int(n) + 1
            if n < 0:
                return 0
        if len(self.right) == 1 and len(self.left) == 0:
            try:
                n = self.right[0].find_value
            except Exception as e:
                print(e)
                return None
            if n <= 0:
                return int(n) - 1
            if n > 0:
                return 0
        if len(self.right) == 1 and len(self.left) == 1:
            try:
                r = self.right[0].find_value
                l = self.left[0].find_value
            except Exception as e:
                print(e)
                return None

            if l < r:
                if r > 0 and l < 0:
                    return 0
                if r < 0 and l < 0:
                    sign = -1
                    r = -1 * l
                    r = -1 * r
                else:
                    sign = 1
                if (r - l) > 1:
                    return int(l) + 1
                else:
                    current = 1
                    denom = 2 ** (current)
                    step = Fraction(1, denom)
                    #guess =int(left)+power
                    guess = int(l) + step
                    while (l >= guess):
                        #print guess
                        if int(guess + step) >= int(r):
                            current += 1
                            denom = 2 ** (current)
                            step = Fraction(1, denom)
                            guess = int(l) + step
                        else:
                            guess = guess + step
                    return sign * guess


    @classmethod
    def create_integer(cls, n):
        if not isinstance(n, int):
            raise TypeError("Function requires an integer")
        if n == 0:
            return cls(left=[], right=[], value=0)
        elif n > 0:
            return cls(left=[cls.create_integer(n - 1)], right=[], value=n)
        else:
            return cls(left=[], right=[cls.create_integer(n + 1)], value=n)

    @staticmethod
    def simplest_between(left, right):
        """Calculates the simplest number between two given numbers.

        Args:
            left (int): an integer that is smaller than right, Can also be
                None.
            right(int): an integer that is larger than left. Can also be
                None.

        """
        if not isinstance(left, Number) or not isinstance(right, Number):
            raise ValueError('One of these is not a Number')
        left = left.value
        right = right.value
        if left > right:
            raise ValueError('Only appropriate for Numbers')
        #print str(left) + ' ' +str(right)
        if left is None:
            if right is None:
                return Number(value=0)
            if right <= 0:
                return Number(value=int(right) - 1)
            else:
                return Number(value=0)
        if right is None:
            if left >= 0:
                return Number(value=int(left) + 1)
            else:
                return Number(value=0)
        if left < Number(value=0) and right > Number(value=0):
            return Number(value=0)

        if right < Number(value=0):
            right, left = -1 * left, -1 * right
            sign = -1
        else:
            sign = 1
        if int(right) - int(left) > 1:
            return Number(value=sign * (int(left) + 1))
        else:
            raise ValueError("Haven't implemented fractions")
            # current=1
            # power=2**(-current)
            # guess =int(left)+power
            # while (left>=guess) or (right<=guess):
            #     #print guess
            #     if int(guess+power)>=int(right):
            #         current+=1
            #         power=2**(-current)
            #         guess = int(left)+power
            #     else:
            #         guess = guess+power
            # return sign * guess


    def __int__(self):
        return Number(value=int(self.value))


def main():
    zero = Number(left=[], right=[])
    print(zero.find_value())
    #one = SurrealNumber(left=[zero], right=[])
    #neg_one = SurrealNumber(left=[], right=[zero])
    #star = SurrealNumber(left=[zero], right=[zero])

    print(str(zero))
    #print(str(one))
    #print(str(one + one))


if __name__ == '__main__':
    main()
