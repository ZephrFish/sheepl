
# LOLBAS: iscsicpl.exe — Legitimate use: opening the iSCSI Initiator control panel to manage iSCSI target connections

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of iscsicpl.exe to open the Windows iSCSI Initiator
 control panel applet, which allows administrators to configure and manage iSCSI
 initiator connections to storage targets.

 No parameters are required; the tool opens the GUI, pauses to simulate a user
 reviewing iSCSI target configuration, then closes the window.

 The master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class IscsIcpl(BaseCMD):
    """
    # LOLBAS: iscsicpl.exe — Legitimate use: opening the iSCSI Initiator control panel to manage iSCSI target connections

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(IscsIcpl, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'IscsIcpl'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > iscsicpl >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > iscsicpl >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] IscsIcpl Interaction.
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
    #  IscsIcpl Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new IscsIcpl interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'IscsIcpl_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned IscsIcpl configuration
        """
        print(self.cl.green("[?] Currently Assigned IscsIcpl Configuration"))
        print("[>] Opens iSCSI Initiator GUI (no parameters required)")


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
    # IscsIcpl AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('IscsIcpl_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_iscsicpl()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        No JSON keys are required for this task.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")
        print("[*] No parameters required — will open iSCSI Initiator GUI")

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
        ; <      IscsIcpl Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "IscsIcpl_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens iscsicpl.exe via Win+R run dialogue and waits for the
        iSCSI Initiator window to become active, then closes it.
        """

        _open_toolwindow = """

        Func IscsIcpl_{}()

            ; Opens the iSCSI Initiator control panel applet

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Launch iscsicpl.exe
            Send('iscsicpl.exe{}')
            ; Wait for the iSCSI Initiator window
            WinWaitActive("iSCSI Initiator", "", 15)
            ; Simulate a user reviewing the iSCSI target configuration
            Sleep({})
            ; Close the window
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), "{ENTER}", random.randint(3000, 8000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_iscsicpl(self):
        """
        Closes the IscsIcpl AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
