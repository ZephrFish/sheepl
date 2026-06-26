
# #######################################################################
#
#  Task : Reg Interaction
#
# #######################################################################

# LOLBAS: reg.exe — Legitimate use: configuration auditing and registry key inspection

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of reg.exe for querying or exporting
 registry keys as part of configuration review and auditing workflows.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Reg(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    Simulates IT admin use of reg.exe to query or export registry keys
    for configuration review and auditing purposes.
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Reg, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Reg'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > reg >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > reg >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # track subtasks
        self.subtask = False

        # Task-specific defaults
        self.action = 'query'
        self.reg_key = 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
        self.export_path = 'C:\\Temp\\reg_export.reg'

        self.introduction = """
        ----------------------------------
        [!] Reg.exe Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set action with 'action' (query or export)
        3: Set registry key with 'key'
        4: Set export path with 'export_path' (used when action=export)
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
    #  Reg Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        Creates a new Reg interaction block.
        """
        if self.check_task_started():
            self.prompt = self.cl.blue(
                "[*] Current Task : 'Reg_{}'".format(str(self.csh.counter.current())) +
                "\n" + self.baseprompt
            )


    def do_action(self, arg):
        """
        Sets the reg.exe action: query or export.
        Default is 'query'.
        Example: action query
                 action export
        """
        if self.taskstarted:
            arg = arg.strip().lower()
            if arg in ('query', 'export'):
                self.action = arg
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] Invalid action. Choose 'query' or 'export'."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Reg Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_key(self, arg):
        """
        Sets the registry key path to query or export.
        Default: HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion
        Example: key HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall
        """
        if self.taskstarted:
            if arg.strip():
                self.reg_key = arg.strip()
                print(self.cl.green("[*] Registry key set to: {}".format(self.reg_key)))
            else:
                print(self.cl.red("[!] Please provide a registry key path."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Reg Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_export_path(self, arg):
        """
        Sets the file path for registry export output.
        Only used when action is set to 'export'.
        Default: C:\\Temp\\reg_export.reg
        Example: export_path C:\\Audit\\hklm_export.reg
        """
        if self.taskstarted:
            if arg.strip():
                self.export_path = arg.strip()
                print(self.cl.green("[*] Export path set to: {}".format(self.export_path)))
            else:
                print(self.cl.red("[!] Please provide a file path for the export."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Reg Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Displays the currently assigned Reg task settings.
        """
        print(self.cl.green("[?] Currently Assigned Reg Settings"))
        print("[>] Action      : {}".format(self.action))
        print("[>] Registry Key: {}".format(self.reg_key))
        if self.action == 'export':
            print("[>] Export Path : {}".format(self.export_path))


    def do_complete(self, arg):
        """
        Completes the Reg task and builds the AutoIT block.
        """
        if self.taskstarted:
            self.create_autoIT_block()

        # reset the tracking values and prompt
        self.complete_task()

        # reset task-specific attributes for potential reuse
        self.action = 'query'
        self.reg_key = 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
        self.export_path = 'C:\\Temp\\reg_export.reg'


    ######################################################################
    # Reg AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block.
        csh.add_tasks takes two positional arguments:
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Reg_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output.
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_cmd_and_run_reg() +
            self.close_reg()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs and builds out task variables when using JSON profiles.
        Sets object attributes in the same way that interactive mode does.

        JSON keys: action, key, export_path
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get('action', 'query').lower()
        self.reg_key = kwargs.get('key', 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion')
        self.export_path = kwargs.get('export_path', 'C:\\Temp\\reg_export.reg')

        print(f"[*] Setting action      : {self.action}")
        print(f"[*] Setting reg_key     : {self.reg_key}")
        if self.action == 'export':
            print(f"[*] Setting export_path : {self.export_path}")

        # push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function.
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      Reg Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Reg_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_cmd_and_run_reg(self):
        """
        Opens CMD via Win+R and executes the appropriate reg.exe command.
        """
        if self.action == 'export':
            reg_command = 'reg export {} {}'.format(self.reg_key, self.export_path)
        else:
            reg_command = 'reg query {}'.format(self.reg_key)

        _open_cmd_and_run_reg = """

        Func Reg_{}()

            ; Simulates IT admin use of reg.exe for configuration auditing
            ; LOLBAS: reg.exe — Legitimate use: configuration auditing and registry key inspection

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

            sleep({})
            Send("{}{}")

        """.format(
            self.csh.counter.current(),
            "{ENTER}",
            random.randint(1500, 4000),
            self._escape_send(reg_command),
            "{ENTER}"
        )

        return textwrap.dedent(_open_cmd_and_run_reg)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_reg(self):
        """
        Closes the Reg function block, exits CMD, and resets focus.
        """
        _close_reg = """
            sleep({})
            Send("exit{}")
            ; Reset Focus
            SendKeepActive("")

        EndFunc

        """.format(
            random.randint(2000, 6000),
            "{ENTER}"
        )

        return textwrap.dedent(_close_reg)
