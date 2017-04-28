import operator
import functools
import itertools
from fractions import Fraction
from math import log


class SurrealNumber(object):
    '''A class that represents a surreal number. Right now we will focus on
    surreal numbers that were born on a finite day.

    Attributes:
        left: (list) a list of the surreal numbers that are possible moves for
                    left.
        right: (list) a list fo the surreal numbers that are a possible move for
                right.

        value: is an attribute which is computed from the left and right lists.

    Start with support for numbers, nimbers, and switches.
    '''

    def __init__(self, **kwargs):
        try:
            setattr(self, '_value', kwargs.pop('value'))
        except:
            pass
        try:
            setattr(self, '_left', kwargs.pop('left'))
        except:
            pass
        try:
            setattr(self, '_right', kwargs.pop('right'))
        except:
            pass
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def value(self):
        #self.simplify()
        if len(self.left) == 0 and len(self.right) == 0:
            return 0
        elif len(self.left) == 1 and len(self.right) == 0:
            try:
                n = self.left[0].value
            except Exception as e:
                print(e)
                return None
            if n >= 0:
                return int(n) + 1
            if n < 0:
                return 0
        if len(self.right) == 1 and len(self.left) == 0:
            try:
                n = self.right[0].value
            except Exception as e:
                print(e)
                return None
            if n <= 0:
                return int(n) - 1
            if n > 0:
                return 0
        if len(self.right) == 1 and len(self.left) == 1:
            try:
                r = self.right[0].value
                l = self.left[0].value
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

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def options(self):
        return (self.left, self.right)

    def __add__(self, other):
        if isinstance(other, SurrealNumber):
            my_left = self.left
            other_left = other.left
            new_left = [self + n for n in other_left] + [other + n for n in
                                                       my_left]
            #print(new_left)
            my_right = self.right
            other_right = other.right
            new_right = [self + n for n in other_right] + [other + n for n in
                                                         my_right]
            #print(new_right)
            n=SurrealNumber(left=new_left, right=new_right)
            n.simplify()
            return n
        else:
            raise TypeError(
                'Must add surreal numbers to other surreal numbers.')

    def __mul__(self, other):
        if isinstance(other, SurrealNumber):
            my_left = self.left
            other_left = other.left
            my_right = self.right
            other_right = other.right
            new_left = [n[0]*other + self*n[1] - n[0]*n[1] for n in itertools.product(my_left, other_left)] +\
                        [n[0]*other + self*n[1] - n[0]*n[1] for n in itertools.product(my_right, other_right)]

            new_right = [n[0]*other + self*n[1] - n[0]*n[1] for n in itertools.product(my_left, other_right)]+\
                        [n[0]*other + self*n[1] - n[0]*n[1] for n in itertools.product(my_left, other_left)]
            return SurrealNumber(left=new_left, right=new_right)
        else:
            raise TypeError(
                'Must multiply surreal numbers to other surreal numbers.')

    def simplify(self):
        for n in self.left:
            n=n.simplify()
        for n in self.right:
            n=n.simplify()
        self.remove_dominated_options()


    def remove_dominated_options(self):
        x=[[n<=m for m in self.right] for n in self.right]
        y=[functools.reduce(operator.mul, y, 1) for y in x]
        right=list(itertools.compress(self.right,y))
        new_right=[]
        for n in right:
            if not n in new_right:
                new_right.append(n)
        self._right=new_right
        x=[[n>=m for m in self.left] for n in self.left]
        y=[functools.reduce(operator.mul, y, 1) for y in x]
        left=list(itertools.compress(self.left,y))
        new_left=[]
        for n in left:
            if not n in new_left:
                new_left.append(n)
        self._left=new_left

    def is_number(self):
        test=itertools.product(self.right,self.left)
        return bool(functools.reduce(operator.mul, [i[0]<i[1] for i in test], 1))

    def __repr__(self):
        if self.is_number():
            try:
                return str(self.value)
            except:
                pass
        ans = '{'
        for i in self.left:
            ans += ' ' + str(i) + ','
        if len(self.left) > 0:
            ans = ans[:-1]
        ans += ' | '
        for i in self.right:
            ans += ' ' + str(i) + ','
        if len(self.right) > 0:
            ans = ans[:-1]
        return ans + ' }'

    def __str__(self):
        if self.is_number():
            try:
                return str(self.value)
            except:
                pass
        return self.__repr__()

    def __lt__(self, other):
        return not other.__ge__(self)

    def __gt__(self, other):
        return not other.__le__(self)

    def __le__(self, other):
        for n in self.left:
            if  other<=n:
                return False
        for n in other.right:
            if  n<=self:
                return False
        return True

    def __ge__(self, other):
        for n in self.right:
            if n<=other:
                return False
        for n in other.left:
            if self<=n:
                return False
        return True

    def __eq__(self, other):
        self.simplify()
        other.simplify()
        return (self.left==other.left) and (self.right==other.right)

    def __neg__(self):
        new_left=[-n for n in self.right]
        new_right=[-n for n in self.left]
        return SurrealNumber(left=new_left, right=new_right)

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

    @classmethod
    def create_fraction(cls, f):
        if not isinstance(f, Fraction):
            raise TypeError("Function requires an fraction")
        denominator = f.denominator
        power = int(log(denominator, 2))
        if 2 ** power != denominator:
            raise TypeError(
                "Function requires a dydatic fraction (power of 2 denominator)")
        leftvalue = Fraction(f.numerator - 1, f.denominator)
        if leftvalue.denominator == 1:
            leftvalue = int(leftvalue)
        rightvalue = Fraction(f.numerator - 1, f.denominator)
        if rightvalue.denominator == 1:
            rightvalue = int(rightvalue)
            leftnum = cls.simplified_form(leftvalue)
            rightnum = cls.simplified_form(rightvalue)
        return cls(left=[leftnum], right=[rightnum])



def main():
    zero2 = SurrealNumber(value=0)
    zero = SurrealNumber(left=[], right=[])
    print(zero.is_number())
    print(zero.value)
    #zero.simplify()
    one = SurrealNumber(left=[zero], right=[])
    neg_one = SurrealNumber(left=[], right=[zero])
    star = SurrealNumber(left=[zero], right=[zero])
    switch=SurrealNumber(left=[one], right=[neg_one])

    print("zero = "+str(zero))
    print("one = "+ str(one))
    print(one.left[0]==zero)
    print(zero>=one)
    print(star)
    print(star.is_number())
    print(neg_one)
    print(switch)
    two = one + one
    two.simplify()
    print (two.left)
    print (two+two+two)
    print("one plus one")
    print(str(one + one))
    print(two + star+switch)
    print(star + star)




if __name__ == '__main__':
    main()
