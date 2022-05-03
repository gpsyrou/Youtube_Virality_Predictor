""" Collection of function used to apply transformations on columns/features
"""
from typing import List


def is_full_capital_string(s: str, threshold: float = 0.7) -> bool:
    """ Identifies if a given string consist only by capital letters.
    The function compares if number of capital letters >= a give threshold
    as defined by the @threshold parameter.
    """
    is_full_capital = False

    letters = [l for l in s if l.isalpha()]
    capital_letters = [l for l in letters if l.isupper()]

    if (len(capital_letters) / len(list(letters))) >= threshold:
        is_full_capital = True

    return is_full_capital


def extract_tags(s: str, sep: str = '|') -> List[str]:
    if 'None' in s:
        return None
    else:
        return s.split(sep)


def get_tag_size(s: str, sep: str = '|') -> int:
    s = extract_tags(s, sep=sep)
    if isinstance(s, type(None)):
        return 0
    else:
        return len(s)
