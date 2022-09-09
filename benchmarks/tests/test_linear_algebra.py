"""This file contains the benchmarks that are run the benchmark.py script."""
import pytest
import qutip
import scipy
import numpy as np


# Available datatypes (using qutip_dense and qutip_csr to avoid confusion
# with density parameters)
@pytest.fixture(params=["numpy", "scipy_csr", "qutip_dense", "qutip_csr"])
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
    raise Exception("The specified dtype is invalid")


def matmul(left, right):
    return left @ right


@pytest.mark.nightly
def test_add(benchmark, left_oper, right_oper, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Add-" + group
    benchmark.group = group

    # Operation to be benchmarked
    def add(left, right):
        return left + right

    # Run benchmark
    result = benchmark(add, left_oper, right_oper)

    return result


@pytest.mark.nightly
def test_matmul_oper_oper(benchmark, left_oper, right_oper, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Matmul_op@op-" + group
    benchmark.group = group

    # Benchmark operations
    result = benchmark(matmul, left_oper, right_oper)

    return result


@pytest.mark.nightly
def test_matmul_oper_ket(benchmark, left_oper, right_ket, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "Matmul_op@ket-" + group
    benchmark.group = group

    # Run benchmark
    result = benchmark(matmul, left_oper, right_ket)

    return result
