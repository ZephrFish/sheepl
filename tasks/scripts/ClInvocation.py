
# LOLBAS: CL_Invocation.ps1 — Legitimate use: running Windows Aero/Audio/Update diagnostics via SyncInvoke

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of the Windows diagnostic script CL_Invocation.ps1
 (found under C:\Windows\diagnostics\system\AERO, Audio, or WindowsUpdate).
 Imports the script in PowerShell and calls SyncInvoke to execute a target executable
 as part of a diagnostic workflow.

 Takes a diagnostic_path parameter (defaults to AERO) and an executable to invoke.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class ClInvocation(BaseCMD):
    """
    # LOLBAS: CL_Invocation.ps1 — Legitimate use: running Windows Aero/Audio/Update diagnostics via SyncInvoke

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ClInvocation, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ClInvocation'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > clinvocation >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > clinvocation >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Diagnostic category: AERO, Audio, or WindowsUpdate
        self.diagnostic_path = 'AERO'
        # Executable to invoke via SyncInvoke (defaults to msinfo32.exe)
        self.invoke_exe = 'msinfo32.exe'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CL_Invocation Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a diagnostic path using 'diagnostic_path <AERO|Audio|WindowsUpdate>'
        3: Optionally set an executable to invoke using 'invoke_exe <executable>'
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
    #  ClInvocation Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ClInvocation interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ClInvocation_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_diagnostic_path(self, diagnostic_path):
        """
        Set the diagnostic category subfolder for CL_Invocation.ps1.
        Valid options: AERO, Audio, WindowsUpdate
        Example: diagnostic_path Audio
        """
        valid_paths = ['AERO', 'Audio', 'WindowsUpdate']
        if diagnostic_path:
            if self.taskstarted:
                dp = diagnostic_path.strip()
                if dp in valid_paths:
                    self.diagnostic_path = dp
                    print(self.cl.green("[*] Diagnostic path set to: {}".format(self.diagnostic_path)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid path. Choose from: {}".format(', '.join(valid_paths))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClInvocation Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a diagnostic path."))


    def do_invoke_exe(self, invoke_exe):
        """
        Set the executable to run via SyncInvoke.
        Example: invoke_exe msinfo32.exe
        """
        if invoke_exe:
            if self.taskstarted:
                self.invoke_exe = invoke_exe.strip()
                print(self.cl.green("[*] Invoke executable set to: {}".format(self.invoke_exe)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClInvocation Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an executable name."))


    def do_assigned(self, arg):
        """
        Get the current assigned ClInvocation configuration
        """
        print(self.cl.green("[?] Currently Assigned ClInvocation Configuration"))
        print("[>] Diagnostic Path : {}".format(self.diagnostic_path))
        print("[>] Invoke Exe      : {}".format(self.invoke_exe))


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
        self.diagnostic_path = 'AERO'
        self.invoke_exe = 'msinfo32.exe'


    ######################################################################
    # ClInvocation AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ClInvocation_' + current_counter, self.create_autoit_function())


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
            diagnostic_path : str — AERO, Audio, or WindowsUpdate (default: AERO)
            invoke_exe      : str — executable to run via SyncInvoke (default: msinfo32.exe)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.diagnostic_path = kwargs.get("diagnostic_path", "AERO")
        self.invoke_exe = kwargs.get("invoke_exe", "msinfo32.exe")
        print(f"[*] Setting diagnostic_path attribute : {self.diagnostic_path}")
        print(f"[*] Setting invoke_exe attribute : {self.invoke_exe}")

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
        ; <      ClInvocation Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ClInvocation_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func ClInvocation_{}()

            ; Creates a ClInvocation Interaction via CMD

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
        Builds the PowerShell CL_Invocation.ps1 command to type into the CMD window.
        Dot-sources the diagnostic script and calls SyncInvoke with the target executable.
        """
        typing_text = '\n'

        script_path = 'C:\\Windows\\diagnostics\\system\\{}\\CL_Invocation.ps1'.format(self.diagnostic_path)
        ps_cmd = 'powershell -Command ". \'{}\'; SyncInvoke {}"'.format(script_path, self.invoke_exe)

        typing_text += 'Send("' + self._escape_send(ps_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the ClInvocation AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
