
# LOLBAS: ComputerDefaults.exe — Legitimate use: opening the Windows Default Apps settings panel

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user interaction with ComputerDefaults.exe to open
 the Windows Default Apps settings panel and review or change default
 application associations (browser, email client, media player, etc.).

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


class ComputerDefaults(BaseCMD):
    """
    # LOLBAS: ComputerDefaults.exe — Legitimate use: opening the Windows Default Apps settings panel

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ComputerDefaults, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ComputerDefaults'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > computerdefaults >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > computerdefaults >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # How long (ms) to keep the Default Apps window open before closing
        self.view_duration = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] ComputerDefaults Interaction.
        Opens the Windows Default Apps settings panel via ComputerDefaults.exe.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set how long to view the panel using 'view_duration <ms>'
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
    #  ComputerDefaults Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ComputerDefaults interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ComputerDefaults_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_view_duration(self, view_duration):
        """
        Optionally set how long (in milliseconds) to keep the Default Apps
        window open before closing it. Defaults to a random value between
        3000 and 8000 ms if not set.
        Example: view_duration 5000
        """
        if view_duration:
            if self.taskstarted:
                try:
                    self.view_duration = int(view_duration.strip())
                    print(self.cl.green("[*] View duration set to: {} ms".format(self.view_duration)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> Please provide a numeric value in milliseconds."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ComputerDefaults Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a duration in milliseconds."))


    def do_assigned(self, arg):
        """
        Get the current assigned ComputerDefaults configuration
        """
        print(self.cl.green("[?] Currently Assigned ComputerDefaults Configuration"))
        duration = self.view_duration if self.view_duration else "(not set — will use random 3000-8000 ms)"
        print("[>] View Duration : {}".format(duration))


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
        self.view_duration = None


    ######################################################################
    # ComputerDefaults AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ComputerDefaults_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.text_typing_block() +
            self.close_computerdefaults()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            view_duration : int — milliseconds to keep the Default Apps window
                                  open before closing (default: random 3000-8000)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.view_duration = kwargs.get("view_duration", None)
        if self.view_duration:
            print(f"[*] Setting view_duration attribute : {self.view_duration}")
        else:
            print("[*] No view_duration provided — will use random 3000-8000 ms")

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
        ; <      ComputerDefaults Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ComputerDefaults_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens ComputerDefaults.exe via Win+R run dialogue and waits for
        the Default Apps settings window to become active.
        """

        _open_toolwindow = """

        Func ComputerDefaults_{}()

            ; Opens the Windows Default Apps settings panel via ComputerDefaults.exe

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('ComputerDefaults.exe{}')
            ; Wait for the Default Apps window (Settings) to become active
            WinWaitActive("Default Apps", "", 15)

        """.format(self.csh.counter.current(), "{ENTER}")

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Typing Output

    def text_typing_block(self):
        """
        Simulates a user viewing the Default Apps settings panel for a
        realistic dwell time before closing the window with Alt+F4.
        """
        duration = self.view_duration if self.view_duration else random.randint(3000, 8000)

        typing_text = '\n'
        typing_text += '; Pause to simulate user reviewing default app assignments\n'
        typing_text += 'sleep({})\n'.format(duration)
        typing_text += '; Close the Default Apps window\n'
        typing_text += 'Send("!{F4}")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_computerdefaults(self):
        """
        Closes the ComputerDefaults AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
