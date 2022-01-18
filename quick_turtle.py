"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A subclass of Turtle with two new methods and add some initial settings
   when an instance generated
"""

import turtle
from puz_setting import PuzzleSetting


TURTLE_SIZE = PuzzleSetting.get_instance().quick_turtle_size


class QuickTurtle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.initialize_quick_turtle()

    def initialize_quick_turtle(self):
        """
        Method initialize_quick_turtle:
            Settings of a turtle for quick drawing. Combine to a method for
            convenient
        :return: None
        """
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.pensize(TURTLE_SIZE)

    def draw_rectangle(self, width, height):
        """
        Method draw_rectangle:
            draw a rectangle with given width and height. The top-left corner
            of the rectangle is where the turtle at
        :param width: a number (integer or float). Width of rectangle
        :param height: a number (integer or float). Height of rectangle
        :return: None
        """
        self.setheading(0)
        self.forward(width)
        self.right(90)
        self.forward(height)
        self.right(90)
        self.forward(width)
        self.right(90)
        self.forward(height)
