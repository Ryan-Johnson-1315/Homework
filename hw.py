from canvasapi import Canvas
from utils import *

def run():
    # Load commandline args and settings
    parser = get_parser()
    args = parser.parse_args()
    config = get_config(args.settings)

    # Canvas object and students classes
    canvas = Canvas(config['url'], config['api'])
    
    courses = config['classes']


    # if the user sets the weeks or days -> use it, if not -> use default of 21 days
    days = args.days if args.weeks == 0 else args.weeks * 7

    if args.reset:
        print('Resetting output space')
        config['longest_desc'] = 0
        config['longest_clas'] = 0

    for course_number in courses:
        course = canvas.get_course(course_number)
        assignments = course.get_assignments()
        for a in assignments:
            try:
                date = get_date(a.due_at)
                delta = date - now
                out = ""
                if delta.days > -2 and delta.days < days:
                    prct = float(delta.days) / float(days)
                    if prct < .25:
                        out += URGENT
                    elif prct < .5:
                        out += HIGH
                    elif prct < .75:
                        out += MEDIUM
                    co = str(course)
                    co = co.split(' ')

                    if len(a.name) > config['longest_desc']:
                        config['longest_desc'] = len(a.name)                    

                    if len(co[1]) > config['longest_clas']:
                        config['longest_clas'] = len(co[1])

                    out += f"{co[1]: <{config['longest_clas']}} | {str(a.name): <{config['longest_desc']}} | {delta.days + 1: <{2}} days left | {date.strftime('%A'): <9} | {a.html_url}" + LOW
                    todo[delta.days].append(out)

            except Exception as e:
                # print(e) # this will occur if the due date is None
                pass


    # Print the Homework assignments
    i = 1
    print(f"    {str('Course'): <{config['longest_clas']}} | {str('Description'): <{config['longest_desc']}} | Days Left    | Day       | Link to Assignment")
    for days_left in sorted(todo.keys()): # sort by days    
        for assn in todo[days_left]:
            print(f'{str(i) + ".": <3} {assn}')
            i += 1

    # Print the annoucements
    print('\n---ANNOUNCEMENTS---\n')
    config['annoucements'] = args.announcements

    c = 1
    for course_number in courses:
        course = canvas.get_course(course_number)

        announcments = course.get_discussion_topics(only_announcements=True)
        
        for i in announcments:
            announce_date = get_date(i.created_at)
            delta = announce_date - now
            co = str(course)
            co = co.split(' ')
            if delta.days > config['announcements']*-1:
                print(f'{(str(c) + "."): <{3}} {str(co[1]): <{config["longest_clas"]}} | {(str(i)[0:config["longest_desc"] - 3] + "..."): <{config["longest_desc"]}} | {(delta.days * -1) - 1} days ago   | {i.html_url}')
                c += 1

    if args.reset:
        print()
        print('Re-run program for newly formatted output')

    save_settings(config, args.settings)


# 
if __name__ == "__main__":
    run()