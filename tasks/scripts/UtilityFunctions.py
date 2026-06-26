
# LOLBAS: UtilityFunctions.ps1 — Legitimate use: PowerShell diagnostic script for Windows networking

# #######################################################################
#
#  Task : UtilityFunctions Interaction
#
# #######################################################################


r"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of the Windows networking diagnostic PowerShell
 script UtilityFunctions.ps1 located at:
   C:\Windows\diagnostics\system\Networking\UtilityFunctions.ps1

 Imports the module and lists available exported functions so an
 administrator can inspect what diagnostics are available.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class UtilityFunctions(BaseCMD):
    """
    # LOLBAS: UtilityFunctions.ps1 — Legitimate use: import and inspect Windows networking diagnostic module

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(UtilityFunctions, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'UtilityFunctions'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > utilityfunctions >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > utilityfunctions >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional: specific function name to get help on
        self.function_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] UtilityFunctions Interaction.
        Imports the Windows networking diagnostic PowerShell module and
        lists its available functions.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally target a specific exported function using 'function_name <name>'
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
    #  UtilityFunctions Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new UtilityFunctions interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'UtilityFunctions_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_function_name(self, function_name):
        """
        Optionally set a specific exported function name to inspect with Get-Help.
        If not set, all exported commands will be listed with Get-Command.
        Example: function_name RegSnapin
        """
        if function_name:
            if self.taskstarted:
                self.function_name = function_name.strip()
                print(self.cl.green("[*] Function name set to: {}".format(self.function_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new UtilityFunctions Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a function name."))


    def do_assigned(self, arg):
        """
        Get the current assigned UtilityFunctions configuration
        """
        print(self.cl.green("[?] Currently Assigned UtilityFunctions Configuration"))
        print("[>] Function Name : {}".format(self.function_name if self.function_name else "(not set — will list all exported commands)"))


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
        self.function_name = None


    ######################################################################
    # UtilityFunctions AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('UtilityFunctions_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_utilityfunctions()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            function_name : str — name of a specific exported function to inspect
                                  if absent, Get-Command is used to list all exports
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.function_name = kwargs.get("function_name", None)
        if self.function_name:
            print(f"[*] Setting function_name attribute : {self.function_name}")
        else:
            print("[*] No function_name provided — will list all exported commands from the module")

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
        ; <      UtilityFunctions Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "UtilityFunctions_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func UtilityFunctions_{}()

            ; Creates a UtilityFunctions Interaction via CMD

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
        Builds the PowerShell commands to type into the CMD window.
        Always imports the UtilityFunctions module and lists its exported commands.
        If function_name is set, also retrieves help for that specific function.
        """
        typing_text = '\n'

        # Import the networking diagnostic module and list all exported commands
        import_cmd = (
            'powershell -ExecutionPolicy Bypass -Command '
            '"Import-Module C:\\Windows\\diagnostics\\system\\Networking\\UtilityFunctions.ps1; '
            'Get-Command -Module UtilityFunctions"'
        )
        typing_text += 'Send("' + self._escape_send(import_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Optionally get help for a specific exported function
        if self.function_name:
            help_cmd = (
                'powershell -ExecutionPolicy Bypass -Command '
                '"Import-Module C:\\Windows\\diagnostics\\system\\Networking\\UtilityFunctions.ps1; '
                'Get-Help {}"'.format(self.function_name)
            )
            typing_text += 'Send("' + self._escape_send(help_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_utilityfunctions(self):
        """
        Closes the UtilityFunctions AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
