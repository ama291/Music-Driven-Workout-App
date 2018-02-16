# Music-Driven-Workout-App
CS 220 Music Driven Workout App Project

The Flask API  with documentation is live at http://138.197.49.155:8000/

Upon pushing to master the Jenkins instance on the server will re-install dependencies and restart the Flask app.

Before running anything locally, make sure you have Python3 installed, the app will use the ```python3``` executables.

Make sure you have VirtualEnv installed - ```sudo pip3 install virtualenv```

## Local Setup
```source setup.sh``` to install the necessary dependencies to run the app and tests. This should probably be run every time you pull from master.

```source env/bin/activate``` should be run every time you work on the project, it'll make sure dependencies are up to date and use the VirtualEnv environment. If you exit your current terminal window, you'll need to re-run this.

If your script uses a new dependency, please add it to the "requirements.txt" file. You can view your requirements via ```pip freeze```.

To run the API locally, ```sh server.sh```

## Testing
Tests will be stored in the "Tests" folder.

```sh test.sh``` to run all test files locally.

## Server Setup - DigitalOcean Box
The server will build itself and run the unit tests upon a push to the GitHub repository.

For manual setup, ```source setup-server.sh```

## Scripts
Place scripts in the "Scripts" folder, import them where necessary.

## Milestone 3b Progress

### Front End and Infrastructure

The server, API, and testing infrastructure is described above.

#### Description of Front End

#### Who Did What

#### Changes

### Working Out

#### Description

For this iteration, we focused on the various interactions a user can have with workouts,
as well as an algorithm to generate the workouts.

The flow of interactions with workouts is as follows:
A user generates a workout with a given set of inputs, and they can regenerate as many times as they like
(a summary of the workout returned will be displayed in the app). From there, they can choose to start the workout.
The user can pause and resume multiple times during the workout, upon a pause they can also exit the workout
and return to it later in via a In Progress section of a View Workouts page in the app. Resuming a workout in
this manner will bring the user to the exercise that the workout was paused on. Once a new workout is complete,
the user can either quit or save the workout. The user can start a saved workout via a Saved
section of a View Workouts page in the app. From here, the user can also unsave a workout, which removes any
in progress version of the workout.

The algorithm to generate workouts is in the generateWorkout function of workout.py. One input is the user's desired duration,
and the algorithm tries to get as close to that duration as possible. For a given number of runs, a random set of exercises
matching the user's inputs are retrieved from the database, and subset of these exercises is chosen for the workout.
The workout chosen is the one that gets the closest to the desired duration. Choosing random sets of exercises ensures
variability in the workouts. As another technique to ensure variability, we set a range of possible durations for each exercise,
and we randomly choose a duration within that range, with a given increment. If the user has tested on an exercise, they
will be given that rpm; otherwise, they will be given the suggested rpm that has been retrieved from the database for that
exercise.

The exercises scraped from bodybuilding.com did not have any information about duration or rpm (it was also not
available in any single source), so we added these fields to the database. For each exercise, we filled in these
fields based on a reasonable range of values for its corresponding category.

We have not yet dealt with getting music that matches the beat of each exercise, that will be the next iteration.
At that time, we will apply the themes chosen by the user.

For this component, the API routes to functions in driver.py, which generally retrieves the user from the database,
builds a User instance from that information, and calls the associated function in user.py.

#### Acceptance Tests


#### Who Did What

Larissa did the unit tests for the workout-related user functions. Manasvi did the unit tests for the Workout class.

Larissa wrote the getUser and all workout-related functions in driver.py. Together, Manasvi and Larissa
added the necessary information for generating workouts into the database (i.e. duration range, increment, and suggested
rpm). We also wrote the generateWorkout function in workout.py together. Manasvi then tested the algorithm with a variety
of inputs, tuning the number of exercises retrieved for each run and the number of runs.

#### Changes

We added an id to the exercises class, since that field is available in the database.

We also changed the function prototype for user.getWorkout, removing the defaults values and changing
the parameter ordering to match the Workout class construction order. The default values were shifted
to the higher-level function in driver.py.

### Fitness Test

#### Description

For this iteration, we focused on setting up fitness testing with the following use cases:

* A user can begin a fitness test. The `getFitnessTest()` function creates a list of exercises from the exercises database table that will be recommended to the user for the test.

* A user can complete an exercise in a fitness test. There will be a button for them to begin the test in the front end, that causes the phone to begin collecting accelerometer logs. These logs are sent to the server to be analyzed for frequency. `processMotionData()` calls `Log.getFrequency()` to determine a frequency from the result, and then saves it to the database along with a timestamp.

* A user can view their results to a fitness test. Since results are displayed by date, we can show how they have progressed over time on an exercise. The front end can display a graph.

* A user can track and untrack exercises. `checkTracked()` checks whether an exercise is tracked and the UI will (in the second iteration) display a button to Add or Remove the exercise from tracked, depending on the result. `toggleTracked()` toggles the bit in the userexercise database, indicating whether the exercise is tracked. When they begin the test, they are specifically asked which tracked exercises they want to complete, and the rest of the exercises are recommended randomly from the database.

#### Acceptance Tests

* For getting a fitness test:
    * Route
        * TODO
    * Procedure 
        * Call the API function with given arguments
    * Cases
        * `categories` can be  `"Cardio"`, `"Olympic Weightlifting"`, `"Plyometrics"`, `"Powerlifting"`, `"Strength"`, `"Stretching"`, or `"Strongman"`. Pass in any number for `"numExercises"`. `trackedIDs` should be a list of numbers
    * Expected result
        * If the categories are valid, the number of exercises is a positive number, and the number of tracked IDs is less than `numExercise`, then you should get a success. There should be `numExercises` exercises that are all be in the right category, and none of them should be in the `trackedIDs` list. Otherwise, you should get a failure.
* For determining frequency from a log:
    * Procedure
        1. Click begin on the fitness test section
        2. Move the phone in the pattern described below
        3. Count the number of repetitions while the timer is running
        4. Calculate frequency per second (divide by 30 for 30 seconds)
    * Expected result
        * The time you calculate should be similar (within 0.1) to the result displayed, or (TODO) an integer multiple or fraction of the result displayed (probably 2x or ½x). 
        * The frequency should be higher for faster movements
    * Cases
        * Move the phone in a regular motion with a slow period, back and forth, period ~2 seconds
        * Move phone in a somewhat faster period
        * Move phone in a regular pattern but pause in the middle to place it on the table for five seconds
        * Move phone in a regular pattern, pause in the middle and shake it vigorously 
        * Move phone with a frequency that begins quick but decreases
    * *Note*: these cases are approximately in order of increasing difficulty. The last ones may be less accurate.
* For getting previous results:
    * Route
        * TODO
    * Procedure
        * Call API function with the give arguments
    * Cases
        * `userID`: 1, `exID`: 144
    * Expected result
        * `[[139, 1, 144, '2012-12-12 12:12:12', 30.5, 0], [140, 1, 144, '2012-12-12 12:18:12', 30.5, 0]]`
* For tracking and un-tracking:
    * Route
        * TODO
    * Procedure
        * Call toggle exercise repeatedly
    * Expected result
        * The tracked bit should alternate between 0 and 1
    * Cases
        * `userID` = 1, `exID` = 12

#### Who Did What

Lucy Newman and Gregory Howlett-Gomez worked on this part of the project. Lucy wrote the functions in `Scripts/fitnessTest.py`, for tracking and un-tracking exercises, getting a list of exercises for a fitness test, and adding a fitness test result to the database. Gregory wrote the functions in `Scripts/log.py` for determining frequency of a exercise movements from accelerometer log data. They wrote test cases for their code in '`Tests/testFitnessTest.py` and `Tests/testLog.py`, respectively.

#### Changes

TODO

### Goals, Themes, and Competitions

#### Description

For this iteration, we focused on setting up the general goals, themes, and competitions infrastructure as well as integrating changes to them with the database (competitions is not fully tested and implemented in this iteration since it will be focused on in iteration 2):

* A user can add and remove goals. The `addGoal()` and `removeGoal()` methods allow the user to specify goals geared towards certain muscle groups and categories

* A user can add and remove themes. These are based on specific genres or artists, and the user can choose how many workouts use the theme is used for.

* (A user can create, join, remove, and leave competitions. These can have specific exercises added to them, the amount of time they span can be edited, participants can be added or removed, and a winner(s) is eventually chosen) (will finalize in iteration 2)

#### Acceptance Tests

* For creating a goal:
    * User should be able to create a goal and input all the appropriate information (name, description, duration, notifications, etc.)
    * User should be able to see this new goal and all their other goals in an easily readable list
    * Will error if user tries to make goals with invalid parameters, such as empty name or negative duration
* For creating a theme:
    * User should be able to create a theme and input all the appropriate information (name, theme i.e. artist or genre it is based on, number of workouts to use it for)
    * User should be able to see all of their themes and their newly created themes in an easily readable list
    * Will error if user tries to make theme with empty name, theme, or negative number of workouts
* For creating a competition:
    * Will be implemented in iteration 2
* For removing a goal:
    * User should be able to remove a specified goal
    * User will no longer see it in the list of all their goals once removed
    * Will error if user tries to remove a goal that they do not already have in their goals 
* For removing a theme:
    * User should be able to remove a specified theme
    * User will no longer see it in the list of all their themes once removed
    * Will error if user tries to remove a theme that they do not already have in their themes
* For removing a competition:
    * Will be implemented in iteration 2

#### Who Did What

Julia Xu and Jessica Wang worked on this part of the project. Julia added methods for the driver.py file to allow users to add/remove goals/themes/competitions and have those changes be reflected in the database, tests for those functions (seen in testDriver.py)the theme and goal classes (Theme.py, Goal.py) and unit tests for both (testTheme.py, testGoal.py). Jessica added the competition (Competition.py) class and unit tests for it (testCompetition.py) and also worked on tests for add/remove goals, themes, and competitions for users (testUser.py).

#### Changes

We did not see any significant changes from our original proposal. TODO
