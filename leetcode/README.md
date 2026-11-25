# LeetCode Solutions

Practice problems, one self-contained Python file per problem in `solutions/pNNNN.py`, with the examples as
doctests. Alternative approaches sit beside the main one as `pNNNN-name.py` (for example `p0006-b.py`). Driven by a Justfile and Nushell
(`tools/leet.nu`); Python runs through [`uv`](https://github.com/astral-sh/uv).

```sh
just get 34         # print a problem statement (no number: the smallest unsolved one)
just daily          # today's daily challenge
just new 34         # solutions/p0034.py from templates/template.py
just check          # run every file's doctests (`just check 34` for one)
```

There is no project file: a solution that needs a package (`numpy`) declares it in a `# /// script` header, and
`just check` runs those files under `uv`.

Shared helpers (`ListNode`, `TreeNode`, ...) are copied into each file that needs them, so a file can be pasted
into LeetCode as is. Known failures: `p0037` and `p0047` doctests.
