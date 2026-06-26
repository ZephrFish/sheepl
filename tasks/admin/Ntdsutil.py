
# #######################################################################
#
#  Task : Ntdsutil Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate Domain Controller administrator use of ntdsutil.exe
 for Active Directory database maintenance, metadata cleanup, and IFM creation.

"""

# SERVER-ONLY: ntdsutil.exe is only present on Windows Server Domain Controllers
# DOMAIN CONTROLLER ONLY: Requires Active Directory Domain Services (AD DS) role
# LOLBAS: ntdsutil.exe — Legitimate use: AD database maintenance and IFM creation on Domain Controllers

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Ntdsutil(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # SERVER-ONLY: ntdsutil.exe is only present on Windows Server Domain Controllers
    # DOMAIN CONTROLLER ONLY: Requires Active Directory Domain Services (AD DS) role
    # LOLBAS: ntdsutil.exe — Legitimate use: AD database maintenance and IFM creation on Domain Controllers
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Ntdsutil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Ntdsutil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ntdsutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ntdsutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Action to perform:
        #   "integrity"        — run AD database integrity check
        #   "metadata_cleanup" — open metadata cleanup menu
        #   "ifm"              — create Install From Media (IFM) snapshot
        self.action = 'integrity'

        # Output path used when action == "ifm"
        self.output_path = 'C:\\IFM'

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Ntdsutil Interaction.
        [!] SERVER-ONLY: Requires a Windows Server Domain Controller with AD DS role.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action' (integrity / metadata_cleanup / ifm)
        3: Optionally set the IFM output path using 'output_path' (used when action=ifm)
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
    #  Ntdsutil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Ntdsutil interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Ntdsutil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, arg):
        """
        Set the ntdsutil action to perform.
        Valid options:
          integrity        — run AD database integrity check (default)
          metadata_cleanup — open metadata cleanup menu
          ifm              — create Install From Media (IFM) snapshot
        Example: action ifm
        """
        valid_actions = ('integrity', 'metadata_cleanup', 'ifm')
        if self.taskstarted:
            if arg.lower() in valid_actions:
                self.action = arg.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ntdsutil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_output_path(self, arg):
        """
        Set the output path for IFM creation (only used when action=ifm).
        Default: C:\\IFM
        Example: output_path C:\\IFM
        """
        if self.taskstarted:
            if arg:
                self.output_path = arg
                print(self.cl.green("[*] IFM output path set to: {}".format(self.output_path)))
            else:
                print(self.cl.green("[*] Using default IFM output path: {}".format(self.output_path)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ntdsutil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current Ntdsutil task settings
        """
        print(self.cl.green("[?] Currently Assigned Ntdsutil Settings"))
        print("[>] Action      : {}".format(self.action))
        print("[>] Output path : {} (used when action=ifm)".format(self.output_path))


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

        # reset task-specific variables for next interaction
        self.action = 'integrity'
        self.output_path = 'C:\\IFM'


    ######################################################################
    # Ntdsutil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Ntdsutil_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_ntdsutil()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads action and output_path from kwargs.

        JSON keys:
          action      — one of: integrity, metadata_cleanup, ifm  (default: integrity)
          output_path — IFM output directory path  (default: C:\\IFM)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", "integrity")
        print(f"[*] Setting the action attribute : {self.action}")

        self.output_path = kwargs.get("output_path", "C:\\IFM")
        print(f"[*] Setting the output_path attribute : {self.output_path}")

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
        ; <      Ntdsutil Interaction
        ; < ----------------------------------- >
        ; SERVER-ONLY: ntdsutil.exe is only present on Windows Server Domain Controllers
        ; DOMAIN CONTROLLER ONLY: Requires Active Directory Domain Services (AD DS) role
        ; LOLBAS: ntdsutil.exe — Legitimate use: AD database maintenance and IFM creation on Domain Controllers

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Ntdsutil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for ntdsutil commands
        """

        _open_commandshell = """

        Func Ntdsutil_{}()

            ; Creates an Ntdsutil Interaction via CMD
            ; SERVER-ONLY: ntdsutil.exe is only present on Windows Server Domain Controllers
            ; DOMAIN CONTROLLER ONLY: Requires Active Directory Domain Services (AD DS) role

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

    def _build_ntdsutil_command(self):
        """
        Builds the appropriate ntdsutil command string based on self.action.

        Supported actions:
          integrity        — ntdsutil "activate instance ntds" "files" "integrity" "quit" "quit"
          metadata_cleanup — ntdsutil "metadata cleanup" "connections" "quit" "quit"
          ifm              — ntdsutil "activate instance ntds" "ifm" "create full <output_path>" "quit" "quit"
        """
        if self.action == 'integrity':
            return 'ntdsutil "activate instance ntds" "files" "integrity" "quit" "quit"'
        elif self.action == 'metadata_cleanup':
            return 'ntdsutil "metadata cleanup" "connections" "quit" "quit"'
        elif self.action == 'ifm':
            return 'ntdsutil "activate instance ntds" "ifm" "create full {}" "quit" "quit"'.format(self.output_path)
        else:
            # Fallback to integrity check
            return 'ntdsutil "activate instance ntds" "files" "integrity" "quit" "quit"'

    def text_typing_block(self):
        """
        Builds the ntdsutil command sequence based on the selected action:
          integrity        : ntdsutil "activate instance ntds" "files" "integrity" "quit" "quit"
          metadata_cleanup : ntdsutil "metadata cleanup" "connections" "quit" "quit"
          ifm              : ntdsutil "activate instance ntds" "ifm" "create full <output_path>" "quit" "quit"
        """
        typing_text = '\n'

        ntdsutil_cmd = self._build_ntdsutil_command()
        escaped_cmd = self._escape_send(ntdsutil_cmd)
        typing_text += 'Send("{}{}")\n'.format(escaped_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(5000, 30000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_ntdsutil(self):
        """
        Closes the Ntdsutil function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
