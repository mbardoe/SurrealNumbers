import surrealnumber
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
            n=kwargs['value']
            if n==int(n):
                if n==0:
                    kwargs['left']=[]
                    kwargs['right']=[]
                if n>0:
                    kwargs['left']=[Number(value=n-1)]
                    kwargs['right']=[]
                if n<0:
                    kwargs['left']=[]
                    kwargs['right']=[Number(value=n+1)]
            else:
                raise ValueError('no non-integers yet.')


        super().__init__(**kwargs)

    def __add__(self, other):
        if isinstance(other,Number):
            new_value=self.value+other.value
            return Number(value=new_value)

    def __repr__(self):
        return str(self.value)

    def __le__(self, other):
        if isinstance(other, Number):
            return self.value<other.value
        else:
            return super().__le__(other)

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value>other.value
        else:
            return super().__ge__(other)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value==other.value
        else:
            return super().__eq__(other)
        return False

    @classmethod
    def createNumber(cls,left,right):
        pass

    @staticmethod
    def simplest_between(left,right):
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
        right= right.value
        if left>right:
            raise ValueError ('Only appropriate for Numbers')
        #print str(left) + ' ' +str(right)
        if left is None:
            if right is None:
                return Number(value=0)
            if right<=0:
                return Number(value = int(right)-1)
            else:
                return Number(value=0)
        if right is None:
            if left >= 0:
                return Number(value = int(left)+1)
            else:
                return Number(value=0)
        if left<Number(value=0) and right>Number(value=0):
            return Number(value=0)

        if right<Number(value=0):
            right,left=-1*left,-1*right
            sign=-1
        else:
            sign=1
        if int(right)-int(left)>1:
            return Number(value = sign*(int(left)+1))
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
