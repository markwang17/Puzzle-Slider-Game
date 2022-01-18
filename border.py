"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of borders in the puzzle game. Creates a temporary QuickTurtle and
   draws on the screen when an instance is generated.
"""


from quick_turtle import QuickTurtle


class Border:
    def __init__(self, top_left_x, top_left_y, width, height, color="black"):
        # x and y coordinates of top left corner
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height
        self.color = color
        # draw when generated
        self.draw()

    def draw(self):
        """
        method draw:
            draw the border with a temporary pen.
        :return: None
        """
        pen = QuickTurtle()
        pen.goto(self.top_left_x, self.top_left_y)
        pen.pencolor(self.color)
        pen.pendown()
        pen.draw_rectangle(self.width, self.height)



