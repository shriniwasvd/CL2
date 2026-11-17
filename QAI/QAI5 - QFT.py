
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


# Step 1: Define QFT function

def qft_circuit(n):
    circuit = QuantumCircuit(n)

    for j in range(n):
        circuit.h(j)

        for k in range(j + 1, n):
            angle = np.pi / (2 ** (k - j))
            circuit.cp(angle, k, j)

    # Reverse qubit order
    for i in range(n // 2):
        circuit.swap(i, n - i - 1)

    return circuit


# Step 2: Create 5-qubit circuit

qc = QuantumCircuit(5, 5)


# Step 3: Prepare input state |10101>

qc.x(0)
qc.x(2)
qc.x(4)


# Step 4: Apply QFT

qc.compose(qft_circuit(5), inplace=True)


# Step 5: Measure qubits

qc.measure(range(5), range(5))


# Step 6: Display circuit

print("QUANTUM FOURIER TRANSFORM CIRCUIT")
print(qc.draw())


# Step 7: Simulate circuit

simulator = AerSimulator()

compiled = transpile(qc, simulator)

simulation = simulator.run(
    compiled,
    shots=4096
).result()

counts = simulation.get_counts()


# Step 8: Display measurement results

print("\nMEASUREMENT RESULTS")
print(counts)


# Step 9: Plot histogram

plot_histogram(counts)
plt.title("5-Qubit Quantum Fourier Transform")
plt.show()
