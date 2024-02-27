from django.test import TestCase
from ..methods.MCDMFactory import MCDAMethodFactory
from ..methods.MCDMTopsis import MCDMTOPSIS
from ..methods.MCDMCopras import MCDMCOPRAS
from ..methods.MCDMSpotis import MCDMSPOTIS


class Factory_TestCase(TestCase):
    def setUp(self):
        self.factory = MCDAMethodFactory()
        self.available_methods = {
            "topsis": MCDMTOPSIS,
            "copras": MCDMCOPRAS,
            "spotis": MCDMSPOTIS,
        }

    def test_get_available_methods(self):
        self.assertEqual(self.factory.get_available_methods(), self.available_methods.keys())

    def test_correct_methods(self):
        for method in self.available_methods:
            self.assertIsInstance(self.factory(method), self.available_methods[method])
    
    def test_incorrect_method(self):
        with self.assertRaises(ValueError):
            self.factory("incorrect")
