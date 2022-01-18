"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   A class of the 15-puzzle. Each time the main game load a new puzzle, create
   a new instance of Puzzle
"""


import random
from tile import Tile
from thumbnail import Thumbnail
from game_function import error_logging
import copy
from puz_setting import PuzzleSetting


SETTING = PuzzleSetting.get_instance()


class Puzzle:
    def __init__(self, file_path, screen, pen):
        # dictionary of all data in .puz file
        self.info_dict = {}
        # dictionary of all tiles instances, keys are from 0 to (num_tiles - 1)
        self.tiles_dict = {}
        # Two-dimensional list to store all keys of tiles.
        # It's mapping the position of each tile on screen
        self.tiles_map = []
        # Similar to tiles_map, this is the wining state of puzzle.
        # Build correct_map is for easier checking and easier resetting.
        self.correct_map = []
        # the index of blank tile in tiles_map.
        self.cur_blank = (-1, -1)
        # blank_dict_key is just for finding initial cur_blank.
        # the blank.gif may not always be the last tile in puz file,
        # so store the key then we can find the initial cur_blank
        self.blank_dict_key = -1
        self.number_of_tiles = None
        self.sqrt_num_of_tiles = None
        self.file_path = file_path
        self.data_error = False
        self.load_info_dict()
        # if successfully load .puz file (still might be a malformed .puz file)
        if not self.data_error:
            self.detect_improper_data()
            self.load_thumbnail(screen, pen)
            self.load_tile_objects(screen, pen)

        if not self.data_error:
            self.build_random_map()
            self.build_correct_map()

    def load_info_dict(self):
        """
        method load_info_dict:
            only called once when generated. load the data to dictionary
            from metadata .puz file
        :return: None
        """
        with open(self.file_path, 'r', encoding='utf8') as puz_info:
            for line in puz_info:
                try:
                    info_key, info_value = line.split()
                except ValueError:
                    error_logging(f"Malformed puzzle file (line): "
                                  f"{self.file_path}",
                                  "Puzzle.load_info_dict()")
                    self.data_error = True
                info_key = info_key.strip(':')
                if info_value[-9:] == "blank.gif":
                    self.blank_dict_key = int(info_key) - 1
                self.info_dict[info_key.lower()] = info_value.lower()

    def detect_improper_data(self):
        """
        method detect_improper_data:
            only called once when generated. Detect malformed number and
            size data. And load number and square root number attribute.
        :return: None
        """
        if self.info_dict['number'] != '16' and self.info_dict['number'] != \
                '9' and self.info_dict['number'] != '4':
            self.data_error = True
            error_logging(f"Malformed puzzle file (number): {self.file_path}",
                          "Puzzle.detect_improper_data()")
        self.number_of_tiles = int(self.info_dict['number'])
        self.sqrt_num_of_tiles = int(self.number_of_tiles ** 0.5)
        if not self.info_dict['size'].isdigit() or \
                int(self.info_dict['size']) < SETTING.min_tile or \
                int(self.info_dict['size']) > SETTING.max_tile:
            self.data_error = True
            error_logging(f"Malformed puzzle file (size): {self.file_path}",
                          "Puzzle.detect_improper_data()")

    def load_tile_objects(self, screen, pen):
        """
        method load_tile_objects:
            only called once when generated. create Tile objects for each gif
            and save in the self.tiles_dict
        :param screen: A turtle.Screen instance
        :param pen: A turtle.Turtle instance
        :return: None
        """
        for i in range(self.number_of_tiles):
            file_path = self.info_dict[str(i + 1)]
            self.tiles_dict[i] = Tile(file_path, screen, pen,
                                      int(self.info_dict['size']))
            if self.tiles_dict[i].error:
                self.data_error = True
                break

    def load_thumbnail(self, screen, pen):
        """
        method load_thumbnail:
            only called once when generated. create Thumbnail objects without
            saving. (the stamp can be removed by pen later)
        :param screen: A turtle.Screen instance
        :param pen: A turtle.Turtle instance
        :return: None
        """
        temp_save = Thumbnail(self.info_dict['thumbnail'], screen, pen)
        if temp_save.error:
            self.data_error = True

    def reset(self):
        """
        method reset:
            reset tiles_map to correct_map. update cur_blank to the
            bottom-right block. Then draw all tiles on the screen.
        :return: None
        """
        self.tiles_map = copy.deepcopy(self.correct_map)
        self.cur_blank = (self.sqrt_num_of_tiles - 1,
                          self.sqrt_num_of_tiles - 1)

        self.draw_all_tiles()

    def build_random_map(self):
        """
        method build_random_map:
            only called once when generated. use randint to generate initial
            tiles_map.
        :return: None
        """
        # create a Two-dimensional list of -1
        self.tiles_map = [[-1 for _ in range(self.sqrt_num_of_tiles)] for __ in
                          range(self.sqrt_num_of_tiles)]
        # create a list of keys, each time randomly pop one and
        # store it in tiles_map
        random_list = list(range(self.number_of_tiles))
        # create a counter of the length of random_list
        counter_of_rest = self.number_of_tiles
        for i in range(self.number_of_tiles):
            # transfer i to index of Two-dimensional list
            x_index = i // self.sqrt_num_of_tiles
            y_index = i % self.sqrt_num_of_tiles
            counter_of_rest -= 1
            random_id = random_list.pop(random.randint(0, counter_of_rest))
            # if the key is blank_dict_key, update the map index tuple
            # of blank tile
            if random_id == self.blank_dict_key:
                self.cur_blank = (x_index, y_index)
            self.tiles_map[x_index][y_index] = random_id

    def build_correct_map(self):
        """
        method build_correct_map:
            only called once when generated. create initial correct_map.
            (e.g. [[0,1,2],[3,4,5],[6,7,8]] for sqrt_num_of_tiles == 3)
        :return: None
        """
        self.correct_map = []
        for i in range(self.sqrt_num_of_tiles):
            self.correct_map.append(list(range(i * self.sqrt_num_of_tiles,
                                               self.sqrt_num_of_tiles *
                                               (i + 1))))

    def test_winning(self):
        return self.tiles_map == self.correct_map

    def draw_all_tiles(self):
        """
        method draw_all_tiles:
            iterate Two-dimensional key list, get corresponding value
        (tile object) and call draw method for each tile
        :return: None
        """
        for x in range(len(self.tiles_map)):
            for y in range(len(self.tiles_map)):
                tile_index = self.tiles_map[x][y]
                self.tiles_dict[tile_index].map_index_to_stamp(x, y)

    def cur_blank_to_neighbours(self):
        """
        method cur_blank_to_neighbours:
            get all tile objects that 'next to' current blank tile in
            Two-dimensional key list, return all objects as a list
        :return: a list of Tile objects
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        output_objects_list = []
        for x_diff, y_diff in directions:
            neighbour_x = self.cur_blank[0] + x_diff
            neighbour_y = self.cur_blank[1] + y_diff
            # out of bound
            if neighbour_x < 0 or neighbour_x >= self.sqrt_num_of_tiles \
                    or neighbour_y < 0 \
                    or neighbour_y >= self.sqrt_num_of_tiles:
                continue
            neighbour_dict_key = self.tiles_map[neighbour_x][neighbour_y]
            output_objects_list.append(self.tiles_dict[neighbour_dict_key])
        return output_objects_list

    def exchange_with_blank(self, from_x, from_y):
        """
        method exchange_with_blank:
            given the x and y index of a tile object key in the map, exchange
            this tile with current blank tile, and update new state of puzzle
        :param from_x: int, valid x index of a tile object key in the map
        :param from_y: int, valid y index of a tile object key in the map
        :return: None
        """
        # according to given index, find the key of object in the map
        from_dict_key = self.tiles_map[from_x][from_y]
        # according to the cur_blank attribute to find the key of blank tile
        to_dict_key = self.tiles_map[
            self.cur_blank[0]][self.cur_blank[1]]
        # call exchange_with method
        self.tiles_dict[from_dict_key].\
            exchange_with(self.tiles_dict[to_dict_key])
        # update(exchange) the location of these tiles' key in the map
        self.tiles_map[from_x][from_y] = to_dict_key
        self.tiles_map[self.cur_blank[0]][self.cur_blank[1]] = from_dict_key
        # update new location of blank tile
        self.cur_blank = (from_x, from_y)
    