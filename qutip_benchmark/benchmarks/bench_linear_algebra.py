"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip
import scipy
import numpy as np


# Available datatypes (using qutip_dense and qutip_csr to avoid confusion
# with density parameters)
@pytest.fixture(
    params=["numpy", "scipy_csr", "qutip_dense", "qutip_csr", "qutip_dia"]
)
def dtype(request):
    return request.param


@pytest.fixture(params=np.logspace(1, 9, 9, base=2, dtype=int).tolist())
def size(request):
    return request.param


@pytest.fixture(params=["dense", "sparse"])
def density(request):
    return request.param


@pytest.fixture()
def left_oper(size, density, dtype):
    """Return a random matrix of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a sparse matrix respectively.
    The matrices are Hermitian."""

    if density == "sparse":
        res = qutip.rand_herm(size, density=1 / size)
    elif density == "dense":
        res = qutip.rand_herm(size, density=1)

    if dtype == "numpy":
        return res.full()
    elif dtype == "scipy_csr":
        return scipy.sparse.csr_matrix(res.full())
    if dtype == "qutip_dense":
        return res.to("dense")
    if dtype == "qutip_csr":
        return res.to("csr")
    if dtype == "qutip_dia":
        return res.to("dia")
    raise Exception("The specified dtype is invalid")


@pytest.fixture()
def right_oper(size, density, dtype):
    """Return a random matrix of size `sizexsize'. Density is either 'dense'
    or 'sparse' and returns a fully dense or a sparse matrix respectively.
    The matrices are Hermitian."""

    if density == "sparse":
        res = qutip.rand_herm(size, density=1 / size)
    elif density == "dense":
        res = qutip.rand_herm(size, density=1)

    if dtype == "numpy":
        return res.full()
    elif dtype == "scipy_csr":
        return scipy.sparse.csr_matrix(res.full())
    if dtype == "qutip_dense":
        return res.to("dense")
    if dtype == "qutip_csr":
        return res.to("csr")
    if dtype == "qutip_dia":
        return res.to("dia")
    raise Exception("The specified dtype is invalid")


@pytest.fixture()
def right_ket(size, density, dtype):
    if density == "sparse":
        res = qutip.rand_ket(size, density=0.3)
    else:
        res = qutip.rand_ket(size, density=1)

    if dtype == "numpy":
        return res.full()
    if dtype == "scipy_csr":
        return scipy.sparse.csr_matrix(res.full())
    if dtype == "qutip_dense":
        return res.to("dense")
    if dtype == "qutip_csr":
        return res.to("csr")
    if dtype == "qutip_dia":
        return res.to("dia")
    raise Exception("The specified dtype is invalid")


def matmul(left, right):
    return left @ right


@pytest.mark.nightly
def bench_add(benchmark, left_oper, right_oper):
    benchmark.group = "math:add:op-plus-ket"

    # Operation to be benchmarked
    def add(left, right):
        return left + right

    # Run benchmark
    benchmark(add, left_oper, right_oper)


@pytest.mark.nightly
def bench_matmul_oper_oper(benchmark, left_oper, right_oper):
    benchmark.group = "math:matmul:op-times-op"

    # Benchmark operations
    benchmark(matmul, left_oper, right_oper)


@pytest.mark.nightly
def bench_matmul_oper_ket(benchmark, left_oper, right_ket):
    benchmark.group = "math:matmul:op-times-ket"

    # Run benchmark
    benchmark(matmul, left_oper, right_ket)
