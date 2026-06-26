
# #######################################################################
#
#  Task : SshClient Interaction
#
# #######################################################################

# LOLBAS: ssh.exe — Legitimate use: remote server management and secure tunnelling (Win10 1809+)

"""
 Creates the autoIT stub code to be passed into the master compile
 Simulates legitimate developer/admin use of the Windows built-in SSH client (ssh.exe)
 Available on Windows 10 1809+ as part of the OpenSSH client optional feature.
"""
__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD


class SshClient(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SshClient, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SshClient'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sshclient >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sshclient >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] SshClient Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the target server using 'server'
        3: Set the SSH username using 'username'
        4: Optionally set a non-default port using 'port'
        5: Optionally set a tunnel using 'tunnel'
        6: Add remote commands using 'commands'
        7: Complete the interaction using 'complete'
        """
        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.server = ''
        self.username = ''
        self.port = '22'
        self.tunnel = ''
        self.commands = []

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    #######################################################################
    # SshClient Console Commands
    #######################################################################

    def do_new(self, arg):
        """
        Start a new SshClient interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'SshClient_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] {}_{}".format("SshClient", str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_server(self, arg):
        """
        Set the target SSH server hostname or IP address
        example: server 192.168.1.10
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SshClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.server = arg
                print("[*] Server set to : {}".format(self.cl.green(self.server)))
            else:
                print(self.cl.red("[!] <ERROR> Please provide a server hostname or IP address."))


    def do_username(self, arg):
        """
        Set the SSH username
        example: username devuser
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SshClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.username = arg
                print("[*] Username set to : {}".format(self.cl.green(self.username)))
            else:
                print(self.cl.red("[!] <ERROR> Please provide a username."))


    def do_port(self, arg):
        """
        Set the SSH port (default is 22)
        example: port 2222
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SshClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.port = arg
                print("[*] Port set to : {}".format(self.cl.green(self.port)))
            else:
                print("[*] Port remains at default : {}".format(self.cl.green(self.port)))


    def do_tunnel(self, arg):
        """
        Set optional local port forwarding (tunnel)
        example: tunnel 8080:localhost:80
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SshClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.tunnel = arg
                print("[*] Tunnel set to : {}".format(self.cl.green(self.tunnel)))
            else:
                print(self.cl.red("[!] <ERROR> Please provide a tunnel specification e.g. 8080:localhost:80."))


    def do_commands(self, command):
        """
        Add a command to run on the remote host after connecting
        example: commands ls -la /var/log
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SshClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if command:
                self.commands.append(command)
                print("[*] Command added : {}".format(self.cl.green(command)))
            else:
                print(self.cl.red("[!] <ERROR> Please provide a command to add."))


    def do_assigned(self, arg):
        """
        Get the current list of assigned remote commands
        """
        print("[?] Currently Assigned Commands")
        if self.commands:
            for command in self.commands:
                print("[>] {}".format(command))
        else:
            print("[>] No commands currently assigned")


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.server and self.username:
                self.create_autoIT_block()
                # reset tracking values and prompt
                self.complete_task()
                self.commands = []
                self.server = ''
                self.username = ''
                self.port = '22'
                self.tunnel = ''
            else:
                print(self.cl.red("[!] You need to set at least 'server' and 'username' to complete this task."))
        else:
            print(self.cl.red("[!] You need to start a new SshClient Interaction first."))


######################################################################
# SshClient AutoIT Block Definition
#######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SshClient_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_sshclient() +
            self.text_typing_block() +
            self.close_sshclient()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys: server, username, port, tunnel, commands
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.server = kwargs["server"]
            self.username = kwargs["username"]
            self.port = str(kwargs.get("port", "22"))
            self.tunnel = kwargs.get("tunnel", "")
            self.commands = kwargs.get("commands", [])

            print(f"[*] Setting the server attribute : {self.server}")
            print(f"[*] Setting the username attribute : {self.username}")
            print(f"[*] Setting the port attribute : {self.port}")
            print(f"[*] Setting the tunnel attribute : {self.tunnel}")
            print(f"[*] Setting the commands attribute : {self.commands}")

        except KeyError as e:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, missing key: {}".format(e)))

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------------- >
        ;         SshClient Interaction
        ; < ----------------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "SshClient_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def _build_ssh_command(self):
        """
        Builds the ssh.exe command string with optional port and tunnel flags.
        """
        cmd_parts = ["ssh"]

        if self.tunnel:
            cmd_parts.append("-L {}".format(self.tunnel))

        if self.port and self.port != "22":
            cmd_parts.append("-p {}".format(self.port))

        cmd_parts.append("{}@{}".format(self.username, self.server))

        return " ".join(cmd_parts)


    def open_sshclient(self):
        """
        Opens CMD via Win+R and launches the SSH client.
        Waits for a ConsoleWindowClass window (CMD prompt) to appear after launch.
        """

        ssh_command = self._build_ssh_command()

        _open_sshclient = """

        Func SshClient_{}()

            ; Simulates developer/admin use of Windows built-in SSH client (ssh.exe)
            ; LOLBAS: ssh.exe available on Windows 10 1809+

            Send("#r")
            ; Wait for the Run dialogue window to appear
            WinWaitActive("Run", "", 10)
            Send("cmd{}")
            ; Wait for the CMD console window to appear
            WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
            SendKeepActive("[CLASS:ConsoleWindowClass]")

            sleep(1500)
            ; Launch the SSH connection
            Send("{}{}")
            sleep(3000)

            ; Wait for the SSH session window — title will contain the server name or 'ssh'
            WinWaitActive("[CLASS:ConsoleWindowClass]", "", 30)
            SendKeepActive("[CLASS:ConsoleWindowClass]")

            sleep(5000)

        """.format(
            str(self.csh.counter.current()),
            "{ENTER}",
            self._escape_send(ssh_command),
            "{ENTER}"
        )

        return textwrap.dedent(_open_sshclient)


    def text_typing_block(self):
        """
        Types any remote commands into the SSH session, then exits.
        """

        typing_text = '\n'

        for command in self.commands:
            typing_text += ('Send("' + self._escape_send(command) + '{ENTER}")\n')
            command_delay = str(random.randint(2000, 20000))
            typing_text += ("sleep(" + command_delay + ")\n")

        # exit the SSH session
        typing_text += 'Send("exit{ENTER}")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def close_sshclient(self):
        """
        Closes the SshClient function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
