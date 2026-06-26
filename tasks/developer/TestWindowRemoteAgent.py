
# LOLBAS: TestWindowRemoteAgent.exe — Legitimate use: establishing RPC connections for Visual Studio remote test execution
# DEVELOPER-ONLY: Requires Microsoft Visual Studio 2022 installation (Community/Professional/Enterprise)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of TestWindowRemoteAgent.exe to establish
 RPC connections for running Visual Studio remote test agents on a target host.

 Takes a required host parameter and an optional port parameter (default 8000).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class TestWindowRemoteAgent(BaseCMD):
    """
    # LOLBAS: TestWindowRemoteAgent.exe — Legitimate use: establishing RPC connections for Visual Studio remote test execution
    # DEVELOPER-ONLY: Requires Microsoft Visual Studio 2022 installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(TestWindowRemoteAgent, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'TestWindowRemoteAgent'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > testwindowremoteagent >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > testwindowremoteagent >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Remote agent connection parameters
        self.host = None
        self.port = '8000'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] TestWindowRemoteAgent Interaction.
        [!] DEVELOPER-ONLY: Requires Visual Studio 2022 installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the remote host using 'host <hostname>'
        3: Optionally set the port using 'port <number>' (default: 8000)
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
    #  TestWindowRemoteAgent Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new TestWindowRemoteAgent interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'TestWindowRemoteAgent_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_host(self, host):
        """
        Set the remote host to connect to via TestWindowRemoteAgent.
        Example: host testserver.example.com
        """
        if host:
            if self.taskstarted:
                self.host = host.strip()
                print(self.cl.green("[*] Host set to: {}".format(self.host)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new TestWindowRemoteAgent Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote host."))


    def do_port(self, port):
        """
        Set the port for the remote agent connection. Defaults to 8000.
        Example: port 8000
        """
        if port:
            if self.taskstarted:
                self.port = port.strip()
                print(self.cl.green("[*] Port set to: {}".format(self.port)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new TestWindowRemoteAgent Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a port number."))


    def do_assigned(self, arg):
        """
        Get the current assigned TestWindowRemoteAgent configuration
        """
        print(self.cl.green("[?] Currently Assigned TestWindowRemoteAgent Configuration"))
        print("[>] Host : {}".format(self.host if self.host else "(not set)"))
        print("[>] Port : {}".format(self.port))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.host:
                print(self.cl.red("[!] <ERROR> You must set a host before completing. Use 'host <hostname>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.host = None
        self.port = '8000'


    ######################################################################
    # TestWindowRemoteAgent AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('TestWindowRemoteAgent_' + current_counter, self.create_autoit_function())


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

        Required JSON keys:
            host : str — remote hostname or IP for the test agent connection

        Optional JSON keys:
            port : str — port number for the agent connection (default: 8000)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", "8000")

        if self.host:
            print(f"[*] Setting host attribute : {self.host}")
        else:
            print("[!] <ERROR> No host provided — this is required for TestWindowRemoteAgent.")
            return

        print(f"[*] Setting port attribute : {self.port}")

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
        ; <      TestWindowRemoteAgent Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "TestWindowRemoteAgent_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func TestWindowRemoteAgent_{}()

            ; Creates a TestWindowRemoteAgent Interaction via CMD

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
        Builds the TestWindowRemoteAgent command to type into the CMD window.
        Uses the full path as the binary lives under VS installation directory.
        Connects to the specified remote host and port as a legitimate remote test agent.
        """
        typing_text = '\n'

        # Build the full path command for TestWindowRemoteAgent
        agent_path = (
            r'"%ProgramFiles%\Microsoft Visual Studio\2022\Community'
            r'\Common7\IDE\CommonExtensions\Microsoft\TestWindow\RemoteAgent\TestWindowRemoteAgent.exe"'
        )
        agent_cmd = '{} start -h {} -p {}'.format(agent_path, self.host, self.port)
        typing_text += 'Send("' + self._escape_send(agent_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the TestWindowRemoteAgent AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
