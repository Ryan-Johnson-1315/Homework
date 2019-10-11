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
today = datetime.datetime.now()

now = datetime.datetime.now()
todo = defaultdict(list)


def get_date(due_at):
    date_string = str(due_at).replace('T',' ')
    date = datetime.datetime.strptime(f'{date_string}', '%Y-%m-%d %H:%M:%SZ')
    date = date.replace(tzinfo=UTC)
    local_due_date = date.astimezone(LOCAL)
    return datetime.datetime.strptime(f'{local_due_date.year}-{local_due_date.month}-{local_due_date.day}', '%Y-%m-%d')


def get_dir(file_location):
    current_loc, file_name = os.path.split(os.path.abspath(__file__))
    return f'{current_loc}/{file_location}'


def get_parser():
    parser = argparse.ArgumentParser(prog='hw.py')
    parser.add_argument('-s', '--settings', help="Path to settings file", default="settings/settings.json", type=str, metavar='')
    parser.add_argument('-d', '--days', help="Show number of assignments due in this amount of days", type=int, default=21, metavar='')
    parser.add_argument('-w', '--weeks', help="Show number of assignments due in this amount of weeks", type=int, default=0, metavar='')
    parser.add_argument('-r', '--reset', help="(true or false). Reset the formatting space. Use this when there is extra whitespace in the outputted formatting, then re-run script",
                    default=False, type=bool, metavar='')
    parser.add_argument('-a', '--announcements', help='Number of days to go back and look at annoucements')

    return parser

def get_config(location):
    location = get_dir(location)
    return json.load(open(location, 'r'))

def save_settings(settings, location):
    location = get_dir(location)
    json.dump(settings, open(location, 'w')) # sys.path[0] works because of line 10
    
def get_date(due_at):
    date_string = str(due_at).replace('T',' ')
    date = datetime.datetime.strptime(f'{date_string}', '%Y-%m-%d %H:%M:%SZ')
    date = date.replace(tzinfo=UTC)
    local_due_date = date.astimezone(LOCAL)
    return datetime.datetime.strptime(f'{local_due_date.year}-{local_due_date.month}-{local_due_date.day}', '%Y-%m-%d')
