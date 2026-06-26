
# LOLBAS: dtutil.exe — Legitimate use: managing SQL Server Integration Services (SSIS) packages
# DEVELOPER-ONLY: Requires Microsoft SQL Server or SQL Server Integration Services installation

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate DBA/developer use of dtutil.exe to copy SQL Server
 Integration Services (SSIS) packages from one file location to another.

 Requires source_path and dest_path parameters; both should be absolute
 paths to .dtsx package files.
 The master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Dtutil(BaseCMD):
    """
    # LOLBAS: dtutil.exe — Legitimate use: copying SQL Server Integration Services (SSIS) packages
    # DEVELOPER-ONLY: Requires Microsoft SQL Server or SQL Server Integration Services installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Dtutil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Dtutil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dtutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dtutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Source and destination SSIS package paths
        self.source_path = None
        self.dest_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Dtutil Interaction.
        [!] NOTE: Requires Microsoft SQL Server / SSIS installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source SSIS package path using 'source_path <path>'
        3: Set the destination SSIS package path using 'dest_path <path>'
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
    #  Dtutil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Dtutil interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Dtutil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source_path(self, source_path):
        """
        Set the absolute path to the source SSIS package file (.dtsx).
        Example: source_path C:\\ETL\\packages\\load_data.dtsx
        """
        if source_path:
            if self.taskstarted:
                self.source_path = source_path.strip()
                print(self.cl.green("[*] Source path set to: {}".format(self.source_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dtutil Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a source path."))


    def do_dest_path(self, dest_path):
        """
        Set the absolute path to the destination SSIS package file (.dtsx).
        Example: dest_path C:\\ETL\\backup\\load_data_backup.dtsx
        """
        if dest_path:
            if self.taskstarted:
                self.dest_path = dest_path.strip()
                print(self.cl.green("[*] Destination path set to: {}".format(self.dest_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dtutil Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a destination path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Dtutil configuration
        """
        print(self.cl.green("[?] Currently Assigned Dtutil Configuration"))
        print("[>] Source Path      : {}".format(self.source_path if self.source_path else "(not set)"))
        print("[>] Destination Path : {}".format(self.dest_path if self.dest_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.source_path:
                print(self.cl.red("[!] <ERROR> Please set a source path using 'source_path <path>'."))
                return
            if not self.dest_path:
                print(self.cl.red("[!] <ERROR> Please set a destination path using 'dest_path <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.source_path = None
        self.dest_path = None


    ######################################################################
    # Dtutil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Dtutil_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_dtutil()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            source_path : str — absolute path to the source SSIS package (.dtsx)
            dest_path   : str — absolute path to the destination SSIS package (.dtsx)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source_path = kwargs.get("source_path", None)
        self.dest_path = kwargs.get("dest_path", None)

        if self.source_path:
            print(f"[*] Setting source_path attribute : {self.source_path}")
        else:
            print("[!] <ERROR> No source_path provided — task cannot complete.")
            return

        if self.dest_path:
            print(f"[*] Setting dest_path attribute : {self.dest_path}")
        else:
            print("[!] <ERROR> No dest_path provided — task cannot complete.")
            return

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
        ; <      Dtutil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Dtutil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Dtutil_{}()

            ; Creates a Dtutil Interaction via CMD

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
        Builds the dtutil copy command to type into the CMD window.
        Copies the source SSIS package file to the destination path.
        """
        typing_text = '\n'

        # Copy source SSIS package to destination using dtutil /FILE /COPY FILE
        copy_cmd = 'dtutil.exe /FILE "{}" /COPY FILE;"{}"'.format(self.source_path, self.dest_path)
        typing_text += 'Send("' + self._escape_send(copy_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_dtutil(self):
        """
        Closes the Dtutil AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
