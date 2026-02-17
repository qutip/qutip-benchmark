import pytest
pytest.importorskip("qutip_qip")
from qutip import basis, tensor
from qutip_qip.circuit import QubitCircuit


def zero_state(n_qubits):
    return tensor([basis(2, 0) for _ in range(n_qubits)])


def ghz_circuit(n_qubits):
    qc = QubitCircuit(n_qubits)
    qc.add_gate("SNOT", targets=[0])
    for i in range(n_qubits - 1):
        qc.add_gate("CNOT", controls=[i], targets=[i + 1])
    return qc


@pytest.mark.qip
@pytest.mark.parametrize("n_qubits", [3, 4, 5, 6, 7])
def bench_qip_ghz_scaling(benchmark, n_qubits):
    benchmark.group = "qip:ghz_scaling"

    qc = ghz_circuit(n_qubits)
    state = zero_state(n_qubits)

    benchmark(qc.run, state)

