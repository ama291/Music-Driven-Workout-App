# Milestone 3b Progress

## Running our code

Please see the information in the `README` file in the root directory of our repository for instructions on how to set up our code for testing.

## Front End & Infrastructure

The server, API, and testing infrastructure is described above.

#### Description of Front End

Our main focus in this iteration was the development of the API routes. Our biggest changes can be found in server.py and our documentation for what functions our API works with and how to call those functions through the API can be found in our API/templates/index.html file. This is hosted on our server at http://138.197.49.155:8000/. We also did some more database infrastructure work. The database is hosted at http://138.197.49.155:5000/. Additionally, we helped the other groups get set up using the database and API.

Additionally, we began creating a basic iOS app interface, though this was not our main focus for this iteration. We expect to have this much more fully developed in the next iteration as more back-end work has completed been developed.

#### Performing the acceptance tests

Since we haven't focused on the UI yet, the acceptance tests can be performed via `curl` requests to our API. We describe in the sections below the commands for the requests, and the expected result.

#### Who Did What

Implementing the API routes in server.py was handled by Alex. Documentation was handled by Chris. Test inputs for the API acceptance tests were provided by individuals from each of the other departments.

## Working Out

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

The acceptance tests below test all functionality of the workout-related functions in driver.py (hence these functions
are not tested in testDriver.py).

Note: In the python interpreter, json.loads() should be called on the "Result" of getworkout to get the
proper string to pass to startworkout. The workout id use in following commands is in this string, under "ID".

Get workout using command-

    $ curl --data "userid=0&equipment=Body Only,Kettlebells&duration=50&difficulty=Intermediate&categories=Cardio,Stretching&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/getworkout/

Start Workout using- (should return 0)

    $ curl --data "userid=0&workout=(Use string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/startworkout/
    
    For this test, we have noticed that the command line does not like the quotation marks in the JSON string returned by the getworkout, so this request needs to be done via Python or a Rest client. When using this method, remove the /-escape characters in the JSON (this is automatically done by json.loads() in Python).

Try to start Workout again using- (should return 2)

    $ curl --data "userid=0&workout=(Use string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/startworkout/

Pause the workout using- (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/pauseworkout/

Pause the workout again using- (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/pauseworkout/

Quit the workout using- (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/quitworkout/

Try to quit again (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/quitworkout/

Try to pause workout that has been quit- (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/pauseworkout/
Try to save workout that has been quit- (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/saveworkout/

Get workout using-

    $ curl --data "userid=0&equipment=Dumbbell&duration=30&difficulty=Beginner&musclegroups=Biceps&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/getworkout/

Start Workout using- (should return 0)

    $ curl --data "userid=0&workout=(Use string returned by getworkout, i.e. "Result")&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/startworkout/

Save the workout using - (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/saveworkout/

Try to save again (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/saveworkout/

Start saved workout using - (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/startsavedworkout/

Unsave workout using- (should return 0)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/unsaveworkout/

Try to unsave workout again - (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/unsaveworkout/

Try to start saved workout after unsave - (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/startsavedworkout/

Try to quit workout that has been unsaved - (should return 2)

    $ curl --data "userid=0&workoutid=(Use the workout id from the string returned by getworkout)&key=SoftCon2018" http://138.197.49.155:8000/api/workouts/quitworkout/

Workouts can be created with a variety of inputs. Options for muscle groups, category, and equipment can be found at https://www.bodybuilding.com/exercises/finder.
Only one of categories or muscle groups should be included in getworkout, not both.

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

## Fitness Test

#### Description

For this iteration, we focused on setting up a back end for fitness testing with the following use cases:

* A user can begin a fitness test. The `getFitnessTest()` function creates a list of exercises from the exercises database table that will be recommended to the user for the test.

* A user can complete an exercise in a fitness test. There will be a button for them to begin the test in the front end, that causes the phone to begin collecting accelerometer logs. These logs are sent to the server to be analyzed for frequency. `processMotionData()` calls `Log.getFrequency()` to determine a frequency from the result, and then saves it to the database along with a timestamp.

* A user can view their results to a fitness test. Since results are displayed by date, we can show how they have progressed over time on an exercise. The front end will later display these results as a graph.

* A user can track and untrack exercises. `checkTracked()` checks whether an exercise is tracked and the UI will (in the second iteration) display a button to Add or Remove the exercise from tracked, depending on the result. `toggleTracked()` toggles the bit in the userexercise database, indicating whether the exercise is tracked. When they begin the test, they are specifically asked which tracked exercises they want to complete, and the rest of the exercises are recommended randomly from the database.

#### Acceptance Tests

* For getting a fitness test:
    * Route
        * `/api/fitness/test/`
    * Procedure
        * Call the API function with given arguments
    * Cases
        * `categories` can be  `"Cardio"`, `"Olympic Weightlifting"`, `"Plyometrics"`, `"Powerlifting"`, `"Strength"`, `"Stretching"`, or `"Strongman"`. Pass in any number for `numExercises`. `trackedIDs` should be a list of numbers
        * Example:

        curl --data "userid=1&categories=Strength,Cardio&numexercises=5&exerciseids=1,2,3&key=SoftCon2018" http://138.197.49.155:8000/api/fitness/test/

    * Expected result
        * If the categories are valid, the number of exercises is a positive number, and the number of tracked IDs is less than `numExercise`, then you should get a success. There should be `numExercises` exercises that are all be in the right category, and none of them should be in the `trackedIDs` list. Otherwise, you should get a failure.
* For determining frequency from a log:
    * Route
        * `/api/fitness/accel/`
    * Procedure
        1. Click begin on the fitness test section
        2. Move the phone in the pattern described below
        3. Count the number of repetitions while the timer is running
        4. Calculate frequency per second (divide by 30 for 30 seconds)
    * Expected result
        * The time you calculate should be similar (within 0.1) to the result displayed, or (TODO) an integer multiple or fraction of the result displayed (probably 2x or ½x). When returning a tempo for the Work Out, we will sometimes scale frequencies by an integer to get a tempo in a reasonable range (say, 80-130 bmp). In this case, the user would do a single exercise in two or four beats, or in 3/4 time, 3 beats. So, it is okay that sometimes the algorithm may pick up on something that is half or double the desired frequency.
        * For the same pattern of movement, frequency should be higher for faster movements
    * Cases
        * Move the phone in a regular motion with a slow period, back and forth, period ~2 seconds
        * Move phone in a somewhat faster period
        * Move phone in a regular pattern but pause in the middle to place it on the table for five seconds
        * Move phone in a regular pattern, pause in the middle and shake it vigorously
        * Move phone with a frequency that begins quick but decreases
    * *Note*: these cases are approximately in order of increasing difficulty. The last ones may be less accurate.
* For getting previous results:
    * We did not write an API route for this yet
* For tracking and un-tracking and checking if an exercise is tracked:
    * Routes
        * `/api/fitness/toggletracked/`
        * `/api/fitness/istracked`
    * Procedure
        * Call toggle exercise repeatedly
        * Call isTracked in between
    * Expected result
        * The tracked bit should alternate between 0 and 1
        * When the returned track bit is 1 for toggling tracked, the subsequent return for isTracked should be true. Otherwise, false.
    * Cases
        * `userID`: 1, `exID`: 12

        curl --data "userid=1&exid=12&key=SoftCon2018" http://138.197.49.155:8000/api/fitness/istracked/

        curl --data "userid=1&exid=12&key=SoftCon2018" http://138.197.49.155:8000/api/fitness/toggletracked/

        * You can also add a new userexercise to the database to ensure that it becomes 1 the first time you toggle it.
* For getting tracked exercises:
    * Route
        * `/api/fitness/tracked`
    * Procedure
        * Pass userID to the given route
    * Cases
        * For User 1:

         curl --data "userid=1&key=SoftCon2018" http://138.197.49.155:8000/api/fitness/tracked/

        * Try the things we do for `getTrackedExercises` in the unit tests
    * Expected result
        * See unit tests

#### Who Did What

Lucy Newman and Gregory Howlett-Gomez worked on this part of the project. Lucy wrote the functions in `Scripts/fitnessTest.py`, for tracking and un-tracking exercises, getting a list of exercises for a fitness test, and adding a fitness test result to the database. Gregory wrote the functions in `Scripts/log.py` for determining frequency of a exercise movements from accelerometer log data. They wrote test cases for their code in '`Tests/testFitnessTest.py` and `Tests/testLog.py`, respectively.

#### Changes

We made the following significant changes:
- Added a userexercises table to the database for saving results from a fitness test. The previous method required saving a list of exercises in a single cell, and it seemed beneficial to set it up as separate rows so that we could get fitness test results from the database, or add them, in a single query.
- Removed the fitness test functionality from the `User` class. Now that the userexercises are a separate database, it is unnecessary to have this functionality in the `User` class. Keeping it in the `User` class would require making an extra database call to get `User`, parsing the resulting JSON, and passing it to a constructor. We save those function calls by removing this functionality from the `User` class.
- Removed the `UserExercise` class altogether. Since we aren't storing the fitness test results as a list in the users database, we decided to work directly with the `userexercises` database, and not create a class, to avoid unnecessary steps in creating it.
- Removed the associated tests and added new tests in `Tests/testFitnessTest.py` for our current version.

## Goals, Themes, and Competitions

#### Description

For this iteration, we focused on setting up the general goals, themes, and competitions infrastructure as well as integrating changes to them with the database (competitions is not fully tested and implemented in this iteration since it will be focused on in iteration 2):

* A user can add and remove goals. The `addGoal()` and `removeGoal()` methods allow the user to specify goals geared towards certain muscle groups and categories

* A user can add and remove themes. These are based on specific genres or artists, and the user can choose how many workouts use the theme is used for.

* (A user can create, join, remove, and leave competitions. These can have specific exercises added to them, the amount of time they span can be edited, participants can be added or removed, and a winner(s) is eventually chosen) (will finalize in iteration 2)

#### Acceptance Tests

We did not yet write API routes for goals, themes, and competitions. This section implements higher-level functionality that depends a lot on the other groups, so we decided to hold off on writing routes for this until the second iteration.

#### Who Did What

Julia Xu and Jessica Wang worked on this part of the project. Julia added methods for the driver.py file to allow users to add/remove goals/themes/competitions and have those changes be reflected in the database, tests for those functions (seen in testDriver.py)the theme and goal classes (Theme.py, Goal.py) and unit tests for both (testTheme.py, testGoal.py). Jessica added the competition (Competition.py) class and unit tests for it (testCompetition.py) and also worked on tests for add/remove goals, themes, and competitions for users (testUser.py).

#### Changes

We did not see any significant changes from our original proposal, though while we do have functions for editing goals like `addCategory` and `addMuscleGroup` and `editGoalDescription` that are implemented in goal.py, we decided not to test those functions in the acceptance tests yet since they are not mandatory, and users can still benefit effectively from the motivating properties of goals by just adding and removing them. We also did not implement getting fitness info because that was naturally more focused on by the Fitness Test and Apple Watch team, and it would have been superfluous for us to have worked on it as well; it is possible in iteration 2 we will combine Goals and Fitness tests more cohesively to enhance the user experience and help users make goals based on their current level of fitness and their fitness test results.
