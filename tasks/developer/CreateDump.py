
# LOLBAS: createdump.exe — Legitimate use: generating .NET process crash dumps for diagnostics
# DEVELOPER-ONLY: requires .NET Core runtime or Microsoft Visual Studio to be installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer/sysadmin use of createdump.exe to capture
 a minidump of a running .NET process by PID for crash analysis.

 Takes a required process_pid parameter and an optional dump_path.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class CreateDump(BaseCMD):
    """
    # LOLBAS: createdump.exe — Legitimate use: generating .NET process crash dumps for diagnostics
    # DEVELOPER-ONLY: requires .NET Core runtime or Microsoft Visual Studio to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(CreateDump, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'CreateDump'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > createdump >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > createdump >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # PID of the target .NET process to dump
        self.process_pid = None
        # Optional output path for the dump file
        self.dump_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CreateDump Interaction.
        DEVELOPER-ONLY: requires .NET Core runtime or Visual Studio installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process PID using 'process_pid <pid>'
        3: Optionally set an output dump path using 'dump_path <path>'
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
    #  CreateDump Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new CreateDump interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'CreateDump_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_process_pid(self, process_pid):
        """
        Set the PID of the target .NET process to dump.
        Example: process_pid 1234
        """
        if process_pid:
            if self.taskstarted:
                self.process_pid = process_pid.strip()
                print(self.cl.green("[*] Process PID set to: {}".format(self.process_pid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CreateDump Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process PID."))


    def do_dump_path(self, dump_path):
        """
        Optionally set the output path for the dump file.
        If not set, the dump is written to %%TEMP%%\\dump.<pid>.dmp
        Example: dump_path C:\\Temp\\myapp.dmp
        """
        if dump_path:
            if self.taskstarted:
                self.dump_path = dump_path.strip()
                print(self.cl.green("[*] Dump path set to: {}".format(self.dump_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CreateDump Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dump path."))


    def do_assigned(self, arg):
        """
        Get the current assigned CreateDump configuration
        """
        print(self.cl.green("[?] Currently Assigned CreateDump Configuration"))
        print("[>] Process PID : {}".format(self.process_pid if self.process_pid else "(not set)"))
        print("[>] Dump Path   : {}".format(self.dump_path if self.dump_path else "(not set — will use %TEMP%\\dump.<pid>.dmp)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.process_pid:
                print(self.cl.red("[!] <ERROR> A process PID is required. Set it with 'process_pid <pid>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.process_pid = None
        self.dump_path = None


    ######################################################################
    # CreateDump AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('CreateDump_' + current_counter, self.create_autoit_function())


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
            process_pid : str — PID of the target .NET process to dump

        Optional JSON keys:
            dump_path   : str — output path for the dump file;
                                if absent, written to %TEMP%\\dump.<pid>.dmp
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.process_pid = kwargs.get("process_pid", None)
        if self.process_pid:
            print(f"[*] Setting process_pid attribute : {self.process_pid}")
        else:
            print("[!] No process_pid provided — this task requires a PID")

        self.dump_path = kwargs.get("dump_path", None)
        if self.dump_path:
            print(f"[*] Setting dump_path attribute : {self.dump_path}")
        else:
            print("[*] No dump_path provided — dump will be written to %TEMP%\\dump.<pid>.dmp")

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
        ; <      CreateDump Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "CreateDump_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func CreateDump_{}()

            ; Creates a CreateDump Interaction via CMD

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
        Builds the createdump command to type into the CMD window.
        Always uses -n (no heap) for a minidump.
        Optionally specifies an output path with -f.
        """
        typing_text = '\n'

        # Build the createdump command
        if self.dump_path:
            createdump_cmd = 'createdump.exe -n -f {} {}'.format(self.dump_path, self.process_pid)
        else:
            createdump_cmd = 'createdump.exe -n {}'.format(self.process_pid)

        typing_text += 'Send("' + self._escape_send(createdump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the CreateDump AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
