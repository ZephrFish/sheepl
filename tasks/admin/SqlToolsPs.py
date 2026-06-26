
# LOLBAS: SQLToolsPS.exe — Legitimate use: running SQL Server PowerShell cmdlets for database administration

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate DBA use of SQLToolsPS.exe to invoke SQL Server
 PowerShell cmdlets (the successor to sqlps.exe in SQL Server 2016+).

 Takes an optional sql_command parameter; defaults to querying local
 SQL Server instance status.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SqlToolsPs(BaseCMD):
    """
    # LOLBAS: SQLToolsPS.exe — Legitimate use: running SQL Server PowerShell cmdlets

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SqlToolsPs, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SqlToolsPs'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sqltoolsps >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sqltoolsps >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional SQL Server PowerShell command to run
        self.sql_command = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] SqlToolsPs Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a SQL Server PowerShell command using 'sql_command <cmd>'
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
    #  SqlToolsPs Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new SqlToolsPs interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SqlToolsPs_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_sql_command(self, sql_command):
        """
        Optionally set a SQL Server PowerShell command to run via SQLToolsPS.
        If not set, defaults to Get-SqlInstance to query local instance status.
        Example: sql_command Get-SqlDatabase -ServerInstance localhost
        """
        if sql_command:
            if self.taskstarted:
                self.sql_command = sql_command.strip()
                print(self.cl.green("[*] SQL command set to: {}".format(self.sql_command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SqlToolsPs Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a SQL Server PowerShell command."))


    def do_assigned(self, arg):
        """
        Get the current assigned SqlToolsPs configuration
        """
        print(self.cl.green("[?] Currently Assigned SqlToolsPs Configuration"))
        print("[>] SQL Command : {}".format(self.sql_command if self.sql_command else "(not set — will run Get-SqlInstance)"))


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
        self.sql_command = None


    ######################################################################
    # SqlToolsPs AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SqlToolsPs_' + current_counter, self.create_autoit_function())


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
            sql_command : str — SQL Server PowerShell command to pass to SQLToolsPS
                                e.g. "Get-SqlDatabase -ServerInstance localhost"
                                if absent, runs Get-SqlInstance by default
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.sql_command = kwargs.get("sql_command", None)
        if self.sql_command:
            print(f"[*] Setting sql_command attribute : {self.sql_command}")
        else:
            print("[*] No sql_command provided — will run Get-SqlInstance")

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
        ; <      SqlToolsPs Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "SqlToolsPs_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func SqlToolsPs_{}()

            ; Creates a SqlToolsPs Interaction via CMD

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
        Builds the SQLToolsPS.exe commands to type into the CMD window.
        Always runs Get-SqlInstance to enumerate local SQL Server instances.
        If sql_command is set, also runs that command via SQLToolsPS.
        """
        typing_text = '\n'

        # Determine the PowerShell command to run
        if self.sql_command:
            ps_cmd = self.sql_command
        else:
            ps_cmd = 'Get-SqlInstance'

        # Invoke SQLToolsPS.exe with -noprofile to suppress profile loading
        sqltoolsps_cmd = 'SQLToolsPS.exe -noprofile -command "{}"'.format(ps_cmd)
        typing_text += 'Send("' + self._escape_send(sqltoolsps_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the SqlToolsPs AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
