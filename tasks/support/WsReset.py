
# LOLBAS: wsreset.exe — Legitimate use: reset Windows Store cache and settings

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates a legitimate IT support action of running wsreset.exe to clear
 the Windows Store cache and reset Store settings, which is a common
 troubleshooting step when the Store is misbehaving.

 wsreset.exe launches silently, resets the Store cache, then opens the
 Windows Store. The task waits briefly for the Store window to appear,
 optionally pauses to observe it, then closes it.

 The master script will already define the typing speed as part of the
 master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WsReset(BaseCMD):
    """
    # LOLBAS: wsreset.exe — Legitimate use: reset Windows Store cache and settings

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WsReset, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WsReset'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wsreset >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wsreset >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] WsReset Interaction.
        Resets Windows Store cache and settings via wsreset.exe.
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
    #  WsReset Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WsReset interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WsReset_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned WsReset configuration
        """
        print(self.cl.green("[?] Currently Assigned WsReset Configuration"))
        print("[>] Action : Reset Windows Store cache via wsreset.exe")


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
    # WsReset AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WsReset_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_wsreset()
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
        ; <      WsReset Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "WsReset_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Launches wsreset.exe via Win+R run dialogue.
        wsreset.exe resets the Windows Store cache silently, then opens
        the Store. We wait for the Store window and close it.
        """

        _open_toolwindow = """

        Func WsReset_{}()

            ; Launches wsreset.exe to reset the Windows Store cache

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('wsreset.exe{}')
            ; wsreset.exe resets the Store cache then opens the Store window
            ; Wait up to 30 seconds for the Store window to appear
            WinWaitActive("Microsoft Store", "", 30)
            sleep({})
            ; Close the Store window once the reset is complete
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), "{ENTER}", random.randint(2000, 5000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_wsreset(self):
        """
        Closes the WsReset AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
