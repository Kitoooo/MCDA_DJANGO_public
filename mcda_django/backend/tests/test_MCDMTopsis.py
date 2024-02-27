from django.test import TestCase
import numpy as np
from ..methods.MCDMTopsis import MCDMTOPSIS
from pymcdm.methods import TOPSIS

class MCDMTOPSIS_TestCase(TestCase):
    def setUp(self):
        self.method = MCDMTOPSIS()

    def test_init(self):
        self.assertEqual(self.method.get_preferences(), None)
        self.assertEqual(self.method.get_ranking(), None)

    def test_call(self):
        decision_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        weights = np.array([0.25, 0.25, 0.5])
        types = np.array([1, 1, 1])

        self.method(decision_matrix, weights, types)
        self.assertTrue(np.allclose(self.method.decision_matrix, decision_matrix))
        self.assertTrue(np.allclose(self.method.weights, weights))
        self.assertTrue(np.allclose(self.method.types, types))

    def test_invalid_input(self):
        correct_decision_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        correct_weights = np.array([0.25, 0.25, 0.5])
        correct_types = np.array([1, 1, 1])
        
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

    def test_sample_data(self):
        decision_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        weights = np.array([0.25, 0.25, 0.5])
        types = np.array([1, 1, -1])
        self.method(decision_matrix, weights, types)
        body = TOPSIS()

        pref1 = self.method.get_preferences()
        pref2 = body(decision_matrix, weights, types)

        rank1 = self.method.get_ranking()
        rank2 = body.rank(pref2)

        self.assertTrue(np.allclose(pref1, pref2))
        self.assertTrue(np.allclose(rank1, rank2))
    

