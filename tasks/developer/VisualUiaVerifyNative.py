
# LOLBAS: VisualUiaVerifyNative.exe — Legitimate use: manual and automated testing of UI Automation implementation and controls
# DEVELOPER-ONLY: Requires Windows SDK / Windows Kits 10 installation (UIAVerify component)

r"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of VisualUiaVerifyNative.exe to launch
 the Visual UI Automation Verify tool for inspecting and testing UI Automation
 implementations on controls and applications.

 VisualUiaVerifyNative.exe is part of the Windows SDK and lives under:
   c:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\UIAVerify\
 It launches a GUI application — no command-line parameters are needed
 for normal developer use.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class VisualUiaVerifyNative(BaseCMD):
    """
    # LOLBAS: VisualUiaVerifyNative.exe — Legitimate use: manual and automated testing of UI Automation implementation and controls
    # DEVELOPER-ONLY: Requires Windows SDK / Windows Kits 10 installation (UIAVerify component)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(VisualUiaVerifyNative, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'VisualUiaVerifyNative'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > visualuiaverifynative >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > visualuiaverifynative >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the VisualUiaVerifyNative executable (SDK version-agnostic via glob or known path)
        self.exe_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] VisualUiaVerifyNative Interaction.
        [!] DEVELOPER-ONLY: Requires Windows SDK (UIAVerify) to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the full exe path using 'exe_path <path>'
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
    #  VisualUiaVerifyNative Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new VisualUiaVerifyNative interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'VisualUiaVerifyNative_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_exe_path(self, exe_path):
        """
        Optionally set the full path to VisualUiaVerifyNative.exe.
        If not set, the default SDK x64 path will be used.
        Example: exe_path C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.22621.0\\x64\\UIAVerify\\VisualUiaVerifyNative.exe
        """
        if exe_path:
            if self.taskstarted:
                self.exe_path = exe_path.strip()
                print(self.cl.green("[*] exe_path set to: {}".format(self.exe_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VisualUiaVerifyNative Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to VisualUiaVerifyNative.exe."))


    def do_assigned(self, arg):
        """
        Get the current assigned VisualUiaVerifyNative configuration
        """
        print(self.cl.green("[?] Currently Assigned VisualUiaVerifyNative Configuration"))
        print("[>] exe_path : {}".format(self.exe_path if self.exe_path else "(not set — will use default SDK x64 path)"))


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
        self.exe_path = None


    ######################################################################
    # VisualUiaVerifyNative AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('VisualUiaVerifyNative_' + current_counter, self.create_autoit_function())


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
            exe_path : str — full path to VisualUiaVerifyNative.exe
                             if absent, default SDK x64 path is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.exe_path = kwargs.get("exe_path", None)
        if self.exe_path:
            print(f"[*] Setting exe_path attribute : {self.exe_path}")
        else:
            print("[*] No exe_path provided — will use default SDK x64 path")

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
        ; <   VisualUiaVerifyNative Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "VisualUiaVerifyNative_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func VisualUiaVerifyNative_{}()

            ; Creates a VisualUiaVerifyNative Interaction via CMD

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
        Builds the VisualUiaVerifyNative command to type into the CMD window.
        Launches the tool from its SDK installation path.
        If exe_path is set it is used directly; otherwise the default x64 path is used.
        """
        typing_text = '\n'

        # Determine the executable path to invoke
        if self.exe_path:
            launch_cmd = '"{}"'.format(self.exe_path)
        else:
            launch_cmd = '"C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.22621.0\\x64\\UIAVerify\\VisualUiaVerifyNative.exe"'

        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Wait for the GUI tool window to appear and then close it
        typing_text += 'WinWaitActive("Visual UI Automation Verify", "", 15)\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += 'WinClose("Visual UI Automation Verify")\n'
        typing_text += 'sleep({})\n'.format(random.randint(1000, 3000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the VisualUiaVerifyNative AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
