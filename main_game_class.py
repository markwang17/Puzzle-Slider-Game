"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   Class of the main game.
"""


import turtle
from quick_turtle import QuickTurtle
from puzzle import Puzzle
from border import Border
from button import Button, CircleButton
from message import Message
from leaderboard import Leaderboard
import game_function as gf
from puz_setting import PuzzleSetting


SETTING = PuzzleSetting.get_instance()
FST_BOR = SETTING.puzzle_border
SND_BOR = SETTING.leaderboard_border
TRD_BOR = SETTING.button_border
R_BUT = SETTING.reset_button
L_BUT = SETTING.load_button
Q_BUT = SETTING.quit_button


class MainGame:
    def __init__(self):
        # dictionary of button objects that need to be checked for click event
        self.check_button_elements = {}
        # dictionary of tile objects that need to be checked for click event
        self.check_click_elements = {}
        # initialize a Screen object for the game
        self.screen = turtle.Screen()
        self.screen.setup(SETTING.screen_size[0],
                          SETTING.screen_size[1])
        # initialize two QuickTurtle for later game functions
        self.turtle_for_tiles = QuickTurtle()
        self.turtle_for_player_moves = QuickTurtle()
        self.turtle_for_player_moves.goto(SETTING.draw_player_moves_at[0],
                                          SETTING.draw_player_moves_at[1])
        # initialize dictionary of message objects and show splash screen
        self.messages = {}
        self.load_messages()
        self.messages["splash_screen"].draw()
        # initialize user input (name, and winning goal of moves)
        self.player_name = ''
        self.move_left = SETTING.moves_setting[0]
        self.initial_user_input()
        # initialize border and button instances
        self.create_border_and_buttons()
        # initialize leaderboard object
        self.leaderboard = Leaderboard(self.messages['leaderboard_error'])
        # initialize counter for moves and load_string for load new puzzle
        self.player_moves = 0
        self.load_string = ''
        # load initial puzzle object and start the game
        self.puzzle = None
        self.start_the_game()

    def start_the_game(self):
        """
        method start_the_game:
            try to load initial puz file, if succeeded,
            start the game (screen.onclick). If not, exit with code 1.
        :return: None
        """
        if 'mario.puz' in gf.get_all_file_by_extension('.puz'):
            self.puzzle = Puzzle('mario.puz', self.screen,
                                 self.turtle_for_tiles)
            if not self.puzzle.data_error:
                self.load_puzzle()
                self.screen.onclick(self.register_click)
                turtle.done()
            else:
                exit(4)
        else:
            self.messages['file_error'].draw()
            gf.error_logging(f'Default File mario.puz does not exist',
                             'MainGame.__init__()')
            exit(2)

    def load_messages(self):
        """
        method load_messages:
            initialize dictionary of message objects
        :return: None
        """
        load_list = ["credits", "file_error", "file_warning",
                     "leaderboard_error", "Lose", "quitmsg",
                     "splash_screen", "winner"]
        for string in load_list:
            self.messages[string] = Message(string, self.screen)

    def initial_user_input(self):
        """
        method initial_user_input:
            pop window for asking user input.
        :return: None
        """
        self.player_name = self.screen.textinput('CS5001 Puzzle Slide',
                                                 'Your Name: (only show first '
                                                 f'{SETTING.name_limit_screen}'
                                                 f' char)')
        # if canceled or empty string
        if not self.player_name:
            self.player_name = 'Anonymous'
        self.move_left = self.screen.numinput('CS5001 Puzzle Slide - Moves',
                                              'Enter the number of moves '
                                              '(changes) you want (5-200)?',
                                              SETTING.moves_setting[0],
                                              SETTING.moves_setting[1],
                                              SETTING.moves_setting[2])
        # if canceled
        if not self.move_left:
            self.move_left = SETTING.moves_setting[0]
        # convert potential decimal(float)
        self.move_left = int(self.move_left)

    def update_player_moves(self):
        """
        method update_player_moves:
            every time the player_moves changes, call this method to update the
            new stat on the screen. For a new puzzle, write 'Click to start'
            instead.
        :return: None
        """
        self.turtle_for_player_moves.clear()
        if self.player_moves == 0:
            self.turtle_for_player_moves.write('Click to start',
                                               font=('Arial', 16, 'normal'))
        else:
            self.turtle_for_player_moves.write(f'Player Moves: '
                                               f'{self.player_moves} / '
                                               f'{self.move_left}',
                                               font=('Arial', 16, 'normal'))

    def create_border_and_buttons(self):
        """
        method create_border_and_buttons:
            only called once in init method. create boarder and button objects
            and draw them on the screen. For border, we don't need to save them
            for this project. For button, save them in dict for later checking.
        :return: None
        """
        Border(FST_BOR[0], FST_BOR[1], FST_BOR[2], FST_BOR[3], FST_BOR[4])
        Border(SND_BOR[0], SND_BOR[1], SND_BOR[2], SND_BOR[3], SND_BOR[4])
        Border(TRD_BOR[0], TRD_BOR[1], TRD_BOR[2], TRD_BOR[3], TRD_BOR[4])
        reset_b = CircleButton(R_BUT[0], R_BUT[1], 'Resources/resetbutton.gif',
                               self.screen, R_BUT[2], R_BUT[3])
        load_b = Button(L_BUT[0], L_BUT[1], 'Resources/loadbutton.gif',
                        self.screen, L_BUT[2], L_BUT[3])
        quit_b = Button(Q_BUT[0], Q_BUT[1], 'Resources/quitbutton.gif',
                        self.screen, Q_BUT[2], Q_BUT[3])
        self.check_button_elements['reset'] = reset_b
        self.check_button_elements['load'] = load_b
        self.check_button_elements['quit'] = quit_b

    def load_puzzle(self):
        """
        method load_puzzle:
            the combined callings of method for each time load a new puzzle
            (include initial one)
        :return: None
        """
        self.player_moves = 0
        self.puzzle.draw_all_tiles()
        self.update_check_tile_elements()
        self.update_player_moves()

    @staticmethod
    def prepare_load_string(str_list):
        """
        staticmethod prepare_load_string:
            prepare string to show in the popping window
        :param str_list: a list of str, each str should be a file name
        :return: a string
        """
        message = 'Enter the name of the puzzle you wish to load. ' \
                  'Choices are:\n'
        message += '\n'.join(str_list)
        return message

    def new_puzzle(self):
        """
        method new_puzzle:
            ask user input and try to load a new puzzle
        :return: None
        """
        # generate puz_list each time because files may change during the game
        puz_list = gf.get_all_file_by_extension('.puz')
        # only show first 10 (just warning, do not log error)
        if len(puz_list) > SETTING.name_limit_screen:
            puz_list = puz_list[:SETTING.name_limit_screen]
            self.messages['file_warning'].draw()
        self.load_string = self.prepare_load_string(puz_list)
        new_puzzle_name = self.screen.textinput('Load Puzzle',
                                                self.load_string)
        if new_puzzle_name in gf.get_all_file_by_extension('.puz'):
            # Delete the turtle_for_tiles’s drawings from the screen
            temp_puzzle = Puzzle(new_puzzle_name, self.screen,
                                 self.turtle_for_tiles)
            if not temp_puzzle.data_error:
                self.turtle_for_tiles.reset()
                self.turtle_for_tiles.initialize_quick_turtle()
                self.puzzle = temp_puzzle
                self.puzzle.load_thumbnail(self.screen, self.turtle_for_tiles)
                self.load_puzzle()
            else:
                self.messages['file_error'].draw()
        else:
            # if canceled or not a puz file name
            self.messages['file_error'].draw()
            gf.error_logging(f'File {new_puzzle_name} does not exist',
                             'MainGame.new_puzzle()')

    def register_click(self, x, y):
        """
        method register_click:
            a function for screen.onclick method. It detects if the given point
            lie in any button or tile currently checked. and trigger the
            corresponding event
        :param x: a number, x coordinates of the clicked point on the canvas
        :param y: a number, y coordinates of the clicked point on the canvas
        :return: None
        """
        output = None
        # first check if the given point lies in any buttons
        for key, button in self.check_button_elements.items():
            click_event_detected = button.press(x, y)
            if click_event_detected:
                # for a point, at most one item can be clicked (or missed all)
                output = key
                # break if found
                break
        # if missed all buttons, check all tiles
        if not output:
            for key, button in self.check_click_elements.items():
                click_event_detected = button.press(x, y)
                if click_event_detected:
                    output = key
                    # break if found
                    break
        if not output:
            return
        # trigger the corresponding method if a click detected
        # if it's a tuple, then exchange the tile of this tuple with blank tile
        if type(output) is tuple:
            self.move_of_puzzle(output[0], output[1])
        elif output == 'quit':
            self.messages["quitmsg"].draw()
            self.messages["credits"].draw()
            self.screen.bye()
        elif output == 'reset':
            # clear all tiles stamp
            self.turtle_for_tiles.clearstamps(-self.puzzle.number_of_tiles)
            self.puzzle.reset()
            self.update_check_tile_elements()
        elif output == 'load':
            self.new_puzzle()

    def add_check_element(self, tile_name, tile):
        # add single tile to the check_click_elements dict
        self.check_click_elements[tile_name] = tile

    def update_check_tile_elements(self):
        """
        method update_check_tile_elements:
            add all 'neighbour' instance of current blank tile to the
            check_click_elements dict, the key is a tuple of index in tiles_map
        :return: None
        """
        self.check_click_elements = {}
        list_of_tiles = self.puzzle.cur_blank_to_neighbours()
        for i in range(len(list_of_tiles)):
            self.add_check_element((list_of_tiles[i].row,
                                    list_of_tiles[i].col), list_of_tiles[i])

    def test_lose(self):
        return self.move_left == self.player_moves

    def move_of_puzzle(self, from_x, from_y):
        """
        method move_of_puzzle:
            call this method when each time a neighbour instance of blank tile
            is clicked. exchange two tiles, update number of moves, and detect
            if the player win or lose the game
        :param from_x: int, the x index of a tile instance in tiles_map
        :param from_y: int, the y index of a tile instance in tiles_map
        :return: None
        """
        self.puzzle.exchange_with_blank(from_x, from_y)
        # update new tiles that need to be checked(new neighbours)
        self.update_check_tile_elements()
        self.player_moves += 1
        self.update_player_moves()
        if self.puzzle.test_winning():
            self.leaderboard.write_data(self.player_moves, self.player_name)
            self.messages["winner"].draw()
            self.messages["credits"].draw()
            exit(0)
        elif self.test_lose():
            self.messages["Lose"].draw()
            self.messages["credits"].draw()
            exit(0)
