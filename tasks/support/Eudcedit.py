
# LOLBAS: eudcedit.exe — Legitimate use: opening the Private Character Editor to create custom font glyphs

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of eudcedit.exe, the Windows Private Character Editor,
 which allows users to create and edit custom characters linked to installed fonts.

 No parameters are required; the task simply launches the editor, pauses to
 simulate user interaction, and then closes the window.

 The master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Eudcedit(BaseCMD):
    """
    # LOLBAS: eudcedit.exe — Legitimate use: opening the Private Character Editor to create custom font glyphs

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Eudcedit, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Eudcedit'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > eudcedit >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > eudcedit >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Eudcedit Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Eudcedit Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Eudcedit interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Eudcedit_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned Eudcedit configuration
        """
        print(self.cl.green("[?] Currently Assigned Eudcedit Configuration"))
        print("[>] No configurable parameters — launches Private Character Editor GUI")


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
    # Eudcedit AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Eudcedit_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_eudcedit()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        No required JSON keys for this task.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] No configurable parameters for this task")

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
        ; <      Eudcedit Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Eudcedit_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens the Private Character Editor via Win+R run dialogue
        """

        _open_toolwindow = """

        Func Eudcedit_{}()

            ; Launches the Private Character Editor GUI

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('eudcedit.exe{}')
            ; Wait for the Private Character Editor to become active
            WinWaitActive("Private Character Editor", "", 15)
            ; Simulate user reviewing the editor
            sleep({})
            ; Close the Private Character Editor
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), "{ENTER}", random.randint(4000, 9000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_eudcedit(self):
        """
        Closes the Eudcedit AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
