
# #######################################################################
#
#  Task : DiskShadow Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate Windows Server administrator use of diskshadow.exe
 for Volume Shadow Copy Service (VSS) management — listing existing shadow
 copies or creating new backup snapshots.

 JSON profile keys:
   action  : "list" (default) or "add"
   volume  : drive letter for snapshot target when action=add (default "C:")
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

# SERVER-ONLY: diskshadow.exe is present only on Windows Server (not Windows client endpoints)
# LOLBAS: diskshadow.exe — Legitimate use: VSS shadow copy management on Windows Server backup hosts

import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DiskShadow(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    Simulates a Windows Server administrator managing Volume Shadow Copies
    via diskshadow.exe.  Two actions are supported:

        list  — runs 'list shadows all' inside diskshadow then exits
        add   — creates a new shadow copy of the target volume

    NOTE: diskshadow.exe ships only with Windows Server editions.
    Running this task against a Windows client endpoint will fail.
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DiskShadow, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DiskShadow'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > diskshadow >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > diskshadow >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.action = 'list'    # "list" or "add"
        self.volume = 'C:'      # target volume when action=add

        self.introduction = """
        ----------------------------------
        [!] DiskShadow Interaction.
        SERVER-ONLY: diskshadow.exe is present only on Windows Server systems.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action [list|add]'  (default: list)
        3: Set the target volume using 'volume <drive>'  (default: C:, used with action=add)
        4: Review assigned settings using 'assigned'
        5: Complete the interaction using 'complete'
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
    #  DiskShadow Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        Creates a new DiskShadow interaction block.
        """
        if self.check_task_started():
            print("[!] Starting : 'DiskShadow_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : DiskShadow_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_action(self, arg):
        """
        Set the VSS action to perform.
        Choices: list  — list all existing shadow copies (default)
                 add   — create a new shadow copy of the target volume
        Example: action list
                 action add
        """
        valid = ['list', 'add']
        if arg.strip().lower() in valid:
            self.action = arg.strip().lower()
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
        else:
            print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid))))


    def do_volume(self, arg):
        """
        Set the target drive letter used when action=add.
        Example: volume C:
                 volume D:
        Default is C:
        """
        if self.taskstarted:
            if arg.strip():
                self.volume = arg.strip().upper()
                if not self.volume.endswith(':'):
                    self.volume += ':'
                print(self.cl.green("[*] Volume set to: {}".format(self.volume)))
            else:
                print(self.cl.red("[!] Please supply a drive letter, e.g. 'volume D:'"))
        else:
            print(self.cl.red("[!] <ERROR> Start a new DiskShadow interaction first with 'new'."))


    def do_assigned(self, arg):
        """
        Display the currently assigned DiskShadow settings.
        """
        print(self.cl.green("[?] Currently Assigned DiskShadow Settings"))
        print("[>] Action : {}".format(self.action))
        print("[>] Volume : {}".format(self.volume))


    def do_complete(self, arg):
        """
        Finalises the DiskShadow interaction and generates the AutoIT block.
        """
        if self.taskstarted:
            self.create_autoIT_block()

        # reset tracking values and prompt
        self.complete_task()

        # reset task-specific state for any subsequent interaction
        self.action = 'list'
        self.volume = 'C:'


    ######################################################################
    # DiskShadow AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block.
        csh.add_tasks takes two positional arguments:
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DiskShadow_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Assembles the full AutoIT output for this task.
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.diskshadow_commands_block() +
            self.close_commandshell()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs and builds task variables when using JSON profiles.
        Expected JSON keys:
            action  : "list" or "add"
            volume  : drive letter, e.g. "C:" (only meaningful when action=add)
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get('action', 'list').lower()
        self.volume = kwargs.get('volume', 'C:').upper()
        if not self.volume.endswith(':'):
            self.volume += ':'

        print(f"[*] Setting action : {self.action}")
        print(f"[*] Setting volume : {self.volume}")

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial entrypoint definition for the AutoIT function.
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      DiskShadow Interaction
        ; <      SERVER-ONLY: Windows Server VSS management
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "DiskShadow_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Open CMD shell

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R.
        diskshadow.exe will be invoked from within CMD.
        """
        _open_cmd = """

        Func DiskShadow_{}()

            ; SERVER-ONLY: diskshadow.exe is present only on Windows Server systems
            ; Opens CMD via Win+R, then runs diskshadow commands

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
    # DiskShadow Command Block

    def diskshadow_commands_block(self):
        """
        Generates the AutoIT Send() calls for the diskshadow interaction.

        action=list : launches diskshadow interactively, lists all shadow copies, then exits
        action=add  : uses a diskshadow script file to add a shadow copy of self.volume
        """
        typing_text = '\n'

        if self.action == 'list':
            # Launch diskshadow interactively and enumerate all VSS snapshots
            typing_text += 'Send("diskshadow{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 4000))
            typing_text += '; List all existing Volume Shadow Copies\n'
            typing_text += 'Send("list shadows all{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))
            typing_text += 'Send("exit{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(1000, 3000))

        elif self.action == 'add':
            # Write a minimal diskshadow script to a temp file, then execute it
            # The script sets the context, adds a volume, creates the snapshot, and exits.
            script_path = r'C:\Windows\Temp\vss_backup.dsh'
            typing_text += '; Write diskshadow script to temp file\n'
            typing_text += 'Send("echo set context persistent> ' + self._escape_send(script_path) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(500, 1500))
            typing_text += 'Send("echo add volume ' + self._escape_send(self.volume) + '>> ' + self._escape_send(script_path) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(500, 1500))
            typing_text += 'Send("echo create>> ' + self._escape_send(script_path) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(500, 1500))
            typing_text += 'Send("echo exit>> ' + self._escape_send(script_path) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(1000, 2000))
            typing_text += '; Execute the diskshadow script to create the shadow copy\n'
            typing_text += 'Send("diskshadow /s ' + self._escape_send(script_path) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(5000, 15000))

        typing_text += '; Exit CMD\n'
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += '; Reset Focus\n'
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the DiskShadow AutoIT function declaration.
        """
        end_func = """

        EndFunc

        """
        return textwrap.dedent(end_func)
