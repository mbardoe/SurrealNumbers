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
        # try:
        #     setattr(self, '_value', kwargs.pop('value'))
        # except:
        #     pass
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
        if not self.is_number():
            raise TypeError("Only numbers have a value")
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
    def nim_value(self):
        if not self.is_nimber():
            raise TypeError("Only nimbers have a nim_value")
        n=0
        while (SurrealNumber.nimber(n) in self.right):
            n+=1
            #print(n)
        return n

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
            if self.is_nimber() and other.is_nimber():
                return SurrealNumber.nimber(self.nim_value^other.nim_value)
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
            n = SurrealNumber(left=new_left, right=new_right)
            #n.simplify()
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
            new_left = [n[0] * other + self * n[1] - n[0] * n[1] for n in
                        itertools.product(my_left, other_left)] + \
                       [n[0] * other + self * n[1] - n[0] * n[1] for n in
                        itertools.product(my_right, other_right)]

            new_right = [n[0] * other + self * n[1] - n[0] * n[1] for n in
                         itertools.product(my_left, other_right)] + \
                        [n[0] * other + self * n[1] - n[0] * n[1] for n in
                         itertools.product(my_left, other_left)]
            n = SurrealNumber(left=new_left, right=new_right)
            n.simplify()
            return n
        else:
            raise TypeError(
                'Must multiply surreal numbers to other surreal numbers.')

    def simplify(self):
        for n in self.left:
            n = n.simplify()
        for n in self.right:
            n = n.simplify()
        oldright=list(self.right)
        oldleft=list(self.left)
        self.remove_dominated_options()
        self.remove_reversible_options()
        while((not oldleft==self.left) and (not oldright==self.right)):
            self.remove_dominated_options()
            self.remove_reversible_options()
            oldright=list(self.right)
            oldleft=list(self.left)


    def remove_dominated_options(self):
        x=self.dominated_right_option()
        while x:
            self._right=[n for n in self.right if n!=x]
            x=self.dominated_right_option()
        x=self.dominated_left_option()
        while x:
            self._right=[n for n in self.left if n!=x]
            x=self.dominated_left_option()

    def dominated_right_option(self):
        testlist=itertools.combinations(self.right,2)
        for a,b in testlist:
            if a<=b:
                return b
        return None

    def dominated_left_option(self):
        testlist=itertools.combinations(self.right,2)
        for a,b in testlist:
            if a<=b:
                return a
        return None

    def remove_reversible_options(self):
        left_remove = []
        left_new = []
        right_remove = []
        right_new = []
        for n in self.right:
            for j in n.left:
                if j >= self:
                    #j is a reversible right option.
                    #print("found one")
                    right_remove.append(n)
                    right_new += j.right
        for n in self.left:
            for j in n.right:
                if j <= self:
                    #j is a reversible left option
                    #print("found one")
                    left_remove.append(n)
                    left_new += j.left
        self._right = [n for n in self.right if
                       n not in right_remove]
        for n in right_new:
            if n not in self.right:
                self._right.append(n)

        self._left = [n for n in self.left if n not in left_remove]
        for n in left_new:
            if n not in self.left:
                self._left.append(n)


    def is_number(self):
        test = itertools.product(self.right, self.left)
        for a,b in test:
            if not a<b:
                return False
        return True

    def is_nimber(self):
        if self.right != self.left:
            return False
        for n in self.right:
            if not n.is_nimber():
                return False
        return True

    def __repr__(self):
        if self.is_nimber():
            try:
                return str('*'+str(self.nim_value))
            except:
                pass
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
        ans += ' |'
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
        if self.is_nimber():
            try:
                return str('*'+str(self.nim_value))
            except:
                pass
        return self.__repr__()

    def __lt__(self, other):
        return not other.__ge__(self)

    def __gt__(self, other):
        return not other.__le__(self)

    def __le__(self, other):
        for n in self.left:
            if other <= n:
                return False
        for n in other.right:
            if n <= self:
                return False
        return True

    def __ge__(self, other):
        for n in self.right:
            if n <= other:
                return False
        for n in other.left:
            if self <= n:
                return False
        return True

    def __eq__(self, other):
        self.simplify()
        other.simplify()
        return (self.left == other.left) and (self.right == other.right)

    def __neg__(self):
        new_left = [-n for n in self.right]
        new_right = [-n for n in self.left]
        return SurrealNumber(left=new_left, right=new_right)

    @classmethod
    def integer(cls, n):
        if not isinstance(n, int):
            raise TypeError("Function requires an integer")
        if n == 0:
            return cls(left=[], right=[])
        elif n > 0:
            return cls(left=[cls.integer(n - 1)], right=[])
        else:
            return cls(left=[], right=[cls.integer(n + 1)])

    @classmethod
    def nimber(cls, n):
        if not isinstance(n, int):
            raise TypeError("Function requires an integer")
        options = []
        for i in range(n):
            options.append(SurrealNumber.nimber(i))
        return cls(left=options, right=options)

    @classmethod
    def ups(cls, n):
        if not isinstance(n, int):
            raise TypeError("Function requires an integer")
        zero=cls.integer(0)
        ans=cls.integer(0)
        up=cls(left=[zero], right=[cls.nimber(1)])
        for i in range(n):
            ans=ans+up
        ans.simplify()
        return ans

    @classmethod
    def fraction(cls, f):
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
    switch = SurrealNumber(left=[one], right=[neg_one])

    print("zero = " + str(zero))
    print("one = " + str(one))
    print(one.left[0] == zero)
    print(zero >= one)
    print(star)
    print(star.is_number())
    print(neg_one)
    print(switch)
    two = one + one
    two.simplify()
    print(two.left)
    print(two + two + two)
    print("one plus one")
    print(str(one + one))
    print(two + star + switch)
    print(star + star)


if __name__ == '__main__':
    main()
