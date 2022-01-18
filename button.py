"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of normal buttons, and a class of circle buttons. Creates a
   temporary QuickTurtle and draws on the screen when an instance is generated.
"""


from quick_turtle import QuickTurtle
from game_function import error_logging
import os


class Button:
    def __init__(self, center_x, center_y, file_path, screen,
                 width, height):
        # x and y coordinates of the center
        self.center_x = center_x
        self.center_y = center_y
        self.file_path = file_path
        self.try_to_register_shape(screen)
        # half_width and half_height are for the later 'press' method
        self.half_width = width // 2
        self.half_height = height // 2
        # draw when generated
        self.draw(file_path)

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
        error_logging(f"Missing Button gif resource: {self.file_path}",
                      "Button.try_to_register_shape()")
        exit(1)

    def draw(self, file_path):
        """
        method draw:
            draw the button with a temporary pen.
        :return: None
        """
        pen = QuickTurtle()
        pen.goto(self.center_x, self.center_y)
        pen.shape(file_path)
        pen.stamp()

    def press(self, click_x, click_y):
        """
        method press:
            Detect whether the coordinate is within the current button by
            input, and return Boolean
        :param click_x: a number (integer or float). The x coordinate of point
        :param click_y: a number (integer or float). The y coordinate of point
        :return: Boolean
        """
        return (self.center_x - self.half_width <= click_x <= self.center_x +
                self.half_width and self.center_y - self.half_height <=
                click_y <= self.center_y + self.half_height)


class CircleButton(Button):
    def press(self, click_x, click_y):
        """
        method press:
            override method of superclass. Detect whether the coordinate is
            within the current button by input, and return Boolean
        :param click_x: a number (integer or float). The x coordinate of point
        :param click_y: a number (integer or float). The y coordinate of point
        :return: Boolean
        """
        x_distance = click_x - self.center_x
        y_distance = click_y - self.center_y
        dis_to_center = ((x_distance ** 2) + (y_distance ** 2)) ** 0.5
        return self.half_width >= dis_to_center
