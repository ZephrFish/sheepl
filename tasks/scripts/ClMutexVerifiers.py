
# LOLBAS: CL_Mutexverifiers.ps1 — Legitimate use: Windows diagnostic script for mutex verification in troubleshooting workflows

# #######################################################################
#
#  Task : CL_Mutexverifiers PowerShell Diagnostic Script Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of the Windows built-in CL_Mutexverifiers.ps1
 diagnostic PowerShell script by dot-sourcing it and calling
 runAfterCancelProcess to launch a specified executable, as used in
 Windows diagnostic troubleshooting workflows.

 Requires a target executable path parameter (target_path).
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


class ClMutexVerifiers(BaseCMD):
    """
    # LOLBAS: CL_Mutexverifiers.ps1 — Legitimate use: Windows diagnostic script for mutex verification

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ClMutexVerifiers, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ClMutexVerifiers'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cl_mutexverifiers >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cl_mutexverifiers >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the target executable to run via runAfterCancelProcess
        self.target_path = None

        # Diagnostic script base path (AERO variant by default)
        self.script_path = r'C:\Windows\diagnostics\system\AERO\CL_Mutexverifiers.ps1'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CL_Mutexverifiers PowerShell Diagnostic Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target executable path using 'target_path <path>'
        3: Optionally set a custom script path using 'script_path <path>'
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
    #  ClMutexVerifiers Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ClMutexVerifiers interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ClMutexVerifiers_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_path(self, target_path):
        """
        Set the path to the executable to launch via runAfterCancelProcess.
        Example: target_path C:\\Windows\\System32\\notepad.exe
        """
        if target_path:
            if self.taskstarted:
                self.target_path = target_path.strip()
                print(self.cl.green("[*] Target path set to: {}".format(self.target_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClMutexVerifiers Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target executable path."))


    def do_script_path(self, script_path):
        """
        Optionally override the default CL_Mutexverifiers.ps1 script path.
        Default: C:\\Windows\\diagnostics\\system\\AERO\\CL_Mutexverifiers.ps1
        Other valid paths include Audio, WindowsUpdate, Video, Speech variants.
        Example: script_path C:\\Windows\\diagnostics\\system\\Audio\\CL_Mutexverifiers.ps1
        """
        if script_path:
            if self.taskstarted:
                self.script_path = script_path.strip()
                print(self.cl.green("[*] Script path set to: {}".format(self.script_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClMutexVerifiers Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a script path."))


    def do_assigned(self, arg):
        """
        Get the current assigned ClMutexVerifiers configuration
        """
        print(self.cl.green("[?] Currently Assigned ClMutexVerifiers Configuration"))
        print("[>] Script Path  : {}".format(self.script_path))
        print("[>] Target Path  : {}".format(self.target_path if self.target_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_path:
                print(self.cl.red("[!] <ERROR> target_path must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_path = None
        self.script_path = r'C:\Windows\diagnostics\system\AERO\CL_Mutexverifiers.ps1'


    ######################################################################
    # ClMutexVerifiers AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ClMutexVerifiers_' + current_counter, self.create_autoit_function())


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
            target_path : str — path to the executable to launch via runAfterCancelProcess

        Optional JSON keys:
            script_path : str — path to CL_Mutexverifiers.ps1 (defaults to AERO variant)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_path = kwargs.get("target_path", None)
        if self.target_path:
            print(f"[*] Setting target_path attribute : {self.target_path}")
        else:
            print("[!] <ERROR> target_path is required for ClMutexVerifiers task.")
            return

        self.script_path = kwargs.get("script_path", r'C:\Windows\diagnostics\system\AERO\CL_Mutexverifiers.ps1')
        print(f"[*] Setting script_path attribute : {self.script_path}")

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
        ; <      ClMutexVerifiers Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ClMutexVerifiers_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func ClMutexVerifiers_{}()

            ; Creates a ClMutexVerifiers Interaction via CMD

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
        Builds the PowerShell command to dot-source CL_Mutexverifiers.ps1
        and call runAfterCancelProcess with the target executable path.
        """
        typing_text = '\n'

        # Build the PowerShell command and escape it for AutoIT Send()
        escaped_cmd = self._escape_send(
            'powershell -Command ". \'{}\'; runAfterCancelProcess \'{}\'"'.format(
                self.script_path, self.target_path
            )
        )

        typing_text += 'Send("' + escaped_cmd + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the ClMutexVerifiers AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
