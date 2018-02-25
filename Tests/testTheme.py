import unittest
from Scripts.theme import Theme
from Scripts.user import User

class TestTheme(unittest.TestCase):

    def test(self):
        self.assertRaises(ValueError, Theme, None, "Beyonce", 88,5)
        self.assertRaises(ValueError, Theme, "", "artist", 88,5)
        self.assertRaises(ValueError, Theme, "Beyonce theme", "artist",88, None)
        self.assertRaises(ValueError, Theme, "Beyonce theme", "artist",88, -1)
        self.assertRaises(ValueError, Theme, "Beyonce theme", 88,None, 5)
        self.assertRaises(ValueError, Theme, "Beyonce theme", "",88, 5)
        self.assertRaises(ValueError, Theme, "Beyonce theme", "artist","88", 5)
        self.assertRaises(ValueError, Theme, "Beyonce theme", "artist blah","88", 5)
        theme1 = Theme("Beyonce theme", "artist", 88, 5)

        ## test constructor
        self.assertEqual(theme1.name, "Beyonce theme")
        self.assertEqual(theme1.theme, "artist")
        self.assertEqual(theme1.spotifyId, 88)
        self.assertEqual(theme1.numWorkouts, 5)

        ## test editThemeNumWorkouts
        theme1.editThemeNumWorkouts(20)
        self.assertFalse(theme1.editThemeNumWorkouts(-10))
        self.assertEqual(theme1.numWorkouts, 20)

if __name__ == '__main__':
    unittest.main()
