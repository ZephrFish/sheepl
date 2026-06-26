
# LOLBAS: sigverif.exe — Legitimate use: verifying digital signatures of system files

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of sigverif.exe to launch the File Signature
 Verification GUI, which allows administrators to scan and verify the digital
 signatures of files on the system.

 The tool opens via Win+R, waits for the main window, and then closes it.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SigVerif(BaseCMD):
    """
    # LOLBAS: sigverif.exe — Legitimate use: verifying digital signatures of system files

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SigVerif, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SigVerif'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sigverif >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sigverif >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] SigVerif Interaction.
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
    #  SigVerif Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new SigVerif interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SigVerif_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned SigVerif configuration
        """
        print(self.cl.green("[?] Currently Assigned SigVerif Configuration"))
        print("[>] Launches sigverif.exe GUI and closes after a brief pause")


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
    # SigVerif AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SigVerif_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_sigverif()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        No required JSON keys for this task — sigverif takes no parameters.
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
        ; <      SigVerif Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "SigVerif_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens sigverif.exe via Win+R run dialogue and waits for the GUI window
        """

        _open_toolwindow = """

        Func SigVerif_{}()

            ; Launches the File Signature Verification GUI via Win+R

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('sigverif.exe{}')
            ; Wait for the sigverif main window to appear
            WinWaitActive("File Signature Verification", "", 15)
            sleep({})
            ; Close the sigverif window
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), "{ENTER}", random.randint(2000, 5000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_sigverif(self):
        """
        Closes the SigVerif AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
