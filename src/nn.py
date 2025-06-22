from __future__ import annotations

import time
from typing import TYPE_CHECKING

import numpy as np

from constants import STATE_LIST

if TYPE_CHECKING:
    from models.quantum import QuantumSimulationResult


class SimpleNeuralNetwork:
    """A simple neural network.

    Architecture: 8→8→7→4
    """

    def __init__(
        self,
        input_size: int = 8,
        hidden1_size: int = 8,
        hidden2_size: int = 7,
        output_size: int = 4,
    ):
        """Initialize the neural network with random weights.

        Parameters
        ----------
        input_size : int
            Number of input neurons, by default 8
        hidden1_size : int
            Number of first hidden layer neurons, by default 8
        hidden2_size : int
            Number of second hidden layer neurons, by default 7
        output_size : int
            Number of output neurons, by default 4
        """
        self.input_size = input_size
        self.hidden1_size = hidden1_size
        self.hidden2_size = hidden2_size
        self.output_size = output_size

        # Use current time for more randomness
        np.random.seed(int(time.time() * 1000) % 2**32)

        # Initialize weights with more variation for 4-layer architecture
        # Layer 1: Input → Hidden1 (8 → 8)
        self.weights_input_hidden1 = np.random.randn(input_size, hidden1_size) * 0.7
        self.bias_hidden1 = np.random.randn(hidden1_size) * 0.15

        # Layer 2: Hidden1 → Hidden2 (8 → 7)
        self.weights_hidden1_hidden2 = np.random.randn(hidden1_size, hidden2_size) * 0.7
        self.bias_hidden2 = np.random.randn(hidden2_size) * 0.15

        # Layer 3: Hidden2 → Output (7 → 4)
        self.weights_hidden2_output = np.random.randn(hidden2_size, output_size) * 0.7
        self.bias_output = np.random.randn(output_size) * 0.15

        # Add some dynamic noise weights that change with each prediction
        self.noise_scale = 0.08

    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip to prevent overflow

    def tanh_activation(self, x: np.ndarray) -> np.ndarray:
        """Tanh activation function for more dynamic range."""
        return np.tanh(x)

    def relu_activation(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation function for better gradient flow."""
        return np.maximum(0, x)

    def forward(self, inputs: np.ndarray, add_noise: bool = True) -> np.ndarray:
        """Forward pass through the 4-layer network: 8→8→7→4.

        Parameters
        ----------
        inputs : np.ndarray
            Input vector of size 8
        add_noise : bool
            Whether to add dynamic noise for variation

        Returns
        -------
        np.ndarray
            Output vector of size 4 with values between 0 and 1
        """
        # Ensure input is the right shape
        if inputs.shape[0] != self.input_size:
            if len(inputs) > self.input_size:
                inputs = inputs[: self.input_size]  # Truncate if too long
            else:
                # Pad with zeros if too short
                padded = np.zeros(self.input_size)
                padded[: len(inputs)] = inputs
                inputs = padded

        # Scale inputs to make network more sensitive to small differences
        scaled_inputs = inputs * 8.0

        # Add slight input-dependent noise for variation
        if add_noise:
            input_hash = np.sum(inputs * np.arange(len(inputs))) % 1000
            np.random.seed(int(input_hash))
            noise = np.random.randn(*scaled_inputs.shape) * self.noise_scale
            scaled_inputs += noise

        # Layer 1: Input → Hidden1 (8 → 8)
        hidden1_input = (
            np.dot(scaled_inputs, self.weights_input_hidden1) + self.bias_hidden1
        )
        hidden1_output = self.tanh_activation(hidden1_input)

        # Layer 2: Hidden1 → Hidden2 (8 → 7)
        hidden2_input = (
            np.dot(hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden2
        )
        hidden2_output = self.relu_activation(hidden2_input)

        # Layer 3: Hidden2 → Output (7 → 4)
        output_input = (
            np.dot(hidden2_output, self.weights_hidden2_output) + self.bias_output
        )
        output = self.sigmoid(output_input)

        return output

    def predict_bits(self, inputs: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predict binary outputs from inputs.

        Parameters
        ----------
        inputs : np.ndarray
            Input vector
        threshold : float
            Threshold for converting to binary, by default 0.5

        Returns
        -------
        np.ndarray
            4-bit binary output
        """
        output = self.forward(inputs)

        # Use adaptive thresholding based on the output distribution
        mean_output = float(np.mean(output))
        adaptive_threshold = max(0.3, min(0.7, mean_output))

        print(f"🎯 Network output values: {output}")
        print(f"🎯 Adaptive threshold: {adaptive_threshold:.3f}")

        return (output > adaptive_threshold).astype(int)

    def bits_to_action_index(self, bits: np.ndarray) -> int:
        """Convert 4-bit binary to action index.

        Parameters
        ----------
        bits : np.ndarray
            4-bit binary array

        Returns
        -------
        int
            Index corresponding to the binary representation
        """
        return int(np.dot(bits, [8, 4, 2, 1]))  # Convert binary to decimal


def create_dynamic_neural_network() -> SimpleNeuralNetwork:
    """Create a new neural network instance with time-based randomness."""
    return SimpleNeuralNetwork()


def infer_current_action(result: QuantumSimulationResult) -> str:
    """Infer the action from the quantum simulation measurements.

    Parameters
    ----------
    result : QuantumSimulationResult
        The quantum simulation result containing probabilities

    Returns
    -------
    str
        The predicted action as a string
    """
    # Create a fresh neural network for each inference (more dynamic)
    neural_network = create_dynamic_neural_network()

    # Convert to neural network inputs
    print("\n🧠 Converting to Neural Network Inputs...")
    dense_input = np.array(result.probabilities_vector)

    # Add some quantum-inspired randomness based on entropy
    quantum_noise = result.entropy * 0.1 * np.random.randn(len(dense_input))
    augmented_input = dense_input + quantum_noise

    print(f"🔮 Input probabilities: {dense_input}")
    print(f"🌊 Quantum entropy: {result.entropy:.3f}")
    print(f"🎲 Augmented input: {augmented_input}")

    # Get neural network prediction
    print("🔮 Running Neural Network Inference...")
    bits = neural_network.predict_bits(augmented_input)
    action_index = neural_network.bits_to_action_index(bits)

    # Ensure index is within bounds
    action_index = action_index % len(STATE_LIST)

    predicted_action = STATE_LIST[action_index]

    print(
        f"""\
📊 Neural Network Output: {bits} -> Index: {action_index} -> Action: {predicted_action}
"""
    )

    return predicted_action
