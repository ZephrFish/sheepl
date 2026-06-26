
# LOLBAS: eventvwr.exe — Legitimate use: viewing Windows Event Logs in the GUI console

# #######################################################################
#
#  Task : Eventvwr Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of eventvwr.exe to open and browse
 the Windows Event Viewer GUI console (e.g. reviewing System or
 Application event logs as part of routine administration).

 Takes an optional log_name parameter; if set the viewer is opened
 with that log path passed on the command line (e.g. System).
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Eventvwr(BaseCMD):
    """
    # LOLBAS: eventvwr.exe — Legitimate use: viewing Windows Event Logs in the GUI console

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Eventvwr, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Eventvwr'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > eventvwr >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > eventvwr >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional log name to pass to eventvwr on the command line (e.g. System, Application)
        self.log_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Eventvwr Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a specific log to open using 'log_name <name>'
           Example log names: System, Application, Security
        3: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Eventvwr Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Eventvwr interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Eventvwr_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_log_name(self, log_name):
        """
        Optionally set a specific Windows Event Log to open.
        If not set, Event Viewer opens at its default view.
        Example: log_name System
        Example: log_name Application
        """
        if log_name:
            if self.taskstarted:
                self.log_name = log_name.strip()
                print(self.cl.green("[*] Log name set to: {}".format(self.log_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Eventvwr Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a log name (e.g. System, Application)."))


    def do_assigned(self, arg):
        """
        Get the current assigned Eventvwr configuration
        """
        print(self.cl.green("[?] Currently Assigned Eventvwr Configuration"))
        print("[>] Log Name : {}".format(self.log_name if self.log_name else "(not set — will open default Event Viewer)"))


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

        # reset task-specific state for the next interaction
        self.log_name = None


    ######################################################################
    # Eventvwr AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Eventvwr_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.close_eventvwr()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            log_name : str — Windows Event Log to open (e.g. System, Application)
                             if absent, Event Viewer opens at its default view
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.log_name = kwargs.get("log_name", None)
        if self.log_name:
            print(f"[*] Setting log_name attribute : {self.log_name}")
        else:
            print("[*] No log_name provided — will open default Event Viewer")

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
        ; <      Eventvwr Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Eventvwr_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens Event Viewer via Win+R run dialogue, waits for the GUI window,
        browses briefly, then closes it.
        """

        # Build the run command: eventvwr.exe optionally followed by a log name
        if self.log_name:
            run_cmd = self._escape_send('eventvwr.exe ' + self.log_name) + '{ENTER}'
        else:
            run_cmd = self._escape_send('eventvwr.exe') + '{ENTER}'

        _open_toolwindow = """

        Func Eventvwr_{}()

            ; Opens Event Viewer as a legitimate admin reviewing Windows Event Logs

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Launch Event Viewer
            Send('{}')
            ; Wait for Event Viewer main window
            WinWaitActive("Event Viewer", "", 15)
            ; Browse the log briefly to simulate reading events
            sleep({})
            ; Close Event Viewer
            Send("!{{F4}}")

        """.format(self.csh.counter.current(), run_cmd, random.randint(4000, 10000))

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_eventvwr(self):
        """
        Closes the Eventvwr AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
