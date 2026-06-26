
# LOLBAS: dsdbutil.exe — Legitimate use: managing Active Directory LDS snapshots for backup and recovery
# SERVER-ONLY: Requires Windows Server with AD LDS (Active Directory Lightweight Directory Services) role installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate AD LDS administrator use of dsdbutil.exe to create
 and manage VSS snapshots of the Active Directory NTDS.dit database.

 Supports creating a snapshot and listing all snapshots.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DsDbUtil(BaseCMD):
    """
    # LOLBAS: dsdbutil.exe — Legitimate use: managing Active Directory LDS snapshots for backup and recovery
    # SERVER-ONLY: Requires Windows Server with AD LDS role installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DsDbUtil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DsDbUtil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dsdbutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dsdbutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Action: 'create' to create a new snapshot, 'list' to list all snapshots
        self.action = 'create'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DsDbUtil Interaction.
        NOTE: SERVER-ONLY — requires Windows Server with AD LDS role installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the snapshot action using 'action <create|list>'
           Default action is 'create' (creates a VSS snapshot of NTDS)
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
    #  DsDbUtil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DsDbUtil interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DsDbUtil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, action):
        """
        Set the dsdbutil snapshot action to perform.
        Valid values: create, list
        Default: create
        Example: action create
        Example: action list
        """
        valid_actions = ['create', 'list']
        if action:
            action = action.strip().lower()
            if self.taskstarted:
                if action in valid_actions:
                    self.action = action
                    print(self.cl.green("[*] Action set to: {}".format(self.action)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid action '{}'. Choose from: {}".format(action, ', '.join(valid_actions))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DsDbUtil Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an action (create or list)."))


    def do_assigned(self, arg):
        """
        Get the current assigned DsDbUtil configuration
        """
        print(self.cl.green("[?] Currently Assigned DsDbUtil Configuration"))
        print("[>] Action : {}".format(self.action))


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
        self.action = 'create'


    ######################################################################
    # DsDbUtil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DsDbUtil_' + current_counter, self.create_autoit_function())


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
            action : str — snapshot action to perform: 'create' or 'list'
                           defaults to 'create' if absent
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", "create").strip().lower()
        print(f"[*] Setting action attribute : {self.action}")

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
        ; <      DsDbUtil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DsDbUtil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DsDbUtil_{}()

            ; Creates a DsDbUtil Interaction via CMD

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
        Builds the dsdbutil commands to type into the CMD window.
        If action is 'create': creates a VSS snapshot of the NTDS database.
        If action is 'list':   lists all existing snapshots.
        """
        typing_text = '\n'

        if self.action == 'list':
            # List all existing snapshots
            snapshot_cmd = 'dsdbutil.exe "activate instance ntds" "snapshot" "list all" "quit" "quit"'
            typing_text += 'Send("' + self._escape_send(snapshot_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        else:
            # Default: create a new VSS snapshot of NTDS
            snapshot_cmd = 'dsdbutil.exe "activate instance ntds" "snapshot" "create" "quit" "quit"'
            typing_text += 'Send("' + self._escape_send(snapshot_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the DsDbUtil AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
