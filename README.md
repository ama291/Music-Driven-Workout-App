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

* A user can begin a fitness test. The `User.testFitness()` method creates a list of UserExercise objects that will be recommended to them for the test.

* A user can complete an exercise in a fitness test. There will be a button for them to begin the test in the front end, that causes the phone to begin collecting accelerometer logs. These logs are sent to the server to be analyzed for frequency. `UserExercise.addFrequency()` saves a frequency to a `UserExercise`, which will be added to the `User.tracked` or `User.untracked`, depending on if they are tracking the exercise. The computation is done in `Log.getFrequency()`.

* A user can view their results to a fitness test. Since results are displayed by date, we can show how they have progressed over time on an exercise. The front end can display a graph.

* A user can track (`User.trackEx()`) and untrack (`User.untrackEx()`) exercises. When they begin the test, they are specifically asked which tracked exercises they want to complete, and the rest of the exercises are recommended randomly from the database.

#### Acceptance Tests

* For beginning a fitness test:
    * TODO
* For determining frequency from a log:
    * TODO
* For getting sorted results:
    * TODO
* For tracking and un-tracking:
    * TODO

#### Who Did What

Lucy Newman and Gregory Howlett-Gomez worked on this part of the project. (TODO: more specific details)

#### Changes

TODO

### Goals, Themes, and Competitions

#### Description

For this iteration, we focused on setting up the general goals, themes, and competitions infrastructure as well as integrating changes to them with the database:

* A user can add and remove goals. The `addGoal()` and `removeGoal()` methods allow the user to specify goals geared towards certain muscle groups and categories

* A user can add and remove themes. These are based on specific genres or artists, and the user can choose how many workouts use the theme

* A user can create, join, and leave competitions. These can have specific exercises added to them, the amount of time they span can be edited, participants can be added or removed, and a winner(s) is eventually chosen

#### Acceptance Tests

* For creating a goal:
    * TODO
* For creating a theme:
    * TODO
* For creating a competition:
    * TODO
* For removing a goal:
    * TODO
* For removing a theme:
    * TODO
* For removing a competition:
    * TODO

#### Who Did What

Julia Xu and Jessica Wang worked on this part of the project. Julia added methods for the driver.py file to allow users to add/remove goals/themes/competitions, the theme and goal classes and unit tests for both. Jessica added the competition class and unit tests for it.

#### Changes
