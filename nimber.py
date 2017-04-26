import surrealnumber
import number
class Nimber(surrealnumber.SurrealNumber):
    '''A class that represents a standard number within the surreal numbers.
    Right now we will focus on numbers that were born on a finite day.

    Attributes:
        left: (list) a list of the surreal numbers that are possible moves for
                    left.
        right: (list) a list fo the surreal numbers that are a possible move for
                right.
        value: (int) the numerical value of the nimber.

    Start with support for numbers, nimbers, and switches.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'value' in kwargs.keys():
            n=kwargs['value']
            if n==int(n):
                if n>=0:
                    kwargs['left']=[Nimber(value=i) for i in range(n)]
                    kwargs['right']=[Nimber(value=i) for i in range(n)]
                if n<0:
                    raise ValueError("Nimbers aren't negative")
            else:
                raise ValueError("Nimbers have to be whole")
        if 'left' in kwargs.keys() and 'right' in kwargs.keys():
            for i in kwargs['left']:
                if not i in kwargs['right']:
                    raise ValueError("Nimbers have equal moves for left and right")
            for i in kwargs['right']:
                if not i in kwargs['left']:
                    raise ValueError("Nimbers have equal moves for left and right")
        super().__init__(**kwargs)
        self.value=Nimber.mex(self.left)


    # @property
    # def value(self):
    #     return mex(self.left)

    def __add__(self, other):
        if isinstance(other, Nimber):
            return Nimber(value=self.value^other.value)
        else:
            return super().__add__(other)

    def __repr__(self):
        if self.value==1:
            return '*'
        return '*'+str(self.value)

    def __eq__(self, other):
        if isinstance(other, Nimber):
            if self.value==other.value:
                return True
        return False

    def __int__(self):
        return int(self.value)

    @staticmethod
    def mex(mylist):
        """mex computes the smallest positive integer that is missing from a list.

        mex is essential to calculations with impartial games. By finding the
        smallest excluded value it is possible to find the equivalent nim stack.

        Args:
            mylist (list): a list of of values of positive integers

        Returns:
            int: the smallest positive integer that is missing from the
                list

        Raises:
            ValueError: If the list is not all positive integers.
            TypeError: if you don't give it a list of integers
        """
        current=0
        mylist=list(mylist)
        mylist=sorted(mylist)
        mylist=[int(i) for i in mylist] # this helps sage do its thing
        #print str(mylist)
        for i in range(len(mylist)):
            if not isinstance(mylist[i],int):
                raise TypeError("Has to be a list of integers.")
            if mylist[i]<0:
                raise ValueError("Must be all positive integers.")
            if mylist[i]==current:
                current+=1
            if mylist[i]>current:
                return current

            #print "step"+str(i)+" "+str(current)
        return current

def main():
    n=Nimber(value=3)
    print(str(n))

if __name__ == '__main__':
    main()
