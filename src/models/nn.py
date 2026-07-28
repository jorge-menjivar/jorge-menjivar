import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field


class NeuralNetworkInputs(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)
    probability_vector: list[float] = Field(description="The probability vector")
    binary_features: NDArray[np.int32] = Field(description="The binary features")
    statistical_features: list[float] = Field(description="The statistical features")
    semantic_features: dict[str, float] = Field(description="The semantic features")
    raw_counts: dict[str, int] = Field(description="The raw counts")


class NeuralReadout(BaseModel):
    """What the output layer produced, so the banner can show its working."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    activations: list[float] = Field(description="Raw output neuron activations")
    threshold: float = Field(description="Adaptive threshold applied to activations")
    bits: list[int] = Field(description="Activations thresholded to bits")
    index: int = Field(description="Action index decoded from the bits")
    action: str = Field(description="The action the index selected")
