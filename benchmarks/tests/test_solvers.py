import pytest
import numpy as np
import qutip
from qutip.solver.mesolve import mesolve
from qutip.solve.mcsolve import mcsolve
from qutip.solve.steadystate import steadystate


@pytest.fixture(params=np.logspace(2, 8, 7, base=2, dtype=int).tolist())
def dimension(request): return request.param


@pytest.fixture(params=["Jaynes-Cummings", "Cavity", "Qubit Spin Chain"])
def model_solve(request): return request.param


@pytest.fixture(params=["Jaynes-Cummings", "Cavity"])
def model_steady(request): return request.param


def jc_setup(dimension):
    dimension = int(dimension/2)

    # initial state
    psi0 = qutip.fock(dimension, 0) & ((qutip.basis(2, 0) +
                                        qutip.basis(2, 1)).unit())

    wc = 1.0 * 2 * np.pi   # cavity frequency
    wa = 1.0 * 2 * np.pi   # atom frequency
    g = 0.25 * 2 * np.pi  # coupling strength

    kappa = 0.015       # cavity dissipation rate
    gamma = 0.15        # atom dissipation rate

    tlist = np.linspace(0, 25, 100)

    # Hamiltonian
    Ia = qutip.qeye(2)
    Ic = qutip.qeye(dimension)

    a = qutip.destroy(dimension)
    a_dag = qutip.create(dimension)
    n = a_dag * a

    sm = qutip.sigmam()
    sp = qutip.sigmap()
    sz = qutip.sigmaz()

    H = (wc * (n & Ia))
    H += (Ic & (wa / 2. * sz))
    H += (g * ((a_dag & sm) + (a & sp)))

    # Collapse operators
    c_ops = []

    n_th = 0.0  # zero temperature

    c_ops = [
        (np.sqrt(kappa*(1+n_th)) * a) & Ia,
        (np.sqrt(kappa*n_th) * a_dag) & Ia,
        Ic & (np.sqrt(gamma) * sm),
    ]

    return (H, psi0, tlist, c_ops, [n & Ia])


def cavity_setup(dimension):
    kappa = 1.
    eta = 1.5
    wc = 1.8
    wl = 2.
    delta_c = wl - wc
    alpha0 = 0.3 - 0.5j
    tlist = np.linspace(0, 10, 200)

    a = qutip.destroy(dimension)
    a_dag = qutip.create(dimension)
    n = a_dag * a

    H = delta_c * n + eta * (a + a_dag)
    c_ops = [np.sqrt(kappa) * a]

    psi0 = qutip.coherent(dimension, alpha0)
    return (H, psi0, tlist, c_ops, [n])


def qubit_setup(dimension):
    N = int(np.log2(dimension))

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

    # times
    tlist = np.linspace(0, 100, 200)

    return (H, psi0, tlist, c_ops, [])


@pytest.mark.nightly
def test_mesolve(benchmark, model_solve, dimension, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "mesolve-" + group
    benchmark.group = group

    if (model_solve == 'Cavity'):
        H, psi0, tspan, c_ops, e_ops = cavity_setup(dimension)
    elif (model_solve == 'Jaynes-Cummings'):
        H, psi0, tspan, c_ops, e_ops = jc_setup(dimension)
    elif (model_solve == 'Qubit Spin Chain'):
        H, psi0, tspan, c_ops, e_ops = qubit_setup(dimension)

    result = benchmark(mesolve, H, psi0, tspan, c_ops, e_ops)
    return result


def test_mcsolve(benchmark, model_solve, dimension, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "mcsolve-" + group
    benchmark.group = group

    if (model_solve == 'Cavity'):
        H, psi0, tspan, c_ops, e_ops = cavity_setup(dimension)
    elif (model_solve == 'Jaynes-Cummings'):
        H, psi0, tspan, c_ops, e_ops = jc_setup(dimension)
    elif (model_solve == 'Qubit Spin Chain'):
        H, psi0, tspan, c_ops, e_ops = qubit_setup(dimension)

    result = benchmark(mcsolve, H, psi0, tspan, c_ops, e_ops)
    return result


@pytest.mark.nightly
def test_steadystate(benchmark, model_steady, dimension, request):
    # Group benchmark by operation, density and size.
    group = request.node.callspec.id
    group = "steadystate-" + group
    benchmark.group = group

    if (model_steady == 'Cavity'):
        H, _, _, c_ops, _ = cavity_setup(dimension)
        result = benchmark(steadystate, H, c_ops)

    elif (model_steady == 'Jaynes-Cummings'):
        H, _, _, c_ops, _ = jc_setup(dimension)
        result = benchmark(steadystate, H, c_ops)

    return result
