"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip
import numpy as np


@pytest.fixture(params=np.logspace(1, 9, 9, base=2, dtype=int).tolist())
def size(request): return request.param


@pytest.fixture(params=["dense", "sparse"])
def density(request): return request.param


@pytest.fixture(scope='function')
def right_ket(size, density):
    if density == "sparse":
        return qutip.rand_ket(size, density=1/size)
    return qutip.rand_ket(size, density=1)


# Supported dtypes
dtype = ['function', 'array', 'string']
@pytest.fixture(params=dtype)
def dtype(request): return request.param


@pytest.fixture(scope='function')
def left_QobjEvo(size, density, dtype):
    """Return a random QobjEvo of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a reandomly sparse matrix
    respectively. The matrices are Hermitian."""

    if density == "sparse":
        res = qutip.rand_herm(size, density=1/size)

    elif density == "dense":
        res = qutip.rand_herm(size, density=1)

    if dtype == 'function':
        def cos_t(t):
            return np.cos(t)
        return qutip.QobjEvo([res, cos_t])

    if dtype == 'string':
        return qutip.QobjEvo([res, 'cos(t)'])

    tlist = np.linspace(0, 10, 101)
    values = np.cos(tlist)
    return qutip.QobjEvo([res, values], tlist=tlist)


def matmul(left, right):
    return left.matmul(2, right)


@pytest.mark.nightly
def test_matmul_QobjEvo_ket(benchmark, left_QobjEvo, right_ket, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Matmul_QobjEvo_op@ket-" + group
    benchmark.group = group
    # Benchmark operations and skip those that are not implemented.

    result = benchmark(matmul, left_QobjEvo, right_ket)

    return result