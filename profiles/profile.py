"""
Creates a Sheepl from a JSON profile file.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import json
import importlib

from utils.base.base_sheepl_class import Sheepl


class Profile(object):

    def __init__(self, cl, profile_file, tasks):
        self.cl = cl
        self.tasks = tasks
        self.interactive = False

        self.profile = self.parse_profile_file(profile_file)

        self.csh = Sheepl(
            self.profile["name"],
            self.profile["total_time"],
            self.profile["typing_speed"],
            self.profile["loop"],
            cl,
            self.interactive
        )
        self.csh.json_parsing = True

        self.create_sheepl_tasks(self.csh, self.profile)


    def parse_profile_file(self, profile_file):
        with open(profile_file) as json_file:
            profile = json.load(json_file)
            return profile["sheepl"]


    def process_subtask(self, subtask_output):
        self.csh.creating_subtasks = True

        for output in subtask_output:
            for k, v in output.items():
                if k == "task":
                    subtask_name = v
                    print("[>] Subtask: " + subtask_name)
                    sheepl_task = self.csh.generate_task(subtask_name)

            sheepl_task.create_autoIT_block()


    def create_sheepl_tasks(self, csh, profile):
        for task in profile["tasks"]:
            task_name = task["task"]
            task_arguments = {}

            for key, value in task.items():
                if value == task_name:
                    print("------------------------------------------------------\n")
                    current_task_name = task_name + "_" + str(self.csh.counter.current())
                    print(self.cl.green(f"[*] Creating Sheepl Task : {current_task_name}"))
                if key == 'subtasks':
                    self.process_subtask(value)
                else:
                    task_arguments.update({key: value})

            self.csh.creating_subtasks = False

            for path, module in self.tasks.locate_available_tasks().items():
                if task_name == module:
                    task_module = importlib.import_module(path)
                    SHEEPL_TASK = getattr(task_module, module)
                    current_task = SHEEPL_TASK(self.csh, self.cl)
                    current_task.parse_json_profile(**task_arguments)

        print("\n------------------------------------------------------\n")
        print("[!] Writing the file {} :".format(self.cl.green(self.csh.file_name)))
        self.csh.write_file(self.csh.file_name)
        print("[!] Written the file {} :".format(self.cl.green(self.csh.file_name)))
