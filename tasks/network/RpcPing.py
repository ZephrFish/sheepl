
# LOLBAS: rpcping.exe — Legitimate use: verifying RPC connectivity to a remote server

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of rpcping.exe to test and verify RPC
 connectivity to a target server. Supports specifying the target server,
 endpoint port, and authentication type for connectivity troubleshooting.

 Takes a target_server parameter and optional endpoint and auth_type.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class RpcPing(BaseCMD):
    """
    # LOLBAS: rpcping.exe — Legitimate use: verifying RPC connectivity to a remote server

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(RpcPing, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'RpcPing'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > rpcping >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > rpcping >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target server to test RPC connectivity against
        self.target_server = None
        # Optional endpoint port (default: 135)
        self.endpoint = None
        # Optional authentication type (e.g. NTLM, Kerberos, WinNT)
        self.auth_type = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] RpcPing Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target server using 'target_server <hostname or IP>'
        3: Optionally set an endpoint port using 'endpoint <port>'
        4: Optionally set an auth type using 'auth_type <type>'  (e.g. NTLM, Kerberos)
        5: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  RpcPing Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new RpcPing interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'RpcPing_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_server(self, target_server):
        """
        Set the target server hostname or IP address for the RPC ping test.
        Example: target_server 192.168.1.10
        Example: target_server dc01.corp.local
        """
        if target_server:
            if self.taskstarted:
                self.target_server = target_server.strip()
                print(self.cl.green("[*] Target server set to: {}".format(self.target_server)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RpcPing Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target server hostname or IP address."))


    def do_endpoint(self, endpoint):
        """
        Optionally set the endpoint port for the RPC connection test.
        If not set, the default RPC endpoint mapper port (135) is used.
        Example: endpoint 135
        Example: endpoint 49152
        """
        if endpoint:
            if self.taskstarted:
                self.endpoint = endpoint.strip()
                print(self.cl.green("[*] Endpoint port set to: {}".format(self.endpoint)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RpcPing Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an endpoint port number."))


    def do_auth_type(self, auth_type):
        """
        Optionally set the authentication type for the RPC ping test.
        Common values: NTLM, Kerberos, WinNT, None
        If not set, the default authentication type is used.
        Example: auth_type NTLM
        Example: auth_type Kerberos
        """
        if auth_type:
            if self.taskstarted:
                self.auth_type = auth_type.strip()
                print(self.cl.green("[*] Auth type set to: {}".format(self.auth_type)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RpcPing Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an authentication type."))


    def do_assigned(self, arg):
        """
        Get the current assigned RpcPing configuration
        """
        print(self.cl.green("[?] Currently Assigned RpcPing Configuration"))
        print("[>] Target Server : {}".format(self.target_server if self.target_server else "(not set)"))
        print("[>] Endpoint Port : {}".format(self.endpoint if self.endpoint else "(not set — will use default 135)"))
        print("[>] Auth Type     : {}".format(self.auth_type if self.auth_type else "(not set — will use default)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_server:
                print(self.cl.red("[!] <ERROR> A target server must be set before completing."))
                print(self.cl.red("[!] <ERROR> Use 'target_server <hostname or IP>' to set it."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_server = None
        self.endpoint = None
        self.auth_type = None


    ######################################################################
    # RpcPing AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('RpcPing_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_rpcping()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            target_server : str — hostname or IP address to send RPC ping to

        Optional JSON keys:
            endpoint  : str — endpoint port number (default 135)
            auth_type : str — authentication type e.g. NTLM, Kerberos
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_server = kwargs.get("target_server", None)
        if self.target_server:
            print(f"[*] Setting target_server attribute : {self.target_server}")
        else:
            print("[!] <ERROR> No target_server provided — this is required for RpcPing.")
            return

        self.endpoint = kwargs.get("endpoint", None)
        if self.endpoint:
            print(f"[*] Setting endpoint attribute : {self.endpoint}")
        else:
            print("[*] No endpoint provided — will use default RPC endpoint mapper port")

        self.auth_type = kwargs.get("auth_type", None)
        if self.auth_type:
            print(f"[*] Setting auth_type attribute : {self.auth_type}")
        else:
            print("[*] No auth_type provided — will use default authentication")

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
        ; <      RpcPing Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "RpcPing_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func RpcPing_{}()

            ; Creates a RpcPing Interaction via CMD

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
        Builds the rpcping command to type into the CMD window.
        Always pings the target server. Optionally specifies endpoint and auth type.
        """
        typing_text = '\n'

        # Build the rpcping command from configured parameters
        rpcping_cmd = 'rpcping -s {}'.format(self.target_server)
        if self.endpoint:
            rpcping_cmd += ' -e {}'.format(self.endpoint)
        if self.auth_type:
            rpcping_cmd += ' -u {}'.format(self.auth_type)

        typing_text += 'Send("' + self._escape_send(rpcping_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_rpcping(self):
        """
        Closes the RpcPing AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
