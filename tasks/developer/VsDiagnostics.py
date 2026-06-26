
# LOLBAS: VSDiagnostics.exe — Legitimate use: launching diagnostics collection sessions in Visual Studio
# DEVELOPER-ONLY: requires Microsoft Visual Studio installation (path under Program Files\Microsoft Visual Studio)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of VSDiagnostics.exe to start a
 diagnostics collection session that launches a target executable for
 profiling or performance analysis inside Visual Studio tooling.

 Requires a session_id (integer) and a target executable path.
 Optionally accepts launch_args to pass arguments to the launched process.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class VsDiagnostics(BaseCMD):
    """
    # LOLBAS: VSDiagnostics.exe — Legitimate use: launching diagnostics collection sessions in Visual Studio
    # DEVELOPER-ONLY: requires Microsoft Visual Studio installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(VsDiagnostics, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'VsDiagnostics'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > vsdiagnostics >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > vsdiagnostics >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.session_id = '1'
        self.target_exe = None
        self.launch_args = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] VsDiagnostics Interaction.
        DEVELOPER-ONLY: requires Visual Studio installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the session ID using 'session_id <id>'
        3: Set the target executable using 'target_exe <path>'
        4: Optionally set launch arguments using 'launch_args <args>'
        5: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  VsDiagnostics Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new VsDiagnostics interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'VsDiagnostics_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_session_id(self, session_id):
        """
        Set the diagnostics session ID (integer, e.g. 1).
        Example: session_id 1
        """
        if session_id:
            if self.taskstarted:
                self.session_id = session_id.strip()
                print(self.cl.green("[*] Session ID set to: {}".format(self.session_id)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsDiagnostics Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a session ID."))


    def do_target_exe(self, target_exe):
        """
        Set the path to the executable to launch for diagnostics collection.
        Example: target_exe C:\\Windows\\System32\\notepad.exe
        """
        if target_exe:
            if self.taskstarted:
                self.target_exe = target_exe.strip()
                print(self.cl.green("[*] Target executable set to: {}".format(self.target_exe)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsDiagnostics Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target executable path."))


    def do_launch_args(self, launch_args):
        """
        Optionally set arguments to pass to the launched executable.
        Example: launch_args /s myfile.txt
        """
        if launch_args:
            if self.taskstarted:
                self.launch_args = launch_args.strip()
                print(self.cl.green("[*] Launch args set to: {}".format(self.launch_args)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VsDiagnostics Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide launch arguments."))


    def do_assigned(self, arg):
        """
        Get the current assigned VsDiagnostics configuration
        """
        print(self.cl.green("[?] Currently Assigned VsDiagnostics Configuration"))
        print("[>] Session ID   : {}".format(self.session_id))
        print("[>] Target EXE   : {}".format(self.target_exe if self.target_exe else "(not set)"))
        print("[>] Launch Args  : {}".format(self.launch_args if self.launch_args else "(not set)"))


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
        self.session_id = '1'
        self.target_exe = None
        self.launch_args = None


    ######################################################################
    # VsDiagnostics AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('VsDiagnostics_' + current_counter, self.create_autoit_function())


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
            target_exe  : str — path to the executable to launch for diagnostics

        Optional JSON keys:
            session_id  : str — diagnostics session ID (default: '1')
            launch_args : str — arguments passed to the launched executable
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.session_id = kwargs.get("session_id", "1")
        self.target_exe = kwargs.get("target_exe", None)
        self.launch_args = kwargs.get("launch_args", None)

        if self.session_id:
            print(f"[*] Setting session_id attribute : {self.session_id}")
        if self.target_exe:
            print(f"[*] Setting target_exe attribute : {self.target_exe}")
        if self.launch_args:
            print(f"[*] Setting launch_args attribute : {self.launch_args}")

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
        ; <      VsDiagnostics Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "VsDiagnostics_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func VsDiagnostics_{}()

            ; Creates a VsDiagnostics Interaction via CMD

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
        Builds the VsDiagnostics commands to type into the CMD window.
        Starts a diagnostics session using the configured session_id and target_exe.
        If launch_args is set, passes them via /launchArgs.
        """
        typing_text = '\n'

        vsdiag_path = r'VSDiagnostics.exe'

        if self.launch_args:
            cmd_str = '{} start {} /launch:{} /launchArgs:"{}"'.format(
                vsdiag_path,
                self.session_id,
                self.target_exe,
                self.launch_args
            )
        else:
            cmd_str = '{} start {} /launch:{}'.format(
                vsdiag_path,
                self.session_id,
                self.target_exe
            )

        typing_text += 'Send("' + self._escape_send(cmd_str) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Stop the diagnostics session after collection
        stop_cmd = '{} stop {}'.format(vsdiag_path, self.session_id)
        typing_text += 'Send("' + self._escape_send(stop_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the VsDiagnostics AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
