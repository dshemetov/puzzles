# 2022 extras

Files here are not run by the batch runner.

- `p11_cython.pyx`: a Cython version of day 11 part b (about 20 ms, against 50 ms for the Numba version in `../d11.py`).
- `p11_cython.c`: the C file Cython generated from it.

`../d11.py` is standalone and uses Numba; it does not need these files. To build the Cython module, run `cythonize -i -a p11_cython.pyx`.
