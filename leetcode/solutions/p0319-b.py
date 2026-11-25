# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
import numpy as np


def p319b(n: int) -> int:
    """Examples
    >>> p319b(3)
    1
    >>> p319b(0)
    0
    >>> p319b(1)
    1
    >>> p319b(5)
    2

    """
    return int(np.sqrt(n))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
