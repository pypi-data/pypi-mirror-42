"""lostc.range

Global functions for range
"""


def char_range(start, end, step=1):
    """Range for char by ord(char)

    - start: the first char
    - end: the end char
    - step: the distance of each step

    return range of char from start to end by step

    Example:
    char_range('a', 'c')            ->   ('a', 'b', 'c')
    char_range('a', 'e', step=2)    ->   ('a', 'c', 'e')
    char_range('a', 'f', step=2)    ->   ('a', 'c', 'e')
    """
    for char in range(ord(start), ord(end) + 1, step):
        yield chr(char)


if __name__ == "__main__":
    from pprint import pprint as pp

    pp(list(char_range("a", "z")))
    pp(list(char_range("a", "z", step=2)))
