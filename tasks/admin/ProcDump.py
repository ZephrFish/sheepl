
# LOLBAS: procdump.exe — Legitimate use: capturing process memory dumps for crash diagnostics

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT/developer use of Sysinternals ProcDump to capture
 a full memory dump of a running process for crash analysis or diagnostics.

 Takes a target_process parameter (name or PID) and an optional output_path
 for the dump file; if output_path is absent a default temp location is used.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class ProcDump(BaseCMD):
    """
    # LOLBAS: procdump.exe — Legitimate use: capturing process memory dumps for crash diagnostics

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ProcDump, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ProcDump'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > procdump >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > procdump >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target process name or PID to dump
        self.target_process = None
        # Optional output path for the .dmp file
        self.output_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] ProcDump Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process using 'target_process <name_or_pid>'
        3: Optionally set an output path using 'output_path <path>'
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
    #  ProcDump Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ProcDump interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ProcDump_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_process(self, target_process):
        """
        Set the target process name or PID to dump.
        Example: target_process explorer.exe
        Example: target_process 1234
        """
        if target_process:
            if self.taskstarted:
                self.target_process = target_process.strip()
                print(self.cl.green("[*] Target process set to: {}".format(self.target_process)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ProcDump Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process name or PID."))


    def do_output_path(self, output_path):
        """
        Optionally set the output path for the dump file.
        If not set, defaults to C:\\Windows\\Temp\\dump.dmp
        Example: output_path C:\\Temp\\myapp_crash.dmp
        """
        if output_path:
            if self.taskstarted:
                self.output_path = output_path.strip()
                print(self.cl.green("[*] Output path set to: {}".format(self.output_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ProcDump Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned ProcDump configuration
        """
        print(self.cl.green("[?] Currently Assigned ProcDump Configuration"))
        print("[>] Target Process : {}".format(self.target_process if self.target_process else "(not set)"))
        print("[>] Output Path    : {}".format(self.output_path if self.output_path else "(not set — will use C:\\Windows\\Temp\\dump.dmp)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_process:
                print(self.cl.red("[!] <ERROR> A target process must be set. Use 'target_process <name_or_pid>'"))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_process = None
        self.output_path = None


    ######################################################################
    # ProcDump AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ProcDump_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_procdump()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            target_process : str — process name or PID to dump (e.g. "explorer.exe" or "1234")

        Optional JSON keys:
            output_path : str — full path for the .dmp output file
                                if absent, defaults to C:\\Windows\\Temp\\dump.dmp
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_process = kwargs.get("target_process", None)
        self.output_path = kwargs.get("output_path", None)

        if self.target_process:
            print(f"[*] Setting target_process attribute : {self.target_process}")
        else:
            print("[!] <ERROR> No target_process provided — cannot create ProcDump block")
            return

        if self.output_path:
            print(f"[*] Setting output_path attribute : {self.output_path}")
        else:
            print("[*] No output_path provided — will default to C:\\Windows\\Temp\\dump.dmp")

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
        ; <      ProcDump Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ProcDump_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func ProcDump_{}()

            ; Creates a ProcDump Interaction via CMD

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
        Builds the procdump command to type into the CMD window.
        Captures a full memory dump of the target process.
        Uses the specified output_path or falls back to a default temp path.
        """
        typing_text = '\n'

        # Resolve output path
        dump_path = self.output_path if self.output_path else 'C:\\Windows\\Temp\\dump.dmp'

        # Accept the Sysinternals EULA silently and write a full dump
        dump_cmd = 'procdump.exe -accepteula -ma {} {}'.format(self.target_process, dump_path)
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(4000, 12000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_procdump(self):
        """
        Closes the ProcDump AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
