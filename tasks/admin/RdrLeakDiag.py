
# LOLBAS: rdrleakdiag.exe — Legitimate use: diagnosing resource leaks by dumping process memory

# #######################################################################
#
#  Task : RdrLeakDiag Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of rdrleakdiag.exe to dump a process by PID
 for resource-leak diagnostics. Produces minidump_<PID>.dmp and
 results_<PID>.hlk in the specified output directory.

 Takes a pid parameter (target process ID) and an output_dir parameter
 (absolute path for dump output). Defaults are provided if absent.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class RdrLeakDiag(BaseCMD):
    """
    # LOLBAS: rdrleakdiag.exe — Legitimate use: diagnosing resource leaks by dumping process memory

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(RdrLeakDiag, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'RdrLeakDiag'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > rdrleakdiag >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > rdrleakdiag >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target process PID to dump
        self.pid = None
        # Output directory for dump files
        self.output_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] RdrLeakDiag Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set target process PID using 'pid <pid>'
        3: Set output directory using 'output_dir <path>'
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
    #  RdrLeakDiag Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new RdrLeakDiag interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'RdrLeakDiag_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_pid(self, pid):
        """
        Set the target process PID to dump.
        Example: pid 940
        """
        if pid:
            if self.taskstarted:
                self.pid = pid.strip()
                print(self.cl.green("[*] PID set to: {}".format(self.pid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RdrLeakDiag Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process PID."))


    def do_output_dir(self, output_dir):
        """
        Set the absolute output directory path where dump files will be written.
        Example: output_dir C:\\Temp\\dumps
        """
        if output_dir:
            if self.taskstarted:
                self.output_dir = output_dir.strip()
                print(self.cl.green("[*] Output directory set to: {}".format(self.output_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RdrLeakDiag Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned RdrLeakDiag configuration
        """
        print(self.cl.green("[?] Currently Assigned RdrLeakDiag Configuration"))
        print("[>] PID        : {}".format(self.pid if self.pid else "(not set — default: 940)"))
        print("[>] Output Dir : {}".format(self.output_dir if self.output_dir else "(not set — default: C:\\Temp)"))


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
        self.pid = None
        self.output_dir = None


    ######################################################################
    # RdrLeakDiag AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('RdrLeakDiag_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_rdrleakdiag()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            pid        : str — target process PID (default: 940)
            output_dir : str — absolute path for dump output (default: C:\\Temp)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.pid = kwargs.get("pid", "940")
        self.output_dir = kwargs.get("output_dir", "C:\\Temp")

        print(f"[*] Setting pid attribute : {self.pid}")
        print(f"[*] Setting output_dir attribute : {self.output_dir}")

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
        ; <      RdrLeakDiag Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "RdrLeakDiag_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func RdrLeakDiag_{}()

            ; Creates a RdrLeakDiag Interaction via CMD

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
        Builds the rdrleakdiag command to type into the CMD window.
        Uses the configured PID and output directory to produce a full memory dump.
        Falls back to sensible defaults if not set interactively.
        """
        typing_text = '\n'

        pid = self.pid if self.pid else "940"
        output_dir = self.output_dir if self.output_dir else "C:\\Temp"

        dump_cmd = 'rdrleakdiag.exe /p {} /o {} /fullmemdmp /wait 1'.format(pid, output_dir)
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_rdrleakdiag(self):
        """
        Closes the RdrLeakDiag AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
