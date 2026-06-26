
# #######################################################################
#
#  Task : SftpClient Interaction
#
# #######################################################################

# LOLBAS: sftp.exe — Legitimate use: secure file transfer to remote servers (Win10 1809+)

"""
 Creates the autoIT stub code to be passed into the master compile
 Simulates legitimate use of sftp.exe (Windows OpenSSH SFTP client, Win10 1809+)
 Developers transferring files to/from Linux servers, IT uploading config files securely.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD


class SftpClient(BaseCMD):

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
        super(SftpClient, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SftpClient'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > sftpclient >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > sftpclient >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] SftpClient Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set server using 'server'
        3: Set username using 'username'
        4: Set port using 'port' (default 22)
        5: Set remote path using 'remote_path'
        6: Complete the interaction using 'complete'
        """
        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.server = ''
        self.username = ''
        self.port = 22
        self.remote_path = ''

        self.assigned = False

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    #######################################################################
    # SftpClient Console Commands
    #######################################################################

    def do_new(self, arg):
        """
        Start a new SftpClient interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'SftpClient_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] {}_{}".format("SftpClient", str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_server(self, arg):
        """
        Set the target server hostname or IP address
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SftpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.server = arg
                self.assigned = True
                print("[*] Server set to : {}".format(self.cl.green(self.server)))
            else:
                server = input("[>] Enter the target server hostname or IP : ")
                self.server = server
                self.assigned = True
                print("[*] Server set to : {}".format(self.cl.green(self.server)))


    def do_username(self, arg):
        """
        Set the username to connect with
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SftpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.username = arg
                print("[*] Username set to : {}".format(self.cl.green(self.username)))
            else:
                username = input("[>] Enter the username to connect with : ")
                self.username = username
                print("[*] Username set to : {}".format(self.cl.green(self.username)))


    def do_port(self, arg):
        """
        Set the SFTP port (default 22)
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SftpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                try:
                    self.port = int(arg)
                    print("[*] Port set to : {}".format(self.cl.green(str(self.port))))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> Port must be a valid integer."))
            else:
                port_input = input("[>] Enter the port number (default 22) : ")
                if port_input:
                    try:
                        self.port = int(port_input)
                    except ValueError:
                        print(self.cl.red("[!] <ERROR> Invalid port, defaulting to 22."))
                        self.port = 22
                else:
                    self.port = 22
                print("[*] Port set to : {}".format(self.cl.green(str(self.port))))


    def do_remote_path(self, arg):
        """
        Set the remote directory path to navigate to after connecting
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SftpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.remote_path = arg
                print("[*] Remote path set to : {}".format(self.cl.green(self.remote_path)))
            else:
                remote_path = input("[>] Enter the remote directory path (leave blank to skip) : ")
                self.remote_path = remote_path
                print("[*] Remote path set to : {}".format(self.cl.green(self.remote_path) if self.remote_path else self.cl.green("(none)")))


    def do_assigned(self, arg):
        """
        Get the current list of assigned SftpClient settings
        """
        print("[?] Currently Assigned SftpClient Settings")
        print("[>] Server      : {}".format(self.server if self.server else "Not set"))
        print("[>] Username    : {}".format(self.username if self.username else "Not set"))
        print("[>] Port        : {}".format(str(self.port)))
        print("[>] Remote Path : {}".format(self.remote_path if self.remote_path else "Not set"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.assigned and self.server and self.username:
                self.create_autoIT_block()
                # now reset the tracking values and prompt
                self.complete_task()
                self.server = ''
                self.username = ''
                self.port = 22
                self.remote_path = ''
                self.assigned = False
            else:
                print(self.cl.red("[!] You need to assign at least a server and username to complete this task."))
        else:
            print(self.cl.red("[!] You need to start a new SftpClient Interaction first."))


######################################################################
# SftpClient AutoIT Block Definition
#######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SftpClient_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_sftpclient() +
            self.sftp_command_block() +
            self.close_sftpclient()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads: server, username, port, remote_path
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.server = kwargs["server"]
            self.username = kwargs["username"]
            self.port = int(kwargs.get("port", 22))
            self.remote_path = kwargs.get("remote_path", "")

            print(f"[*] Setting the server attribute      : {self.server}")
            print(f"[*] Setting the username attribute    : {self.username}")
            print(f"[*] Setting the port attribute        : {self.port}")
            print(f"[*] Setting the remote_path attribute : {self.remote_path}")

            self.assigned = True

        except KeyError as e:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, missing key: {}".format(e)))

        # once these have all been set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------------- >
        ;         SftpClient Interaction
        ; < ----------------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "SftpClient_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_sftpclient(self):
        """
        Opens CMD via Win+R and launches sftp.exe with the target connection string
        """

        # Build the sftp command: sftp [-P <port>] <username>@<server>
        if self.port != 22:
            sftp_command = "sftp -P {} {}@{}".format(self.port, self.username, self.server)
        else:
            sftp_command = "sftp {}@{}".format(self.username, self.server)

        _open_sftpclient = """

        Func SftpClient_{}()

            ; Simulates legitimate SFTP file transfer session (Win10 1809+ sftp.exe)

            Send("#r")
            ; Wait for the Run dialogue window to appear
            WinWaitActive("Run", "", 10)
            Send("cmd{}")
            WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
            SendKeepActive("[CLASS:ConsoleWindowClass]")

            sleep(1500)
            ; Launch sftp client connecting to remote server
            Send("{}{}")
            ; Wait for SFTP connection and password/host-key prompt
            sleep(8000)

        """.format(
            str(self.csh.counter.current()),
            "{ENTER}",
            self._escape_send(sftp_command),
            "{ENTER}"
        )

        return textwrap.dedent(_open_sftpclient)


    def sftp_command_block(self):
        """
        Issues SFTP interactive commands: cd to remote_path if set, ls, then bye
        """

        typing_text = '\n'

        # Navigate to remote path if configured
        if self.remote_path:
            typing_text += '; Navigate to remote directory\n'
            typing_text += 'Send("cd {}{}") \n'.format(
                self._escape_send(self.remote_path), "{ENTER}"
            )
            nav_delay = str(random.randint(2000, 5000))
            typing_text += "sleep({})\n".format(nav_delay)

        # List remote files
        typing_text += '; List remote directory contents\n'
        typing_text += 'Send("ls{}")\n'.format("{ENTER}")
        ls_delay = str(random.randint(3000, 8000))
        typing_text += "sleep({})\n".format(ls_delay)

        # Exit the SFTP session
        typing_text += '; Exit SFTP session\n'
        typing_text += 'Send("bye{}")\n'.format("{ENTER}")
        typing_text += "sleep(2000)\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def close_sftpclient(self):
        """
        Closes the SftpClient function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
