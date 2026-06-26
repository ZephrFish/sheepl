
# #######################################################################
#
#  Task : PnpUtil Interaction
#
# #######################################################################

# LOLBAS: pnputil.exe — Legitimate use: driver inventory auditing and device management
# Admin required: pnputil /add-driver and /delete-driver require elevation

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of pnputil.exe to enumerate
 installed drivers or connected devices on a Windows endpoint.

 JSON keys:
   action : "enum-drivers" | "enum-devices"  (default: "enum-drivers")
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


# Map action names to their pnputil commands
PNPUTIL_COMMANDS = {
    "enum-drivers": "pnputil /enum-drivers",
    "enum-devices": "pnputil /enum-devices",
}

VALID_ACTIONS = list(PNPUTIL_COMMANDS.keys())


class PnpUtil(BaseCMD):
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
        super(PnpUtil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PnpUtil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > pnputil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > pnputil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.action = "enum-drivers"

        self.introduction = """
        ----------------------------------
        [!] PnpUtil Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action'
           Choices: enum-drivers | enum-devices
        3: Review assigned action using 'assigned'
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
    #  PnpUtil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new PnpUtil interaction block
        """
        # method from parent class BaseCMD
        if self.check_task_started():
            print("[!] Starting : 'PnpUtil_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : PnpUtil_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_action(self, arg):
        """
        Set the pnputil action to perform.
        Choices: enum-drivers | enum-devices
        Default: enum-drivers

        enum-drivers  — pnputil /enum-drivers  (list all installed OEM drivers)
        enum-devices  — pnputil /enum-devices  (list all connected devices)

        Example: action enum-devices
        """
        arg = arg.strip().lower()
        if not arg:
            print(self.cl.green("[?] Current action: {}".format(self.action)))
            print("[*] Valid options: {}".format(", ".join(VALID_ACTIONS)))
            return

        if arg in VALID_ACTIONS:
            self.action = arg
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
            print("[*] Will run: {}".format(PNPUTIL_COMMANDS[self.action]))
        else:
            print(self.cl.red("[!] Unknown action '{}'. Choose from: {}".format(
                arg, ", ".join(VALID_ACTIONS)
            )))


    def do_assigned(self, arg):
        """
        Show the currently assigned pnputil action
        """
        print(self.cl.green("[?] Currently Assigned PnpUtil Action"))
        print("[>] Action : {}".format(self.action))
        print("[>] Command: {}".format(PNPUTIL_COMMANDS.get(self.action, "<unknown>")))


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

        # reset action to default for next interaction
        self.action = "enum-drivers"


    ######################################################################
    # PnpUtil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PnpUtil_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.pnputil_typing_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            action : "enum-drivers" | "enum-devices"
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        action = kwargs.get("action", "enum-drivers").strip().lower()
        if action in VALID_ACTIONS:
            self.action = action
        else:
            print(self.cl.red("[!] Unknown action '{}', defaulting to 'enum-drivers'".format(action)))
            self.action = "enum-drivers"

        print(f"[*] Setting the action attribute : {self.action}")

        # once attributes are set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      PnpUtil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "PnpUtil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R for pnputil execution
        """
        _open_commandshell = """

        Func PnpUtil_{}()

            ; Creates a CMD shell for pnputil interaction

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
    # PnpUtil Command Output

    def pnputil_typing_block(self):
        """
        Generates the AutoIT Send() calls for the selected pnputil command
        """
        command = PNPUTIL_COMMANDS.get(self.action, PNPUTIL_COMMANDS["enum-drivers"])

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
        Closes the PnpUtil function declaration
        """
        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
