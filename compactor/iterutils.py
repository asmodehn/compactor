
import itertools


def unique_everseen(iterable, key=None):
    """
    List unique elements, preserving order.
    Remembers all elements ever seen.

    >>> [c for c in unique_everseen('AAAABBBCCDAABBB')]
    ['A', 'B', 'C', 'D']
    >>> [c for c in unique_everseen('ABBCcAD', str.lower)]
    ['A', 'B', 'C', 'D']
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


if __name__ == '__main__':
    import doctest
    doctest.testmod()
