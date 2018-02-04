#testing example
import unittest
from Scripts.competition import Competition
from Scripts.user import User

class TestCompetition(unittest.TestCase):

    def test(self):
        competition1 = Competition("Race", "Who'll get 1st", "02-05-18")

        ## test constructor
        self.assertEqual(competition1.name, "Race")
        self.assertEqual(competition1.description, "Who'll get 1st")
        self.assertEqual(competition1.date, "02-05-18")
        self.assertFalse(competition1.completed)

        ## test competitionCompleted
        competition1.competitionCompleted()
        self.assertTrue(competition1.completed)

        ## test editCompetitionName
        competition1.editCompetitionName("Squats")
        self.assertEqual(competition1.name, "Squats")

        ## test editCompetitionDescription
        competition1.editCompetitionDescription("Maxing squats")
        self.assertEqual(competition1.description, "Maxing squats")

        ## test editCompetitionDate
        competition1.editCompetitionDate("06-06-20")
        self.assertEqual(competition1.date, "06-06-20")

if __name__ == '__main__':
    unittest.main()
