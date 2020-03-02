from canvasapi import Canvas
import canvasapi
import utils

def run():
    # Load commandline args and settings
    parser = utils.get_parser()
    args = parser.parse_args()
    config = utils.get_config(args.settings)

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
        # print(str(course)[12:])


        '''This is working from here down'''
        assignments = course.get_assignments()
        for a in assignments:
            try:
                assignment_name = str(a).split('(')[0]
                due_date, day_of_week = utils.get_date(a.due_at)
                out = ""
                if due_date > -2 and due_date < days:
                    prct = float(due_date) / float(days)
                    if prct < .25:
                        out += utils.URGENT
                    elif prct < .5:
                        out += utils.HIGH
                    elif prct < .75:
                        out += utils.MEDIUM
                    co = str(course)
                    co = co.split(' ')

                    if len(a.name) > config['longest_desc'] and len(a.name) < 10:
                        config['longest_desc'] = len(a.name)                    

                    if len(co[1]) > config['longest_clas'] and len(co[1]) < 10:
                        config['longest_clas'] = len(co[1])

                    out += f"{co[2][0:config['longest_desc']]: <{config['longest_clas']}} | "
                    out += f"{str(a.name)[0:config['longest_desc']]: <{config['longest_desc']}} | "
                    out += f"{due_date + 1: <{2}} days left | "
                    out += f"{day_of_week: <9} | "

                    out += f"{a.html_url}" + utils.LOW
                    utils.todo_hw[due_date].append(out)

            except Exception as e:
                # print(e) # this will occur if the due date is None
                pass


    # Print the Homework assignments
    i = 1
    print(f"    {str('Course'): <{config['longest_clas']}}    | {str('Homework'): <{config['longest_desc']}} |  Days Left   | Day       | Link to Assignment")
    utils.print_assignmentes()

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
            time_till_due = announce_date - now
            co = str(course)
            co = co.split(' ')
            if time_till_due.days >= config['announcements']*-1:
                out = f'{str(co[2])[0:config["longest_clas"] + 4]: <{config["longest_clas"]}} | {(str(i)[0:config["longest_desc"] - 3] + "..."): <{config["longest_desc"]}} | {(time_till_due.days * -1)} days ago   | {i.html_url}'
                todo_an[time_till_due.days].append(out)
                
    c = 1
    for days_left in sorted(todo_an.keys())[::-1]:
        for annoucement in todo_an[days_left]:
            print(f'{(str(c) + "."): <{3}} {annoucement}')
            c += 1
    save_settings(config, args.settings)


# 
if __name__ == "__main__":
    run()
