from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Function to create teleportation circuit
def teleportation_circuit(theta, phi, basis):

    # 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Step 1: Prepare Alice's original quantum state
    qc.ry(theta, 0)
    qc.rz(phi, 0)

    # Step 2: Create Bell pair between Alice and Bob
    qc.h(1)
    qc.cx(1, 2)

    # Step 3: Alice performs Bell-state measurement
    qc.cx(0, 1)
    qc.h(0)

    # Step 4: Measure Alice's qubits
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Step 5: Bob applies corrections

    # X correction
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)

    # Z correction
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(2)

    # Step 6: Choose Bob's measurement basis
    if basis == "X":
        qc.h(2)

    elif basis == "Y":
        qc.sdg(2)
        qc.h(2)

    # Step 7: Measure Bob's qubit separately
    qc.measure(2, 2)

    return qc


# Prepare arbitrary quantum state
theta = np.pi / 3
phi = np.pi / 4

# Initialize simulator
simulator = AerSimulator()

# Test all three measurement bases
for basis in ["X", "Y", "Z"]:

    qc = teleportation_circuit(theta, phi, basis)

    compiled = transpile(qc, simulator)

    result = simulator.run(
        compiled,
        shots=2048
    ).result()

    counts = result.get_counts()

    # Bob's result is the leftmost bit (c2)
    bob_ones = sum(
        count for outcome, count in counts.items()
        if outcome.replace(" ", "")[0] == "1"
    )

    probability = bob_ones / 2048

    print(f"\nMeasurement basis: {basis}")
    print("Results:", counts)
    print("Probability of Bob measuring 1:", probability)

    # Display circuit
    if basis == "Z":
        print("\nQuantum Circuit:")
        print(qc.draw())