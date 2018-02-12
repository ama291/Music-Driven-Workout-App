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

### Wokring Out

#### Description

#### Acceptance Tests

#### Who Did What

#### Changes

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

#### Acceptance Tests

#### Who Did What

#### Changes