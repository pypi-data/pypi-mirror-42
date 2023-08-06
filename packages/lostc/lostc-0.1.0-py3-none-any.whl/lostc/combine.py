"""lostc.combine

Global combine functions
"""


def combination(items, sequential=True):
    """Generate a combination.

    - items: a list like object
    - sequential: need sequential? True/False

    Return a combination generated from items.

    Example:
    data = [1, 2]
    combination(data)                     ->   {(1, 2), (1, 1), (2, 1), (2, 2)}
    combination(data, sequential=False)   ->   {(1, 2), (1, 1), (2, 2)}
    """
    if sequential:
        return {tuple(item) for item in product(items, repeat=2)}
    else:
        return {tuple(sorted(item)) for item in product(items, repeat=2)}


def product(*lists, repeat=1):
    """Generate a product.

    - lists: a list of list like object
    - repeat: the repeat number of lists

    Return a product iterator generated from lists.

    Example:
    list(product([1, 2], [2, 3]))   ->   [(1, 2), (1, 3), (2, 2), (2, 3)]
    list(product([1, 2]))           ->   [(1,), (2,)]
    list(product())                 ->   [()]
    """

    def _product(lists):
        if not lists:
            yield tuple()
        else:
            for item in lists[0]:
                for rest in _product(lists[1:]):
                    yield (item,) + rest

    return _product(lists * repeat)


if __name__ == "__main__":
    from pprint import pprint as pp

    pp(list(product([1, 2, 3], [2, 3, 4])))
    pp(list(product([1, 2, 3])))
    pp(list(product()))
    pp(combination([1, 2, 3]))
    pp(combination([1, 2, 3], sequential=False))
