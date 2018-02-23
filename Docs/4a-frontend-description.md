Iteration 2 Front End Design
============================

Workouts
--------

### Get a workout

1.  Navigate to Workout page from home page where user makes selections in following drop-down menus (NOTE: user can select either category or muscle groups, not both):
	1.  Category (for now, options from “Exercise Type” in [bodybuilding.com](https://www.google.com/url?q=https://www.bodybuilding.com/exercises/finder&sa=D&ust=1519356779402000&usg=AFQjCNFU0iGztuI6R80T4ehi1VNNKri7gg)) \- can select any number
	2.  or Muscle Groups (for now, options from “Muscles” in [bodybuilding.com](https://www.google.com/url?q=https://www.bodybuilding.com/exercises/finder&sa=D&ust=1519356779403000&usg=AFQjCNGFzIzNrR80eq9XMqGZ8BHJIyJiPg)) \- can select any number
	3.  Equipment (options from “Equipment” in [bodybuilding.com](https://www.google.com/url?q=https://www.bodybuilding.com/exercises/finder&sa=D&ust=1519356779403000&usg=AFQjCNGFzIzNrR80eq9XMqGZ8BHJIyJiPg)) \- can select any number
	4.  Difficulty (options “Beginner” or “Intermediate”) - select one
	5.  Duration (options 10min to 60min, in steps of 5) - select one
	6.  Themes (for now, leave empty and do not use)
2.  User presses “Get Workout” button on bottom of the page (NOTE: make sure all fields have been set, with either categories or muscle groups, otherwise display alert)
	1.  Calls driver.getWorkout with the chosen options (see driver.py for description, requires json parsing)
		1.  Returns empty json if error, otherwise a workout json (using jsonpickle.encode on Workout instance)
		2.  If error, display [alert](https://www.google.com/url?q=https://learnappmaking.com/uialertcontroller-alerts-swift-how-to/&sa=D&ust=1519356779404000&usg=AFQjCNHevhW02skm5oFpgY_1ZYSsdK4YRA) “Unable to get workout. Please try again.”
		3.  If no error, app moves to workout summary page

### Workout summary

1.  Parsing the json received from step 1,
2.  Display the workout in a [tableview](https://www.google.com/url?q=https://developer.apple.com/library/content/referencelibrary/GettingStarted/DevelopiOSAppsSwift/CreateATableView.html&sa=D&ust=1519356779405000&usg=AFQjCNFkhOGSB1cgc0d4BaoY29WMQl8CEg), where each cell has information for a single exercise (for now name, rpm, and duration is sufficient)
3.  User can either press back button (use a Navigation controller) or “Start Workout” button on the bottom of the page
	1.  If press “Start Workout”, call driver.startWorkout with user ID and workout json
	2.  Check return value
		1.  0 = success, bring to next page
		2.  1 = database failure, display alert “Unable to start workout. Please try again.”
		3.  2 = already in progress, display alert “Workout already in progress.”

### Working out

1.  3 buttons - “Pause”, “Quit”, and “Start”
	1.  Pause - call driver.pauseWorkout with user ID, workout ID (should have gotten from workout json in step 2, note this is indeed a string), and 0
	2.  Quit -  call driver.quitWorkout with user ID and workout ID
	3.  Save -  call driver.saveWorkout with user ID and workout ID
	4.  In all cases, check return value
		1.  0 = success, bring back to home page
		2.  1 = database failure, display alert “Encountered an error, please try again.”
		3.  2 = failure, display alert “Action is invalid.”

### View in progress and saved workouts

1.  Navigate to View Workouts page from home page
	1.  Call driver.workoutsSaved with user ID and driver.workoutsInProgress with user ID to get the jsons
2.  Use a grouped table view, one section “In Progress” and another section “Saved”
3.  Each cell contains information about a single workout (for now, maybe ID, difficulty, and duration)

Fitness test
------------

### Testing an exercise

This has already been implemented in the first iteration.

1.  Button to “Begin” collecting data
2.  Partly for the purpose of testing (2) and (3) quickly, add “Skip exercise” button that will not run the 30-second script/timer
3.  Run my Swift script to collect JSON log
4.  Display a timer to the user for 30 seconds (can be skipped for now)
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

### Join a competition (this can be implemented later in iteration 2)

1.  Have a “Join Competition” button
2.  Maybe have three built in competitions 1, 2, and 3
3.  Click one and calls driver.addCompetition passing in the clicked competition
4.  Competition’s name should now show up under a section called “Current Competitions” (See the Overleaf doc for our UI Design)

### Remove a competition (this can be implemented later in iteration 2)

1.  Under “Current Competitions”, click one listed. Option to remove appears
2.  Calls driver.removeCompetition passing selected competition
3.  Competition should be removed from “Current Competitions”