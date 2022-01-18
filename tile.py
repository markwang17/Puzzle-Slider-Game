"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of each single tile of a puzzle. It contains exchange method of two
   tiles and press method to detect if click event occurred
"""


import os
from game_function import error_logging
from puz_setting import PuzzleSetting


SETTING = PuzzleSetting.get_instance()
PUZZLE_TOP_LEFT = (SETTING.puzzle_border[0], SETTING.puzzle_border[1])
MAX_TILE_SIZE = SETTING.max_tile
INTERVAL_BETWEEN_TILE = SETTING.interval_tile


class Tile:
    def __init__(self, file_path, screen, pen, size):
        self.pen = pen
        self.file_path = file_path
        self.error = False
        self.try_to_register_shape(screen)
        self.size = size
        # store stamp_id for later removing the stamp
        self.stamp_id = None
        # the coordinates of puzzle_border (this is able to switch to a
        # class attribute)
        self.puzzle_top_left_x = PUZZLE_TOP_LEFT[0]
        self.puzzle_top_left_y = PUZZLE_TOP_LEFT[1]
        # initialize the coordinates of this tile
        self.top_left_x = None
        self.top_left_y = None
        # initialize the row and column of this tile in the whole puzzle
        self.row = None
        self.col = None
        # Used to record whether border has been painted for this tile
        self.border_painted = False

    def try_to_register_shape(self, screen):
        """
            method try_to_register_shape
                try to register the self.file_path for the given Screen. If the
                file_path is invalid, log error and exit with code 1
            :param screen: A turtle.Screen instance.
            :return: None
        """
        if os.path.isfile(self.file_path):
            screen.register_shape(self.file_path)
            return
        error_logging(f"Malformed puzzle file (tile): {self.file_path}",
                      "Tile.try_to_register_shape()")
        self.error = True

    def map_index_to_stamp(self, row, column):
        """
        method map_index_to_stamp:
            By passing new row and new column of this tile in the whole puzzle,
            this method :
                1) calculate the new coordinates on screen,
                2) draw border of this tile if there's not,
                3) update attributes,
                4) and draw the tile on screen
        :param row: int, the row index of current tile in whole puzzle
        :param column: int, the column index of current tile in whole puzzle
        :return: None
        """
        # (110 - self.size)//2 is for setting the stamp at the center of
        # MAX_TILE_SIZE * MAX_TILE_SIZE block of screen
        stamp_top_left_x = (self.puzzle_top_left_x + column *
                            (MAX_TILE_SIZE + INTERVAL_BETWEEN_TILE) +
                            (MAX_TILE_SIZE - self.size)//2)
        stamp_top_left_y = (self.puzzle_top_left_y - row *
                            (MAX_TILE_SIZE + INTERVAL_BETWEEN_TILE) -
                            (MAX_TILE_SIZE - self.size)//2)
        if not self.border_painted:
            self.draw_border(stamp_top_left_x, stamp_top_left_y)
            self.border_painted = True
        # update four attributes
        self.top_left_x = stamp_top_left_x
        self.top_left_y = stamp_top_left_y
        self.row = row
        self.col = column

        # move the pen to the center of tile and stamp
        self.pen.penup()
        self.pen.goto(stamp_top_left_x + self.size / 2,
                      stamp_top_left_y - self.size / 2)
        self.pen.shape(self.file_path)
        # store stamp_id for later removing the stamp
        self.stamp_id = self.pen.stamp()

    def draw_border(self, x, y):
        """
        method draw_border:
            move the pen to (x,y) and draw a border for self
        :param x: a number (integer or float), x coordinate of top_left corner
        :param y: a number (integer or float), y coordinate of top_left corner
        :return: None
        """
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.draw_rectangle(self.size, self.size)

    def exchange_with(self, another_tile):
        """
        method exchange_with
            remove old stamp, exchange row and column index of two tiles, and
            draw stamp at new coordinate
        :param another_tile: Another Tile instance
        :return: None
        """
        self.pen.clearstamp(self.stamp_id)
        another_tile.pen.clearstamp(another_tile.stamp_id)
        # temporary save row and col attributes for later call of method
        new_row, new_column = another_tile.row, another_tile.col
        another_tile.map_index_to_stamp(self.row, self.col)
        self.map_index_to_stamp(new_row, new_column)

    def press(self, click_x, click_y):
        """
        method press:
            Detect whether the coordinate is within the current tile by
            input, and return Boolean
        :param click_x: a number (integer or float). The x coordinate of point
        :param click_y: a number (integer or float). The y coordinate of point
        :return: Boolean
        """
        return (self.top_left_x <= click_x <= self.top_left_x + self.size and
                self.top_left_y >= click_y >= self.top_left_y - self.size)
