from django.test import TestCase
from ..CSVDataProcessor import CSVDataProcessor
from ..methods.MCDMFactory import MCDAMethodFactory
import numpy as np


class CSVDataProcessor_TestCase(TestCase):
    def setUp(self):
        self.available_methods = MCDAMethodFactory.get_available_methods()
        self.sample_data = {
            "topsis": b"1,1,1\n0.25,0.25,0.5\n1,1,1\n1,2,3\n4,5,6\n7,8,9",
            "copras": b"1,-1,-1\n0.25,0.25,0.5\n1,1,1\n1,2,3\n4,5,6\n7,8,9",
            "spotis": b"1,-1,1\n0.2,0.3,0.5\n-5,12,-6,10,-8,5\n10.5,-3.1,1.7\n-4.7,0,3.4\n8.1,0.3,1.3\n3.2,7.3,-5.3\n-3,2,4.2\n",
        }
        self.expected_preferences = {
            "topsis": {
                "preferences": np.array([0.000, 0.207, 0.594, 1.000]),
                "ranking": np.array([4, 3, 2, 1]),
            },
            "copras": {
                "preferences": np.array([12.322, 26.070, 63.035, 100.000]),
                "ranking": np.array([4, 3, 2, 1]),
            },
            "spotis": {
                "preferences": np.array([0.199, 0.371, 0.306, 0.749, 0.357]),
                "ranking": np.array([1,3,5,2,4]),
            },
        }

    def test_init(self):
        for method in self.available_methods:
            processor = CSVDataProcessor(method, self.sample_data[method])
            self.assertEqual(processor.method_name, method)

    def test_invalid_method(self):
        with self.assertRaises(ValueError):
            processor = CSVDataProcessor("incorrect", self.sample_data["topsis"])

    def test_invalid_data(self):
        with self.assertRaises(ValueError):
            processor = CSVDataProcessor("topsis", b"")

    def test_get_prefernces(self):
        for method in self.available_methods:
            processor = CSVDataProcessor(method, self.sample_data[method])
            preferences = processor.preferences
            expected_preferences = self.expected_preferences[method]["preferences"]
            self.assertTrue(np.allclose(preferences, expected_preferences, atol=1e-3))

    def test_get_ranking(self):
        for method in self.available_methods:
            processor = CSVDataProcessor(method, self.sample_data[method])
            ranking = processor.ranking
            expected_ranking = self.expected_preferences[method]["ranking"]
            self.assertTrue(np.allclose(ranking, expected_ranking))

    def test_get_alts_number(self):
        for method in self.available_methods:
            processor = CSVDataProcessor(method, self.sample_data[method])
            alts_number = processor.alts_number
            expected_alts_number = len(self.expected_preferences[method]["ranking"])
            self.assertEqual(alts_number, expected_alts_number)