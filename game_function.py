"""
   CS5001
   Project
   Fall 2021
   Yuxuan Wang
   Two functions that do not belong to any classes and may be used in later
   versions or other projects.
"""


import os
import time


def get_all_file_by_extension(file_extension):
    """
    Function get_all_file_by_extension:
        get all files with input file extension in current path and return them
        as a list of string
    :param file_extension: A file extension (E.g. '.txt', '.gif')
    :return: a list of string
    """
    path = os.getcwd()
    out_list = []
    f_list = os.listdir(path)
    for each in f_list:
        if os.path.splitext(each)[1] == file_extension:
            out_list.append(each)
    return out_list


def error_logging(error_string, location):
    """
    Function error_logging:
        function for error logging. Print and write the type of error,
        the location that error occurred, and the current time
    :param error_string: A string describes what error occurred
    :param location: A string of the function (method) where the error occurred
    :return: None
    """
    time_str = time.asctime()
    err_str = f'{time_str}: Error: {error_string} LOCATION: {location}\n'
    print(err_str)
    with open('5001_puzzle.err', 'a+', encoding='utf8') as err_log:
        err_log.write(err_str)
