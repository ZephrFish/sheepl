
# LOLBAS: dump64.exe — Legitimate use: creating memory dump files for crash analysis
# DEVELOPER-ONLY: Requires Microsoft Visual Studio installation (ships with VS Installer Feedback component)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of dump64.exe to create a memory dump
 of a running process for crash analysis or debugging.

 Takes a target process ID (pid) parameter; the output dump file path
 defaults to a temp location if not supplied.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Dump64(BaseCMD):
    """
    # LOLBAS: dump64.exe — Legitimate use: creating memory dump files for crash analysis
    # DEVELOPER-ONLY: Requires Microsoft Visual Studio installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Dump64, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Dump64'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dump64 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dump64 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target PID to dump
        self.pid = None
        # Output dump file path
        self.dump_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Dump64 Interaction.
        [!] DEVELOPER-ONLY: Requires Microsoft Visual Studio to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process ID using 'pid <PID>'
        3: Optionally set the output dump file path using 'dump_path <path>'
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
    #  Dump64 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Dump64 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Dump64_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_pid(self, pid):
        """
        Set the target process ID to create a memory dump of.
        Example: pid 1234
        """
        if pid:
            if self.taskstarted:
                self.pid = pid.strip()
                print(self.cl.green("[*] PID set to: {}".format(self.pid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dump64 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process ID."))


    def do_dump_path(self, dump_path):
        """
        Optionally set the output memory dump file path.
        If not set, defaults to %TEMP%\\crash.dmp
        Example: dump_path C:\\Temp\\myapp.dmp
        """
        if dump_path:
            if self.taskstarted:
                self.dump_path = dump_path.strip()
                print(self.cl.green("[*] Dump path set to: {}".format(self.dump_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dump64 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dump file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Dump64 configuration
        """
        print(self.cl.green("[?] Currently Assigned Dump64 Configuration"))
        print("[>] PID       : {}".format(self.pid if self.pid else "(not set)"))
        print("[>] Dump Path : {}".format(self.dump_path if self.dump_path else "%TEMP%\\crash.dmp (default)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.pid:
                print(self.cl.red("[!] <ERROR> You must set a target PID before completing."))
                print(self.cl.red("[!] <ERROR> Use 'pid <PID>' to set the target process ID."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.pid = None
        self.dump_path = None


    ######################################################################
    # Dump64 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Dump64_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_dump64()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            pid       : str — process ID to create a memory dump of

        Optional JSON keys:
            dump_path : str — output file path for the dump (default: %TEMP%\\crash.dmp)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.pid = kwargs.get("pid", None)
        if self.pid:
            print(f"[*] Setting pid attribute : {self.pid}")
        else:
            print("[!] <ERROR> No pid provided — this is required for Dump64.")
            return

        self.dump_path = kwargs.get("dump_path", None)
        if self.dump_path:
            print(f"[*] Setting dump_path attribute : {self.dump_path}")
        else:
            print("[*] No dump_path provided — will use %TEMP%\\crash.dmp")

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
        ; <      Dump64 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Dump64_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Dump64_{}()

            ; Creates a Dump64 Interaction via CMD

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
        Builds the dump64 command to type into the CMD window.
        Uses the configured PID and optional dump output path.
        """
        typing_text = '\n'

        # Determine output dump file path
        out_path = self.dump_path if self.dump_path else r'%TEMP%\crash.dmp'

        # Build the dump64 command using the VS Installer Feedback path
        dump_cmd = (
            r'"C:\Program Files (x86)\Microsoft Visual Studio\Installer\Feedback\dump64.exe"'
            + ' {} {}'.format(self.pid, out_path)
        )
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_dump64(self):
        """
        Closes the Dump64 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
