from canvasapi import Canvas
import canvasapi
from utils import *

def run():
    # Load commandline args and settings
    parser = get_parser()
    args = parser.parse_args()
    config = get_config(args.settings)


    # Canvas object and students classes
    canvas = Canvas(config['url'], config['api'])
    
    courses = config['classes']
    days = args.days if args.weeks == 0 else args.weeks * 7

    if args.reset:
        print('Resetting output space')
        config['longest_desc'] = 0
        config['longest_clas'] = 0
    
    for course_number in courses:
        course = canvas.get_course(course_number)


        '''This is working from here down'''
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

                    if len(a.name) > config['longest_desc'] and len(co[1]) < 15:
                        config['longest_desc'] = len(a.name)                    

                    if len(co[1]) > config['longest_clas'] and len(co[1]) < 15:
                        config['longest_clas'] = len(co[1])

                    out += f"{co[2][0:config['longest_desc']]: <{config['longest_clas']}} | {str(a.name)[0:config['longest_desc']]: <{config['longest_desc']}} | {delta.days + 1: <{2}} days left | {date.strftime('%A'): <9} | {a.html_url}" + LOW
                    todo_hw[delta.days].append(out)

            except Exception as e:
                # print(e) # this will occur if the due date is None
                pass


    # Print the Homework assignments
    i = 1
    print(f"    {str('Course'): <{config['longest_clas']}} | {str('Description'): <{config['longest_desc']}} | Days Left    | Day       | Link to Assignment")
    for days_left in sorted(todo_hw.keys()): # sort by days    
        for assn in todo_hw[days_left]:
            print(f'{str(i) + ".": <3} {assn}')
            i += 1

    if args.announcements != config["announcements"] and args.announcements is not None: # 5 is default
        config["announcements"] = args.announcements

    if args.reset:
        print()
        print('Re-run program for newly formatted output')

    
    print(f'\n---Announcements for last {config["announcements"]} days---\n')

    for course_number in courses:
        course = canvas.get_course(course_number)

        announcments = course.get_discussion_topics(only_announcements=True)
        
        for i in announcments:
            announce_date = get_date(i.created_at)
            delta = announce_date - now
            co = str(course)
            co = co.split(' ')
            if delta.days >= config['announcements']*-1:
                out = f'{str(co[1]): <{config["longest_clas"]}} | {(str(i)[0:config["longest_desc"] - 3] + "..."): <{config["longest_desc"]}} | {(delta.days * -1)} days ago   | {i.html_url}'
                todo_an[delta.days].append(out)
                
    c = 1
    for days_left in sorted(todo_an.keys())[::-1]:
        for annoucement in todo_an[days_left]:
            print(f'{(str(c) + "."): <{3}} {annoucement}')
            c += 1
    save_settings(config, args.settings)


# 
if __name__ == "__main__":
    run()
