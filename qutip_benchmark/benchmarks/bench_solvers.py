import pytest
import numpy as np
import qutip
from qutip.solver.mesolve import mesolve
from qutip.solver.mcsolve import mcsolve
from qutip.solver.steadystate import steadystate


@pytest.fixture(params=np.logspace(2, 7, 6, base=2, dtype=int).tolist())
def size(request):
    return request.param


@pytest.fixture(params=["Jaynes-Cummings", "Cavity", "Qubit Spin Chain"])
def model_solve(request):
    return request.param


@pytest.fixture(params=["Jaynes-Cummings", "Cavity"])
def model_steady(request):
    return request.param


# times
tlist = np.linspace(0, 20, 80)


def jc_setup(size):
    size = int(size / 2)

    # initial state
    psi0 = qutip.fock(size, 0) & (
        (qutip.basis(2, 0) + qutip.basis(2, 1)).unit()
    )

    wc = 1.0 * 2 * np.pi  # cavity frequency
    wa = 1.0 * 2 * np.pi  # atom frequency
    g = 0.25 * 2 * np.pi  # coupling strength

    kappa = 0.015  # cavity dissipation rate
    gamma = 0.15  # atom dissipation rate

    # Hamiltonian
    Ia = qutip.qeye(2)
    Ic = qutip.qeye(size, dtype="csr")

    a = qutip.destroy(size, dtype="csr")
    a_dag = qutip.create(size, dtype="csr")
    n = a_dag * a

    sm = qutip.sigmam()
    sp = qutip.sigmap()
    sz = qutip.sigmaz()

    H = wc * (n & Ia)
    H += Ic & (wa / 2.0 * sz)
    H += g * ((a_dag & sm) + (a & sp))

    # Collapse operators
    c_ops = []

    n_th = 0.0  # zero temperature

    c_ops = [
        (np.sqrt(kappa * (1 + n_th)) * a) & Ia,
        (np.sqrt(kappa * n_th) * a_dag) & Ia,
        Ic & (np.sqrt(gamma) * sm),
    ]

    return (H, psi0, c_ops, [n & Ia])


def cavity_setup(size):
    kappa = 1.0
    eta = 1.5
    wc = 1.8
    wl = 2.0
    delta_c = wl - wc
    alpha0 = 0.3 - 0.5j

    a = qutip.destroy(size)
    a_dag = qutip.create(size)
    n = a_dag * a

    H = delta_c * n + eta * (a + a_dag)
    c_ops = [np.sqrt(kappa) * a]

    psi0 = qutip.coherent(size, alpha0)
    return (H, psi0, c_ops, [n])


def qubit_setup(size):
    N = int(np.log2(size))

    # initial state
    state_list = [qutip.basis(2, 1)] + [qutip.basis(2, 0)] * (N - 1)
    psi0 = qutip.tensor(state_list)

    # Energy splitting term
    h = 2 * np.pi * np.ones(N)

    # Interaction coefficients
    Jx = 0.2 * np.pi * np.ones(N)
    Jy = 0.2 * np.pi * np.ones(N)
    Jz = 0.2 * np.pi * np.ones(N)

    # Setup operators for individual qubits
    sx_list, sy_list, sz_list = [], [], []
    for i in range(N):
        op_list = [qutip.qeye(2)] * N
        op_list[i] = qutip.sigmax()
        sx_list.append(qutip.tensor(op_list))
        op_list[i] = qutip.sigmay()
        sy_list.append(qutip.tensor(op_list))
        op_list[i] = qutip.sigmaz()
        sz_list.append(qutip.tensor(op_list))

    # Hamiltonian - Energy splitting terms
    H = 0
    for i in range(N):
        H -= 0.5 * h[i] * sz_list[i]

    # Interaction terms
    for n in range(N - 1):
        H += -0.5 * Jx[n] * sx_list[n] * sx_list[n + 1]
        H += -0.5 * Jy[n] * sy_list[n] * sy_list[n + 1]
        H += -0.5 * Jz[n] * sz_list[n] * sz_list[n + 1]

    # dephasing rate
    gamma = 0.02 * np.ones(N)

    # collapse operators
    c_ops = [np.sqrt(gamma[i]) * sz_list[i] for i in range(N)]

    return (H, psi0, c_ops, [])


@pytest.mark.nightly
def bench_mesolve(benchmark, model_solve, size):
    benchmark.group = "solvers:master-equation"

    if model_solve == "Cavity":
        H, psi0, c_ops, e_ops = cavity_setup(size)
    elif model_solve == "Jaynes-Cummings":
        H, psi0, c_ops, e_ops = jc_setup(size)
    elif model_solve == "Qubit Spin Chain":
        H, psi0, c_ops, e_ops = qubit_setup(size)

    result = benchmark(mesolve, H, psi0, tlist, c_ops, e_ops)


def bench_mcsolve(benchmark, model_solve, size):
    benchmark.group = "solvers:monte-carlo"

    if model_solve == "Cavity":
        H, psi0, c_ops, e_ops = cavity_setup(size)
    elif model_solve == "Jaynes-Cummings":
        H, psi0, c_ops, e_ops = jc_setup(size)
    elif model_solve == "Qubit Spin Chain":
        H, psi0, c_ops, e_ops = qubit_setup(size)

    result = benchmark(mcsolve, H, psi0, tlist, c_ops, e_ops, ntraj=1)


@pytest.mark.nightly
def bench_steadystate(benchmark, model_steady, size):
    benchmark.group = "solvers:steadystate"

    if model_steady == "Cavity":
        H, _, c_ops, _ = cavity_setup(size)
        # Steadystate is bad with Dia.
        H = H.to("csr")
        c_ops = [c_ops[0].to("csr")]

    elif model_steady == "Jaynes-Cummings":
        H, _, c_ops, _ = jc_setup(size)

    result = benchmark(steadystate, H, c_ops)
