# Milestone 3b Progress

## Running our code

Please see the information in the `README` file in the root directory of our repository for instructions on how to set up our code for testing.


### Testing our iOS code

The functions using accelerometer data need to be tested on the iPhone. To run the iOS app on your phone, connect your phone to your computer with a USB, and in Xcode 9.2, open our project. You will need to enter our Apple ID and password. Please ask someone in our group if you need this information. You can then go into your phone's settings > general > device management (at least for my version of iOS), and trust our app. You can then press Run from Xcode, and the app should open in your phone. The UI will then guide you through the process of acceptance testing our function that determines the frequency of motion.

### `curl` acceptance tests

Since we haven't focused on the UI yet, the acceptance tests can be performed via `curl` requests to our API. We describe in the sections below the commands for the requests, and the expected result. See `Docs/3b-documentation-original.md` for a detailed description of how `curl` acceptance tests can be run. Now that we have implemented a console app (described below), we don't intend our acceptance tests to be run through `curl` commands.

### Console app acceptance tests

We now have a console app that can be used to test the fitness test and work out features. It can be run by the following: 

1. In one terminal, source setup.sh and env/bin/actvate
2.  From this terminal, from the root directory of our project, run sh server.sh to run the local server
3.  Open another terminal. Don't source setup.sh, because at this point the virtual environment can only been activated in one terminal at a time
4.  From the other terminal, from the root directory of our project, run the command `python3 -m CLI.cli --help`
5. If there are dependencies you are missing, such as the python Click module which allows for an interactive console app, then you will need to install them on your computer with `pip3 install _`
6. Repaeat seps 4-5 until 4 is successful
7. When 4 is successful, you will be given a list of commands that you can test. This should include `fitnesstest`, `testexercise`, and `workout`. 
    * `fitnesstest` accepts user information for what kind of fitness test they want, creates the fitness test, and then guides them through each exercise, allowing them to add or remove tracked exercises after the test.
    * `testexercise` is the fitness test for a single exercise with a given exercise ID (A number between 1 and around 1000).
    * `workout` allows a user to start a workout and then pause, save, or quit, in any order.


## Implementation details

### Front End & Infrastructure

The server, API, and testing infrastructure is described above.

#### Description of Front End

Our main focus in this iteration was the development of the API routes. Our biggest changes can be found in server.py and our documentation for what functions our API works with and how to call those functions through the API can be found in our API/templates/index.html file. This is hosted on our server at http://138.197.49.155:8000/. We also did some more database infrastructure work. The database is hosted at http://138.197.49.155:5000/. Additionally, we helped the other groups get set up using the database and API.

Additionally, we began creating a basic iOS app interface, though this was not our main focus for this iteration. We expect to have this much more fully developed in the next iteration as more back-end work has completed been developed.

Implementing the API routes in server.py was handled by Alex. Documentation was handled by Chris. Test inputs for the API acceptance tests were provided by individuals from each of the other departments.

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

For this iteration, we focused on setting up a back end for fitness testing with the following use cases:

* A user can begin a fitness test. The `getFitnessTest()` function creates a list of exercises from the exercises database table that will be recommended to the user for the test.

* A user can complete an exercise in a fitness test. There will be a button for them to begin the test in the front end, that causes the phone to begin collecting accelerometer logs. These logs are sent to the server to be analyzed for frequency. `processMotionData()` calls `Log.getFrequency()` to determine a frequency from the result, and then saves it to the database along with a timestamp.

* A user can view their results to a fitness test. Since results are displayed by date, we can show how they have progressed over time on an exercise. The front end will later display these results as a graph.

* A user can track and untrack exercises. `checkTracked()` checks whether an exercise is tracked and the UI will (in the second iteration) display a button to Add or Remove the exercise from tracked, depending on the result. `toggleTracked()` toggles the bit in the userexercise database, indicating whether the exercise is tracked. When they begin the test, they are specifically asked which tracked exercises they want to complete, and the rest of the exercises are recommended randomly from the database.


#### Who Did What

Lucy Newman and Gregory Howlett-Gomez worked on this part of the project. Lucy wrote the functions in `Scripts/fitnessTest.py`, for tracking and un-tracking exercises, getting a list of exercises for a fitness test, and adding a fitness test result to the database. Gregory wrote the functions in `Scripts/log.py` for determining frequency of a exercise movements from accelerometer log data. They wrote test cases for their code in '`Tests/testFitnessTest.py` and `Tests/testLog.py`, respectively.

#### Changes

We made the following significant changes:
- Added a userexercises table to the database for saving results from a fitness test. The previous method required saving a list of exercises in a single cell, and it seemed beneficial to set it up as separate rows so that we could get fitness test results from the database, or add them, in a single query.
- Removed the fitness test functionality from the `User` class. Now that the userexercises are a separate database, it is unnecessary to have this functionality in the `User` class. Keeping it in the `User` class would require making an extra database call to get `User`, parsing the resulting JSON, and passing it to a constructor. We save those function calls by removing this functionality from the `User` class.
- Removed the `UserExercise` class altogether. Since we aren't storing the fitness test results as a list in the users database, we decided to work directly with the `userexercises` database, and not create a class, to avoid unnecessary steps in creating it.
- Removed the associated tests and added new tests in `Tests/testFitnessTest.py` for our current version.

### Goals, Themes, and Competitions

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
