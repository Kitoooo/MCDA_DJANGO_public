from django.test import TestCase
import numpy as np
from ..methods.MCDMCopras import MCDMCOPRAS


class MCDMCOPRAS_TestCase(TestCase):
    def setUp(self):
        self.method = MCDMCOPRAS()

        self.sample_data = {
            1: {
                "types": np.array([1, -1, -1, -1, -1]),
                "weights": np.array([0.5300, 0.1175, 0.1175, 0.1175, 0.1175]),
                "decision_matrix": np.array(
                    [
                        [30.0, 12.487, 6.261, 10.88, 7.61],
                        [20.0, 12.372, 5.961, 10.88, 7.46],
                        [27.0, 11.096, 6.262, 9.92, 6.69],
                        [18.0, 10.982, 5.962, 9.92, 6.54],
                        [24.0, 11.017, 6.283, 9.98, 7.0],
                        [16.0, 10.903, 5.983, 9.98, 6.85],
                    ]
                ),
            },
            2: {
                "types": np.array([1, -1, -1, -1, -1]),
                "weights": np.array([0.075, 0.7, 0.075, 0.075, 0.075]),
                "decision_matrix": np.array(
                    [
                        [30.0, 12.487, 6.261, 10.88, 7.61],
                        [20.0, 12.372, 5.961, 10.88, 7.46],
                        [27.0, 11.096, 6.262, 9.92, 6.69],
                        [18.0, 10.982, 5.962, 9.92, 6.54],
                        [24.0, 11.017, 6.283, 9.98, 7.0],
                        [16.0, 10.903, 5.983, 9.98, 6.85],
                    ]
                ),
            },
        }

        self.expected_output = {
            1: {"ranks": np.array([1, 3, 5, 2, 4, 6])},
            2: {"ranks": np.array([1, 2, 3, 5, 4, 6])},
        }

    def test_init(self):
        self.assertEqual(self.method.get_preferences(), None)
        self.assertEqual(self.method.get_ranking(), None)

    def test_call(self):
        for i, input in self.sample_data.items():
            self.method(**input)
            self.assertTrue(np.allclose(self.method.decision_matrix, input["decision_matrix"]))
            self.assertTrue(np.allclose(self.method.weights, input["weights"]))
            self.assertTrue(np.allclose(self.method.types, input["types"]))

    def test_invalid_input(self):
        correct_decision_matrix = self.sample_data[1]["decision_matrix"]
        correct_weights = self.sample_data[1]["weights"]
        correct_types = self.sample_data[1]["types"]

        # wrong number of columns = decision matrix
        wrong_decision_matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        with self.assertRaises(ValueError):
            self.method(wrong_decision_matrix, correct_weights, correct_types)

        # wrong number of weights
        wrong_weights = np.array([0.25, 0.25, 0.5, 0.25])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, wrong_weights, correct_types)

        # wrong number of types
        wrong_types = np.array([1, 1, 1, 1])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, correct_weights, wrong_types)

        # negative weights
        negative_weights = np.array([-0.25, 0.25, 0.5])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, negative_weights, correct_types)

        # sum of weights != 1
        wrong_weights = np.array([0.25, 0.25, 0.25])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, wrong_weights, correct_types)

        # types not -1 or 1
        wrong_types = np.array([1, 1, 0])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, correct_weights, wrong_types)

        # criteria all benefit
        wrong_types = np.array([1, 1, 1, 1, 1])
        with self.assertRaises(ValueError):
            self.method(correct_decision_matrix, correct_weights, wrong_types)
        
    def test_sample_data(self):
        for i, input in self.sample_data.items():
            self.method(**input)
            expected_ranking = self.expected_output[i]["ranks"]
            ranking = self.method.get_ranking()
            self.assertTrue(np.allclose(ranking, expected_ranking))