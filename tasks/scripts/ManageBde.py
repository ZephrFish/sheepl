
# LOLBAS: manage-bde.wsf — Legitimate use: querying BitLocker Drive Encryption status via cscript

# #######################################################################
#
#  Task : ManageBde Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of manage-bde.wsf to query BitLocker Drive
 Encryption status on local drives. The script is invoked via cscript.exe
 from the System32 directory.

 Takes an optional drive_letter parameter (e.g. C:); defaults to C:.
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


class ManageBde(BaseCMD):
    """
    # LOLBAS: manage-bde.wsf — Legitimate use: querying BitLocker Drive Encryption status

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ManageBde, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ManageBde'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > manage-bde >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > manage-bde >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional drive letter to query (e.g. C:)
        self.drive_letter = 'C:'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] ManageBde Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a drive letter using 'drive_letter <letter>'
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
    #  ManageBde Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ManageBde interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ManageBde_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_drive_letter(self, drive_letter):
        """
        Optionally set a drive letter to query BitLocker status for.
        Defaults to C: if not set.
        Example: drive_letter C:
        """
        if drive_letter:
            if self.taskstarted:
                self.drive_letter = drive_letter.strip()
                print(self.cl.green("[*] Drive letter set to: {}".format(self.drive_letter)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ManageBde Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a drive letter (e.g. C:)."))


    def do_assigned(self, arg):
        """
        Get the current assigned ManageBde configuration
        """
        print(self.cl.green("[?] Currently Assigned ManageBde Configuration"))
        print("[>] Drive Letter : {}".format(self.drive_letter))


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
        self.drive_letter = 'C:'


    ######################################################################
    # ManageBde AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ManageBde_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_managebde()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            drive_letter : str — drive letter to query (e.g. C:)
                                 defaults to C: if absent
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.drive_letter = kwargs.get("drive_letter", "C:")
        print(f"[*] Setting drive_letter attribute : {self.drive_letter}")

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
        ; <      ManageBde Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ManageBde_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func ManageBde_{}()

            ; Creates a ManageBde Interaction via CMD

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
    # Typing Output

    def text_typing_block(self):
        """
        Builds the manage-bde.wsf commands to type into the CMD window.
        Queries BitLocker status for the configured drive letter.
        """
        typing_text = '\n'

        # Query BitLocker status for the specified drive
        status_cmd = 'cscript.exe //nologo C:\\Windows\\System32\\manage-bde.wsf -status {}'.format(self.drive_letter)
        typing_text += 'Send("' + self._escape_send(status_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_managebde(self):
        """
        Closes the ManageBde AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
