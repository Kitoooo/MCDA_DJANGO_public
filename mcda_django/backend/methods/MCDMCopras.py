import numpy as np
from .MCDMBase import MCDMBase


class MCDMCOPRAS(MCDMBase):
    def _validate_input(self):
        super()._validate_input()

        if np.all(self.types == 1):
            raise ValueError(
                f"COPRAS is not applicable for benefit criteria only\nGot: {self.types}"
            )

    def _calculate(self):
        normalized_decision_matrix = self._normalize()

        weighted_matrix = normalized_decision_matrix * self.weights

        sums_profit = np.sum(weighted_matrix[:, self.types == 1], axis=1)
        sums_cost = np.sum(weighted_matrix[:, self.types == -1], axis=1)

        self.preferences = self._caculate_preferences(sums_profit, sums_cost)
        self.ranking = self._calculate_ranking()

    def _normalize(self):
        return self.decision_matrix / np.sum(self.decision_matrix, axis=0)

    def _caculate_preferences(self, sums_profit, sums_cost):
        Q = sums_profit + (
            (np.min(sums_cost) * sums_cost)
            / (sums_cost * (np.min(sums_cost) / sums_cost))
        )
        return Q / np.max(Q) * 100

    def _calculate_ranking(self):
        return np.argsort(self.preferences)[::-1] + 1