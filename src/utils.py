"""Module providing utility functions"""
from typing import List, TypeVar

T = TypeVar("T")
def pad_list(lst: List[T], padding: T, pre_pad: int = 0, post_pad: int = 0) -> List[T]:
    """
    Create a new list by concatenating pre_pad copies of padding at the beginning,
    the original list, and post_pad copies of padding at the end.
    """
    return ([padding] * pre_pad) + lst + ([padding] * post_pad)