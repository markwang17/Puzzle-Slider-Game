# Puzzle-Slider-Game
This is a project of CS5001 in fall 2021.
_________________________
Project description

This is a project of CS5001 in fall 2021.
Puzzle Slider Game is a game based on turtle library where a player tries to
match the solution by sliding pieces vertically or horizontally on a board.Cancel changes
The project is heavily based on object-oriented programming.

__________________________
Classes

I designed several classes for this project. They are:

    1. MainGame:
        this class is designed to run the whole game. It contains methods that
        for user interface, game behavior, and user interaction. It also
        contains many instances from other classes as attributes.

    2. Border:
        A class of borders in the puzzle game. Creates a temporary QuickTurtle
        and draws on the screen when an instance is generated.

    3. Button:
        A class of normal buttons, and a class of circle buttons. Creates a
        temporary QuickTurtle and draws on the screen when an instance is
        generated.

    4. Leaderboard:
        A class of the leaderboard showing in the puzzle slider game.

    5. Message:
        A class of message boxes. Creates a temporary QuickTurtle and draws on
        the screen when the corresponding event occurred in the main game.

    6. PuzzleSetting:
        A class of most changeable settings of sliding puzzle game. May reduce
        some readability, easier to change settings instead.

    7. Puzzle:
        A class of the 15-puzzle. A Puzzle instance should any information of
        a single puzzle. Create new Puzzle instance when the main game load
        new puzzle file.

    8. QuickTurtle:
        A subclass of Turtle with two new methods and add some initial settings
        when an instance generated.

    9. Thumbnail:
        A class of the thumbnail of a puzzle. Uses the given pen to draw on the
        screen when generated.

    10. Tile:
        A class of each single tile of a puzzle. It contains exchange method of
        two tiles and press method to detect if click event occurred

__________________________
Functions

There are two functions I designed in game_function.py that do not belong to
any classes and may be used in later versions or other projects.

    1. get_all_file_by_extension:
        get all files with input file extension in current path and return them
        as a list of string

    2. error_logging:
        function for error logging. Print and write the type of error,
        the location that error occurred, and the current time

__________________________
Error and exit code

There are a few type of errors that may occur for this program. Some of them
won't crack the program, the others will. For errors that may crack program,
the program log the error then exit with exit code.

    1. Missing Button gif resource: crucial error, exit with code 1
    2. Malformed leaderboard.txt: non-crucial error
    3. Fail to open leaderboard.txt: non-crucial error, create new txt
    4. Default File mario.puz does not exist: crucial error, exit with code 2
    5. new .puz file does not exist: non-crucial error, stop loading
    6. Missing Message gif resource: crucial error, exit with code 3
    7. Malformed puzzle file (line, number, size, thumbnail, tile):
        1) crucial error for init, exit with code 4
        2) non-crucial error for new .puz file loading, stop loading progress
