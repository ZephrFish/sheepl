
# LOLBAS: VSIISExeLauncher.exe — Legitimate use: launching IIS Express processes with arguments during VS/VSCode development
# DEVELOPER-ONLY: Requires Visual Studio or VSCode installation (ships under VS Web Tools extension path)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of VSIISExeLauncher.exe to launch
 a target executable with arguments, as done by Visual Studio when
 starting IIS Express-hosted web projects during development.

 Takes a target_path parameter (path to executable) and optional
 target_args parameter (arguments to pass to the executable).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class VsIisExeLauncher(BaseCMD):
    """
    # LOLBAS: VSIISExeLauncher.exe — Legitimate use: launching IIS Express processes with arguments during VS/VSCode development
    # DEVELOPER-ONLY: Requires Visual Studio or VSCode installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(VsIisExeLauncher, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'VsIisExeLauncher'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > vsiisexelauncher >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > vsiisexelauncher >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the executable to launch via VSIISExeLauncher
        self.target_path = None
        # Optional arguments to pass to the target executable
        self.target_args = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] VsIisExeLauncher Interaction.
        [!] DEVELOPER-ONLY: Requires Visual Studio or VSCode installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target executable path using 'target_path <path>'
        3: Optionally set arguments using 'target_args <args>'
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
    #  VsIisExeLauncher Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new VsIisExeLauncher interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'VsIisExeLauncher_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_path(self, target_path):
        """
        Set the path to the executable to be launched via VSIISExeLauncher.
        Example: target_path C:\\Windows\\System32\\notepad.exe
        """
        if target_path:
            if self.taskstarted:
                self.target_path = target_path.strip()
                print(self.cl.green("[*] Target path set to: {}".format(self.target_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsIisExeLauncher Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target executable path."))


    def do_target_args(self, target_args):
        """
        Optionally set arguments to pass to the target executable.
        Example: target_args /quiet /norestart
        """
        if target_args:
            if self.taskstarted:
                self.target_args = target_args.strip()
                print(self.cl.green("[*] Target args set to: {}".format(self.target_args)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsIisExeLauncher Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide target arguments."))


    def do_assigned(self, arg):
        """
        Get the current assigned VsIisExeLauncher configuration
        """
        print(self.cl.green("[?] Currently Assigned VsIisExeLauncher Configuration"))
        print("[>] Target Path : {}".format(self.target_path if self.target_path else "(not set)"))
        print("[>] Target Args : {}".format(self.target_args if self.target_args else "(not set)"))


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
        self.target_args = None


    ######################################################################
    # VsIisExeLauncher AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('VsIisExeLauncher_' + current_counter, self.create_autoit_function())


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
            target_path : str — full path to the executable to launch via VSIISExeLauncher

        Optional JSON keys:
            target_args : str — arguments to pass to the target executable
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_path = kwargs.get("target_path", None)
        if self.target_path:
            print(f"[*] Setting target_path attribute : {self.target_path}")
        else:
            print("[!] No target_path provided — this is required for VsIisExeLauncher")

        self.target_args = kwargs.get("target_args", None)
        if self.target_args:
            print(f"[*] Setting target_args attribute : {self.target_args}")
        else:
            print("[*] No target_args provided — launching target without additional arguments")

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
        ; <      VsIisExeLauncher Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "VsIisExeLauncher_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func VsIisExeLauncher_{}()

            ; Creates a VsIisExeLauncher Interaction via CMD

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
        Builds the VSIISExeLauncher command to type into the CMD window.
        Launches the target executable via VSIISExeLauncher -p <path> with optional -a <args>.
        """
        typing_text = '\n'

        launcher_path = (
            '"C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community'
            '\\Common7\\IDE\\Extensions\\Microsoft\\Web Tools\\ProjectSystem'
            '\\VSIISExeLauncher.exe"'
        )

        if self.target_args:
            launch_cmd = '{} -p "{}" -a "{}"'.format(
                launcher_path,
                self.target_path,
                self.target_args
            )
        else:
            launch_cmd = '{} -p "{}"'.format(launcher_path, self.target_path)

        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the VsIisExeLauncher AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
