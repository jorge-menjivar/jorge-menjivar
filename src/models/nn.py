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
