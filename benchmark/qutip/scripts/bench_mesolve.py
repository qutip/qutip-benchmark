import pytest
import numpy as np
from qutip import mesolve, basis, sigmax, sigmaz

@pytest.mark.solvers
def bench_mesolve(benchmark):
    benchmark.group = "solvers:mesolve"

    delta = np.pi
    g = 0.2

    H = delta/2.0 * sigmax()
    c_ops = [np.sqrt(g) * sigmaz()]

    psi0 = basis(2, 0)
    tlist = np.linspace(0, 10, 100)

    benchmark(mesolve, H, psi0, tlist, c_ops, e_ops=[sigmaz()])
