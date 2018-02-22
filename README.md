# Music-Driven-Workout-App
CS 220 Music Driven Workout App Project

The Flask API  with documentation is live at http://138.197.49.155:8000/

Upon pushing to master the Jenkins instance at http://138.197.49.155:7777 will re-install dependencies and restart the Flask app.

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
