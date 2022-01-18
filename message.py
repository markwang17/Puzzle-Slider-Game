"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of message boxes. Creates a temporary QuickTurtle and draws on the
   screen when the corresponding event occurred in the main game.
"""


from quick_turtle import QuickTurtle
import time
from game_function import error_logging
import os
from puz_setting import PuzzleSetting


SETTING_OBJECT = PuzzleSetting.get_instance()
LINGER_TIME = SETTING_OBJECT.message_linger_time
MESSAGE_AT = SETTING_OBJECT.draw_message_at


class Message:
    def __init__(self, file_path, screen):
        file_path = 'Resources/' + file_path + '.gif'
        self.file_path = file_path
        self.try_to_register_shape(screen)

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
        error_logging(f"Missing Message gif resource: {self.file_path}",
                      "Message.try_to_register_shape()")
        exit(3)

    def draw(self):
        """
        method draw:
            draw the message gif with a temporary pen. It lingers on the screen
            for a few seconds before it erased
        :return: None
        """
        temp_pen = QuickTurtle()
        temp_pen.goto(MESSAGE_AT[0], MESSAGE_AT[1])
        temp_pen.shape(self.file_path)
        temp_pen.showturtle()
        stamp_id = temp_pen.stamp()
        time.sleep(LINGER_TIME)
        temp_pen.hideturtle()
        temp_pen.clearstamp(stamp_id)
