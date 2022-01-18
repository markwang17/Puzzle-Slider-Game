"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of the leaderboard showing in the puzzle slider game.
"""


from quick_turtle import QuickTurtle
from game_function import error_logging
from puz_setting import PuzzleSetting


SETTING = PuzzleSetting.get_instance()


class Leaderboard:
    def __init__(self, err_msg):
        self.player_move_list = []
        # error_message, an instance of Message
        self.err_msg = err_msg
        self.load_data()
        self.write_on_screen()

    def load_data(self):
        """
        method load_data:
            load data from leaderboard. If error occur, log the error.
            for each line of leaderboard.txt, create a list of moves (int) and
            name, and append to self.player_move_list.
        :return: None
        """
        try:
            with open('leaderboard.txt', 'r', encoding='utf8') as data:
                for line in data:
                    try:
                        move_num, name = line.split(',')
                    except ValueError:
                        error_logging('Malformed leaderboard.txt.',
                                      'Leaderboard.load_data()')
                        self.player_move_list = []
                        break
                    self.player_move_list.append([int(move_num), name])
        except OSError:
            error_logging('Could not open leaderboard.txt.',
                          'Leaderboard.load_data()')
            self.err_msg.draw()
            # create new blank leaderboard.txt
            with open('leaderboard.txt', 'w', encoding='utf8'):
                pass

    def prepare_string(self):
        """
        method prepare_string:
            it prepares a string of all records in leaderboard.txt. it only
            gets called when there is some record in leaderboard.txt
        :return: a string
        """
        list_string = []
        for one_player_list in self.player_move_list:
            # truncate long name
            if len(one_player_list[1]) > SETTING.name_limit_screen:
                list_string.append(
                    f'{one_player_list[0]}: {one_player_list[1][:10]}\n')
            else:
                list_string.append(f'{one_player_list[0]}: '
                                   f'{one_player_list[1]}')
        string = '\n'.join(list_string)
        return string

    def write_data(self, move, name):
        """
        Method write_data:
            Detect if the leaderboard.txt is needed to be updated, if needed,
            update
        :param move: int, the num of moves player took to finish the puzzle
        :param name: str, string of the player's name
        :return: None
        """
        # It might be frustrated for users who have long-name, so the limit of
        # record is set higher. (though the screen shows 10 char at max)
        name = name[:SETTING.name_limit_save]
        # prevent potential error (because data use ',' as seperator)
        name = name.replace(',', '')
        # if the first record
        if not self.player_move_list:
            with open('leaderboard.txt', 'w', encoding='utf8') as data:
                data.write(f'{move},{name}\n')
            return
        # if not beat the top ten records
        if len(self.player_move_list) == 10 and \
                move > self.player_move_list[-1][0]:
            return
        current_record_wrote = False
        with open('leaderboard.txt', 'w', encoding='utf8') as data:
            for one_player_list in self.player_move_list[:9]:
                # write behind the former records that have the same moves
                if one_player_list[0] > move and not current_record_wrote:
                    data.write(f'{move},{name}\n')
                    current_record_wrote = True
                data.write(f'{one_player_list[0]},{one_player_list[1]}')
            if not current_record_wrote:
                data.write(f'{move},{name}\n')

    def write_on_screen(self):
        """
        method write_on_screen:
            create a temporary QuickTurtle and draw on the screen
        :return: None
        """
        temp_pen = QuickTurtle()
        temp_pen.goto(SETTING.leaderboard_border[0] + SETTING.topten_shift[0],
                      SETTING.leaderboard_border[1] + SETTING.topten_shift[1])
        temp_pen.write('Top 10:', font=('Arial', 16, 'normal'))
        # 35*len(self.player_move_list) adjust location for different length
        # the int 35 may change with the font-size (IDK math function of these)
        temp_pen.goto(SETTING.leaderboard_border[0] + SETTING.record_shift[0],
                      SETTING.leaderboard_border[1] + SETTING.record_shift[1]
                      - 35 * len(self.player_move_list))
        # fail to load data or data txt is blank
        if not self.player_move_list:
            temp_pen.write('no data found', font=('Arial', 16, 'normal'))
        else:
            string = self.prepare_string()
            temp_pen.write(string, font=('Arial', 13, 'normal'))
