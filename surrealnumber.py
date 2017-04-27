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
