from .MCDMBase import MCDMBase
import numpy as np


class MCDMSPOTIS(MCDMBase):
    def __call__(self, decision_matrix, weights, types, bounds):
        self.bounds = bounds
        super().__call__(decision_matrix, weights, types)

    def _validate_input(self):
        super()._validate_input()
        num_columns = self.decision_matrix.shape[1]
        if self.bounds.shape != (num_columns, 2):
            raise ValueError(
                f"Bounds must be a 2D array with {num_columns} rows and 2 columns.\nGot: {self.bounds.shape}"
            )

        if not np.all(self.bounds[:, 0] <= self.bounds[:, 1]):
            raise ValueError(
                f"Lower bounds must be lower than upper bounds.\nGot: {np.round(self.bounds,3)}"
            )

        if not np.all(self.bounds[:, 0] <= self.decision_matrix) or not np.all(
            self.decision_matrix <= self.bounds[:, 1]
        ):
            raise ValueError(
                f"Decision matrix must be within bounds."
            )

    def _calculate(self):
        isp = self._find_ISP()

        distances = np.abs(self.decision_matrix - isp)

        normalized_distances = self._normalize_distances(distances)

        self.preferences = self._calculate_preferences(normalized_distances)

        self.ranking = self._calculate_ranking()

    def _find_ISP(self):
        isp = np.zeros(self.decision_matrix.shape[1])
        for i, (lower, upper) in enumerate(self.bounds):
            if self.types[i] == 1:
                isp[i] = upper
            else:
                isp[i] = lower
        return isp

    def _normalize_distances(self, distances):
        return distances / (self.bounds[:, 1] - self.bounds[:, 0])

    def _calculate_preferences(self, normalized_distances):
        return np.sum(normalized_distances * self.weights, axis=1)

    def _calculate_ranking(self):
        return np.argsort(self.preferences) + 1
