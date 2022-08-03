qutip-benchmark:
================


To run the benchmarks first clone and install Qutip (this plugin is meant to run with qutip v5 which is not realeased yet).
```
pip install git+https://github.com/qutip/qutip@dev.major

```

To run the benchmarks use
```
python benchmarks/benchmarks.py
```

This will store the resulting data and figures in the folder `.benchmarks/`.

The benchmarks consist on a set of operations, such as matrix multiplication,
and solvers, such as MeSolve.
The benchmarks run the same operations for different hermitian matrix sizes 
that can either be dense or sparse (tridiagonal).  The script also includes 
a few other options.
You can get a description of the arguments with `python
benchmarks/benchmarks.py --help`. It also accepts any argument that
[pytest-benchmark](https://pytest-benchmark.readthedocs.io/en/latest/) accepts.
Examples:

-`python benchmarks/benchmarks.py -k"test_linear_algebra" --collect-only`:
Shows all the available benchmarks. Useful to filter them with the `-k`
argument. 

-`python benchmarks/benchmarks.py -k"matmul"`: Runs only the benchmarks for
`matmul`.

-`python benchmarks/benchmarks.py -k"add and -dense-"`: Runs only the
benchmarks for `add` (addition) with dense random matrices. 

-`python benchmarks/benchmarks.py -k"add and -dense- and qutip_dense"`: runs only the
benchmarks for `add` with dense random matrices and only for the `qutip_dense`
data type. 

-`python benchmarks/benchmarks.py -k"add and -dense- and qutip_"`: runs only the
benchmarks for `add` with dense random matrices for all the specialisations in
QuTiP. 

-`python benchmarks/benchmarks.py -k"(numpy or qutip_dense) and
-2-"`: Runs the benchmarks for every operation with hermitian
matrices of size 2x2 represented with either `numpy` or the
`qutip_dense` data type.


Support
-------

[![Unitary Fund](https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=flat)](https://unitary.fund)
[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.org)

We are proud to be affiliated with [Unitary Fund](https://unitary.fund) and
[NumFOCUS](https://numfocus.org).  QuTiP development is supported by [Nori's
lab](https://dml.riken.jp/) at RIKEN, by the University of Sherbrooke, and by
Aberystwyth University, [among other supporting
organizations](https://qutip.org/#supporting-organizations).  Initial work on
this project was sponsored by [Google Summer of Code
2022](https://summerofcode.withgoogle.com).


