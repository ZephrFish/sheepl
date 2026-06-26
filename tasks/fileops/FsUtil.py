
# LOLBAS: fsutil.exe — Legitimate use: disk space monitoring and volume health checks
# Admin required: most fsutil commands require elevated privileges

# #######################################################################
#
#  Task : FsUtil Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of fsutil.exe to query file
 system information such as disk free space, volume details, and dirty
 bit status. Note: most fsutil operations require elevated privileges.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class FsUtil(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(FsUtil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'FsUtil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > fsutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > fsutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Default action and drive
        self.action = 'diskfree'
        self.drive = 'C:'

        self.introduction = """
        ----------------------------------
        [!] FsUtil Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action' (diskfree / volume / dirty)
        3: Set the target drive using 'drive' (e.g. C:)
        4: Complete the interaction using 'complete'
        Note: most fsutil commands require elevated privileges.
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  FsUtil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new FsUtil interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'FsUtil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, action):
        """
        Set the fsutil action to perform.
        Options:
            diskfree  - check free space on the specified drive (fsutil volume diskfree <drive>)
            volume    - list all volumes on the system (fsutil volume list)
            dirty     - query the dirty bit on the specified drive (fsutil dirty query <drive>)
        Default: diskfree
        Example: action dirty
        """
        valid_actions = ['diskfree', 'volume', 'dirty']
        if self.taskstarted:
            if action.lower() in valid_actions:
                self.action = action.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new FsUtil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_drive(self, drive):
        """
        Set the drive letter to target for the fsutil operation.
        Default: C:
        Example: drive D:
        Note: used by diskfree and dirty actions; ignored by volume (which lists all).
        """
        if self.taskstarted:
            if drive:
                self.drive = drive.upper().rstrip(':') + ':'
                print(self.cl.green("[*] Drive set to: {}".format(self.drive)))
            else:
                print(self.cl.yellow("[*] No drive supplied, using default: {}".format(self.drive)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new FsUtil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the currently assigned FsUtil action and drive
        """
        print(self.cl.green("[?] Currently Assigned FsUtil Settings"))
        print("[>] Action : {}".format(self.action))
        print("[>] Drive  : {}".format(self.drive))


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

        # reset to defaults for next interaction
        self.action = 'diskfree'
        self.drive = 'C:'


    ######################################################################
    # FsUtil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('FsUtil_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.fsutil_command_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            action : fsutil action to perform — "diskfree", "volume", or "dirty"
            drive  : drive letter to target, e.g. "C:" (used by diskfree and dirty)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "action" in kwargs:
            self.action = kwargs["action"]
        print(f"[*] Setting the action attribute : {self.action}")

        if "drive" in kwargs:
            self.drive = kwargs["drive"]
        print(f"[*] Setting the drive attribute : {self.drive}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      FsUtil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "FsUtil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens CMD via Win+R run dialogue
        """

        _open_commandshell = """

        Func FsUtil_{}()

            ; Opens CMD to run fsutil command
            ; Note: fsutil requires elevated privileges for most operations

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; note this needs to be escaped
            Send('cmd{}')
            ; check to see if we are already in an RDP session
            $active_window = _WinAPI_GetClassName(WinGetHandle("[ACTIVE]"))
            ConsoleWrite($active_window & @CRLF)
            $inRDP = StringInStr($active_window, "TscShellContainerClass")
            ; if the result is greater than 1 we are inside an RDP session
            if $inRDP < 1 Then
                WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
                SendKeepActive("[CLASS:ConsoleWindowClass]")
            EndIf


        """.format(self.csh.counter.current(), "{ENTER}")

        return textwrap.dedent(_open_commandshell)


    # --------------------------------------------------->
    # FsUtil Command Block

    def fsutil_command_block(self):
        """
        Builds and sends the appropriate fsutil command based on the selected action,
        then exits the shell.

        Actions:
            diskfree : fsutil volume diskfree <drive>
            volume   : fsutil volume list
            dirty    : fsutil dirty query <drive>
        """

        if self.action == 'diskfree':
            fsutil_cmd = 'fsutil volume diskfree {}'.format(self.drive)
        elif self.action == 'volume':
            fsutil_cmd = 'fsutil volume list'
        elif self.action == 'dirty':
            fsutil_cmd = 'fsutil dirty query {}'.format(self.drive)
        else:
            fsutil_cmd = 'fsutil volume diskfree {}'.format(self.drive)

        command_text = '\n'
        command_text += 'Send("' + self._escape_send(fsutil_cmd) + '{ENTER}")\n'
        command_text += 'sleep({})\n'.format(random.randint(3000, 10000))
        command_text += "Send('exit{ENTER}')\n"
        command_text += "; Reset Focus\n"
        command_text += 'SendKeepActive("")'

        return textwrap.indent(command_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the FsUtil function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
