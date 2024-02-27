from django.test import TestCase
import numpy as np
from ..methods.MCDMSpotis import MCDMSPOTIS


class MCDMSPOTIS_TestCase(TestCase):
    def setUp(self):
        self.method = MCDMSPOTIS()
        # sample data from 
        # Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). 
        # The SPOTIS rank reversal free method for multi-criteria decision-making support. 
        # In 2020 IEEE 23rd International Conference on Information Fusion (FUSION) (pp. 1-8). IEEE.
        self.sample_inputs = {
            1: {
                "weights": np.array([0.2, 0.3, 0.5]),
                "decision_matrix": np.array(
                    [
                        [10.5, -3.1, 1.7],
                        [-4.7, 0, 3.4],
                        [8.1, 0.3, 1.3],
                        [3.2, 7.3, -5.3],
                        [-3, 2, 4.2],
                    ]
                ),
                "bounds": np.array([[-5, 12], [-6, 10], [-8, 5]]),
                "types": np.array([1, -1, 1]),
            },
            2: {
                "weights": np.array([0.2941, 0.2353, 0.2353, 0.0588, 0.1765]),
                "decision_matrix": np.array(
                    [
                        [15000, 4.3, 99, 42, 737],
                        [15290, 5.0, 116, 42, 892],
                        [15350, 5.0, 114, 45, 952],
                        [15490, 5.3, 123, 45, 1120],
                    ]
                ),
                "bounds": np.array(
                    [(14000, 16000), (3, 8), (80, 140), (35, 60), (650, 1300)]
                ),
                "types": np.array([-1, -1, -1, 1, 1]),
            },
        }
        self.expected_outputs = {
            1: {
                "preferences": np.array([0.1989, 0.3707, 0.3063, 0.7491, 0.3572]),
                "ranking": np.array([1,3,5,2,4]),
            },
            2: {
                "preferences": np.array([0.4779, 0.5781, 0.5558, 0.5801]),
                "ranking": np.array([1,3,2,4]),
            },
        }

    def test_init(self):
        self.assertEqual(self.method.get_preferences(), None)
        self.assertEqual(self.method.get_ranking(), None)

    def test_call(self):
        self.method(**self.sample_inputs[1])
        self.assertTrue(
            np.allclose(
                self.method.decision_matrix, self.sample_inputs[1]["decision_matrix"]
            )
        )
        self.assertTrue(
            np.allclose(self.method.weights, self.sample_inputs[1]["weights"])
        )
        self.assertTrue(np.allclose(self.method.types, self.sample_inputs[1]["types"]))
        self.assertTrue(
            np.allclose(self.method.bounds, self.sample_inputs[1]["bounds"])
        )

    def test_invalid_input(self):
        correct_decision_matrix = self.sample_inputs[1]["decision_matrix"]
        correct_weights = self.sample_inputs[1]["weights"]
        correct_types = self.sample_inputs[1]["types"]
        correct_bounds = self.sample_inputs[1]["bounds"]

        # wrong number of columns = decision matrix
        wrong_decision_matrix = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        with self.assertRaises(ValueError):
            self.method(
                wrong_decision_matrix, correct_weights, correct_types, correct_bounds
            )

        # wrong number of weights
        wrong_weights = np.array([0.25, 0.25, 0.5, 0.25])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, wrong_weights, correct_types, correct_bounds
            )

        # wrong number of types
        wrong_types = np.array([1, 1, 1, 1])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, correct_weights, wrong_types, correct_bounds
            )

        # negative weights
        negative_weights = np.array([-0.25, 0.25, 0.5])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, negative_weights, correct_types, correct_bounds
            )

        # sum of weights != 1
        wrong_weights = np.array([0.25, 0.25, 0.25])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, wrong_weights, correct_types, correct_bounds
            )

        # types not -1 or 1
        wrong_types = np.array([1, 1, 0])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, correct_weights, wrong_types, correct_bounds
            )
        
        # bounds not 2D
        wrong_bounds = np.array([1, 2, 3])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, correct_weights, correct_types, wrong_bounds
            )

        # bounds wrong shape
        wrong_bounds = np.array([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, correct_weights, correct_types, wrong_bounds
            )
        
        # bounds lower > upper
        wrong_bounds = np.array([[1, 2], [4, 3], [6, 5]])
        with self.assertRaises(ValueError):
            self.method(
                correct_decision_matrix, correct_weights, correct_types, wrong_bounds
            )

        # decision matrix not within bounds
        wrong_decision_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            self.method(
                wrong_decision_matrix, correct_weights, correct_types, correct_bounds
            )
        
        # decision matrix not within bounds
        wrong_decision_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            self.method(
                wrong_decision_matrix, correct_weights, correct_types, correct_bounds
            )

    def test_sample_data(self):
        for i in range(1, 3):
            self.method(**self.sample_inputs[i])
            preferences = self.method.get_preferences()
            ranking = self.method.get_ranking()
            expected_preferences = self.expected_outputs[i]["preferences"]
            expected_ranking = self.expected_outputs[i]["ranking"]
            self.assertTrue(np.allclose(preferences, expected_preferences, atol=1e-3))

            self.assertTrue(np.allclose(ranking, expected_ranking))

