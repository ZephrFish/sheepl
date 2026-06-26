
# LOLBAS: vsjitdebugger.exe — Legitimate use: launching a target executable under the Visual Studio Just-In-Time debugger
# DEVELOPER-ONLY: requires Visual Studio to be installed (ships vsjitdebugger.exe)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of vsjitdebugger.exe to launch a
 local executable as a subprocess under the Visual Studio Just-In-Time
 (JIT) debugger.  A target executable path must be provided.

 The master script will already define the typing speed as part of
 the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class VsJitDebugger(BaseCMD):
    """
    # LOLBAS: vsjitdebugger.exe — Legitimate use: launching a target executable under the Visual Studio Just-In-Time debugger
    # DEVELOPER-ONLY: requires Visual Studio to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(VsJitDebugger, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'VsJitDebugger'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > vsjitdebugger >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > vsjitdebugger >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the target executable to launch under the JIT debugger
        self.target_exe = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] VsJitDebugger Interaction.
        [!] DEVELOPER-ONLY: requires Visual Studio installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target executable using 'target_exe <path>'
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
    #  VsJitDebugger Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new VsJitDebugger interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'VsJitDebugger_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_exe(self, target_exe):
        """
        Set the path to the executable to launch under vsjitdebugger.exe.
        Example: target_exe C:\\Windows\\System32\\calc.exe
        """
        if target_exe:
            if self.taskstarted:
                self.target_exe = target_exe.strip()
                print(self.cl.green("[*] Target executable set to: {}".format(self.target_exe)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsJitDebugger Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target executable path."))


    def do_assigned(self, arg):
        """
        Get the current assigned VsJitDebugger configuration
        """
        print(self.cl.green("[?] Currently Assigned VsJitDebugger Configuration"))
        print("[>] Target EXE : {}".format(self.target_exe if self.target_exe else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_exe:
                print(self.cl.red("[!] <ERROR> You must set a target_exe before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_exe = None


    ######################################################################
    # VsJitDebugger AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('VsJitDebugger_' + current_counter, self.create_autoit_function())


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
            target_exe : str — full path to the executable to launch under
                               vsjitdebugger.exe (e.g. C:\\Windows\\System32\\calc.exe)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_exe = kwargs.get("target_exe", None)
        if self.target_exe:
            print(f"[*] Setting target_exe attribute : {self.target_exe}")
        else:
            print("[!] <ERROR> No target_exe provided — this task requires a target executable path.")
            return

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
        ; <      VsJitDebugger Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "VsJitDebugger_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func VsJitDebugger_{}()

            ; Creates a VsJitDebugger Interaction via CMD

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
        Builds the vsjitdebugger command to type into the CMD window.
        Launches the target executable as a subprocess of vsjitdebugger.exe.
        """
        typing_text = '\n'

        # Launch target exe under the JIT debugger
        jit_cmd = 'vsjitdebugger.exe {}'.format(self.target_exe)
        typing_text += 'Send("' + self._escape_send(jit_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the VsJitDebugger AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
