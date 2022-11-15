from __future__ import annotations
from typing import Generic, TypeVar

T = TypeVar('T')

class StackLink(Generic[T]):
    """
    Represents a segment in the stack structure, used to one-way link data in the stack

    Attributes
    ----------
    item : any
        The data contained in link
    link : _StackLink
        The next link segment in the stack
    is_last : bool
        True if this is the last stack link in the data structure
    """

    def __init__(self, item: T, link: StackLink[T]|None):
        self.__item = item
        self.__link = link

    @property
    def data(self):
        return self.__item

    @property
    def link(self) -> StackLink[T]:
        return self.__link

    @property
    def is_last(self) -> bool:
        return self.__link == None

class StackIterator(Generic[T]):
    """
    Iterator object for the stack
    """
    def __init__(self, link: StackLink[T]) -> None:
        self.__link = link

    def __next__(self) -> T:
        if (self.__link.is_last):
            raise StopIteration
        value = self.__link.data
        self.__link = self.__link.link
        return value

class Stack(Generic[T]):
    """
    Represents a one way liked stack data structure. The structure can be
    iterated from the top to the bottom, new items are placed on top and
    are removed from the top down. Utilizes a dummy node at the end of the
    data structure.

    Attributes
    ----------
    top : T
        The top item in the stack
    size : int
        The number of items in the stack

    Methods
    -------
    put(item : T)
        Adds an item to the top of the stack
    pop(item : T)
        Removes the top of the stack
    """
    def __init__(self):
        self.__top = StackLink[T](None, None)
        self.__size = 0

    @property
    def top(self):
        return self.__top.data

    @property
    def size(self) -> int:
        return self.__size

    def put(self, item: T):
        """
        Adds an item to the top of the stack

        Attributes
        ----------
        item : any
            The item to add to the stack
        """
        self.__top = StackLink[T](item, self.__top)
        self.__size += 1

    def pop(self) -> T|None:
        """
        Removes the top item from the stack and returns it

        Returns
        -------
        item : any
            The top item in the stack
        """
        data = self.__top.data
        if not self.__top.is_last:
            self.__top = self.__top.link
            self.__size -= 1
        return data
    
    def __eq__(self, other):
        if not isinstance(other, Stack) or self.size != other.size:
            return False
        for (a, b) in zip(self, other):
            if a != b:
                return False
        return True

    def __iter__(self):
        return StackIterator[T](self.__top)
