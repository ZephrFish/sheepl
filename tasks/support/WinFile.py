
# LOLBAS: winfile.exe — Legitimate use: browsing and managing files using the classic Windows File Manager GUI

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user interaction with winfile.exe (Windows File Manager).
 Opens the classic File Manager GUI, optionally navigates to a target path,
 and closes the window after a brief dwell period.

 Takes an optional target_path parameter; if absent the File Manager opens
 to its default location.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WinFile(BaseCMD):
    """
    # LOLBAS: winfile.exe — Legitimate use: browsing and managing files using the classic Windows File Manager GUI

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WinFile, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WinFile'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > winfile >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > winfile >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional target path to navigate to inside File Manager
        self.target_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] WinFile Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a path to browse using 'target_path <path>'
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
    #  WinFile Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WinFile interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WinFile_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_path(self, target_path):
        """
        Optionally set a directory path to browse inside File Manager.
        If not set, File Manager opens to its default location.
        Example: target_path C:\\Users\\Public\\Documents
        """
        if target_path:
            if self.taskstarted:
                self.target_path = target_path.strip()
                print(self.cl.green("[*] Target path set to: {}".format(self.target_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new WinFile Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target path."))


    def do_assigned(self, arg):
        """
        Get the current assigned WinFile configuration
        """
        print(self.cl.green("[?] Currently Assigned WinFile Configuration"))
        print("[>] Target Path : {}".format(self.target_path if self.target_path else "(not set — opens to default location)"))


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
        self.target_path = None


    ######################################################################
    # WinFile AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WinFile_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.text_typing_block() +
            self.close_winfile()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            target_path : str — directory path to open inside File Manager
                                if absent, File Manager opens to its default location
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_path = kwargs.get("target_path", None)
        if self.target_path:
            print(f"[*] Setting target_path attribute : {self.target_path}")
        else:
            print("[*] No target_path provided — File Manager will open to its default location")

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
        ; <      WinFile Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "WinFile_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens winfile.exe via Win+R run dialogue and waits for the File Manager window
        """

        if self.target_path:
            run_cmd = self._escape_send('winfile.exe "' + self.target_path + '"')
        else:
            run_cmd = self._escape_send('winfile.exe')

        counter = self.csh.counter.current()

        _open_toolwindow = (
            "\n\n        Func WinFile_{}()\n\n".format(counter) +
            "            ; Creates a WinFile Interaction via Run dialogue\n\n" +
            '            Send("#r")\n' +
            "            ; Wait 10 seconds for the Run dialogue window to appear.\n" +
            '            WinWaitActive("Run", "", 10)\n' +
            "            ; Launch winfile.exe with optional target path\n" +
            "            Send('" + run_cmd + "{ENTER}')\n" +
            "            ; Wait for the File Manager window to become active\n" +
            '            WinWaitActive("File Manager", "", 15)\n' +
            '            SendKeepActive("File Manager")\n\n' +
            "        \n"
        )

        return _open_toolwindow


    # --------------------------------------------------->
    # Typing Output

    def text_typing_block(self):
        """
        Simulates browsing inside File Manager then closes the window.
        """
        typing_text = '\n'

        # Dwell inside File Manager to simulate browsing
        typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        # Close File Manager with Alt+F4
        typing_text += 'Send("!{F4}")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_winfile(self):
        """
        Closes the WinFile AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
