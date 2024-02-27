from abc import ABC, abstractmethod
import numpy as np


class MCDMBase(ABC):
    def __init__(self):
        self.preferences = None
        self.ranking = None

    def __call__(self, decision_matrix, weights, types):
        self.decision_matrix = decision_matrix
        self.weights = weights
        self.types = types
        self._validate_input()
        self._calculate()

    @abstractmethod
    def _calculate(self):
        NotImplementedError("Subclasses must implement this method")

    def get_ranking(self):
        return self.ranking

    def get_preferences(self):
        return self.preferences

    def _validate_input(self):
        self.decision_matrix = np.asarray(self.decision_matrix)
        self.weights = np.asarray(self.weights)
        self.types = np.asarray(self.types)

        if self.decision_matrix.ndim != 2:
            raise ValueError(
                f"Decision matrix must be a 2D array\nGot: {self.decision_matrix.ndim}D array"
            )
        if self.weights.ndim != 1:
            raise ValueError(
                f"Weights must be a 1D array\nGot: {self.weights.ndim}D array"
            )
        if self.types.ndim != 1:
            raise ValueError(f"Types must be a 1D array\nGot: {self.types.ndim}D array")
        
        num_columns = self.decision_matrix.shape[1]
        if not (num_columns == self.weights.size == self.types.size):
            raise ValueError(
                f"Number of columns in decision matrix ({num_columns}) must match number of weights ({self.weights.size}) and types ({self.types.size})"
            )

        if np.any(self.weights < 0):
            raise ValueError(f"Weights must be non-negative\nGot: {self.weights}")

        if not np.isclose(np.sum(self.weights), 1):
            raise ValueError(f"Sum of weights must be 1\nGot: {np.sum(self.weights)}")

        if not np.all(np.isin(self.types, [-1, 1])):
            raise ValueError(
                f"Types must be either -1(cost) or 1(benefit).\nGot: {self.types}"
            )
        