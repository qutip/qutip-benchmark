"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip
import numpy as np


@pytest.fixture(params=np.logspace(1, 9, 9, base=2, dtype=int).tolist())
def size(request):
    return request.param


@pytest.fixture(params=["dense", "sparse"])
def density(request):
    return request.param


coeftype = ["function", "array", "string"]


@pytest.fixture(params=coeftype)
def coeftype(request):
    return request.param


@pytest.fixture(scope="function")
def left_QobjEvo(size, density, coeftype):
    """Return a random QobjEvo of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a reandomly sparse matrix
    respectively. The matrices are Hermitian."""

    # Creating static Qobj
    if density == "sparse":
        q_obj = qutip.rand_herm(size, density=1 / size)

    elif density == "dense":
        q_obj = qutip.rand_herm(size, density=1)

    # Creating coefficients
    tlist = None
    if coeftype == "function":

        def cos_t(t):
            return np.cos(t)

        coeff = cos_t

    elif coeftype == "string":
        coeff = "cos(t)"

    elif coeftype == "array":
        tlist = np.linspace(0, 10, 101)
        coeff = np.cos(tlist)
    else:
        raise Exception("Invalid coefficient type")

    return qutip.QobjEvo([q_obj, coeff], tlist=tlist)


@pytest.fixture(scope="function")
def right_ket(size):
    return qutip.rand_ket(size, density=1)


def matmul(left, right):
    return left.matmul(2, right)


@pytest.mark.nightly
def bench_matmul_QobjEvo_ket(benchmark, left_QobjEvo, right_ket):
    benchmark.group = "math:matmul:qobjevo-op-times-ket"

    result = benchmark(matmul, left_QobjEvo, right_ket)
