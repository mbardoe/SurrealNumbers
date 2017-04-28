import operator
import functools
import itertools


class SurrealNumber(object):
    '''A class that represents a surreal number. Right now we will focus on
    surreal numbers that were born on a finite day.

    Attributes:
        left: (list) a list of the surreal numbers that are possible moves for
                    left.
        right: (list) a list fo the surreal numbers that are a possible move for
                right.

    Start with support for numbers, nimbers, and switches.
    '''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __add__(self, other):
        if isinstance(other, SurrealNumber):
            my_left = self.left
            other_left = other.left
            new_left = [self + n for n in other_left] + [other + n for n in
                                                       my_left]
            my_right = self.right
            other_right = other.right
            new_right = [self + n for n in other_right] + [other + n for n in
                                                         my_right]
            return SurrealNumber(left=new_left, right=new_right)
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
            n=n.simplify
        for n in self.right:
            n=n.simplify
        self.remove_dominated_options()


    def remove_dominated_options(self):
        x=[[n<=m for m in self.right] for n in self.right]
        y=[functools.reduce(operator.mul, y, 1) for y in x]
        self.right=list(itertools.compress(self.right,y))
        x=[[n>=m for m in self.left] for n in self.left]
        y=[functools.reduce(operator.mul, y, 1) for y in x]
        self.left=list(itertools.compress(self.left,y))

    def is_number(self):
        test=itertools.product(self.right,self.left)
        return bool(functools.reduce(operator.mul, [i[0]<i[1] for i in test], 1))

    def __repr__(self):
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
        return ans + '}'

    def __le__(self, other):
        for n in self.right:
            if not n<other:
                return False
        for n in other.left:
            if not self<n:
                return False
        return True

    def __ge__(self, other):
        for n in self.right:
            if not n>other:
                return False
        for n in other.left:
            if not self>n:
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





def main():
    zero = SurrealNumber(left=[], right=[])
    one = SurrealNumber(left=[zero], right=[])
    neg_one = SurrealNumber(left=[], right=[zero])
    star = SurrealNumber(left=[zero], right=[zero])

    print(str(zero))
    print(str(one))
    print(str(one + one))


if __name__ == '__main__':
    main()
