import unittest
from Scripts.competition import Competition
from Scripts.user import User

class TestCompetition(unittest.TestCase):

    def test(self):
        competition1 = Competition("Race", "Who'll get 1st", "02-05-18")
        competition2 = Competition("Race", "Who'll get 1st", "02-07-18")

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

        ## test addParticipant and removeParticipant
        self.assertFalse(competition1.removeParticipant("1"))
        self.assertTrue(competition1.addParticipant("1"))
        self.assertEqual(competition1.participants,{"1":0})

        self.assertTrue(competition1.removeParticipant("1"))
        self.assertFalse(competition1.removeParticipant("2"))

        ## test addExercise and removeExercise
        self.assertFalse(competition1.removeExercise("Squats"))
        competition1.addExercise("Squats")
        self.assertEqual(competition1.exercises, ["Squats"])
        competition1.removeExercise("Pushups")
        self.assertEqual(competition1.exercises, ["Squats"])
        competition1.removeExercise("Squats")
        self.assertEqual(competition1.exercises, [])
        competition1.addExercise("Pushups")
        competition1.addExercise("Burpees")
        self.assertEqual(competition1.exercises, ["Pushups", "Burpees"])
        competition1.addExercise("Burpees")
        self.assertEqual(competition1.exercises, ["Pushups", "Burpees", "Burpees"])

        ## test findWinner
        competition2.participants = {'1':1, '9':0}
        competition2.findWinner()
        self.assertEqual(competition2.winners,['1'])
        competition2.participants = {'1':1, '2':1}
        competition2.findWinner()
        self.assertTrue(competition2.winners, ['2'])

        ## test getNumParticipants
        p = len(competition2.participants)
        self.assertEqual(p, competition2.getNumParticipants())

if __name__ == '__main__':
    unittest.main()
