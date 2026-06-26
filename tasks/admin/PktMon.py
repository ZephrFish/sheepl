
# #######################################################################
#
#  Task : PktMon Interaction
#
# #######################################################################

# LOLBAS: pktmon.exe — Legitimate use: network interface enumeration and packet capture (Win10 1809+)
# Admin required: pktmon start/stop (packet capture) requires elevated privileges

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate network administrator use of pktmon.exe (Packet Monitor),
 a built-in Windows network diagnostic tool available from Windows 10 version 1809.

 Legitimate use cases: Network admins listing network components (adapters, filters,
 counters) for diagnostics, or checking the current capture status.

 Note: pktmon list and pktmon status do not require elevation.
       pktmon start / pktmon stop require administrator privileges.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class PktMon(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    Simulates network administrator use of pktmon.exe for network diagnostics.
    Supported actions: list (enumerate network components), status (show capture status)
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(PktMon, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PktMon'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > pktmon >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > pktmon >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] PktMon Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action' (list / status)
        3: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Default action is list — enumerate network components (no elevation needed)
        self.action = 'list'

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  PktMon Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        Start a new PktMon interaction block
        """
        if self.check_task_started():
            # Reset per-block state
            self.action = 'list'
            print("[!] Starting : 'PktMon_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] {}_{}".format("PktMon", str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_action(self, arg):
        """
        Set the pktmon.exe action to perform.
        Valid options: list, status
          list   — enumerate network components (adapters, filters, counters); no elevation needed
          status — show current packet capture status; no elevation needed
        Default is 'list'.
        Example: action list
        """
        valid_actions = ['list', 'status']
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new PktMon Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        if arg.lower() in valid_actions:
            self.action = arg.lower()
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
        else:
            print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))


    def do_assigned(self, arg):
        """
        Show the currently assigned PktMon settings
        """
        print(self.cl.green("[?] Currently Assigned PktMon Settings"))
        print("[>] Action : {}".format(self.action))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            self.create_autoIT_block()

        # Reset tracking values and prompt
        self.complete_task()

        # Reset per-block state
        self.action = 'list'


    ######################################################################
    # PktMon AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PktMon_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.build_pktmon_command_block() +
            self.close_pktmon()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys: action
        this function sets the various object attributes in the same way
        that the interactive mode does
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.action = kwargs.get("action", "list")
            print(f"[*] Setting the action attribute : {self.action}")

        except KeyError as e:
            print(self.cl.red("[!] Error setting JSON Profile attributes, missing key: {}".format(e)))

        # Once attributes are set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      PktMon Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "PktMon_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function — open CMD via Win+R

    def open_commandshell(self):
        """
        Opens a CMD window using Win+R run dialogue
        """

        _open_commandshell = """

        Func PktMon_{}()

            ; Opens CMD to run pktmon.exe network diagnostic commands

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
    # Build pktmon Command Block

    def build_pktmon_command_block(self):
        """
        Constructs the appropriate pktmon.exe command based on self.action,
        then appends exit and focus reset.
        """
        pktmon_command = self._resolve_pktmon_command()

        typing_text = '\n'
        typing_text += 'Send("' + self._escape_send(pktmon_command) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(3000, 12000))
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def _resolve_pktmon_command(self):
        """
        Returns the correct pktmon.exe command string based on self.action.

        action == "list"   : pktmon list  (enumerate network components — no elevation needed)
        action == "status" : pktmon status (show capture status — no elevation needed)
        """
        if self.action == 'list':
            return 'pktmon list'
        elif self.action == 'status':
            return 'pktmon status'
        else:
            # Fallback — enumerate network components
            return 'pktmon list'


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_pktmon(self):
        """
        Closes the PktMon function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
