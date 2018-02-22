Iteration 2 Plan
================

Basic Goals
-----------

*   The most important goal for this iteration is to clean up and integrate what we already have, and create a front end for it
*   A few new features are being added as well, but integrating existing features should be prioritized
*   We can still make changes on this. However, since a lot of these features are interconnected now, we should let the group chat know first!

Higher priority implementation
------------------------------

### Infrastructure

*   Mock database (Gregory -- Milestone 4a)

*   Ask TA/Professor

*   Redoing User database and class (Lucy -- Milestone 4a)
*   Returning dictionaries from database queries -- everyone
*   Getting Spotify access token (Jessica and Julia -- can begin in Milestone 4a)

*   Having premium
*   Storing (?) refresh token

*   [https://developer.spotify.com/web-api/authorization-guide/](https://www.google.com/url?q=https://developer.spotify.com/web-api/authorization-guide/&sa=D&ust=1519334535014000&usg=AFQjCNGqFfJiDSSWEdY0BWoMqHAZHrztxQ)

*   Add competitions database (Jessica and Julia -- can begin in Milestone 4a)

### Front End

*   iOS front end for all use cases, beginning with those fully implemented in Iteration 1 (begin in Milestone 4a)
*   Restricting access by level

### Work Out

*   Basic matching of workout with tempo data

*   Assume that the Fitness Test group will supply you with a rate at which the user can do an exercise
*   You can multiply it by a factor or multiple of the time signature (for 4/4 time, song tempo can be 2, 4, 8, times the exercise tempo for  3/4 time, 3 or 6 times)

*   Consider themes
*   Considering a list of songs/artists/genres they want to work out to, based on recommendations from the goals/themes/competitions group

### Fitness Test, etc.

*   Improve motion data processing algorithm to get more accurate frequency (Gregory)
*   Route for previous trials (Lucy - Milestone 4a probably)
*   “Add exercise” option -- variation of the fitness test where they add the exercise at the exact pace they want to do it at (Lucy)
*   Accept muscle groups and equipment for choosing the fitness test (Lucy)
*   Getting desired tempo for a song (Lucy)
*   Collecting heart rate data and determining if they’re within their target heart rate range for cardio workouts (Gregory)
*   Setting level by number of fitness tests completed (Lucy)

### Goals, Themes, Competitions

*   Spotify SDK
*   Collecting information on which of their top Spotify songs/artists/genres they want to work out to for suggesting themes
*   Integrating goals and themes with workouts
*   Levels - reevaluate benchmarks

Lower priority
--------------

*   Making a separate database for competitions
*   Integrating competitions with the user experience
*   Login/authentication (Alex and Chris)

Database Changes
----------------

### Users table

We have made the following changes to the `users` table in our database, and we have made the consequent changes to the User class, tests, and `getUser` function in `driver.py`

|Column             |Type        |Change              |
|-----------------------------------------------------|
|id                 |INTEGER     |INTEGER PRIMARY KEY |
|name               |VCHAR(50)   |\[remove\]          |
|spotifyUsername    |VCHAR(50)   |\[add\]             |
|height             |INT         |\[add\]             |
|weight             |INT         |\[add\]             |
|birthyear          |YEAR        |\[add\]             |
|tracked            |VCHAR(9999) |\[remove\]          |
|untracked          |VCHAR(9999) |\[remove\]          |
|goals              |VCHAR(9999) |                    |
|themes             |VCHAR(9999) |                    |
|competition        |VCHAR(9999) |INT FOREIGN KEY REF |
|inProgressWorkouts |VCHAR(9999) |                    |
|savedWorkouts      |VCHAR(9999) |                    |

UserExercises table
-------------------

We have added a column for whether a `userexercise` is intended to be interpreted as the exact time a user wants to work out at (from the new Add Exercise feature) or as a fitness test, which is done more quickly than the user may want to work out at.

Competitions table
------------------

If the goals/themes/competitions group has time to implement competitions, they will make a new table with the following rows. This is a lower priority, however, and this group will focus first on helping out with getting the Spotify SDK set up, and doing themes and goals.

|Column              |Type                 |
|------------------------------------------|
|id                  |INT PRIMARY KEY      |
|name                |VCHAR(50)            |
|description         |VCHAR(50)            |
|members             |INT FOREIGN KEY REFS |
|admins              |INT FOREIGN KEY REFS |
|startDate           |DATE                 |
|endDate             |DATE                 |
|exercises           |INT FOREIGN KEY REFS |
|Winner (maybe)      |INT FOREIGN KEY REF  |