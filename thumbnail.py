"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of the thumbnail of a puzzle. Uses the given pen to draw on the
   screen when generated.
"""


from game_function import error_logging
import os
from puz_setting import PuzzleSetting


SETTING = PuzzleSetting.get_instance()
LEADERBOARD_TOP_LEFT_COORDINATE = (SETTING.leaderboard_border[0] +
                                   SETTING.leaderboard_border[2],
                                   SETTING.leaderboard_border[1])
DEFAULT_THUMBNAIL_SHIFT = - SETTING.thumbnail_size // 2


class Thumbnail:
    def __init__(self, file_path, screen, pen):
        self.file_path = file_path
        self.error = False
        self.try_to_register_shape(screen)
        if not self.error:
            self.draw(pen)

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
        error_logging(f"Malformed puzzle file (Thumbnail): {self.file_path}",
                      "Thumbnail.try_to_register_shape()")
        self.error = True

    def draw(self, pen):
        """
        method draw:
            draw the thumbnail gif with the given pen
        :return: None
        """
        pen.penup()
        pen.goto(LEADERBOARD_TOP_LEFT_COORDINATE[0] + DEFAULT_THUMBNAIL_SHIFT,
                 LEADERBOARD_TOP_LEFT_COORDINATE[1] + DEFAULT_THUMBNAIL_SHIFT)
        pen.shape(self.file_path)
        pen.stamp()
