
# LOLBAS: SqlDumper.exe — Legitimate use: generate a process memory dump file for SQL Server diagnostics
# #######################################################################
#
#  Task : SqlDumper Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of SqlDumper.exe to generate a process
 memory dump file for diagnostic purposes (e.g. SQL Server support cases).

 Requires a target process PID. An optional dump type flag may be supplied;
 defaults to 0x0110 (mini-dump with thread and handle data).

 The master script will already define the typing speed as part of the
 master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SqlDumper(BaseCMD):
    """
    # LOLBAS: SqlDumper.exe — Legitimate use: generate a process memory dump file for SQL Server diagnostics

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SqlDumper, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SqlDumper'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sqldumper >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sqldumper >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target process PID to dump
        self.target_pid = None
        # Dump type flag (default 0x0110 — mini-dump with threads and handles)
        self.dump_flag = '0x0110'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] SqlDumper Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target process PID using 'pid <PID>'
        3: Optionally set the dump flag using 'dump_flag <flag>'  (default: 0x0110)
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
    #  SqlDumper Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new SqlDumper interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SqlDumper_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_pid(self, pid):
        """
        Set the target process PID to dump.
        Example: pid 464
        """
        if pid:
            if self.taskstarted:
                self.target_pid = pid.strip()
                print(self.cl.green("[*] Target PID set to: {}".format(self.target_pid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SqlDumper Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process PID."))


    def do_dump_flag(self, dump_flag):
        """
        Optionally set the dump type flag passed to SqlDumper.
        Default is 0x0110 (mini-dump with thread and handle data).
        Example: dump_flag 0x0110
        """
        if dump_flag:
            if self.taskstarted:
                self.dump_flag = dump_flag.strip()
                print(self.cl.green("[*] Dump flag set to: {}".format(self.dump_flag)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SqlDumper Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dump flag value."))


    def do_assigned(self, arg):
        """
        Get the current assigned SqlDumper configuration
        """
        print(self.cl.green("[?] Currently Assigned SqlDumper Configuration"))
        print("[>] Target PID  : {}".format(self.target_pid if self.target_pid else "(not set)"))
        print("[>] Dump Flag   : {}".format(self.dump_flag))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_pid:
                print(self.cl.red("[!] <ERROR> A target PID must be set before completing."))
                print(self.cl.red("[!] <ERROR> Use 'pid <PID>' to set one."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_pid = None
        self.dump_flag = '0x0110'


    ######################################################################
    # SqlDumper AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SqlDumper_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_sqldumper()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            target_pid : str — process PID to dump

        Optional JSON keys:
            dump_flag  : str — dump type flag (default: 0x0110)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_pid = kwargs.get("target_pid", None)
        if self.target_pid:
            print(f"[*] Setting target_pid attribute : {self.target_pid}")
        else:
            print("[!] <ERROR> No target_pid provided — this is required for SqlDumper")

        self.dump_flag = kwargs.get("dump_flag", "0x0110")
        print(f"[*] Setting dump_flag attribute : {self.dump_flag}")

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
        ; <      SqlDumper Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "SqlDumper_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func SqlDumper_{}()

            ; Creates a SqlDumper Interaction via CMD

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
        Builds the SqlDumper command to type into the CMD window.
        Runs SqlDumper.exe with the configured PID and dump flag.
        """
        typing_text = '\n'

        # Build the sqldumper command: sqldumper.exe <PID> 0 <flag>
        dump_cmd = 'sqldumper.exe {} 0 {}'.format(self.target_pid, self.dump_flag)
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_sqldumper(self):
        """
        Closes the SqlDumper AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
