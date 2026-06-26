
# #######################################################################
#
#  Task : Netsh Interaction
#
# #######################################################################

# LOLBAS: netsh.exe — Legitimate use: network interface and firewall configuration review
# SERVER-ONLY: netsh advfirewall add rule (firewall rule creation) is a server administration activity

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of netsh.exe to inspect
 network interface status, firewall state, WiFi profiles, and port proxy rules.

 JSON keys:
   query : "interfaces" | "firewall" | "wlan" | "portproxy"  (default: "interfaces")
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


# Map query names to their netsh commands
NETSH_COMMANDS = {
    "interfaces": "netsh interface show interface",
    "firewall":   "netsh advfirewall show currentprofile",
    "wlan":       "netsh wlan show profiles",
    "portproxy":  "netsh interface portproxy show all",
}

VALID_QUERIES = list(NETSH_COMMANDS.keys())


class Netsh(BaseCMD):
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
        super(Netsh, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Netsh'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > netsh >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > netsh >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.netsh_query = "interfaces"

        self.introduction = """
        ----------------------------------
        [!] Netsh Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the query type using 'query'
           Choices: interfaces | firewall | wlan | portproxy
        3: Review assigned query using 'assigned'
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
    #  Netsh Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Netsh interaction block
        """
        # method from parent class BaseCMD
        if self.check_task_started():
            print("[!] Starting : 'Netsh_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : Netsh_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_query(self, arg):
        """
        Set the netsh query type to run.
        Choices: interfaces | firewall | wlan | portproxy
        Default: interfaces

        interfaces  — netsh interface show interface
        firewall    — netsh advfirewall show currentprofile
        wlan        — netsh wlan show profiles
        portproxy   — netsh interface portproxy show all

        Example: query firewall
        """
        arg = arg.strip().lower()
        if not arg:
            print(self.cl.green("[?] Current query: {}".format(self.netsh_query)))
            print("[*] Valid options: {}".format(", ".join(VALID_QUERIES)))
            return

        if arg in VALID_QUERIES:
            self.netsh_query = arg
            print(self.cl.green("[*] Query set to: {}".format(self.netsh_query)))
            print("[*] Will run: {}".format(NETSH_COMMANDS[self.netsh_query]))
        else:
            print(self.cl.red("[!] Unknown query '{}'. Choose from: {}".format(
                arg, ", ".join(VALID_QUERIES)
            )))


    def do_assigned(self, arg):
        """
        Show the currently assigned netsh query
        """
        print(self.cl.green("[?] Currently Assigned Netsh Query"))
        print("[>] Query  : {}".format(self.netsh_query))
        print("[>] Command: {}".format(NETSH_COMMANDS.get(self.netsh_query, "<unknown>")))


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

        # reset query to default for next interaction
        self.netsh_query = "interfaces"


    ######################################################################
    # Netsh AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Netsh_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.netsh_typing_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            query : "interfaces" | "firewall" | "wlan" | "portproxy"
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        query = kwargs.get("query", "interfaces").strip().lower()
        if query in VALID_QUERIES:
            self.netsh_query = query
        else:
            print(self.cl.red("[!] Unknown query '{}', defaulting to 'interfaces'".format(query)))
            self.netsh_query = "interfaces"

        print(f"[*] Setting the netsh_query attribute : {self.netsh_query}")

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
        ; <      Netsh Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Netsh_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R for netsh execution
        """
        _open_commandshell = """

        Func Netsh_{}()

            ; Creates a CMD shell for netsh interaction

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
    # Netsh Command Output

    def netsh_typing_block(self):
        """
        Generates the AutoIT Send() calls for the selected netsh command
        """
        command = NETSH_COMMANDS.get(self.netsh_query, NETSH_COMMANDS["interfaces"])

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
        Closes the Netsh function declaration
        """
        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
