
# #######################################################################
#
#  Task : DnsCmd Interaction
#
# #######################################################################

# SERVER-ONLY: dnscmd.exe is only available on systems with the DNS Server role installed (Windows Server)
# LOLBAS: dnscmd.exe — Legitimate use: DNS zone and record management on DNS servers

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate DNS server administrator use of dnscmd.exe to list
 DNS zones, retrieve server statistics, and enumerate DNS records.

 dnscmd.exe is the DNS Server management command-line utility (LOLBAS reference).
 It is only present on Windows Server systems with the DNS Server role installed.

 JSON keys:
   action : "enumzones" | "statistics" | "enumrecords"  (default: "enumzones")
   zone   : DNS zone name, required when action is "enumrecords" (e.g. "domain.local")
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


VALID_ACTIONS = ["enumzones", "statistics", "enumrecords"]


class DnsCmd(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DnsCmd, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DnsCmd'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dnscmd >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dnscmd >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.action = "enumzones"
        self.zone = ""

        self.introduction = """
        ----------------------------------
        [!] DnsCmd Interaction.
        Type help or ? to list commands.
        ----------------------------------
        NOTE: dnscmd.exe requires the DNS Server role (Windows Server only)
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action'
           Choices: enumzones | statistics | enumrecords
        3: Set the DNS zone using 'zone' (required for enumrecords)
           Example: zone domain.local
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
    #  DnsCmd Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DnsCmd interaction block
        """
        # method from parent class BaseCMD
        if self.check_task_started():
            print("[!] Starting : 'DnsCmd_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : DnsCmd_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_action(self, arg):
        """
        Set the dnscmd action to perform.
        Choices: enumzones | statistics | enumrecords
        Default: enumzones

        enumzones   — dnscmd /enumzones          (list all DNS zones)
        statistics  — dnscmd /statistics         (display DNS server statistics)
        enumrecords — dnscmd /enumrecords <zone> @ /type A  (list A records in zone)

        Example: action enumzones
        Example: action enumrecords
        """
        arg = arg.strip().lower()
        if not arg:
            print(self.cl.green("[?] Current action: {}".format(self.action)))
            print("[*] Valid options: {}".format(", ".join(VALID_ACTIONS)))
            return

        if arg in VALID_ACTIONS:
            self.action = arg
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
            if self.action == "enumrecords":
                print("[*] Remember to set a zone name using 'zone <name>'")
        else:
            print(self.cl.red("[!] Unknown action '{}'. Choose from: {}".format(
                arg, ", ".join(VALID_ACTIONS)
            )))


    def do_zone(self, arg):
        """
        Set the DNS zone name (required when action is 'enumrecords').
        Example: zone domain.local
        """
        if self.taskstarted:
            arg = arg.strip()
            if not arg:
                print(self.cl.green("[?] Current zone: {}".format(self.zone if self.zone else "<not set>")))
                return
            self.zone = arg
            print(self.cl.green("[*] Zone set to: {}".format(self.zone)))
        else:
            print(self.cl.red("[!] <ERROR> Start a new DnsCmd interaction first with 'new'."))


    def do_assigned(self, arg):
        """
        Show the currently assigned dnscmd action and zone
        """
        print(self.cl.green("[?] Currently Assigned DnsCmd Settings"))
        print("[>] Action : {}".format(self.action))
        if self.action == "enumrecords":
            print("[>] Zone   : {}".format(self.zone if self.zone else "<not set — required for enumrecords>"))
        command = self._build_command()
        print("[>] Command: {}".format(command))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.action == "enumrecords" and not self.zone:
                print(self.cl.red("[!] <ERROR> Zone name is required for 'enumrecords' action."))
                print(self.cl.red("[-] Set a zone name using 'zone <name>' before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset state to defaults for next interaction
        self.action = "enumzones"
        self.zone = ""


    ######################################################################
    # DnsCmd AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DnsCmd_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.dnscmd_typing_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            action : "enumzones" | "statistics" | "enumrecords"
            zone   : DNS zone name (required when action is "enumrecords")
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        action = kwargs.get("action", "enumzones").strip().lower()
        if action in VALID_ACTIONS:
            self.action = action
        else:
            print(self.cl.red("[!] Unknown action '{}', defaulting to 'enumzones'".format(action)))
            self.action = "enumzones"

        self.zone = kwargs.get("zone", "").strip()

        print(f"[*] Setting the action attribute : {self.action}")
        if self.action == "enumrecords":
            print(f"[*] Setting the zone attribute  : {self.zone}")

        # once attributes are set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Helper

    def _build_command(self):
        """
        Returns the dnscmd command string for the current action and zone.
        """
        if self.action == "enumzones":
            return "dnscmd /enumzones"
        elif self.action == "statistics":
            return "dnscmd /statistics"
        elif self.action == "enumrecords":
            zone = self.zone if self.zone else "domain.local"
            return "dnscmd /enumrecords {} @ /type A".format(zone)
        return "dnscmd /enumzones"


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      DnsCmd Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "DnsCmd_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R for dnscmd execution
        """
        _open_commandshell = """

        Func DnsCmd_{}()

            ; Creates a CMD shell for dnscmd interaction
            ; SERVER-ONLY: dnscmd.exe requires the DNS Server role (Windows Server)

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
    # DnsCmd Command Output

    def dnscmd_typing_block(self):
        """
        Generates the AutoIT Send() calls for the selected dnscmd command
        """
        command = self._build_command()

        typing_text = '\n'
        typing_text += 'Send("' + self._escape_send(command) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the DnsCmd function declaration
        """
        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
