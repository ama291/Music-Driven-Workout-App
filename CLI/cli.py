#!/usr/bin/env python3

import click
from regex import split
from Scripts.fitnessTest import *

dbURL = "http://138.197.49.155:5000/api/database/"
key = "SoftCon2018"


@click.group()
def cli():
    pass

def trackOrUntrack(userID, exID, exName):
    tracked = isTracked(userID, exID)
    if tracked:
        prompt = "Do you want to remove this exercise from your tracked exercises?"
    else:
        prompt = "Do you want to add this exercise to your tracked exercises?"
    if click.confirm(prompt):
        if exID in list(map(lambda x:x[0], getUserExercises(userID))):
            toggleTracked(userID, exID)
        else:
            click.echo("You don't have trials of this exercise")
            click.echo("If this were an iPhone you would have just added one, so this wouldn't happen")

def testEx(userID, exID):
    ex = getExerciseFromID(exID)
    name = ex[1]
    click.echo(name)
    click.echo("Do this exercise for 30 seconds as fast as you can")
    if not click.confirm("Begin?"):
        click.echo("Skipping exercise")
        return
    click.echo("If this were an iPhone you would do the exercise now, holding your phone")
    click.echo("Let's pretend you did it anyways")
    click.echo("If this were an iPhone we would show the frequency and add it to the database")
    trackOrUntrack(userID, exID, name)
    click.echo("Done with exercise '%s'" % name)

@click.command()
def testExercise():
    userID = click.prompt("Enter userID", type=int)
    exID = click.prompt("Enter exercise ID", type=int)
    testEx(userID, exID)


def exAndIDStr(exArray):
    string = "%d -- %s\n" % (exArray[0], exArray[1])
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

@click.command()
def fitnessTest():
    userID = click.prompt("Enter userID", type=int)
    categoriesPrompt = getCategoriesPrompt()
    categories = split(",\s*", click.prompt(categoriesPrompt, type=str))
    numEx = click.prompt("How many exercises do you want to test on?", type=int)
    trackedPrompt = getChoseTrackedString(userID, numEx, categories)
    tracked = list(map(lambda x: int(x), split("\s*", click.prompt(trackedPrompt, type=str))))
    if len(tracked) > numEx:
        click.echo("You can't have more than %d suggested exercises. Truncating." % numEx)
        tracked = tracked[:numEx]
    test = getFitnessTest(categories, numEx, tracked)
    click.echo("Your fitness test has the following exercises:")
    for t in test:
        click.echo("\t%s" % t[1])
    if not click.confirm("Begin workout?"):
        ## TODO, we may want to add more options here
        return
    for t in test:
        testEx(userID, t[0])
    click.echo("Done with fitness test")


cli.add_command(testExercise)
cli.add_command(fitnessTest)

def main():
    cli()

if __name__ == '__main__':
    main()