import unittest

# Import all our test modules
from test_Map import TestMap
from test_MapFileManager import TestMapFileManager
from test_TSP import TestTSP

# Create a master test suite
def master_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestMap))
    suite.addTest(loader.loadTestsFromTestCase(TestMapFileManager))
    suite.addTest(loader.loadTestsFromTestCase(TestTSP))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(master_suite())