from collections import defaultdict


def p49(strs: list[str]) -> list[list[str]]:
    """49. Group Anagrams https://leetcode.com/problems/group-anagrams/

    Examples
    --------
    >>> p49(["eat", "tea", "tan", "ate", "nat", "bat"])
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    >>> p49([""])
    [['']]
    >>> p49(["a"])
    [['a']]

    """

    def group_key(s: str) -> tuple[str, ...]:
        return tuple(sorted(s))

    groups = defaultdict(list)
    for s in strs:
        groups[group_key(s)].append(s)

    return list(groups.values())
