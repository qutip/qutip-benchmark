import pytest
import numpy as np
from qutip import tensor, basis


@pytest.fixture(params=[5, 10, 20])
def n_qubits(request):
    return request.param


@pytest.fixture(params=[2, 5, 10, 50])
def depth(request):
    return request.param


@pytest.fixture(params=["Dense", "jax", "CuState"])
def backend(request):
    name = request.param
    if name == "jax":
        pytest.importorskip("qutip_jax", reason="qutip-jax not installed")
    elif name == "CuState":
        pytest.importorskip("qutip_cuquantum", reason="qutip-cuquantum not installed")
    return name


def _build_circuit(n_qubits, depth):
    from qutip_qip.circuit import QubitCircuit

    rng = np.random.default_rng(seed=42)
    qc = QubitCircuit(n_qubits)
    for _ in range(depth):
        for q in range(n_qubits):
            qc.add_gate("RX", targets=q, arg_value=rng.uniform(0, 2 * np.pi))
        for q in range(n_qubits - 1):
            qc.add_gate("CNOT", controls=q, targets=q + 1)
    return qc


@pytest.mark.qip
def bench_circuit_sv(benchmark, n_qubits, depth, backend):
    """State-vector simulation across backends, qubit counts, and depths."""
    from qutip_qip.circuit import CircuitSimulator

    qc = _build_circuit(n_qubits, depth)
    state = tensor([basis(2, 0)] * n_qubits).to(backend)
    sim = CircuitSimulator(qc, mode="state_vector_simulator")

    # Run once beforehand to trigger JIT compilation for JAX/CuState
    CircuitSimulator(qc, mode="state_vector_simulator").run(state)

    benchmark.group = f"circuit:sv:{n_qubits}q"
    benchmark.extra_info["total_gates"] = depth * (2 * n_qubits - 1)
    benchmark.extra_info["backend"] = backend
    benchmark.extra_info["n_qubits"] = n_qubits
    benchmark.extra_info["depth"] = depth

    benchmark(sim.run, state)
