from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a 16-qubit circuit
n = 16
qc = QuantumCircuit(n, n)

# Apply Hadamard to all qubits
qc.h(range(n))

# Measure all qubits
qc.measure(range(n), range(n))

# Simulate
simulator = AerSimulator()
compiled = transpile(qc, simulator)

result = simulator.run(
    compiled,
    shots=1000
).result()

counts = result.get_counts()

# Display results
print("Random numbers generated:")

for number, frequency in counts.items():
    print(number, ":", frequency)

# Plot histogram
plot_histogram(counts)
plt.show()
