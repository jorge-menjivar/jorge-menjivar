from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class QuantumProperties(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    quantum_state_vector: Any
    probability_distribution: dict[str, float]
    entanglement_measure: float
    quantum_coherence: float
    superposition_states: int = Field(
        description="Number of states in the superposition",
        default=0,
    )

    @field_serializer("quantum_state_vector")
    def serialize_quantum_state_vector(self, quantum_state_vector: Any) -> str:
        return "Statevector"


class CircuitInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str
    qubits: int
    depth: int
    gates: dict[str, int] = Field(description="The gates used in the quantum circuit")
    timestamp: str = Field(description="The timestamp of the quantum circuit")


class StateAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    state: str = Field(description="The state of the quantum circuit")
    probability: float = Field(description="The probability of the state")


class NeuralInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    consciousness_level: float = Field(
        description="The consciousness level of the quantum circuit"
    )
    creativity_index: float = Field(
        description="The creativity index of the quantum circuit"
    )
    innovation_potential: float = Field(
        description="The innovation potential of the quantum circuit"
    )
    problem_solving_capability: str = Field(
        description="The problem solving capability of the quantum circuit"
    )


class QuantumCircuitReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    circuit_info: CircuitInfo
    quantum_properties: QuantumProperties
    state_analysis: list[StateAnalysis]
    neural_interpretation: NeuralInterpretation
    circuit_ascii: str


class QuantumSimulationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    counts: dict[str, int]
    probabilities: dict[str, float]
    probabilities_vector: list[float]
    entropy: float
    max_prob: float
    dominant_state: int
