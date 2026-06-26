
# LOLBAS: DumpMinitool.exe — Legitimate use: creating process memory dumps for diagnostic analysis
# DEVELOPER-ONLY: Requires Visual Studio 2022 installation (ships with Test Platform extensions)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates a developer using DumpMinitool.exe (shipped with Visual Studio 2022)
 to create a full process memory dump for offline diagnostic analysis.

 Takes a required process_id parameter and an optional dump_path parameter
 specifying where to write the .dmp file.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DumpMinitool(BaseCMD):
    """
    # LOLBAS: DumpMinitool.exe — Legitimate use: creating process memory dumps for diagnostic analysis
    # DEVELOPER-ONLY: Requires Visual Studio 2022 (Community/Professional/Enterprise)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DumpMinitool, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DumpMinitool'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dumpminitool >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dumpminitool >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Process ID to dump
        self.process_id = None
        # Output dump file path
        self.dump_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DumpMinitool Interaction.
        [!] DEVELOPER-ONLY: Requires Visual Studio 2022.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process ID using 'process_id <pid>'
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
    #  DumpMinitool Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DumpMinitool interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DumpMinitool_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_process_id(self, process_id):
        """
        Set the target process ID to dump.
        Example: process_id 1234
        """
        if process_id:
            if self.taskstarted:
                self.process_id = process_id.strip()
                print(self.cl.green("[*] Process ID set to: {}".format(self.process_id)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DumpMinitool Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process ID."))


    def do_dump_path(self, dump_path):
        """
        Optionally set the output path for the dump file.
        If not set, defaults to C:\\Temp\\process_dump.dmp
        Example: dump_path C:\\Temp\\myapp_dump.dmp
        """
        if dump_path:
            if self.taskstarted:
                self.dump_path = dump_path.strip()
                print(self.cl.green("[*] Dump path set to: {}".format(self.dump_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DumpMinitool Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dump file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned DumpMinitool configuration
        """
        print(self.cl.green("[?] Currently Assigned DumpMinitool Configuration"))
        print("[>] Process ID : {}".format(self.process_id if self.process_id else "(not set)"))
        print("[>] Dump Path  : {}".format(self.dump_path if self.dump_path else "(not set — will use C:\\Temp\\process_dump.dmp)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.process_id:
                print(self.cl.red("[!] <ERROR> process_id must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.process_id = None
        self.dump_path = None


    ######################################################################
    # DumpMinitool AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DumpMinitool_' + current_counter, self.create_autoit_function())


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
            process_id : str — PID of the process to dump

        Optional JSON keys:
            dump_path  : str — output path for the .dmp file
                               if absent, defaults to C:\\Temp\\process_dump.dmp
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.process_id = kwargs.get("process_id", None)
        if self.process_id:
            print(f"[*] Setting process_id attribute : {self.process_id}")
        else:
            print("[!] <ERROR> process_id is required for DumpMinitool.")
            return

        self.dump_path = kwargs.get("dump_path", None)
        if self.dump_path:
            print(f"[*] Setting dump_path attribute : {self.dump_path}")
        else:
            print("[*] No dump_path provided — will use C:\\Temp\\process_dump.dmp")

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
        ; <      DumpMinitool Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DumpMinitool_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DumpMinitool_{}()

            ; Creates a DumpMinitool Interaction via CMD

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
        Builds the DumpMinitool command to type into the CMD window.
        Uses the full VS2022 path to DumpMinitool.exe with a Full dump type.
        """
        typing_text = '\n'

        # Resolve the output dump path
        output_path = self.dump_path if self.dump_path else r'C:\Temp\process_dump.dmp'

        dump_cmd = (
            r'"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE'
            r'\Extensions\TestPlatform\Extensions\DumpMinitool.exe"'
            ' --file {} --processId {} --dumpType Full'.format(output_path, self.process_id)
        )

        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(4000, 10000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the DumpMinitool AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
