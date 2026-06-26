
# LOLBAS: sqlps.exe — Legitimate use: launching a SQL Server PowerShell mini-console for DBA administration
# DEVELOPER-ONLY: Requires Microsoft SQL Server installation (any version 100–150)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate DBA use of sqlps.exe to open an interactive SQL Server
 PowerShell mini-console and run basic SQL Server cmdlets.

 Takes an optional ps_command parameter; if absent opens the mini-console
 and runs a simple Get-ChildItem against the SQLSERVER: provider.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Sqlps(BaseCMD):
    """
    # LOLBAS: sqlps.exe — Legitimate use: launching a SQL Server PowerShell mini-console for DBA administration
    # DEVELOPER-ONLY: Requires Microsoft SQL Server installation (any version 100–150)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Sqlps, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Sqlps'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sqlps >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sqlps >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional PowerShell command to run inside the sqlps mini-console
        self.ps_command = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Sqlps Interaction.
        [!] NOTE: Requires Microsoft SQL Server installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a PowerShell command using 'ps_command <command>'
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
    #  Sqlps Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Sqlps interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Sqlps_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_ps_command(self, ps_command):
        """
        Optionally set a PowerShell command to run inside the sqlps mini-console.
        If not set, a basic Get-ChildItem SQLSERVER: listing is performed.
        Example: ps_command Get-SqlDatabase -ServerInstance localhost
        """
        if ps_command:
            if self.taskstarted:
                self.ps_command = ps_command.strip()
                print(self.cl.green("[*] PowerShell command set to: {}".format(self.ps_command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Sqlps Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a PowerShell command."))


    def do_assigned(self, arg):
        """
        Get the current assigned Sqlps configuration
        """
        print(self.cl.green("[?] Currently Assigned Sqlps Configuration"))
        print("[>] PowerShell Command : {}".format(self.ps_command if self.ps_command else "(not set — will run Get-ChildItem SQLSERVER:)"))


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
        self.ps_command = None


    ######################################################################
    # Sqlps AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Sqlps_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_sqlps()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            ps_command : str — PowerShell command to run inside the sqlps mini-console
                               if absent, Get-ChildItem SQLSERVER: is run instead
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.ps_command = kwargs.get("ps_command", None)
        if self.ps_command:
            print(f"[*] Setting ps_command attribute : {self.ps_command}")
        else:
            print("[*] No ps_command provided — will run Get-ChildItem SQLSERVER:")

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
        ; <      Sqlps Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Sqlps_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Sqlps_{}()

            ; Creates a Sqlps Interaction via CMD

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
        Builds the sqlps commands to type into the CMD window.
        Launches sqlps.exe -noprofile and runs a SQL Server PowerShell command.
        If ps_command is set, runs that command; otherwise runs Get-ChildItem SQLSERVER:.
        """
        typing_text = '\n'

        # Launch the sqlps mini-console with -noprofile
        launch_cmd = 'sqlps.exe -noprofile'
        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Run the desired PowerShell command inside the sqlps session
        if self.ps_command:
            cmd_to_run = self.ps_command
        else:
            cmd_to_run = 'Get-ChildItem SQLSERVER:'

        typing_text += 'Send("' + self._escape_send(cmd_to_run) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_sqlps(self):
        """
        Closes the Sqlps AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
