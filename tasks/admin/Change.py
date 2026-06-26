
# LOLBAS: change.exe — Legitimate use: querying Remote Desktop Services user, port, and logon settings
# SERVER-ONLY: change.exe is part of Remote Desktop Services (chgusr/chgport/chglogon); RDS role required

# #######################################################################
#
#  Task : Change Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of change.exe to query Remote Desktop Services
 session configuration — user install mode, COM port mappings, and logon status.

 Takes an optional 'query_type' parameter (user, port, or logon); defaults to 'user /query'.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Change(BaseCMD):
    """
    # LOLBAS: change.exe — Legitimate use: querying Remote Desktop Services user, port, and logon settings
    # SERVER-ONLY: change.exe delegates to chgusr/chgport/chglogon which are part of the RDS role

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Change, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Change'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > change >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > change >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Query type: user, port, or logon
        self.query_type = 'user'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Change Interaction.
        [!] SERVER-ONLY: Requires Remote Desktop Services role.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a query type using 'query_type <user|port|logon>'
           Default is 'user' (queries install/execute mode)
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
    #  Change Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Change interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Change_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_query_type(self, query_type):
        """
        Set which RDS component to query.
        Options: user, port, logon
          user  — query install/execute mode for the session (default)
          port  — list COM port to LPT port mappings
          logon — show whether RDS logons are enabled
        Example: query_type logon
        """
        valid = ('user', 'port', 'logon')
        if query_type:
            if self.taskstarted:
                query_type = query_type.strip().lower()
                if query_type in valid:
                    self.query_type = query_type
                    print(self.cl.green("[*] Query type set to: {}".format(self.query_type)))
                else:
                    print(self.cl.red("[!] <ERROR> query_type must be one of: user, port, logon"))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Change Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a query type (user, port, or logon)."))


    def do_assigned(self, arg):
        """
        Get the current assigned Change configuration
        """
        print(self.cl.green("[?] Currently Assigned Change Configuration"))
        print("[>] Query Type : {}".format(self.query_type))


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
        self.query_type = 'user'


    ######################################################################
    # Change AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Change_' + current_counter, self.create_autoit_function())


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
            query_type : str — one of 'user', 'port', or 'logon' (default: 'user')
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.query_type = kwargs.get("query_type", "user").strip().lower()
        print(f"[*] Setting query_type attribute : {self.query_type}")

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
        ; <      Change Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Change_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Change_{}()

            ; Creates a Change Interaction via CMD

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
        Builds the change.exe query command to type into the CMD window.
        Runs 'change <query_type> /query' to inspect RDS configuration.
        """
        typing_text = '\n'

        # Build the appropriate query command
        if self.query_type == 'user':
            change_cmd = 'change user /query'
        elif self.query_type == 'port':
            change_cmd = 'change port /query'
        elif self.query_type == 'logon':
            change_cmd = 'change logon /query'
        else:
            change_cmd = 'change user /query'

        typing_text += 'Send("' + self._escape_send(change_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Change AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
