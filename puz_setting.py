"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of most changeable settings of sliding puzzle game. May reduce
   some readability, easier to change settings instead.
"""


class PuzzleSetting:
    instance = None

    def __init__(self):
        # init pen size of QuickTurtle class
        self.quick_turtle_size = 5

        # setting of message box
        self.message_linger_time = 3
        self.draw_message_at = (0, 0)

        # screen setting
        self.screen_size = (800, 700)

        # 'xcor and ycor of top-left corner, width, height, color' of borders
        self.puzzle_border = (-355, 280, 450, 450, 'black')
        self.leaderboard_border = (115, self.puzzle_border[1], 250,
                                   self.puzzle_border[3], 'blue')
        bb_width = (self.leaderboard_border[0] - self.puzzle_border[0] +
                    self.leaderboard_border[2])
        self.button_border = (self.puzzle_border[0], -190, bb_width,
                              100, 'black')

        # the xcor and ycor of the player moves info(change with button_border)
        self.draw_player_moves_at = (self.button_border[0] + 20,
                                     self.button_border[1] -
                                     self.button_border[3] // 2 - 15)

        # 'xcor and ycor of center, width and height of gif' of buttons
        button_y = self.button_border[1] - (self.button_border[3] // 2)
        button_distance = 110
        self.reset_button = (90, button_y, 80, 80)
        self.load_button = (self.reset_button[0] + button_distance, button_y,
                            80, 76)
        self.quit_button = (self.load_button[0] + button_distance, button_y,
                            80, 53)

        # position shift of 'Top 10' and records (better not change this)
        self.topten_shift = (10, -30)
        self.record_shift = (self.topten_shift[0] + 5,
                             self.topten_shift[1] - 50)

        # average size of thumbnail gif (thumbnails' size should be similar)
        # use this to calculate the distance shifting from the border's corner
        self.thumbnail_size = 100

        # max and min of acceptable tile size and the interval between tiles
        # (max should be calculated from size of puzzle_border (and interval),
        # for this project, just set it as 110 for convenience)
        self.max_tile = 110
        self.min_tile = 50
        self.interval_tile = 3

        # 'default value, lower limit, upper limit' of user moves input
        self.moves_setting = (50, 5, 200)

        # the limit of name length on screen and save data
        # (name_limit_save should >= name_limit_screen)
        self.name_limit_screen = 10
        self.name_limit_save = 30

    @classmethod
    def get_instance(cls):
        # create an instance as a class attribute if there's not
        if not cls.instance:
            cls.instance = PuzzleSetting()
        return cls.instance
