import datetime
from dateutil import tz
import os
URGENT = "\033[;31m" # Red
HIGH   = "\033[;33m" # Yellow
MEDIUM = "\033[;32m" # Green
LOW    = "\033[;37m" # White


# Set up the date objects that will be needed
UTC = tz.gettz('UTC')
LOCAL = tz.tzlocal()
today = datetime.datetime.now()

def get_date(due_at):
    date_string = str(due_at).replace('T',' ')
    date = datetime.datetime.strptime(f'{date_string}', '%Y-%m-%d %H:%M:%SZ')
    date = date.replace(tzinfo=UTC)
    local_due_date = date.astimezone(LOCAL)
    return datetime.datetime.strptime(f'{local_due_date.year}-{local_due_date.month}-{local_due_date.day}', '%Y-%m-%d')

def get_dir(file_location):
    current_loc, file_name = os.path.split(os.path.abspath(__file__))
    return f'{current_loc}/{file_location}'


