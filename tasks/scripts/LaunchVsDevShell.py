# LOLBAS: Launch-VsDevShell.ps1 — Legitimate use: initialise a Visual Studio Developer PowerShell environment
# DEVELOPER-ONLY: Requires a Visual Studio installation (2019 or 2022) to provide the script and the Enter-VsDevShell cmdlet

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of the Visual Studio-supplied
 Launch-VsDevShell.ps1 script to open a Developer PowerShell session.
 The script locates the VS installation via vswhere.exe and calls
 Enter-VsDevShell to configure the environment for build tooling.

 Takes an optional vs_path parameter pointing to the vswhere.exe
 executable; if absent a default Community 2022 path is used.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class LaunchVsDevShell(BaseCMD):
    """
    # LOLBAS: Launch-VsDevShell.ps1 — Legitimate use: initialise a Visual Studio Developer PowerShell environment
    # DEVELOPER-ONLY: Requires a Visual Studio installation (2019 or 2022)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(LaunchVsDevShell, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'LaunchVsDevShell'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > launchvsdevshell >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > launchvsdevshell >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional path to vswhere.exe; defaults to VS 2022 Community location
        self.vs_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] LaunchVsDevShell Interaction.
        [!] DEVELOPER-ONLY: Requires Visual Studio 2019 or 2022 to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally override the vswhere path using 'vs_path <absolute_path>'
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
    #  LaunchVsDevShell Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new LaunchVsDevShell interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'LaunchVsDevShell_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_vs_path(self, vs_path):
        """
        Optionally override the absolute path to vswhere.exe.
        If not set, the default VS 2022 Community vswhere path is used.
        Example: vs_path C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vswhere.exe
        """
        if vs_path:
            if self.taskstarted:
                self.vs_path = vs_path.strip()
                print(self.cl.green("[*] vswhere path set to: {}".format(self.vs_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new LaunchVsDevShell Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an absolute path to vswhere.exe."))


    def do_assigned(self, arg):
        """
        Get the current assigned LaunchVsDevShell configuration
        """
        default_path = r'C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe'
        print(self.cl.green("[?] Currently Assigned LaunchVsDevShell Configuration"))
        print("[>] vswhere Path : {}".format(self.vs_path if self.vs_path else "(not set — will use default: {})".format(default_path)))


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
        self.vs_path = None


    ######################################################################
    # LaunchVsDevShell AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('LaunchVsDevShell_' + current_counter, self.create_autoit_function())


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
            vs_path : str — absolute path to vswhere.exe; if absent the default
                            VS 2022 Community installer path is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.vs_path = kwargs.get("vs_path", None)
        if self.vs_path:
            print(f"[*] Setting vs_path attribute : {self.vs_path}")
        else:
            print("[*] No vs_path provided — will use default VS 2022 Community vswhere path")

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
        ; <      LaunchVsDevShell Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "LaunchVsDevShell_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func LaunchVsDevShell_{}()

            ; Creates a LaunchVsDevShell Interaction via CMD

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
        Builds the PowerShell command to launch the VS Developer Shell.
        Uses the VsWherePath flag to locate the VS installation.
        If vs_path is not set, falls back to the default VS 2022 Community path.
        """
        default_vswhere = r'C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe'
        effective_path = self.vs_path if self.vs_path else default_vswhere

        script_path = r'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\Launch-VsDevShell.ps1'

        typing_text = '\n'

        # Launch the VS Developer Shell via the signed PowerShell script
        ps_cmd = 'powershell -ep RemoteSigned -f "{}" -VsWherePath "{}"'.format(
            script_path, effective_path
        )
        typing_text += 'Send("' + self._escape_send(ps_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(4000, 8000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the LaunchVsDevShell AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
