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

    @property
    def left(self):
        return self.left

    @property
    def right(self):
        return self.right


    def __add__(self, other):
        if isinstance(other, SurrealNumber):
            myleft=self.get_left
            otherleft=other.get_left

    def __repr__(self):
        ans='{'
        for i in self.left:
            ans+=' '+str(i)+','
        ans=ans[:-1]
        ans+=' | '
        for i in self.left:
            ans+=' '+str(i)+','
        return ans[:-1]+'}'

