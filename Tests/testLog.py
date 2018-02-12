import unittest
from Scripts.log import Log, LogFromFile

class TestLog(unittest.TestCase):

    def assertApprox(self, n1, n2, scale):
        if n1 > n2:
            tmp = n1
            n1 = n2
            n2 = tmp
        err = (n1 + n2) / 2.0 * scale
        self.assertTrue(n1 + err >= n2)

    def test(self):
        ## test constructor 
        log1 = LogFromFile("Logs/log1.json")
        self.assertEqual(len(log1.times), len(log1.xAccl))
        self.assertEqual(len(log1.xAccl), len(log1.yAccl))
        self.assertEqual(len(log1.yAccl), len(log1.zAccl))
        self.assertApprox(len(log1.times), 300, .05)
        self.assertApprox(max(log1.times), 30.0, .05)

        ## test getFrequency
        log2 = LogFromFile("Logs/log2.json")
        log3 = LogFromFile("Logs/log3.json")
        log4 = LogFromFile("Logs/log4.json")
        log5 = LogFromFile("Logs/log5.json")

        ## these numbers were determined by counting peaks visually
        self.assertApprox(log1.getFrequency(), 60 * 35.0/30, .1)
        self.assertApprox(log2.getFrequency(), 60 * 16.0/30, .1)
        self.assertApprox(log3.getFrequency(), 60 * 9.0/30, .1)
        self.assertApprox(log4.getFrequency(), 60 * 8.0/30, .1)
        self.assertApprox(log5.getFrequency(), 60 * 27.0/30, .3)

if __name__ == '__main__':
    unittest.main()

## log 5: 27 or 38
## log 4: 8
## log 3: 8 or 10
## log 2: 16
## log 1: 35