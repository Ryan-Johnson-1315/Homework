import os
import json
import sys
import datetime
from collections import defaultdict
from canvasapi import Canvas
from utils import *
import argparse


parser = argparse.ArgumentParser(prog='hw.py')
parser.add_argument('-s', '--settings', help="Path to settings file", default="settings/settings.json", type=str, metavar='')
parser.add_argument('-d', '--days', help="Show number of assignments due in this amount of days", type=int, default=21, metavar='')
parser.add_argument('-w', '--weeks', help="Show number of assignments due in this amount of weeks", type=int, default=0, metavar='')
parser.add_argument('-r', '--reset', help="(true or false). Reset the formatting space. Use this when there is extra whitespace in the outputted formatting, then re-run script",
                default=False, type=bool, metavar='')

args = parser.parse_args()

# Load default settings file
args.settings = get_dir(args.settings)
settings = json.load(open(args.settings, 'r'))
courses = settings['classes']
canvas = Canvas(settings['url'], settings['api'])

# Other variables that we will need
now = datetime.datetime.now()
todo = defaultdict(list)


def get_date(due_at):
    date_string = str(due_at).replace('T',' ')
    date = datetime.datetime.strptime(f'{date_string}', '%Y-%m-%d %H:%M:%SZ')
    date = date.replace(tzinfo=UTC)
    local_due_date = date.astimezone(LOCAL)
    return datetime.datetime.strptime(f'{local_due_date.year}-{local_due_date.month}-{local_due_date.day}', '%Y-%m-%d')

# if the user sets the weeks or days -> use it, if not -> use default of 21 days
recent = args.days if args.weeks == 0 else args.weeks * 7

if args.reset:
    print('Resetting output space')
    settings['longest_desc'] = 0
    settings['longest_clas'] = 0

for course_number in courses:
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    for a in assignments:
        try:
            date = get_date(a.due_at)
            delta = date - now
            out = ""
            if delta.days > -1 and delta.days < recent:
                prct = float(delta.days) / float(recent)
                if prct < .25:
                    out += URGENT
                elif prct < .5:
                    out += HIGH
                elif prct < .75:
                    out += MEDIUM
                co = str(course)
                co = co.split(' ')

                if len(a.name) > settings['longest_desc']:
                    settings['longest_desc'] = len(a.name)
                

                if len(co[1]) > settings['longest_clas']:
                    settings['longest_clas'] = len(co[1])
                # .strftime('%b-%d')
                out += f"{co[1]: <{settings['longest_clas']}} | {str(a.name): <{settings['longest_desc']}} | {delta.days + 1: <{2}} days left | {date.strftime('%A'): <9} | {a.html_url}" + LOW
                todo[delta.days].append(out)

        except Exception as e:
            #print(e) # this will occur if the due date is None
            pass

str_course = "Course"
str_descri = "Description"
str_daysl = "Days Left"


i = 1
print(f"    {str('Course'): <{settings['longest_clas']}} | {str('Description'): <{settings['longest_desc']}} | Days Left    | Day       | Link to Assignment")
for days_left in sorted(todo.keys()):
    for assn in todo[days_left]:
        print(f'{str(i) + ".": <3} {assn}')
        i += 1

if args.reset:
    print()
    print('Re-run program for newly formatted output')

json.dump(settings, open(args.settings, 'w')) # sys.path[0] works because of line 10
