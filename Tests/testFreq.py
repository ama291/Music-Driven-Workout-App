import unittest
from Scripts.getFreq import Frequency

'''In this test case, we take a 30 second log and manually count the number of periods
From that, we get an expected frequency, and if the frequency is within an acceptable rage,
we consider the test passed.'''
class TestFreq(unittest.TestCase):
	def test(self):
		freq1 = Frequency('Logs/log1.json').get_freq()
		freq2 = Frequency('Logs/log2.json').get_freq()
		freq3 = Frequency('Logs/log3.json').get_freq()
		freq4 = Frequency('Logs/log4.json').get_freq()
		freq5 = Frequency('Logs/log5.json').get_freq()

		tolerance = .1

		actual_val1 = (17.0 / 30.0)
		actual_val2 = (38.0 / 30.0)
		actual_val3 = (17.0 / 30.0)
		actual_val4 = (8.0 / 30.0)
		actual_val5 = (20.0 / 30.0)

		diff1 = abs(freq1 - actual_val1)
		print("freq 5 is: " + str(freq5))
		print("ACTUAL val is: " + str(actual_val5))
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

