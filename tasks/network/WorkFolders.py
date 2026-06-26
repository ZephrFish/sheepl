
# LOLBAS: WorkFolders.exe — Legitimate use: opening the Work Folders sync client UI

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates a user launching the Work Folders sync client (WorkFolders.exe),
 a built-in Windows feature that lets users sync corporate files from a
 file server to their device.

 WorkFolders.exe opens a GUI control panel applet; no parameters are accepted.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WorkFolders(BaseCMD):
    """
    # LOLBAS: WorkFolders.exe — Legitimate use: opening the Work Folders sync client UI

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WorkFolders, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WorkFolders'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > workfolders >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > workfolders >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] WorkFolders Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Complete the interaction using 'complete'
        ----------------------------------
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  WorkFolders Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WorkFolders interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WorkFolders_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned WorkFolders configuration
        """
        print(self.cl.green("[?] Currently Assigned WorkFolders Configuration"))
        print("[>] No configurable parameters — launches Work Folders GUI directly")


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()


    ######################################################################
    # WorkFolders AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WorkFolders_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_workfolders()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        No required JSON keys — WorkFolders takes no parameters.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        fn = """
        ; < ----------------------------------- >
        ; <      WorkFolders Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "WorkFolders_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Launches WorkFolders.exe via the Win+R run dialogue and waits for its window.
        WorkFolders opens a GUI control panel applet — no CMD shell is needed.
        """

        _open_toolwindow = """

        Func WorkFolders_{}()

            ; Launches the Work Folders sync client GUI via Win+R
            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('WorkFolders.exe{}')
            ; Wait for the Work Folders control panel window
            WinWaitActive("Work Folders", "", 15)
            ; Browse the UI briefly to simulate legitimate user activity
            sleep({})
            ; Close the Work Folders window
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), "{ENTER}", random.randint(4000, 9000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_workfolders(self):
        """
        Closes the WorkFolders AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
