qutip-benchmark
===============
Installation
-------

To run the benchmarks first clone and install QuTiP (this plugin is meant to run with qutip v5 which is not realeased yet).
```
pip install git+https://github.com/qutip/qutip@dev.major
```
You will then want to install this repo by cloning it from github.

The benchmarks
-------
The benchmarks so far are two different types, basic operations such as matrix multiplication or addition and solvers.  
The operations are benchmarked using 3 parameters:  
- Density: either sparse or dense, matrices and vectors are created usning `qutip.rand_herm(size, density=1/size)`for sparse operators and `density=1` for dense. Sparse kets ase using `qutip.rand_ket(size, density=0.3)`.  
- Size: 2**N with N going from 1 to 9. (2 to 512)
- dtype (or coeftype fro QobjEvo operations).

Solvers are benchmarked using 2 fixtures:
- Size 2**N with N going from 2 to 7. (4 to 128)
- The models used are common models such as a cavity, the Jaynes-Cummings model and a qubit spin chain.

Running the benchmarks
-------

to run the benchmarks use the following command from the root of the repository:
```
python benchmark/qutip/runbenchmark.py
```

This will store the resulting data and figures in the folder `.benchmarks/`.

The benchmarks consist on a set of operations, such as matrix multiplication,
and solvers, such as MeSolve.
The benchmarks run the same operations for different hermitian matrix sizes 
that can either be dense or sparse (tridiagonal).  The script also includes 
a few other options.
You can get a description of the arguments with `python
benchmarks/benchmarks.py --help` or
see the [Pytest documentation](https://docs.pytest.org/en/7.1.x/reference/reference.html#command-line-flags) 
and [Pytest-Benchmark documetation](https://pytest-benchmark.readthedocs.io/en/stable/usage.html#commandline-options)
for all command line flags.
Examples:

-`python -m qutip_benchmarks.cli.run_benchmarks -k "test_linear_algebra" --collect-only`:
Shows all the available benchmarks. Useful to filter them with the `-k`
argument. 

-`python -m qutip_benchmarks.cli.run_benchmarks -k "matmul"`: Runs only the benchmarks for
`matmul`.

Viewing the benchmarks
-------
The default method to view the benchmarks is by using:
```
python -m qutip_benchmarks.cli.view_benchmarks
```
This will plot the benchmarks in an identical manner to what is found on the Qutip's benchmark [website](https://qutip.org/qutip-benchmark).

This scipts accepts 4 flags:
| Flag      | Description |
| ----------- | ----------- |
| `--plotpath` | By default separates nightly and scaling into `./images/plots/scaling` and `./images/plots/nightly` if you want them to be separated with a custom path you will need to run this file twice using the `--scaling` and `--nightly` flags and the desired path |
| `--benchpath`   | Path to folder in which the benchmarks are stored  | 
| `--scaling`   | Only plot scaling (time vs matirx size) from the latest benchmark file  | 
| `--nightly`   | Plot the performance over time using results from all the benchmark files   | 

If you wish to have more control on what to plot you can import view_utilities.py to a python script and use the available functions. 
These functions all contain an extensive description of the accepted parameters and outputs can be used for which you can find in `benchmarks/view_utilities.py` so only a brief description will be given here, you can also view a use case example in this [tutorial](tutorial.md).

| Function      | Description |
| ----------- | ----------- |
|`json_to_dataframe()` | accepts a path to one folder and creates a dataframe with only the information required to produce the plots.|
|`get_paths()` | accepts the path to the folder containin the results the benchmarks you have run and returns a list of paths to each file conatined within ordered by date.|
|`create_dataframe()` | accepts a list of paths (produced by `get_paths()`) and creates on big datafram containing all the informaition for the benchmark files.|
|`sort_ops()` | accepts the dataframe and sort the information by operation and allows you to filter out certain operation if you do not wish to plot them. It outputs a dictionnary with the operation as the key and a dataframe of the corresponding information as the value.|
|`sort_params()` | accepts the dictionnary produced by `sort_ops()` and sort the data using the fixtures used to perform the benchamrks, such as matrix size or density. You can choose to exclude a certain parameter from the sorting. This effetively separates the information by plot. You can also designate a parameter to be used separate the data into different lines on the same plot. This function outputs a dictionnary with the plot title as a key and the corresponding dataframe and line separators, if any a provided, as the value.|
|`plot_data()`| Accepts the dictionnary produced by `sort_params()` and creates all the plots, this function also separates the data using a line separator if provided an add a CPU name to the legend, if the benchmarks were performed on VMs or different machines this function will also separete the data into diffrent lines, assigning a color to data separated by a line separator and a diffrent line and marker to the data separated by CPU, as seen on the [qutip benchmarks website](https://qutip.org/qutip-benchmark). You can also choose what should be plotted on the x and y axes, and whether they use logarithmic scaling or not|


Support
-------

[![Unitary Fund](https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=flat)](https://unitary.fund)
[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.org)

We are proud to be affiliated with [Unitary Fund](https://unitary.fund) and
[NumFOCUS](https://numfocus.org).  QuTiP development is supported by [Nori's
lab](https://dml.riken.jp/) at RIKEN, by the University of Sherbrooke, and by
Aberystwyth University, [among other supporting
organizations](https://qutip.org/#supporting-organizations). The update of this project was sponsored by [Google Summer of Code
2022](https://summerofcode.withgoogle.com).


