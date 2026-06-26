
# #######################################################################
#
#  Task : Esentutl Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of esentutl.exe — ESE database maintenance
 used by Windows Search, WSUS, and Active Directory.

"""

# LOLBAS: esentutl.exe — Legitimate use: ESE database integrity checks (Windows Search, WSUS)
# SERVER-ONLY: WSUS (C:\\Windows\\WID\\Data\\susdb.mdf) and AD (ntds.dit) operations are server-only

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Esentutl(BaseCMD):
    """
    # LOLBAS: esentutl.exe — Legitimate use: ESE database integrity checks (Windows Search, WSUS)
    # SERVER-ONLY: WSUS (C:\\Windows\\WID\\Data\\susdb.mdf) and AD (ntds.dit) operations are server-only

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Esentutl, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Esentutl'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > esentutl >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > esentutl >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # "integrity" runs esentutl /g; "defrag" runs esentutl /d
        self.action = 'integrity'
        # Default to Windows Search database — workstation-safe target
        self.database = 'C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb'

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Esentutl Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action' (integrity / defrag)
        3: Set the database path using 'database'
        4: Show assigned settings using 'assigned'
        5: Complete the interaction using 'complete'

        NOTE: WSUS and AD (ntds.dit) database operations are server-only activities.
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Esentutl Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Esentutl interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Esentutl_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, arg):
        """
        Set the esentutl action to perform.
        Options:
            integrity  — run an integrity check on the database (esentutl /g)
            defrag     — defragment the database (esentutl /d)
        Default: integrity
        Example: action defrag
        """
        if self.taskstarted:
            valid_actions = ['integrity', 'defrag']
            if arg.lower() in valid_actions:
                self.action = arg.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] <ERROR> Invalid action '{}'. Choose from: {}".format(arg, ', '.join(valid_actions))))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Esentutl Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_database(self, arg):
        """
        Set the path to the ESE database file to operate on.
        Default: C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb
        SERVER-ONLY examples:
            WSUS  : C:\\Windows\\WID\\Data\\susdb.mdf
            AD DC : C:\\Windows\\NTDS\\ntds.dit
        Example: database C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb
        """
        if self.taskstarted:
            if arg:
                self.database = arg.strip()
                print(self.cl.green("[*] Database path set to: {}".format(self.database)))
            else:
                print(self.cl.green("[*] Using default database path: {}".format(self.database)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Esentutl Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the currently assigned Esentutl task settings
        """
        print(self.cl.green("[?] Currently Assigned Esentutl Settings"))
        print("[>] Action   : {}".format(self.action))
        print("[>] Database : {}".format(self.database))


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

        # reset task-specific variables for the next interaction
        self.action = 'integrity'
        self.database = 'C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb'


    ######################################################################
    # Esentutl AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Esentutl_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_esentutl()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads action and database from kwargs.

        JSON keys:
            action   : str — "integrity" (esentutl /g) or "defrag" (esentutl /d)
            database : str — path to the ESE database file
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", "integrity")
        print(f"[*] Setting the action attribute : {self.action}")

        self.database = kwargs.get("database", 'C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\Windows.edb')
        print(f"[*] Setting the database attribute : {self.database}")

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      Esentutl Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Esentutl_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for esentutl commands
        """

        _open_commandshell = """

        Func Esentutl_{}()

            ; Creates an Esentutl Interaction via CMD

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
        Builds the esentutl command to type into the CMD window.
            integrity  : esentutl /g <database>
            defrag     : esentutl /d <database>
        """
        typing_text = '\n'

        escaped_db = self._escape_send(self.database)

        if self.action == 'defrag':
            esentutl_cmd = 'esentutl /d {}'.format(escaped_db)
        else:
            # default: integrity check
            esentutl_cmd = 'esentutl /g {}'.format(escaped_db)

        typing_text += 'Send("{}{}")\n'.format(esentutl_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_esentutl(self):
        """
        Closes the Esentutl AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
