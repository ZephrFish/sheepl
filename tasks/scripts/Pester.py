
# LOLBAS: Pester.bat — Legitimate use: running PowerShell Pester unit tests for module validation
# #######################################################################
#
#  Task : Pester Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of Pester.bat, the batch wrapper for the
 PowerShell Pester testing framework, to invoke unit tests against a
 specified PowerShell module or test script path.

 Takes a test_path parameter pointing to a .Tests.ps1 file or directory;
 if absent a default help invocation is used.
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


class Pester(BaseCMD):
    """
    # LOLBAS: Pester.bat — Legitimate use: running PowerShell Pester unit tests

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Pester, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Pester'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > pester >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > pester >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional path to a Pester test script or directory
        self.test_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Pester Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a test path using 'test_path <path>'
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
    #  Pester Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Pester interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Pester_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_test_path(self, test_path):
        """
        Optionally set the path to a Pester test file or directory to run.
        If not set, Pester.bat will be invoked with /help to display usage.
        Example: test_path C:\\Scripts\\MyModule.Tests.ps1
        """
        if test_path:
            if self.taskstarted:
                self.test_path = test_path.strip()
                print(self.cl.green("[*] Test path set to: {}".format(self.test_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Pester Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a test path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Pester configuration
        """
        print(self.cl.green("[?] Currently Assigned Pester Configuration"))
        print("[>] Test Path : {}".format(self.test_path if self.test_path else "(not set — will invoke /help)"))


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
        self.test_path = None


    ######################################################################
    # Pester AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Pester_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_function()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            test_path : str — path to a Pester .Tests.ps1 file or test directory
                              if absent, Pester.bat /help is invoked instead
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.test_path = kwargs.get("test_path", None)
        if self.test_path:
            print(f"[*] Setting test_path attribute : {self.test_path}")
        else:
            print("[*] No test_path provided — will invoke Pester.bat /help")

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
        ; <      Pester Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Pester_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Pester_{}()

            ; Creates a Pester Interaction via CMD

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
        Builds the Pester commands to type into the CMD window.
        If test_path is set, invokes Pester.bat with that path to run tests.
        Otherwise invokes Pester.bat /help to display usage information.
        """
        typing_text = '\n'

        if self.test_path:
            # Run Pester tests against the given path
            pester_cmd = (
                '"C:\\Program Files\\WindowsPowerShell\\Modules\\Pester\\bin\\Pester.bat" '
                + self.test_path
            )
            typing_text += 'Send("' + self._escape_send(pester_cmd) + '{ENTER}")\n'
        else:
            # Default: display help to confirm Pester is present and functional
            help_cmd = '"C:\\Program Files\\WindowsPowerShell\\Modules\\Pester\\bin\\Pester.bat" /help'
            typing_text += 'Send("' + self._escape_send(help_cmd) + '{ENTER}")\n'

        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Pester AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
