
# LOLBAS: AccCheckConsole.exe — Legitimate use: verifying UI accessibility requirements for a window
# DEVELOPER-ONLY: Requires Windows SDK / Windows Kits 10 (AccChecker tool)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of AccCheckConsole.exe to verify
 UI accessibility requirements against a named window using a custom
 verification DLL (as documented in the Windows Accessibility SDK).

 Takes a window_name parameter (the target window to check) and an
 optional dll_path for a custom verification DLL assembly.

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


class AccCheckConsole(BaseCMD):
    """
    # LOLBAS: AccCheckConsole.exe — Legitimate use: verifying UI accessibility requirements for a window
    # DEVELOPER-ONLY: Requires Windows SDK / Windows Kits 10 (AccChecker tool)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(AccCheckConsole, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'AccCheckConsole'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > acccheckconsole >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > acccheckconsole >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target window name to check accessibility on
        self.window_name = None
        # Optional path to a custom verification DLL
        self.dll_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] AccCheckConsole Interaction.
        [!] DEVELOPER-ONLY: Requires Windows SDK (AccChecker).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target window name using 'window_name <name>'
        3: Optionally set a verification DLL using 'dll_path <path>'
        4: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  AccCheckConsole Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new AccCheckConsole interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'AccCheckConsole_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_window_name(self, window_name):
        """
        Set the name of the window to run accessibility checks against.
        Example: window_name Untitled - Notepad
        """
        if window_name:
            if self.taskstarted:
                self.window_name = window_name.strip()
                print(self.cl.green("[*] Window name set to: {}".format(self.window_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AccCheckConsole Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a window name."))


    def do_dll_path(self, dll_path):
        """
        Optionally set the path to a custom verification DLL assembly.
        If not set, AccCheckConsole runs with no additional DLL argument.
        Example: dll_path C:\\AccCheck\\MyVerification.dll
        """
        if dll_path:
            if self.taskstarted:
                self.dll_path = dll_path.strip()
                print(self.cl.green("[*] DLL path set to: {}".format(self.dll_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AccCheckConsole Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL path."))


    def do_assigned(self, arg):
        """
        Get the current assigned AccCheckConsole configuration
        """
        print(self.cl.green("[?] Currently Assigned AccCheckConsole Configuration"))
        print("[>] Window Name : {}".format(self.window_name if self.window_name else "(not set)"))
        print("[>] DLL Path    : {}".format(self.dll_path if self.dll_path else "(not set — no DLL argument)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.window_name:
                print(self.cl.red("[!] <ERROR> window_name is required. Set it using 'window_name <name>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.window_name = None
        self.dll_path = None


    ######################################################################
    # AccCheckConsole AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('AccCheckConsole_' + current_counter, self.create_autoit_function())


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

        Required JSON keys:
            window_name : str — the name of the window to run accessibility checks against

        Optional JSON keys:
            dll_path    : str — path to a custom verification DLL assembly
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.window_name = kwargs.get("window_name", None)
        if self.window_name:
            print(f"[*] Setting window_name attribute : {self.window_name}")
        else:
            print("[!] No window_name provided — this is required")

        self.dll_path = kwargs.get("dll_path", None)
        if self.dll_path:
            print(f"[*] Setting dll_path attribute : {self.dll_path}")
        else:
            print("[*] No dll_path provided — running without DLL argument")

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
        ; <      AccCheckConsole Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "AccCheckConsole_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func AccCheckConsole_{}()

            ; Creates an AccCheckConsole Interaction via CMD

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
        Builds the AccCheckConsole command to type into the CMD window.
        Uses the -window flag with the supplied window_name, and optionally
        appends a DLL path for custom verification routines.
        """
        typing_text = '\n'

        # Build the AccCheckConsole command
        if self.dll_path:
            acc_cmd = 'AccCheckConsole.exe -window "{}" {}'.format(self.window_name, self.dll_path)
        else:
            acc_cmd = 'AccCheckConsole.exe -window "{}"'.format(self.window_name)

        typing_text += 'Send("' + self._escape_send(acc_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the AccCheckConsole AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
