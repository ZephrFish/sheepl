
# LOLBAS: comsvcs.dll — Legitimate use: creating process memory dump files via MiniDumpWriteDump for crash analysis

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrator use of comsvcs.dll via rundll32 to
 create a process memory dump using the MiniDump exported function.
 This wraps MiniDumpWriteDump and is used for crash diagnostics and
 memory analysis by support and operations teams.

 Requires a target process PID and an output path for the dump file.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Comsvcs(BaseCMD):
    """
    # LOLBAS: comsvcs.dll — Legitimate use: creating process memory dump files via MiniDumpWriteDump for crash analysis

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Comsvcs, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Comsvcs'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > comsvcs >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > comsvcs >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target process PID to dump
        self.target_pid = None
        # Output path for the dump file
        self.dump_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Comsvcs DLL Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process PID using 'target_pid <pid>'
        3: Set the output dump file path using 'dump_path <path>'
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
    #  Comsvcs Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Comsvcs interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Comsvcs_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_pid(self, target_pid):
        """
        Set the PID of the process to dump.
        Example: target_pid 1234
        """
        if target_pid:
            if self.taskstarted:
                self.target_pid = target_pid.strip()
                print(self.cl.green("[*] Target PID set to: {}".format(self.target_pid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Comsvcs Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process PID."))


    def do_dump_path(self, dump_path):
        """
        Set the output file path for the memory dump.
        Example: dump_path C:\\Temp\\process.dmp
        """
        if dump_path:
            if self.taskstarted:
                self.dump_path = dump_path.strip()
                print(self.cl.green("[*] Dump path set to: {}".format(self.dump_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Comsvcs Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dump file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Comsvcs configuration
        """
        print(self.cl.green("[?] Currently Assigned Comsvcs Configuration"))
        print("[>] Target PID : {}".format(self.target_pid if self.target_pid else "(not set)"))
        print("[>] Dump Path  : {}".format(self.dump_path if self.dump_path else "(not set — will use C:\\Temp\\process.dmp)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            # Apply defaults if not set
            if not self.target_pid:
                self.target_pid = '1234'
                print(self.cl.yellow("[*] No PID set — using default placeholder PID: 1234"))
            if not self.dump_path:
                self.dump_path = 'C:\\Temp\\process.dmp'
                print(self.cl.yellow("[*] No dump path set — using default: C:\\Temp\\process.dmp"))
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_pid = None
        self.dump_path = None


    ######################################################################
    # Comsvcs AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Comsvcs_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_comsvcs()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            target_pid : str — PID of the process to dump
            dump_path  : str — output file path for the memory dump
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_pid = kwargs.get("target_pid", "1234")
        self.dump_path = kwargs.get("dump_path", "C:\\Temp\\process.dmp")
        print(f"[*] Setting target_pid attribute : {self.target_pid}")
        print(f"[*] Setting dump_path attribute  : {self.dump_path}")

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
        ; <      Comsvcs Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Comsvcs_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Comsvcs_{}()

            ; Creates a Comsvcs Interaction via CMD

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
        Builds the rundll32 comsvcs.dll MiniDump command to type into the CMD window.
        Uses the MiniDump export to write a process memory dump to the specified path.
        """
        typing_text = '\n'

        # Invoke MiniDump via comsvcs.dll through rundll32
        dump_cmd = 'rundll32.exe comsvcs.dll MiniDump {} {} full'.format(
            self.target_pid, self.dump_path
        )
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_comsvcs(self):
        """
        Closes the Comsvcs AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
