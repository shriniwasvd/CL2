from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create circuit with 5 qubits and 5 classical bits
qc = QuantumCircuit(5, 5)

# Step 1: Encode logical qubit |0>
qc.cx(0, 1)
qc.cx(0, 2)

# Step 2: Introduce bit-flip error on q1
qc.x(1)

# Step 3: Detect errors using syndrome qubits
qc.cx(0, 3)
qc.cx(1, 3)

qc.cx(1, 4)
qc.cx(2, 4)

# Step 4: Measure syndrome qubits
qc.measure(3, 3)
qc.measure(4, 4)

qc.barrier()

# Step 5: Correct the detected error

# Error on q0: syndrome 10
with qc.if_test((qc.clbits[3], 1)):
    with qc.if_test((qc.clbits[4], 0)):
        qc.x(0)

# Error on q1: syndrome 11
with qc.if_test((qc.clbits[3], 1)):
    with qc.if_test((qc.clbits[4], 1)):
        qc.x(1)

# Error on q2: syndrome 01
with qc.if_test((qc.clbits[3], 0)):
    with qc.if_test((qc.clbits[4], 1)):
        qc.x(2)

# Step 6: Measure corrected data qubits
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)

# Step 7: Simulate
simulator = AerSimulator()

compiled = transpile(qc, simulator)

result = simulator.run(
    compiled,
    shots=1000
).result()

counts = result.get_counts()

# Step 8: Display results
print("Quantum Error Correction Results:")
print(counts)

print("\nQuantum Circuit:")
print(qc.draw())