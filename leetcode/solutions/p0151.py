def p151(s: str) -> str:
    """151. Reverse Words In A String https://leetcode.com/problems/reverse-words-in-a-string/

    Lesson learned:
    - Python string built-ins are fast.
    - The follow-up asks: can you use only O(1) extra space? Here is the trick:
    first reverse the whole string and then reverse each word. Reversing each
    requires keeping track of two pointers: the start of a word and the end of a
    word (terminated by a space).

    Examples
    --------
    >>> p151("the sky is blue")
    'blue is sky the'
    >>> p151("  hello world!  ")
    'world! hello'
    >>> p151("a good   example")
    'example good a'
    >>> p151("  Bob    Loves  Alice   ")
    'Alice Loves Bob'

    """
    return " ".join(s.split()[::-1])
