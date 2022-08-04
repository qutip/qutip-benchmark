"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip as qt
import numpy as np
import scipy as sc


# Available datatypes (using qutip_dense and qutip_csr to avoid confusion
# with density parameters)
@pytest.fixture(params=['numpy', 'scipy_csr', 'qutip_dense', 'qutip_csr'])
def dtype(request): return request.param


@pytest.fixture(params=np.logspace(1, 9, 9, base=2, dtype=int).tolist())
def size(request): return request.param


@pytest.fixture(params=["dense", "sparse"])
def density(request): return request.param


@pytest.fixture()
def matrix(size, density, dtype):
    """Return a random matrix of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a tridiagonal matrix respectively.
    The matrices are Hermitian."""
    np.random.seed(1)

    if density == "sparse":
        ofdiag = np.random.rand(size-1) + 1j*np.random.rand(size-1)
        diag = np.random.rand(size) + 1j*np.random.rand(size)

        res = (np.diag(ofdiag, k=-1) +
               np.diag(diag, k=0) +
               np.diag(ofdiag.conj(), k=1))

    elif density == "dense":
        H = np.random.random((size, size)) + 1j*np.random.random((size, size))
        res = H + H.T.conj()

    if dtype == 'numpy':
        return res
    elif dtype == 'scipy_csr':
        return sc.sparse.csr_matrix(res)
    else:
        res = qt.Qobj(res)
        # the to() method only accepts dense or csr as inputs
        return res.to(dtype[6:])


@pytest.fixture(params=["op", 'ket'])
def matrix_2(matrix, size, density, dtype, request):
    if request.param == "op":
        return matrix
    if density == "sparse":
        res = qt.rand_ket(size, density=0.3)
    else:
        res = qt.rand_ket(size, density=1)

    if dtype == 'numpy':
        return res.full()
    if dtype == 'scipy_csr':
        return sc.sparse.csr_matrix(res.full())
    else:
        return res


def add(A, B):
    return A+B


def matmul(A, B):
    return A@B


def test_add(benchmark, matrix, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Add-" + group
    benchmark.group = group

    A = matrix
    B = matrix

    # Benchmark operations
    result = benchmark(add, A, B)

    return result


def test_matmul(benchmark, matrix, matrix_2, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Matmul-" + group
    benchmark.group = group

    A = matrix
    B = matrix_2

    # Benchmark operations
    result = benchmark(matmul, A, B)

    return result
