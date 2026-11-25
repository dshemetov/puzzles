from collections import Counter


def p30(s: str, words: list[str]) -> list[int]:
    """30. Substring with Concatenation of All Words https://leetcode.com/problems/substring-with-concatenation-of-all-words/

    Example:
    >>> p30("barfoothefoobarman", ["foo", "bar"])
    [0, 9]
    >>> p30("wordgoodgoodgoodbestword", ["word", "good", "best", "word"])
    []
    >>> p30("barfoofoobarthefoobarman", ["bar", "foo", "the"])
    [6, 9, 12]
    >>> p30("afoobar", ["foo", "bar"])
    [1]
    """
    n = len(s)
    n_words = len(words)
    word_length = len(words[0])

    if word_length * n_words > n:
        return []

    target_counter = Counter(words)
    answer = []
    for i in range(word_length):
        lo = i
        cur_len = 0
        cur_counter = Counter({})
        for j in range(i, len(s), word_length):
            # print(cur_counter)
            entering_word = s[j : j + word_length]
            if entering_word not in words:
                cur_counter = Counter({})
                lo = j + word_length
                cur_len = 0
                continue
            cur_counter[entering_word] += 1
            cur_len += 1
            if cur_len > n_words:
                exiting_word = s[lo : lo + word_length]
                cur_counter[exiting_word] -= 1
                lo += word_length
            if cur_counter == target_counter:
                answer.append(lo)

    return sorted(answer)
