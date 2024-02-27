from django.test import TestCase
from ..methods.MCDMBase import MCDMBase

class MockMCDM(MCDMBase):
    def _calculate(self):
        pass

class MCDMBase_TestCase(TestCase):
    def setUp(self):
        self.mcdm = MockMCDM()

    def test_dimensions_validate(self):
        with self.assertRaises(ValueError):
            self.mcdm([0], [0], [0])
        
        with self.assertRaises(ValueError):
            self.mcdm([[0], [0]], [[0]], [0])

        with self.assertRaises(ValueError):
            self.mcdm([[0], [0]], [0, 0], [[0]])
    
