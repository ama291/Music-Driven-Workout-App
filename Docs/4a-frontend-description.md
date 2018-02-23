Iteration 2 Front End Design
============================

The UI design has been reached by each of the back end groups working collaboratively with the front end group.

Overall UI Design
-----------------

A working sketch of our user interface flow can be found [here](https://docs.google.com/drawings/d/1D-Ky7AeJO76EZFbQIF8An-GPB5pjLO9zqRpSkIncV6Q/edit?usp=sharing).

Workouts
--------

### Get a workout

1.  The user navigates to the Get Workout page from main menu where they make selections in the following drop-down menus (NOTE - user can select either category or muscle groups, not both):
	1.  Category - can select any number, at least one
	2.  or Muscle Groups - can select any number, at least one
	3.  Equipment - can select any number
	4.  Difficulty - select one
	5.  Duration - select one
	6.  Themes - select up to 5
2.  After making selections, the user presses “Get Workout” and they are brought to the Workout Summary page.

### Workout summary

1.  This page displays a summary of the workout, with a cell for each exercise containing information such as exercise name, songs to be played during the exercise, equipment required, rpm, and duration.
2.  The user can scroll through these exercises, and if they decide they like the workout they press the "Start Workout" button.  They are then walked through the workout in a series of Exercise pages.

### Working out

1.  The Exercise page displays similar information to the cells in the Workout Summary page, though it also displays a timer counting down the remaining time of the exercise, playback information for the song currently being played, as well as "Pause/Resume", "Quit", and "Skip" (skip an exercise) buttons. During the exercise, music will be playing at an appropriate bpm (beats per minute) given the rpm (reps per minute) of the exercise.
2.  At the end of a workout, the user is brought back to the Workout Summary page where they can review the workout and decide to either save or quit the workout.

### View in progress and saved workouts

1.  The user navigates to the View Workouts page from main menu.
2.  This page has an "In Progress" and "Saved" section for in progress workouts and saved workouts, respectively. The cells in each section contain information about a single workout.
3.  Clicking on the cell in the "In Progress" section brings the user to the Exercise page corresponding to the exercise that they paused on, and from there they can do the workout.
4.  Clicking on the cell in the "Saved" section brings the user to the Exercise page corresponding to the first exercise in the workout (or produces an alert if they already have a version of this workout in progress), and from there they can do the workout. The user can also swipe the cell to unsave the workout, which also removes any in progress versions of that workout.

Fitness test
------------

### Testing an exercise

This has already been implemented in the first iteration.

1.  Button to “Begin” collecting data
2.  Partly for the purpose of testing (2) and (3) quickly, add “Skip exercise” button that will not run the 30-second script/timer
3.  Run my Swift script to collect JSON log
4.  Display a timer to the user for 30 seconds
5.  Call processMotionData, (Scripts.fitnessTest, Scripts.log, Tests.testLog) passing a timestamp and the raw motion data
6.  Display result (API call returns string for the rate)

### Getting full fitness test

1.  Ask user what category they want
2.  Ask user how many exercises
3.  Call getTrackedExercises (Scripts.fitnessTest)
4.  Ask the user to select which exercises they want to test on of results from the above query  
5.  Call getFitnessTest (Scripts.fitnessTest, Tests.testUser) to return a list of IDs of exercises to be tested  
6.  Display the results of their test and the previous results, as well as their level and whether they have leveled up. (These will all be returned by the API function.)
7.  Iterate through this list testing each exercise (step 1 above)

### Tracking and untracking exercises

1.  When an exercise is completed, check whether there is tracked via isTracked (Scripts.fitnessTest)  
2.  If so, display an untrack exercise button. If not, display a track exercise button
3.  When the user clicks the button, call toggleTracked (Scripts.testFitness) to toggle the tracked bit in the database for that exercise and all other rows with the same userID and exerciseID  

Goals/themes/competitions
-------------------------

### Adding a Goal

1.  Click “Goals” button on main menu to navigate to Goals page with current goals listed. There would ideally be “Edit” and “Add Goal” (or “+”) buttons in the top right corner (Scripts.goal, Tests.testGoal, Tests.testUser)
2.  On click “Add Goals” button, allows user to add a Goal name, description, # of times they want to work on this goal, category of Goal (ie: arms), muscle group of Goal (ie: biceps), duration, and days per week
3.  Initiate Goal(name, description, goalNum, categories, muscleGroups, duration, daysPerWeek, notify) with parameters given and call driver.addGoal(thisgoal)
4.  The Goals List should update to add a row with the Goal’s name, the date it was created (Goal.date), and its description

### Removing a Goal (Scripts.goal, Tests.testGoal, Tests.testUser)

1.  Click a goal in the Goals List, option to remove it appears (e.g. trash can icon or “Remove” button somewhere on the screen)
2.  Calls driver.removeGoal passing the goal clicked
3.  Goal should not appear on Goals List

### Adding a Theme (Scripts.theme, Tests.testTheme, Tests.testUser)

1.  “Themes” button on main menu - on click takes you to Themes screen where you see list of current themes, or just the “Add theme” button
2.  “Add theme” button - on click allows user to enter the Theme’s name (ie: Running), the actual theme itself (could be by artist, genre, or song), and the # of workouts
3.  Initiates a Theme(name, theme, numWorkouts) with these parameters and calls driver.addTheme(thisTheme)
4.  The Theme could show up on the page along with any others user has created

### Removing a Theme (Scripts.theme, Tests.testTheme, Tests.testUser)

1.  On the list of current themes, clicking one gives option to remove
2.  Calls driver.removeTheme passing the theme clicked
3.  Themes should not appear on themes list
