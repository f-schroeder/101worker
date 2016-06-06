from .program import run

import unittest
from unittest.mock import Mock, patch

class SmellsPerContributionTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.read_dump.return_value = { "javaComposition": 171 }
        self.env.get_derived_resource.return_value = 171

    def test_run(self):
        res = {
            'file': 'contributions/java/some-file.java'
        }
        run(self.env, res)

        self.env.write_dump.assert_called_with('smellsPerContribution', { "javaComposition": 171 })

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(SmellsPerContributionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
