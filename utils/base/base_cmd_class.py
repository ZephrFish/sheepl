"""
Base class for task CMD consoles.
Provides common menu commands (back, discard, complete, subtask) via inheritance.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd

try:
    import readline
except ImportError:
    print("[>] Cannot import readline")

from utils.tasks import Tasks
from utils.counter import Counter


class BaseCMD(cmd.Cmd):

    def __init__(self, csh, cl):
        cmd.Cmd.__init__(self)

        self.cl = cl
        self.csh = csh
        self.completed = True
        self.discard = False
        self.taskstarted = False
        self.baseprompt = ''
        self.prompt = ''
        self.taskname = ''
        self.subtask_supported = False


    def do_back(self, arg):
        """
        Return to main menu
        """
        if not self.completed:
            print(self.cl.red("[!] <ERROR> Still creating task : ") + self.taskname)
            print("[!] Run 'discard' to reset\n")
        else:
            print(self.cl.red('[>] Returning to the main menu'))
            return -1


    def emptyline(self):
        pass


    def do_killwindow(self, window_title):
        """
        Add a window title to the kill list so it is closed at the end of each loop
        example: killwindow Windows PowerShell
        """
        if window_title:
            print("[!] Adding {} to the Kill Window Title list".format(window_title))
            self.csh.window_kill_list.append(window_title)


    def do_discard(self, arg):
        """
        Discard the current task and reset
        """
        self.discard = True
        self.completed = True
        self.taskstarted = False
        self.csh.creating_subtasks = False
        print('[>] Discarding : ' + self.cl.red("{}".format(self.taskname)))
        self.prompt = self.baseprompt
        try:
            if self.commands:
                self.commands = []
        except AttributeError:
            pass


    def check_task_started(self):
        """
        Returns True if a new task can start; prints an error and returns False if one is already in progress.
        """
        if self.taskstarted:
            print(self.cl.red("[!] <ERROR> Already creating a task. Run 'discard' to reset"))
            return False
        self.taskstarted = True
        self.completed = False
        return True


    def complete_task(self):
        """
        Mark the current task complete and reset state.
        """
        if self.taskstarted:
            print(self.cl.green("[>] Completing this task interaction"))
            self.prompt = self.baseprompt
            self.completed = True
            self.taskstarted = False
            self.csh.creating_subtasks = False
        else:
            print("{} There is no current task to complete.".format(self.cl.red("[!]")))
            print("{} Issue the 'new' command to create new interaction.".format(self.cl.red("[!]")))


    def _escape_send(self, text):
        """
        Escape AutoIT Send() special characters in user-supplied text.
        Processes one character at a time to avoid sequential-replacement corruption.
        """
        _map = {'{': '{{}', '}': '{}}', '+': '{+}', '!': '{!}', '^': '{^}', '"': '" & Chr(34) & "'}
        return ''.join(_map.get(c, c) for c in text)


    def ask_yes_no_question(self, question):
        """
        Prompt for yes/no input; returns True for 'yes'.
        """
        while 1:
            input_answer = input(question)
            if input_answer.lower() in ("yes", "no"):
                break
        return input_answer.lower() == "yes"


    def do_subtask_list(self, arg=None):
        """
        List subtasks assigned to the current task
        """
        print("[*] Assigned subtasks:")
        for task in self.csh.subtasks.keys():
            print(f"[-] {task}")


    def do_subtask(self, st):
        """
        Assign a subtask (only supported in tasks like RemoteDesktop)
        example: subtask PowerShell
        """
        if not self.subtask_supported:
            print(self.cl.red("[!] SubTasks are not supported in this module"))
            return

        if not st:
            print(self.cl.green("\n[!] Available subtasks:\n"))
            for task in self.csh.task_list.values():
                print("[*] {}".format(task))
            print()
            return

        for task in self.csh.task_list.values():
            if st == task:
                print(self.cl.blue("[>] Creating SubTask Assignment >> {}".format(st)))
                self.csh.creating_subtasks = True
                self.csh.generate_task(task)
                return

        print(self.cl.red("[!] Unknown subtask '{}'. Use 'subtask' with no args to list options.".format(st)))
