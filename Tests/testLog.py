import unittest
from Scripts.log import Log

'''In this test case, we take a 30 second log and manually count the number of periods
From that, we get an expected Log, and if the Log is within an acceptable rage,
we consider the test passed.'''
class TestLog(unittest.TestCase):
    def test(self):
        freq1 = Log('Logs/log1.json').getFrequency()
        freq2 = Log('Logs/log2.json').getFrequency()
        freq3 = Log('Logs/log3.json').getFrequency()
        freq4 = Log('Logs/log4.json').getFrequency()
        freq5 = Log('Logs/log5.json').getFrequency()

        tolerance = .1

        actual_val1 = (17.0 / 30.0)
        actual_val2 = (38.0 / 30.0)
        actual_val3 = (17.0 / 30.0)
        actual_val4 = (8.0 / 30.0)
        actual_val5 = (20.0 / 30.0)

        diff1 = abs(freq1 - actual_val1)
        diff2 = abs(freq2 - actual_val2)
        diff3 = abs(freq3 - actual_val3)
        diff4 = abs(freq4 - actual_val4)
        diff5 = abs(freq5 - actual_val5)

        self.assertTrue(diff1 < tolerance)
        self.assertTrue(diff2 < tolerance)
        self.assertTrue(diff3 < tolerance)
        self.assertTrue(diff4 < tolerance)
        self.assertTrue(diff5 < tolerance)

if __name__ == '__main__':
    unittest.main()