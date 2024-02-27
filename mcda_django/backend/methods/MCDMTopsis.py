import numpy as np
from .MCDMBase import MCDMBase

class MCDMTOPSIS(MCDMBase):

    def _calculate(self):
        self.normalized_decision_matrix = self._normalize()
        weighted_matrix = self.normalized_decision_matrix * self.weights
        ideal_best, ideal_worst = self._get_ideal_vectors(weighted_matrix)
        self.preferences = self._calculate_preferences(weighted_matrix, ideal_best, ideal_worst)
        self.ranking = self._calculate_ranking()

    def _normalize(self):
        # Minmax normalization
        normalized_matrix = np.zeros(self.decision_matrix.shape)
        columns = self.decision_matrix.shape[1]

        for i in range(columns):
            x = self.decision_matrix[:, i]
            if self.types[i] == -1:
                normalized_matrix[:, i] = (np.max(x) - x) / (np.max(x) - np.min(x))
            else:
                normalized_matrix[:, i] = (x - np.min(x)) / (np.max(x) - np.min(x))
        return normalized_matrix

    def _get_ideal_vectors(self, weighted_matrix):
        ideal_best = np.max(weighted_matrix, axis=0)
        ideal_worst = np.min(weighted_matrix, axis=0)
        return ideal_best, ideal_worst

    def _calculate_preferences(self, weighted_matrix, ideal_best, ideal_worst):
        distances_to_best = np.linalg.norm(weighted_matrix - ideal_best, axis=1)
        distances_to_worst = np.linalg.norm(weighted_matrix - ideal_worst, axis=1)
        return distances_to_worst / (distances_to_best + distances_to_worst)

    def _calculate_ranking(self):
        return np.argsort(self.preferences)[::-1] + 1
