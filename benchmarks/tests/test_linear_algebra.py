"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip as qt
import numpy as np
import scipy as sc
from . import benchmark_binary

# Number of times the operations will be repeated.
rep = 100

# Retrieve operations
binary_ops = [
    getattr(benchmark_binary, _) for _ in
    dir(benchmark_binary) if _[:3] == "get"]
binary_ids = [_[4:] for _ in dir(benchmark_binary) if _[:3] == "get"]

# Available datatypes
dtype_list = [np, sc, qt.data.Dense, qt.data.CSR]
dtype_ids = ['numpy', 'scipy_csr', 'qutip_dense', 'qutip_csr']


@pytest.fixture(params=np.logspace(1, 9, 9, base=2, dtype=int).tolist())
def size(request): return request.param


@pytest.fixture(params=["dense", "sparse"])
def density(request): return request.param


@pytest.fixture(scope='function')
def matrix(size, density):
    """Return a random matrix of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a tridiagonal matrix respectively.
    The matrices are Hermitian."""
    np.random.seed(1)

    if density == "sparse":
        ofdiag = np.random.rand(size-1) + 1j*np.random.rand(size-1)
        diag = np.random.rand(size) + 1j*np.random.rand(size)

        return (np.diag(ofdiag, k=-1) +
                np.diag(diag, k=0) +
                np.diag(ofdiag.conj(), k=1))

    elif density == "dense":
        H = np.random.random((size, size)) + 1j*np.random.random((size, size))
        return H + H.T.conj()


def change_dtype(A, dtype):
    """Changes a numpy matrix to tensorflow, scipy sparse or to a qutip.Data
    specified by dtype"""
    if dtype == np:
        return A
    elif dtype == sc:
        return sc.sparse.csr_matrix(A)
    elif issubclass(dtype, qt.data.base.Data):
        A = qt.Qobj(A)
        return A.to(dtype)


@pytest.fixture(params=dtype_list, ids=dtype_ids)
def dtype(request): return request.param


@pytest.mark.parametrize("get_operation", binary_ops, ids=binary_ids)
def test_linear_algebra_binary(
        benchmark, matrix, dtype,
        get_operation, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = group.split('-')
    benchmark.group = '-'.join(group)
    benchmark.extra_info['dtype'] = group[0]

    matrix = change_dtype(matrix, dtype)

    # Benchmark operations
    operation = get_operation()
    result = benchmark(operation, matrix, matrix, rep)

    return result
