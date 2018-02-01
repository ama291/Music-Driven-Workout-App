#testing example
import unittest

class exampleTest(unittest.TestCase):

    def test(self):
    	#pass example
        self.assertEqual(1,1)
        #fail example
        #self.assertEqual(2,1)

if __name__ == '__main__':
    unittest.main()
