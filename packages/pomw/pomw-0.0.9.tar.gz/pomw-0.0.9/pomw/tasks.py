#!/usr/bin/env python3
# -*- python-indent-offset: 4; -*-

from datetime import datetime, timedelta
from itertools import zip_longest

from dateutil.rrule import DAILY, rrule
from taskw import TaskWarrior
from timew import TimeWarrior
from urwid import (
    Columns,
    ExitMainLoop,
    Filler,
    MainLoop,
    Pile,
    Text,
    raw_display,
    set_encoding,
)

from .config import Config
from .exceptions import ArgumentException, TaskNotFoundException
from .model import Entries, Entry, Interval, Pomodoro
from .tdt import Complete, CompleteUnplanned, Empty, Interrupt, Void, VoidUnplanned


class Tasks:
    def __init__(self):
        self.config = Config().config
        self.taskw = TaskWarrior()
        #        self.taskw = TaskWarrior(config_filename="/home/tjaart/Code/pomw/testdata/taskrc")
        if self.config.getboolean("timew", "sync", fallback=True):
            self.timew = TimeWarrior()

        self.duration = self.config.getint("pomodoro", "length", fallback=25)

    def __parse_quantity(self, quantity):
        increment = False
        if quantity[0] == "+":
            increment = True
            quantity = int(quantity[1:])
        else:
            if quantity[0] == "-":
                increment = True
            quantity = int(quantity)

        return quantity, increment

    def __split_project(self, project):
        tags = []
        if "." in project:
            tags.extend([tag for tag in project.split(".")])
        tags.append(project)
        return tags

    def activity(self, action, date):
        print("activity")
        print(date)

    def default(self):
        print("default")

    def delete(self, action, pomodoro):
        print(action)
        print(pomodoro)

    def interrupt(self, action, time, type, task, quantity):
        # TODO: The current implementation only allows for interruptions in the current, unfinished pomodoro
        #       To retroactively add interruptions will require some more work.

        task_id, cur_task = self.taskw.get_task(id=task)
        quantity, increment = self.__parse_quantity(quantity)

        if not task_id:
            raise TaskNotFoundException(task)

        entries = Entries()
        entry = entries.find(date=time.date(), uuid=cur_task["uuid"])
        if entry:
            # If the last pomodoro already has a completed time, create a new pomodoro for the interruption
            if entry.pomodoros[-1].time:
                # TODO: Simplify internal/external if block
                if type == "internal":
                    entry.pomodoros = entry.pomodoros + [
                        Pomodoro(internal_interrupt=quantity)
                    ]
                else:
                    entry.pomodoros = entry.pomodoros + [
                        Pomodoro(external_interrupt=quantity)
                    ]
            else:
                if type == "internal":
                    if increment:
                        entry.pomodoros[-1].internal_interrupt += quantity
                    else:
                        entry.pomodoros[-1].internal_interrupt = quantity
                else:
                    if increment:
                        entry.pomodoros[-1].external_interrupt += quantity
                    else:
                        entry.pomodoros[-1].external_interrupt = quantity

        else:
            # TODO: Simplify internal/external if block
            if type == "internal":
                entry = Entry(
                    uuid=cur_task["uuid"],
                    date=time.date(),
                    pomodoros=[Pomodoro(internal_interrupt=quantity)],
                )
            else:
                entry = Entry(
                    uuid=cur_task["uuid"],
                    date=time.date(),
                    pomodoros=[Pomodoro(external_interrupt=quantity)],
                )
        entries.entries = entries.entries + [entry]
        entries.save()

    def complete(self, action, task, end_time):
        task_id, cur_task = self.taskw.get_task(id=task)

        if not task_id:
            raise TaskNotFoundException(task)

        entries = Entries()
        entry = entries.find(date=end_time.date(), uuid=cur_task["uuid"])
        if not entry:
            entry = Entry(uuid=cur_task["uuid"], date=end_time.date())
            entries.entries += [entry]

        last_pomodoro = None
        if entry.pomodoros:
            last_pomodoro = entry.pomodoros[-1]

        if not last_pomodoro or last_pomodoro.void or last_pomodoro.time is not None:
            entry.intervals.append(
                Pomodoro(
                    start_time=(end_time - timedelta(minutes=self.duration)),
                    end_time=end_time,
                )
            )
        else:
            last_pomodoro.time = end_time

        tags = [cur_task.get("description", "")] + self.__split_project(
            cur_task.get("project", "")
        )

        if self.config.getboolean("timew", "sync", fallback=True):
            self.timew.track(
                end_time - timedelta(minutes=self.duration), end_time, tags=tags
            )

        entries.save()

    def plan(self, action, task, quantity, date):
        # get the corresponding Taskwarrior task
        task_id, cur_task = self.taskw.get_task(id=task)

        if not task_id:
            raise TaskNotFoundException(task)

        quantity, increment = self.__parse_quantity(quantity)

        entries = Entries()
        entry = entries.find(date=date, uuid=cur_task["uuid"])

        if not entry:
            entry = Entry(uuid=cur_task["uuid"], date=date)
            entries.entries += [entry]

        if increment:
            entry.planned += quantity
        else:
            entry.planned = quantity

        entries.save()

    def start(self, action):
        print(action)
        # data = json.loads(Popen([cmd, 'export'], stdout=PIPE).stdout.read())

    def void(self, action, task, date):
        task_id, cur_task = self.taskw.get_task(id=task)

        if not task_id:
            raise TaskNotFoundException(task)

        entries = Entries()
        entry = entries.find(date=date, uuid=cur_task["uuid"])

        if not entry:
            entry = Entry(uuid=cur_task["uuid"], date=date)
            entries.entries += [entry]

        # If last pomodoro is complete, add new voided pomodoro, else void the existing pomodoro
        if not entry.pomodoros:
            entry.pomodoros += [Pomodoro(void=True)]
        if not entry.pomodoros[-1].time:
            entry.pomodoros[-1].void = True
        else:
            entry.pomodoros += [Pomodoro(void=True)]

        entries.save()

    def nonpom(self, action, task, start_time, end_time, duration):
        task_id, cur_task = self.taskw.get_task(id=task)
        if not task_id:
            raise TaskNotFoundException(task)

        tags = [cur_task.get("description", "")] + self.__split_project(
            cur_task.get("project", "")
        )

        entries = Entries()
        entry = entries.find(uuid=cur_task["uuid"], date=end_time.date())

        if not entry:
            entry = Entry(uuid=cur_task["uuid"], date=end_time.date())
            entries.entries += [entry]

        if end_time and duration:
            start_time = end_time - timedelta(minutes=duration)
        elif start_time and duration:
            end_time = start_time + timedelta(minutes=duration)
        elif start_time and end_time:
            pass
        else:
            raise ArgumentException(
                "Two of END_TIME, START_TIME and DURATION must be provided!"
            )

        entry.intervals += [Interval(start_time=start_time, end_time=end_time)]
        if self.config.getboolean("timew", "sync", fallback=True):
            self.timew.track(start_time, end_time, tags=tags)

        entries.save()

    def list(self, action, date):
        entries = Entries()

        # underlined_headers = ''.join(tuple(x + y for x, y in zip_longest(
        #     'Type   ID    Start Time      End Time', '\u0332', fillvalue='\u0332')))
        id_h = "".join(tuple(x + y for x, y in zip_longest("ID", "̲", fillvalue="̲")))
        project_h = "".join(
            tuple(x + y for x, y in zip_longest("Project", "̲", fillvalue="̲"))
        )
        task_h = "".join(
            tuple(x + y for x, y in zip_longest("Task", "̲", fillvalue="̲"))
        )
        type_h = "".join(
            tuple(x + y for x, y in zip_longest("Type", "̲", fillvalue="̲"))
        )
        date_h = "".join(
            tuple(x + y for x, y in zip_longest("Date", "̲", fillvalue="̲"))
        )
        start_h = "".join(
            tuple(x + y for x, y in zip_longest("Start", "̲", fillvalue="̲"))
        )
        end_h = "".join(tuple(x + y for x, y in zip_longest("End", "̲", fillvalue="̲")))

        # print(underlined_headers)

        if len(entries.intervals()) > 0:
            print(
                "{:6} {:11} {:15} {:14} {:12} {:29} {}".format(
                    id_h, type_h, date_h, start_h, end_h, project_h, task_h
                )
            )
            interval_id = 1
            for interval in entries.intervals():
                task_id, cur_task = self.taskw.get_task(id=interval.task)

                interval_type = "Pom" if isinstance(interval, Pomodoro) else "NonPom"
                print(
                    "\033[91m@{:<3}\033[00m {:7} {!s:11} {!s:9} {!s:9} {!s:22} {!s}".format(
                        interval_id,
                        interval_type,
                        interval.start_time.date(),
                        interval.start_time.time(),
                        interval.end_time.time(),
                        cur_task.get("project", None),
                        cur_task.get("description", None),
                    )
                )
                interval_id += 1
        else:
            print("No entries to display")

    def tdt(self, action, date):
        def unhandled_input(key):
            if key in ("Q", "q", "esc"):
                raise ExitMainLoop()

        entries = Entries()
        data = entries.find(date=date)
        render_pomodoros = []
        render_nonpom = []
        nonpom_to_render = False
        grand_total_pom = timedelta()
        grand_total_nonpom = timedelta()

        for entry in data:
            task_id, task = self.taskw.get_task(uuid=entry.uuid)
            if not task_id:
                task_id = "-"

            project = task["project"]
            description = task["description"]
            planned = entry.planned
            pomodoros = entry.pomodoros
            nonpomodoros = entry.nonpomodoros

            rendered_pomodoros = []
            if planned or pomodoros:
                # TODO: Simplify the code here!
                if planned >= len(pomodoros):
                    for i in range(0, len(pomodoros)):
                        if pomodoros[i].void:
                            rendered_pomodoros.append((3, Void()))
                        else:
                            rendered_pomodoros.append((3, Complete()))
                            grand_total_pom += timedelta(minutes=self.duration)
                    for i in range(0, planned - len(pomodoros)):
                        rendered_pomodoros.append((3, Empty()))
                else:
                    for i in range(0, planned):
                        if pomodoros[i].void:
                            rendered_pomodoros.append((3, Void()))
                        else:
                            rendered_pomodoros.append((3, Complete()))
                            grand_total_pom += timedelta(minutes=self.duration)
                    for i in range(planned, len(pomodoros)):
                        if pomodoros[i].void:
                            rendered_pomodoros.append((3, VoidUnplanned()))
                        else:
                            rendered_pomodoros.append((3, CompleteUnplanned()))
                            grand_total_pom += timedelta(minutes=self.duration)

                row = Columns(
                    [
                        Filler(Text("{:>3}  {}".format(task_id, description))),
                        Columns(rendered_pomodoros),
                    ]
                )
                render_pomodoros.append((3, row))

            if nonpomodoros:
                nonpom_to_render = True
                total_time = timedelta()

                for i in range(0, len(nonpomodoros)):
                    total_time += nonpomodoros[i].end_time - nonpomodoros[i].start_time
                    grand_total_nonpom += total_time

                row = Columns(
                    [
                        Filler(Text("{:>3}  {}".format(task_id, description))),
                        Filler(Text("{}".format(total_time))),
                    ]
                )
                render_nonpom.append((2, row))

        pom_header = (
            "pack",
            Columns(
                [
                    Text("To Do Today\n-----------"),
                    Text("{}\n----------".format(date), align="right"),
                ]
            ),
        )
        pom_footer = (
            "pack",
            Columns([Text(""), Text("-------\n{}".format(grand_total_pom))]),
        )

        nonpom_header = ("pack", Columns([Text("")]))
        nonpom_footer = ("pack", Columns([Text("")]))
        if nonpom_to_render:
            nonpom_header = (
                "pack",
                Columns([Text("\nNon Pomodoro Time\n-----------------")]),
            )
            nonpom_footer = (
                "pack",
                Columns([Text(""), Text("-------\n{}".format(grand_total_nonpom))]),
            )

        # footer = ('pack', Text('Footer'))

        widget = Pile(
            [pom_header]
            + render_pomodoros
            + [pom_footer]
            + [nonpom_header]
            + render_nonpom
            + [nonpom_footer]
        )

        loop = MainLoop(
            widget,
            screen=raw_display.Screen(),
            unhandled_input=unhandled_input,
            pop_ups=True,
        )
        loop.run()
