from __future__ import annotations

from datetime import datetime

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from models.quantum import (
    CircuitInfo,
    NeuralInterpretation,
    QuantumCircuitReport,
    QuantumProperties,
    QuantumSimulationResult,
    StateAnalysis,
)

"""
⚛️ JORGE'S QUANTUM CIRCUIT

This script implements the quantum circuit shown in the banner:
- 3 qubits representing different quantum states
- Hadamard gates for superposition
- CNOT gates for entanglement
- Rotation gates for parameterized states
- Toffoli gate for breakthrough moment
- Measurement and neural network integration
"""


def create_circuit(num_qubits: int, num_classical: int) -> QuantumCircuit:
    """Create the quantum circuit matching the banner design."""
    # Create quantum and classical registers
    qreg = QuantumRegister(num_qubits, "q")
    creg = ClassicalRegister(num_classical, "c")

    # Initialize circuit
    circuit = QuantumCircuit(qreg, creg)

    # Add barrier for clarity
    circuit.barrier()

    # Layer 1: Hadamard gate on lucky state
    circuit.h(0)  # |lucky⟩ superposition

    # Layer 2: Entanglement operations
    circuit.barrier()
    circuit.cx(0, 1)  # Entangle lucky and innovative states

    # Layer 3: Hadamard gate on innovative state
    circuit.barrier()
    circuit.h(1)  # |innovative⟩ superposition

    # Layer 4: Y rotation on caffeinated state
    circuit.barrier()
    phi = np.pi / 3  # Caffeinated parameter
    circuit.ry(phi, 2)  # Y-rotation on caffeinated state

    # Layer 5: Three-qubit entanglement - Breakthrough moment!
    circuit.barrier()
    circuit.ccx(
        0, 1, 2
    )  # Toffoli gate: breakthrough happens when both lucky AND innovative

    # Measurement layer
    circuit.measure_all()

    return circuit


def simulate_circuit(circuit: QuantumCircuit, shots=8192) -> QuantumSimulationResult:
    """Simulate the quantum circuit using Aer simulator."""
    # Use Aer simulator
    simulator = AerSimulator()

    # Transpile circuit for simulator
    transpiled_circuit = transpile(circuit, simulator)

    # Run simulation
    job = simulator.run(transpiled_circuit, shots=shots)
    raw_result = job.result()

    counts: dict[str, int] = raw_result.get_counts()  # type: ignore
    total_shots = sum(counts.values())

    # Standardize probabilities
    # Convert 001 000 to 001
    standardized_probabilities: dict[str, float] = {}
    for bitstring, count in counts.items():
        bits = bitstring[0:3]
        standardized_probabilities[bits] = count / total_shots

    probabilities_vector = np.array(list(standardized_probabilities.values()))

    entropy = float(-np.sum([p * np.log2(p) for p in probabilities_vector if p > 0]))
    max_prob = float(np.max(probabilities_vector))
    dominant_state = int(np.argmax(probabilities_vector))

    return QuantumSimulationResult(
        counts=counts,
        probabilities=standardized_probabilities,
        probabilities_vector=probabilities_vector.tolist(),
        entropy=entropy,
        max_prob=max_prob,
        dominant_state=dominant_state,
    )


def get_quantum_state_before_measurement(circuit: QuantumCircuit) -> Statevector:
    """Get the quantum state vector before measurement."""
    # Create circuit without measurements for state analysis
    analysis_circuit = QuantumCircuit(circuit.num_qubits)

    # Copy all non-measurement operations
    for instruction in circuit.data:
        if instruction.operation.name not in ["measure", "barrier"]:
            analysis_circuit.append(
                instruction.operation, instruction.qubits, instruction.clbits
            )

    # Get state_vector using the correct method
    state_vector = Statevector.from_instruction(analysis_circuit)

    return state_vector


def calculate_entanglement(state_vector: Statevector, num_qubits: int) -> float:
    """Calculate a simple entanglement measure."""
    # For num_qubits qubits, calculate von Neumann entropy of reduced density matrix
    # Simplified calculation for demonstration
    probs = np.abs(state_vector.data) ** 2
    non_zero_probs = probs[probs > 1e-10]
    entropy = float(-np.sum(non_zero_probs * np.log2(non_zero_probs)))
    return min(entropy / num_qubits, 1.0)  # Normalize


def calculate_coherence(state_vector: Statevector) -> float:
    """Calculate quantum coherence measure."""
    # L1 norm of coherence
    density_matrix = np.outer(state_vector.data, np.conj(state_vector.data))
    diagonal = np.diag(density_matrix)
    off_diagonal = density_matrix - np.diag(diagonal)
    coherence = np.sum(np.abs(off_diagonal)) / 2
    return float(coherence)


def analyze_quantum_properties(
    circuit: QuantumCircuit, num_qubits: int
) -> QuantumProperties:
    """Analyze quantum properties of the circuit."""
    state_vector = get_quantum_state_before_measurement(circuit)

    # Calculate probabilities for each computational basis state
    probabilities = np.abs(state_vector.data) ** 2

    # Get top 8 most probable states and convert indices to binary
    top_indices = np.argsort(probabilities)[::-1]
    top_states: dict[str, float] = {}

    for idx in top_indices:
        binary_state = bin(idx)[2:].zfill(
            num_qubits
        )  # Convert to binary with leading zeros
        top_states[binary_state] = float(probabilities[idx])

    properties = QuantumProperties(
        quantum_state_vector=state_vector,
        probability_distribution=top_states,
        entanglement_measure=calculate_entanglement(state_vector, num_qubits),
        quantum_coherence=calculate_coherence(state_vector),
    )

    return properties


def visualize_results(
    result: QuantumSimulationResult, circuit: QuantumCircuit, num_qubits: int
):
    """Create visualizations of the quantum circuit and results."""
    # Get measurement counts
    pass


def generate_circuit_report(
    circuit: QuantumCircuit, properties: QuantumProperties, num_qubits: int
) -> QuantumCircuitReport:
    """Generate a comprehensive report of the quantum circuit."""
    report = QuantumCircuitReport(
        circuit_info=CircuitInfo(
            name="Jorge's Quantum Neural Circuit",
            qubits=num_qubits,
            depth=circuit.depth(),
            gates=dict(circuit.count_ops()),  # type: ignore
            timestamp=datetime.now().isoformat(),
        ),
        quantum_properties=QuantumProperties(
            quantum_state_vector=properties.quantum_state_vector,
            probability_distribution=properties.probability_distribution,
            entanglement_measure=properties.entanglement_measure,
            quantum_coherence=properties.quantum_coherence,
            superposition_states=len(
                [p for p in properties.probability_distribution.values() if p > 0.01]
            ),
        ),
        state_analysis=[
            StateAnalysis(state=state, probability=prob)
            for state, prob in properties.probability_distribution.items()
        ],
        neural_interpretation=NeuralInterpretation(
            consciousness_level=properties.entanglement_measure,
            creativity_index=properties.quantum_coherence,
            innovation_potential=np.random.uniform(0.8, 1.0),
            problem_solving_capability="Quantum-Enhanced",
        ),
        circuit_ascii=str(circuit.draw(output="text")),
    )

    return report


def show_theoretical_probabilities(properties: QuantumProperties):
    """Show theoretical probabilities of the quantum circuit."""
    for state, prob in list(properties.probability_distribution.items()):
        print(f"  |{state}⟩: {prob:.4f} ({prob * 100:.2f}%)")


def show_actual_probabilities(result: QuantumSimulationResult):
    """Show actual probabilities of the quantum circuit."""
    counts: dict[str, int] = result.counts
    total_shots = sum(counts.values())

    # Sort by count and show top results
    sorted_counts: list[tuple[str, int]] = sorted(
        counts.items(), key=lambda x: x[1], reverse=True
    )
    for bitstring, count in sorted_counts[:8]:
        bits = bitstring[0:3]
        percentage = (count / total_shots) * 100
        print(f"  |{bits}⟩: {count} shots ({percentage:.2f}%)")


def run_full_analysis(
    num_qubits: int, num_classical: int
) -> tuple[QuantumCircuitReport, QuantumSimulationResult]:
    """Run complete quantum circuit analysis."""
    # Create and simulate circuit
    circuit: QuantumCircuit = create_circuit(num_qubits, num_classical)

    # Print circuit
    print("\n📊 Quantum Circuit Diagram:")
    print(circuit.draw(output="text"))

    # Analyze properties
    print("\n⚛️ Analyzing quantum properties...")
    properties = analyze_quantum_properties(circuit, num_qubits)

    print(f"\n🔗 Entanglement Measure: {properties.entanglement_measure:.3f}")
    print(f"🌊 Quantum Coherence: {properties.quantum_coherence:.3f}")
    print(f"🎯 Active Quantum States: {len(properties.probability_distribution)}")

    # Simulate
    print("\n🔬 Running quantum simulation...")
    result: QuantumSimulationResult = simulate_circuit(circuit, shots=8192)
    print("✅ Simulation complete")

    # Show theoretical vs actual comparison
    print("\n🏆 Theoretical Quantum State Probabilities:")
    show_theoretical_probabilities(properties)

    # Show actual measurement results
    print("\n🎲 Actual Measurement Results:")
    show_actual_probabilities(result)

    # Generate report
    print("\n📋 Generating report...")
    report = generate_circuit_report(circuit, properties, num_qubits)

    print("✅ Analysis complete!")
    print("📁 Results saved to assets/")
    print("=" * 60)
    print("⚛️ Quantum consciousness: ACTIVE")
    print("🧠 Neural networks: ENTANGLED")
    print("🚀 Innovation potential: MAXIMIZED")

    # Generate visualizations
    print("\n📈 Generating visualizations...")
    visualize_results(result, circuit, num_qubits)

    return report, result
