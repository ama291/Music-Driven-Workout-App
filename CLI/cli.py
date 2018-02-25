#!/usr/bin/env python3

import click
from regex import split
# from Scripts.fitnessTest import ...
# from Scripts.driver import quitWorkout
from Scripts.dbfunctions import testDB, realDB
from CLI.apiCalls import isTracked, toggleTracked, getFitnessTest, \
 getTrackedExercises, getExerciseFromID, getUserExercises, getPreviousResults,\
 getWorkout, startWorkout, pauseWorkout, quitWorkout, saveWorkout, workoutsSaved, \
 startSavedWorkout, unsaveWorkout

dbURL = testDB
key = "SoftCon2018"

@click.group()
def cli():
    pass

def showPrevious(userID, exID):
    click.echo("Your previous results are")
    prev = getPreviousResults(userID, exID)
    for p in prev:
        click.echo("%s: %f" % (p["timestamp"], p["rate"]))


def trackOrUntrack(userID, exID, exName):
    tracked = isTracked(userID, exID)
    if tracked:
        prompt = "Do you want to remove this exercise from your tracked exercises?"
    else:
        prompt = "Do you want to add this exercise to your tracked exercises?"
    if click.confirm(prompt):
        if exID in list(map(lambda x:x["id"], getUserExercises(userID))):
            toggleTracked(userID, exID)
        else:
            click.echo("You don't have trials of this exercise")
            click.echo("If this were an iPhone you would have just added one, so this wouldn't happen")


def testEx(userID, exID):
    ex = getExerciseFromID(exID)
    name = ex["name"]
    click.echo(name)
    click.echo("Do this exercise for 30 seconds as fast as you can")
    if not click.confirm("Begin?"):
        click.echo("Skipping exercise")
        return
    click.echo("If this were an iPhone you would do the exercise now, holding your phone")
    click.echo("Let's pretend you did it anyways")
    click.echo("If this were an iPhone we would show the frequency and add it to the database")
    click.echo("Great job, you've completed %s" % name)
    showPrevious(userID, exID)
    trackOrUntrack(userID, exID, name)
    click.echo("Done with exercise '%s'" % name)

@click.command()
def testExercise():
    userID = click.prompt("Enter userID", type=int)
    exID = click.prompt("Enter exercise ID", type=int)
    testEx(userID, exID)


def exAndIDStr(exercise):
    string = "%d -- %s\n" % (exercise["id"], exercise["name"])
    return string

def getChoseTrackedString(userID, numExercises, categories):
    string = "You have the following tracked exercises in this category\n"
    tracked = getTrackedExercises(userID, categories=categories)
    for t in tracked:
        string += "\t%s" % exAndIDStr(t)
    string += "Please list the IDs of the ones you want to use, separated by comma\n"
    string += "You may select at most %d exercises from this list" % numExercises
    return string

def getCategoriesPrompt():
    categories = ["Cardio", "Olympic Weightlifting", "Plyometrics", "Powerlifting", "Strength", "Stretching", "Strongman"]
    string = "Enter categories separated by a single comma from the following options:\n"
    for cat in categories:
        string += "\t%s\n" % cat
    return string

@click.command
def addExercise():
    categories = getCategoriesList()
    category = click.prompt()

@click.command()
def fitnessTest():
    userID = click.prompt("Enter userID", type=int)
    categoriesPrompt = getCategoriesPrompt()
    categories = split(",\s*", click.prompt(categoriesPrompt, type=str))
    numEx = click.prompt("How many exercises do you want to test on?", type=int)
    trackedPrompt = getChoseTrackedString(userID, numEx, categories)
    tracked = list(map(lambda x: int(x), split(",\s*", click.prompt(trackedPrompt, type=str))))
    if len(tracked) > numEx:
        click.echo("You can't have more than %d suggested exercises. Truncating." % numEx)
        tracked = tracked[:numEx]
    test = getFitnessTest(categories, numEx, tracked)
    click.echo("Your fitness test has the following exercises:")
    for t in test:
        click.echo("\t%s" % t["name"])
    if not click.confirm("Begin workout?"):
        ## TODO, we may want to add more options here
        return
    for t in test:
        testEx(userID, t["id"])
    click.echo("Done with fitness test")

def showRes(res):
    if res == 0:
        click.echo("Success")
    elif res == 1:
        click.echo("Database failure")
    elif res == 2:
        click.echo("Failure")

def CLIstartWorkout(userID, workout):
    click.echo("Starting workout")
    res = startWorkout(userID, workout)
    showRes(res)
    return res

def chooseSavedWorkout(userID):
    click.echo("You have the following saveud workouts")
    saved = list(workoutsSaved(userID))
    i = 1
    for w in saved:
        click.echo("\t%d -- %s" % (i, str(w)))
        i += 1
    choice = click.prompt("Please select a saved workout", type=int)
    click.echo(type(saved))
    click.echo(choice-1)
    return saved[choice-1]

def CLIstartSavedWorkout(userID):
    saved = chooseSavedWorkout(userID)
    click.echo("Starting saved workout")
    res = startSavedWorkout(userID, saved)
    return res

def CLIunsaveSavedWorkout(userID):
    saved = chooseSavedWorkout(userID)
    click.echo("Unsaving workout")
    res = unsaveWorkout(userID, saved)
    return saved


def CLIsaveWorkout(userID, workout):
    click.echo("Saving workout")
    res = saveWorkout(userID, workout)
    showRes(res)
    return res

def CLIpauseWorkout(userID, workout):
    click.echo("Pausing workout")
    res = pauseWorkout(userID, workout)
    showRes(res)
    return res

def CLIquitWorkout(userID, workout):
    click.echo("Quitting workout")
    res = quitWorkout(userID, workout)
    showRes(res)
    return res


def promptNext(options):
    string = "What do you want to do next?\n"
    i = 1
    for opt in options:
        string += "\t%d -- %s\n" % (i, opt)
        i += 1
    string += "\t0 -- exit\n"
    command = click.prompt(string, type=int)
    return command

def CLIgetWorkout():
    userID = click.prompt("Enter userID", type=int)
    equipment = ["Body Only", "Kettlebells"]
    duration = 60
    difficulty = "Beginner"
    categories = ["Cardio","Stretching"]
    workout = getWorkout(userID, equipment, duration, difficulty, categories=categories)
    wid = workout["ID"]
    while True:
        command = promptNext(["Start Workout", "Start Saved Workout", "Save Workout", "Pause Workout", "Quit Workout", "Unsave Workout"])
        click.echo("command: %d" % command)
        if command == 0:
            break
        if command == 1:
            CLIstartWorkout(userID, workout)
        if command == 2:
            CLIstartSavedWorkout(userID)
        if command == 3:
            CLIsaveWorkout(userID, wid)
        if command == 4:
            CLIpauseWorkout(userID, wid)
        if command == 5:
            CLIquitWorkout(userID, wid)
        if command == 6:
            CLIunsaveSavedWorkout(userID)


@click.command()
def workout():
    CLIgetWorkout()

cli.add_command(testExercise)
cli.add_command(fitnessTest)
cli.add_command(workout)

def main():
    cli()

if __name__ == '__main__':
    main()