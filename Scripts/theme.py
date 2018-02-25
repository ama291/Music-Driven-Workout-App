#!/usr/bin/env python3

class Theme(object):
    """
    Class for creating themes that users can use to help motivate themselves.
    Themes can be based around an artist or genre.
    Users can choose how many workouts the theme is used for.
    """
    def __init__(self, name, theme, spotifyId, numWorkouts):
        """
        name = name of track, artist, genre
        theme = 'track','artist','genre'
        spotifyId = spotify id if it's track or artist, name of genre if it's genre
        """
        if(name is None or name == ""):
            raise ValueError("name can't be empty or invalid string")
        if(numWorkouts is None):
            raise ValueError("numWorkouts can't be None")
        if(numWorkouts < 0):
            raise ValueError("numWorkouts can't less than 0")
        if(theme is None or theme == "" or theme not in ["track","artist","genre"]):
            raise ValueError("invalid theme")
        if(type(spotifyId)!= str):
            raise ValueError("spotify id needs to be string")
        self.name = name
        self.theme = theme
        self.spotifyId = spotifyId
        self.numWorkouts = numWorkouts

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        string = "%s Theme: %s to be used for next %d workouts" % (self.theme, self.name, self.numWorkouts)
        return string

    def editThemeNumWorkouts(self, _numWorkouts):
        if(_numWorkouts < 0):
            print("numWorkouts can't be less than 0")
            return False
        else:
            self.numWorkouts = _numWorkouts
            return True
