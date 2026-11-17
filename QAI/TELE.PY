from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(3, 3)

qc.x(0)
qc.h(1)

qc.cx(1, 2)
qc.cx(0, 1)

qc.h(0)
qc.measure([0, 1], [0, 1])

qc.cx(1, 2)
qc.cz(0, 2)

qc.measure(2, 2)

simulator = AerSimulator()
counts = simulator.run(qc).result().get_counts()

print("Teleportation Outcomes (Bit string format: q2 q1 q0):")
print(counts)

import matplotlib.pyplot as plt
plt.bar(counts.keys(), counts.values())