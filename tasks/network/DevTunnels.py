
# LOLBAS: devtunnel.exe — Legitimate use: forwarding local ports to the internet for remote access and development tunnels

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of devtunnel.exe to host and expose
 a locally running service port to the internet via Microsoft Dev Tunnels.

 Takes a required port parameter (default 8080) and an optional protocol
 parameter (http/https/tcp; defaults to http).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DevTunnels(BaseCMD):
    """
    # LOLBAS: devtunnel.exe — Legitimate use: forwarding local ports to the internet for remote access and development tunnels

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DevTunnels, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DevTunnels'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > devtunnel >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > devtunnel >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Port to expose via dev tunnel
        self.port = '8080'
        # Protocol for the tunnel (http, https, tcp)
        self.protocol = 'http'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DevTunnels Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the local port to expose using 'port <number>'
        3: Optionally set the protocol using 'protocol <http|https|tcp>'
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
    #  DevTunnels Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DevTunnels interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DevTunnels_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_port(self, port):
        """
        Set the local port number to expose via the dev tunnel.
        Example: port 8080
        """
        if port:
            if self.taskstarted:
                self.port = port.strip()
                print(self.cl.green("[*] Port set to: {}".format(self.port)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DevTunnels Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a port number."))


    def do_protocol(self, protocol):
        """
        Set the tunnel protocol. Choices: http, https, tcp (default: http).
        Example: protocol https
        """
        if protocol:
            if self.taskstarted:
                self.protocol = protocol.strip().lower()
                print(self.cl.green("[*] Protocol set to: {}".format(self.protocol)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DevTunnels Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a protocol (http, https, or tcp)."))


    def do_assigned(self, arg):
        """
        Get the current assigned DevTunnels configuration
        """
        print(self.cl.green("[?] Currently Assigned DevTunnels Configuration"))
        print("[>] Port     : {}".format(self.port))
        print("[>] Protocol : {}".format(self.protocol))


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

        # reset task-specific state for the next interaction
        self.port = '8080'
        self.protocol = 'http'


    ######################################################################
    # DevTunnels AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DevTunnels_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_devtunnels()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            port     : str — local port number to expose (default: '8080')
            protocol : str — tunnel protocol: http, https, or tcp (default: 'http')
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.port = kwargs.get("port", "8080")
        self.protocol = kwargs.get("protocol", "http")
        print(f"[*] Setting port attribute     : {self.port}")
        print(f"[*] Setting protocol attribute : {self.protocol}")

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
        ; <      DevTunnels Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DevTunnels_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DevTunnels_{}()

            ; Creates a DevTunnels Interaction via CMD

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
        Builds the devtunnel host command to type into the CMD window.
        Exposes the configured local port using the specified protocol.
        The tunnel runs briefly then the shell is closed.
        """
        typing_text = '\n'

        host_cmd = 'devtunnel host -p {} --protocol {}'.format(self.port, self.protocol)
        typing_text += 'Send("' + self._escape_send(host_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_devtunnels(self):
        """
        Closes the DevTunnels AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
