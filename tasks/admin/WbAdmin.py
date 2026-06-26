
# #######################################################################
#
#  Task : WbAdmin Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate Windows Server administrator use of wbadmin.exe
 for Windows Server Backup management — checking backup job status,
 listing available backup versions, or enumerating backed-up items.

 JSON profile keys:
   action  : "status" (default), "versions", or "items"
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

# SERVER-ONLY: wbadmin.exe requires Windows Server Backup feature (Windows Server only, not Windows client)
# LOLBAS: wbadmin.exe — Legitimate use: backup job status monitoring on Windows Server

import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WbAdmin(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    Simulates a Windows Server administrator querying backup state via
    wbadmin.exe.  Three actions are supported:

        status   — runs 'wbadmin get status'   (current backup job status)
        versions — runs 'wbadmin get versions'  (list available backup versions)
        items    — runs 'wbadmin get items'     (list items in latest backup)

    NOTE: wbadmin.exe is only present on Windows Server systems with the
    Windows Server Backup feature installed.  Running this task against a
    Windows client endpoint will fail.
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WbAdmin, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WbAdmin'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wbadmin >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wbadmin >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.action = 'status'  # "status", "versions", or "items"

        self.introduction = """
        ----------------------------------
        [!] WbAdmin Interaction.
        SERVER-ONLY: wbadmin.exe requires Windows Server Backup feature (Windows Server only).
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action [status|versions|items]'  (default: status)
        3: Review assigned settings using 'assigned'
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  WbAdmin Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        Creates a new WbAdmin interaction block.
        """
        if self.check_task_started():
            print("[!] Starting : 'WbAdmin_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : WbAdmin_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_action(self, arg):
        """
        Set the wbadmin action to perform.
        Choices: status   — get current backup job status (default)
                 versions — list available backup versions
                 items    — get items in the latest backup
        Example: action status
                 action versions
                 action items
        """
        valid = ['status', 'versions', 'items']
        if arg.strip().lower() in valid:
            self.action = arg.strip().lower()
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
        else:
            print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid))))


    def do_assigned(self, arg):
        """
        Display the currently assigned WbAdmin settings.
        """
        print(self.cl.green("[?] Currently Assigned WbAdmin Settings"))
        print("[>] Action : {}".format(self.action))


    def do_complete(self, arg):
        """
        Finalises the WbAdmin interaction and generates the AutoIT block.
        """
        if self.taskstarted:
            self.create_autoIT_block()

        # reset tracking values and prompt
        self.complete_task()

        # reset task-specific state for any subsequent interaction
        self.action = 'status'


    ######################################################################
    # WbAdmin AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block.
        csh.add_tasks takes two positional arguments:
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WbAdmin_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Assembles the full AutoIT output for this task.
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.wbadmin_commands_block() +
            self.close_commandshell()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs and builds task variables when using JSON profiles.
        Expected JSON keys:
            action  : "status", "versions", or "items"
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get('action', 'status').lower()

        print(f"[*] Setting action : {self.action}")

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial entrypoint definition for the AutoIT function.
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      WbAdmin Interaction
        ; <      SERVER-ONLY: Windows Server Backup management
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "WbAdmin_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Open CMD shell

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R.
        wbadmin.exe will be invoked from within CMD.
        """
        _open_cmd = """

        Func WbAdmin_{}()

            ; SERVER-ONLY: wbadmin.exe requires Windows Server Backup feature (Windows Server only)
            ; Opens CMD via Win+R, then runs wbadmin commands

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
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

        return textwrap.dedent(_open_cmd)


    # --------------------------------------------------->
    # WbAdmin Command Block

    def wbadmin_commands_block(self):
        """
        Generates the AutoIT Send() calls for the wbadmin interaction.

        action=status   : runs 'wbadmin get status'
        action=versions : runs 'wbadmin get versions'
        action=items    : runs 'wbadmin get items'
        """
        typing_text = '\n'

        if self.action == 'status':
            # Query the status of the most recent or currently running backup job
            typing_text += '; Query current backup job status\n'
            typing_text += 'Send("wbadmin get status{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        elif self.action == 'versions':
            # List all backup versions available for recovery
            typing_text += '; List available backup versions\n'
            typing_text += 'Send("wbadmin get versions{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        elif self.action == 'items':
            # Enumerate items contained in the most recent backup
            typing_text += '; Get items in the latest backup\n'
            typing_text += 'Send("wbadmin get items{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        typing_text += '; Exit CMD\n'
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += '; Reset Focus\n'
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the WbAdmin AutoIT function declaration.
        """
        end_func = """

        EndFunc

        """
        return textwrap.dedent(end_func)
