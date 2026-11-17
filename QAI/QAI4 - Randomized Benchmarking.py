
import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_experiments.library import StandardRB


# Step 1: Create quantum noise model

noise = NoiseModel()

error = depolarizing_error(0.005, 1)

noise.add_all_qubit_quantum_error(
    error, ["sx", "x"]
)

simulator = AerSimulator(noise_model=noise)


# Step 2: Define RB parameters

lengths = [1, 2, 4, 8, 16, 32, 64]

num_samples = 20
seed = 42


# Step 3: Create RB experiment

experiment = StandardRB(
    physical_qubits=(0,),
    lengths=lengths,
    num_samples=num_samples,
    seed=seed
)


# Step 4: Run experiment

data = experiment.run(
    simulator,
    shots=1024
)

data.block_for_results()


# Step 5: Display experiment data

print("\nRANDOMIZED BENCHMARKING RESULTS")

print(data)


# Step 6: Plot benchmarking curve

data.figure(0)
plt.show()


# Step 7: Display example RB circuit

print("\nEXAMPLE RB CIRCUIT")

print(experiment.circuits()[0].draw())
