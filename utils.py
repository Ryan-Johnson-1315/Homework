import datetime
from dateutil import tz
import os
import argparse
import json
from collections import defaultdict

URGENT = "\033[;31m" # Red
HIGH   = "\033[;33m" # Yellow
MEDIUM = "\033[;32m" # Green
LOW    = "\033[;37m" # White


# Set up the date objects that will be needed
UTC = tz.gettz('UTC')
LOCAL = tz.tzlocal()

now = datetime.datetime.now()
todo_hw = defaultdict(list)
todo_an = defaultdict(list)
todo_em = defaultdict(list)

def get_date(due_at):
    date_string = str(due_at).replace('T',' ')
    date = datetime.datetime.strptime(f'{date_string}', '%Y-%m-%d %H:%M:%SZ')
    date = date.replace(tzinfo=UTC)
    local_due_date = date.astimezone(LOCAL)
    tmp = datetime.datetime.strptime(f'{local_due_date.year}-{local_due_date.month}-{local_due_date.day}', '%Y-%m-%d')
    due_date = tmp - now
    return due_date.days, tmp.strftime("%A")


def get_dir(file_location):
    current_loc, file_name = os.path.split(os.path.abspath(__file__))
    return f'{current_loc}/{file_location}'


def get_parser():
    parser = argparse.ArgumentParser(prog='hw.py')
    parser.add_argument('-s', '--settings', help="Path to settings file", default="settings/my_settings.json", type=str, metavar='')
    parser.add_argument('-d', '--days', help="Show number of assignments due in this amount of days", type=int, default=21, metavar='')
    parser.add_argument('-w', '--weeks', help="Show number of assignments due in this amount of weeks", type=int, default=0, metavar='')
    parser.add_argument('-r', '--reset', help="Reset the formatting space. Use this when there is extra whitespace in the outputted formatting, then re-run script",
                    default=False, action='store_true', type=bool, metavar='')
    parser.add_argument('-a', '--announcements', help='Number of days to go back and look at annoucements', type=int, metavar='')

    return parser

def get_config(location):
    location = get_dir(location)
    return json.load(open(location, 'r'))

def save_settings(settings, location):
    location = get_dir(location)
    json.dump(settings, open(location, 'w')) # sys.path[0] works because of line 10

def print_assignmentes():
    i = 1
    for days_left in sorted(todo_hw.keys()): # sort by days    
        for assn in todo_hw[days_left]:
            print(f'{str(i) + ".": <3} {assn}')
            i += 1

def print_announcements():
    c = 1
    for days_left in sorted(todo_an.keys())[::-1]:
        for annoucement in todo_an[days_left]:
            print(f'{(str(c) + "."): <{3}} {annoucement}')
            c += 1
    