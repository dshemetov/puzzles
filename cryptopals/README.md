# Cryptopals

[The Cryptopals Crypto Challenges](https://cryptopals.com/), one self-contained file per challenge in
`solutions/set<S>/cNN.py`. Each script is a [uv](https://docs.astral.sh/uv/) script (dependencies declared inline),
prints its answer and asserts it against the published one. Challenge data files go in `data/`.

```sh
just new 1 4        # solutions/set1/c04.py from templates/template.py
just run 1 3        # run set 1 challenge 3
just check          # run every challenge; `just check 1` for one set
just fetch 4        # download data/c04.txt
```
