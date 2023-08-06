"""lostc.collection

Global functions for collections
"""

from collections import defaultdict


def divide(collection, divide_func):
    """Divide a collection into two parts.

    - collection: list or dict like object
    - divide_func: the divide function to return True/False

    Return two parts of the collection.

    Example:
    divide([1, 2, 3], lambda x: x > 1)             ->   [2, 3], [1]
    divide({'a': 1, 'b': 2}, lambda k, v: v > 1)   ->   {'b': 2}, {'a': 1}
    """
    func = divide_dict if isinstance(collection, dict) else divide_list
    return func(collection, divide_func)


def divide_list(a_list, divide_func):
    """Divide a list like object into two parts.

    - a_list: list like object
    - divide_func: the divide function to return True/False

    Return two parts of the list.

    Example:
    divide_list([1, 2, 3], lambda x: x > 1)   ->   [2, 3], [1]
    """
    suit, not_suit = [], []
    for item in a_list:
        result = suit if divide_func(item) else not_suit
        result.append(item)
    return suit, not_suit


def divide_dict(a_dict, divide_func):
    """Divide a dict like object into two parts.

    - a_dict: dict like object
    - divide_func: the divide function to return True/False

    Return two parts of the dict.

    Example:
    divide({'a': 1, 'b': 2}, lambda k, v: v > 1)   ->   {'b': 2}, {'a': 1}
    """
    suit, not_suit = {}, {}
    for key, value in a_dict.items():
        result = suit if divide_func(key, value) else not_suit
        result[key] = value
    return suit, not_suit


def classify(collection, *filters, **kfilters):
    """Classfy a list or dict like object. Multiple filters in one loop.

    - collection: list or dict like object
    - filters: the filter functions to return True/False
    - kfilters: the filter functions with key to return True/False

    Return multiple filter results.

    Example:
    data = [1, 2, 3]
    m1 = lambda x: x > 1
    m2 = lambda x: x > 2
    classify(data, m1, m2)         ->   [2, 3], [3]
    classify(data, m1=m1, m2=m2)   ->   {'m1': [2, 3], 'm2': [3]}

    data = {'a': 1, 'b': 2}
    dm1 = lambda k, v: v > 1
    dm2 = lambda k, v: v > 2
    classify(data, dm1, dm2)           ->   {'b': 2}, {}
    classify(data, dm1=dm1, dm2=dm2)   ->   {'dm1': {'b': 2}, 'dm2': {}}
    """
    func = classify_dict if isinstance(collection, dict) else classify_list
    return func(collection, *filters, **kfilters)


def classify_dict(a_dict, *filters, **kfilters):
    """Classfy a dict like object. Multiple filters in one loop.

    - a_dict: dict like object
    - filters: the filter functions to return True/False
    - kfilters: the filter functions with key to return True/False

    Return multiple filter results.

    Example:
    data = {'a': 1, 'b': 2}
    dm1 = lambda k, v: v > 1
    dm2 = lambda k, v: v > 2
    classify_dict(data, dm1, dm2)           ->   {'b': 2}, {}
    classify_dict(data, dm1=dm1, dm2=dm2)   ->   {'dm1': {'b': 2}, 'dm2': {}}
    """
    if kfilters:
        return classify_dict_kf(a_dict, **kfilters)
    elif filters:
        return classify_dict_f(a_dict, *filters)
    else:
        return dict(a_dict)


def classify_dict_kf(a_dict, **kfilters):
    """Classfy a dict like object. Multiple filters in one loop.

    - a_dict: dict like object
    - kfilters: the filter functions with key to return True/False

    Return multiple filter results.

    Example:
    data = {'a': 1, 'b': 2}
    dm1 = lambda k, v: v > 1
    dm2 = lambda k, v: v > 2
    classify_dict_kf(data, dm1=dm1, dm2=dm2)   ->   {'dm1': {'b': 2}, 'dm2': {}}
    """
    results = defaultdict(dict)
    for key, value in a_dict.items():
        for name, filter_func in kfilters.items():
            if filter_func(key, value):
                results[name][key] = value
    return results


def classify_dict_f(a_dict, *filters):
    """Classfy a dict like object. Multiple filters in one loop.

    - a_dict: dict like object
    - filters: the filter functions to return True/False

    Return multiple filter results.

    Example:
    data = {'a': 1, 'b': 2}
    dm1 = lambda k, v: v > 1
    dm2 = lambda k, v: v > 2
    classify_dict_f(data, dm1, dm2)   ->   {'b': 2}, {}
    """
    results = tuple({} for i in range(len(filters)))
    for key, value in a_dict.items():
        for filter_func, result in zip(filters, results):
            if filter_func(key, value):
                result[key] = value
    return results


def classify_list(a_list, *filters, **kfilters):
    """Classfy a list like object. Multiple filters in one loop.

    - collection: list like object
    - filters: the filter functions to return True/False
    - kfilters: the filter functions with key to return True/False

    Return multiple filter results.

    Example:
    data = [1, 2, 3]
    m1 = lambda x: x > 1
    m2 = lambda x: x > 2
    classify(data, m1, m2)         ->   [2, 3], [3]
    classify(data, m1=m1, m2=m2)   ->   {'m1': [2, 3], 'm2': [3]}
    """
    if kfilters:
        return classify_list_kf(a_list, **kfilters)
    elif filters:
        return classify_list_f(a_list, *filters)
    else:
        return list(a_list)


def classify_list_kf(a_list, **kfilters):
    """Classfy a list like object. Multiple filters in one loop.

    - collection: list like object
    - kfilters: the filter functions with key to return True/False

    Return multiple filter results.

    Example:
    data = [1, 2, 3]
    m1 = lambda x: x > 1
    m2 = lambda x: x > 2
    classify(data, m1=m1, m2=m2)   ->   {'m1': [2, 3], 'm2': [3]}
    """
    results = defaultdict(list)
    for item in a_list:
        for name, filter_func in kfilters.items():
            if filter_func(item):
                results[name].append(item)
    return results


def classify_list_f(a_list, *filters):
    """Classfy a list like object. Multiple filters in one loop.

    - collection: list like object
    - filters: the filter functions to return True/False

    Return multiple filter results.

    Example:
    data = [1, 2, 3]
    m1 = lambda x: x > 1
    m2 = lambda x: x > 2
    classify(data, m1, m2)   ->   [2, 3], [3]
    """
    results = tuple([] for i in range(len(filters)))
    for item in a_list:
        for filter_func, result in zip(filters, results):
            if filter_func(item):
                result.append(item)
    return results


def unique(collection, unique_func=None, replace=False):
    """Unique a list or dict like object.

    - collection: list or dict like object
    - unique_func: the filter functions to return a hashable sign for unique
    - replace: the following replace the above with the same sign

    Return the unique subcollection of collection.

    Example:
    data = [(1, 2), (2, 1), (2, 3), (1, 2)]
    unique_func = lambda x: tuple(sorted(x))
    unique(data)                              ->   [(1, 2), (2, 1), (2, 3)]
    unique(data, unique_func)                 ->   [(1, 2), (2, 3)]
    unique(data, unique_func, replace=True)   ->   [(2, 1), (2, 3)]

    data = {'a': 1, 'b': 2, 'c': 1}
    unique_func = lambda k, v: v
    unique(data)                              ->   {'a': 1, 'b': 2, 'c': 1}
    unique(data, unique_func)                 ->   {'a': 1, 'b': 2}
    unique(data, unique_func, replace=True)   ->   {'b': 2, 'c': 1}
    """
    func = unique_dict if isinstance(collection, dict) else unique_list
    return func(collection, unique_func, replace)


def unique_dict(a_dict, unique_func=None, replace=False):
    """Unique a dict like object.

    - collection: dict like object
    - unique_func: the filter functions to return a hashable sign for unique
    - replace: the following replace the above with the same sign

    Return the unique subcollection of collection.

    Example:
    data = {'a': 1, 'b': 2, 'c': 1}
    unique_func = lambda k, v: v
    unique(data)                              ->   {'a': 1, 'b': 2, 'c': 1}
    unique(data, unique_func)                 ->   {'a': 1, 'b': 2}
    unique(data, unique_func, replace=True)   ->   {'b': 2, 'c': 1}
    """
    unique_func = unique_func or (lambda k, v: k)
    result = {}
    for key, value in a_dict.items():
        hashable_sign = unique_func(key, value)
        if hashable_sign not in result or replace:
            result[hashable_sign] = (key, value)
    return dict(result.values())


def unique_list(a_list, unique_func=None, replace=False):
    """Unique a list like object.

    - collection: list like object
    - unique_func: the filter functions to return a hashable sign for unique
    - replace: the following replace the above with the same sign

    Return the unique subcollection of collection.

    Example:
    data = [(1, 2), (2, 1), (2, 3), (1, 2)]
    unique_func = lambda x: tuple(sorted(x))
    unique(data)                              ->   [(1, 2), (2, 1), (2, 3)]
    unique(data, unique_func)                 ->   [(1, 2), (2, 3)]
    unique(data, unique_func, replace=True)   ->   [(2, 1), (2, 3)]
    """
    unique_func = unique_func or (lambda x: x)
    result = {}
    for item in a_list:
        hashable_sign = unique_func(item)
        if hashable_sign not in result or replace:
            result[hashable_sign] = item
    return list(result.values())


def dict_from(iterable, from_func=lambda x, y: y, ignore=lambda k, v: False):
    """Generate a dict from (key, value) iterator.

    - iterable: a (key, value) iterator
    - from_func: a reduce function with same key for generation
    - ignore: a function to ignore key/value

    Return a generated dict.

    Example:
    data = [('tom', 1), ('jack', 2), ('tom', 3), ('candy', 4)]
    dict_from(data)   ->   {'jack': 2, 'tom': 3, 'candy': 4}
    dict_from(data, ignore=lambda k, v: v > 2)   ->   {'tom': 1, 'jack': 2}

    data = [('tom', 1), ('jack', 2), ('tom', 3), ('candy', 4)]
    dict_from_sum = lambda iterable: dict_from(iterable, lambda x, y: x + y)
    dict_from_sum(data)   ->   {'tom': 4, 'jack': 2, 'candy': 4}
    """
    result = {}
    for key, value in iterable:
        value = from_func(result[key], value) if key in result else value
        if not ignore(key, value):
            result[key] = value
    return result


def dict_from_sum(iterable):
    """Generate a dict from (key, value) iterator.

    - iterable: a (key, value) iterator

    Return a generated dict.

    Example:
    data = [('tom', 1), ('jack', 2), ('tom', 3), ('candy', 4)]
    dict_from_sum(data)   ->   {'tom': 4, 'jack': 2, 'candy': 4)}
    """
    return dict_from(iterable, lambda x, y: x + y)


def first(collection, find_func):
    """Find the first matched item in collection
    same as 'find' with default options

    - collection: list or dict like object
    - find_func: the filter function to find a matched item

    Return a item or (key, value)

    Example:
    first(range(10), lambda x: x > 3)                     ->   4
    first({'a': 1, 'b': 2: 'c': 3}, lambda k, v: v > 1)   ->   'b', 2
    """
    return find(collection, find_func, reverse=False)


def last(collection, find_func):
    """Find the first matched item in collection

    - collection: list or dict like object
    - find_func: the filter function to find a matched item

    Return a item or (key, value)

    Example:
    first(range(10), lambda x: x > 3)                     ->   4
    first({'a': 1, 'b': 2: 'c': 3}, lambda k, v: v > 1)   ->   'b', 2
    """
    return find(collection, find_func, reverse=True)


def find(collection, find_func, reverse=False):
    """Find the last matched item in collection

    - collection: list or dict like object
    - find_func: the filter function to find a matched item

    Return a item or (key, value)

    Example:
    last(range(10), lambda x: x > 3)                     ->   9
    last({'a': 1, 'b': 2: 'c': 3}, lambda k, v: v > 1)   ->   'c', 3
    """
    func = find_in_dict if isinstance(collection, dict) else find_in_list
    return func(collection, find_func, reverse=reverse)


def find_in_dict(a_dict, find_func, reverse=False):
    """Find a matched item in dict

    - a_dict: dict like object
    - find_func: the filter function to find a matched item
    - reverse: find in reversed? True/False

    Return (key, value) of the dict

    Example:
    data = {'a': 1, 'b': 2: 'c': 3}
    find_in_dict(data, lambda k, v: v > 1)                 ->   'b', 2
    find_in_dict(data, lambda k, v: v > 1, reverse=True)   ->   'c', 3
    """
    items = reversed(list(a_dict.items())) if reverse else a_dict.items()
    iterable = ((key, value) for key, value in items if find_func(key, value))
    return next(iterable, None)


def find_in_list(a_list, find_func, reverse=False):
    """Find a matched item in list

    - a_list: list like object
    - find_func: the filter function to find a matched item
    - reverse: find in reversed? True/False

    Return a item in the list

    Example:
    data = [1, 2, 3]
    find_in_dict(data, lambda x: x > 1)                 ->   2
    find_in_dict(data, lambda x: x > 1, reverse=True)   ->   3
    """
    items = reversed(list(a_list)) if reverse else a_list
    iterable = (item for item in items if find_func(item))
    return next(iterable, None)


def groupby(collection, groupby_func):
    """Groupby items in collection

    - collection: list or dict like object
    - groupby_func: the hash function to group items

    Return a groups dict

    Example:
    data = range(3)
    groupby_func = lambda x: x % 2
    groupby(data, groupby_func)   ->   { 0: [0, 2], 1: [1] }

    data = { 0: 1, 1: 1, 2: 0 }
    groupby_func = lambda k, v: k + v
    groupby(data, groupby_func)   ->   { 1: {0: 1}, 2: {1: 1, 2: 0} }
    """
    func = groupby_dict if isinstance(collection, dict) else groupby_list
    return func(collection, groupby_func)


def groupby_dict(a_dict, groupby_func):
    """Groupby items in dict

    - a_dict: dict like object
    - groupby_func: the hash function to group items

    Return a groups dict

    Example:
    data = { 0: 1, 1: 1, 2: 0 }
    groupby_func = lambda k, v: k + v
    groupby(data, groupby_func)   ->   { 1: {0: 1}, 2: {1: 1, 2: 0} }
    """
    groups = defaultdict(dict)
    for key, value in a_dict.items():
        group_key = groupby_func(key, value)
        groups[group_key][key] = value
    return dict(groups)


def groupby_list(a_list, groupby_func):
    """Groupby items in list

    - a_list: list like object
    - groupby_func: the hash function to group items

    Return a groups dict

    Example:
    data = range(3)
    groupby_func = lambda x: x % 2
    groupby(data, groupby_func)   ->   { 0: [0, 2], 1: [1] }
    """
    groups = defaultdict(list)
    for item in a_list:
        group_key = groupby_func(item)
        groups[group_key].append(item)
    return dict(groups)


if __name__ == "__main__":
    from pprint import pprint as pp
    import range as urange

    data = range(10)
    pp(divide(data, lambda x: x > 5))
    pp(classify(data, lambda x: x > 3, lambda x: x > 5))
    pp(classify(data, gt3=lambda x: x > 3, gt5=lambda x: x > 5))
    pp(classify(data, lambda x: x > 1, gt3=lambda x: x > 3))

    data = dict(zip(urange.char_range("a", "z"), range(26)))
    pp(divide(data, lambda k, v: v > 5))
    pp(classify(data, lambda k, v: v > 3, lambda k, v: v > 5))
    pp(classify(data, gt3=lambda k, v: v > 3, gt5=lambda k, v: v > 5))
    pp(classify(data, lambda k, v: v > 1, gt3=lambda k, v: v > 3))

    data = [(1, 2), (2, 1), (2, 3)]
    pp(unique(data, lambda x: tuple(sorted(x))))
    pp(unique(data, lambda x: tuple(sorted(x)), replace=True))

    data = {"a": 1, "b": 2, "c": 1}
    pp(unique(data, lambda k, v: v))
    pp(unique(data, lambda k, v: v, replace=True))

    data = [("tom", 1), ("jack", 2), ("tom", 3), ("candy", 4)]
    pp(dict_from(data))
    pp(dict_from_sum(data))

    data = range(10)
    pp(find(data, lambda x: x > 3))
    pp(first(data, lambda x: x > 3))
    pp(find(data, lambda x: x > 3, reverse=True))
    pp(last(data, lambda x: x < 6))

    data = dict(zip(urange.char_range("a", "z"), range(26)))
    pp(find(data, lambda k, v: v > 3))
    pp(first(data, lambda k, v: v > 3))
    pp(find(data, lambda k, v: v < 6, reverse=True))
    pp(last(data, lambda k, v: v < 6))

    data = range(10)
    pp(groupby(data, lambda x: x % 2))

    data = {"a": 1, "b": 2, "c": 1}
    pp(groupby(data, lambda k, v: v))
