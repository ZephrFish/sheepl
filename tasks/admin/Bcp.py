
# LOLBAS: bcp.exe — Legitimate use: bulk import/export of data between SQL Server and flat files
# DEVELOPER-ONLY: Requires Microsoft SQL Server or SQL Server Client Tools installation

# #######################################################################
#
#  Task : Bcp Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate DBA/developer use of bcp.exe (SQL Server Bulk Copy Program)
 to export a query result set from a SQL Server instance to a flat file,
 or to import data from a flat file into a SQL Server table.

 Requires SQL Server Client Tools (bcp.exe) to be installed.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Bcp(BaseCMD):
    """
    # LOLBAS: bcp.exe — Legitimate use: bulk export/import of SQL Server data to/from flat files
    # DEVELOPER-ONLY: Requires Microsoft SQL Server Client Tools installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Bcp, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Bcp'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > bcp >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > bcp >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.table_or_query = None   # e.g. "AdventureWorks.dbo.Product" or a query string
        self.output_file = None      # destination file path for the export
        self.server = None           # SQL Server instance name

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Bcp Interaction.
            Requires: Microsoft SQL Server Client Tools (bcp.exe)
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source table using 'table <table>'
        3: Set the output file using 'output_file <path>'
        4: Set the server instance using 'server <name>'
        5: Complete the interaction using 'complete'
        ----------------------------------
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Bcp Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Bcp interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Bcp_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_table(self, table):
        """
        Set the source table (or view) to export from SQL Server.
        Example: table AdventureWorks.dbo.Product
        """
        if table:
            if self.taskstarted:
                self.table_or_query = table.strip()
                print(self.cl.green("[*] Table set to: {}".format(self.table_or_query)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Bcp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a table name."))


    def do_output_file(self, output_file):
        """
        Set the destination file path for the bcp export.
        Example: output_file C:\\Temp\\products.csv
        """
        if output_file:
            if self.taskstarted:
                self.output_file = output_file.strip()
                print(self.cl.green("[*] Output file set to: {}".format(self.output_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Bcp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path."))


    def do_server(self, server):
        """
        Set the SQL Server instance name to connect to.
        Example: server localhost
        """
        if server:
            if self.taskstarted:
                self.server = server.strip()
                print(self.cl.green("[*] Server set to: {}".format(self.server)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Bcp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a server name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Bcp configuration
        """
        print(self.cl.green("[?] Currently Assigned Bcp Configuration"))
        print("[>] Table       : {}".format(self.table_or_query if self.table_or_query else "(not set — will use default: AdventureWorks.dbo.Product)"))
        print("[>] Output File : {}".format(self.output_file if self.output_file else "(not set — will use default: C:\\Temp\\bcp_export.csv)"))
        print("[>] Server      : {}".format(self.server if self.server else "(not set — will use default: localhost)"))


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
        self.table_or_query = None
        self.output_file = None
        self.server = None


    ######################################################################
    # Bcp AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Bcp_' + current_counter, self.create_autoit_function())


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
            table_or_query : str — SQL Server table/view to export (default: AdventureWorks.dbo.Product)
            output_file    : str — destination file path for the export
            server         : str — SQL Server instance name (default: localhost)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.table_or_query = kwargs.get("table_or_query", "AdventureWorks.dbo.Product")
        self.output_file = kwargs.get("output_file", "C:\\Temp\\bcp_export.csv")
        self.server = kwargs.get("server", "localhost")

        print(f"[*] Setting table_or_query attribute : {self.table_or_query}")
        print(f"[*] Setting output_file attribute    : {self.output_file}")
        print(f"[*] Setting server attribute         : {self.server}")

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
        ; <      Bcp Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Bcp_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Bcp_{}()

            ; Creates a Bcp Interaction via CMD

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
        Builds the bcp commands to type into the CMD window.
        Exports a table from SQL Server to a character-delimited flat file
        using Windows integrated authentication (-T) and character mode (-c).
        """

        # Apply defaults if not set interactively
        table = self.table_or_query if self.table_or_query else "AdventureWorks.dbo.Product"
        outfile = self.output_file if self.output_file else "C:\\Temp\\bcp_export.csv"
        server = self.server if self.server else "localhost"

        typing_text = '\n'

        # Export the table to a flat file using trusted connection and character mode
        bcp_cmd = 'bcp {} out {} -S {} -T -c'.format(table, outfile, server)
        typing_text += 'Send("' + self._escape_send(bcp_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Bcp AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
