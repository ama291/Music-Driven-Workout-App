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

        ## test addParticipant and removeParticipant
        self.assertFalse(competition1.removeParticipant("Jessica"))
        competition1.addParticipant("Jessica")
        participants1 = ["Jessica"]
        self.assertEqual(competition1.participants, participants1) # checks adding 1 participant
        competition1.removeParticipant("Jessica")
        participants2 = []
        self.assertEqual(competition1.participants, participants2) # checks removing 1 participant for the empty array
        competition1.addParticipant("Julia")
        competition1.addParticipant("Jessica")
        participants3 = ["Julia", "Jessica"]
        self.assertEqual(competition1.participants, participants3) # checks two added participants
        competition1.removeParticipant("BOBBY")
        self.assertEqual(competition1.participants, participants3) # checks removing participant not in competition
        competition1.removeParticipant("Julia")
        self.assertEqual(competition1.participants, participants1) # checks removing participant in competition
        competition1.addParticipant("Jessica")
        self.assertEqual(competition1.participants, participants1) # checks adding participant already in competition

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

if __name__ == '__main__':
    unittest.main()
