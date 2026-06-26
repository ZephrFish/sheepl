
# #######################################################################
#
#  Task : FtpClient Interaction
#
# #######################################################################

# LOLBAS: ftp.exe — Legitimate use: legacy FTP server access for internal file distribution
# Note: FTP transmits credentials in cleartext. Modern environments prefer SFTP/HTTPS.

"""
 Creates the autoIT stub code to be passed into the master compile
 Simulates legitimate use of the Windows built-in ftp.exe client.

 Legitimate use cases: Legacy IT environments using FTP for file transfers,
 connecting to internal FTP servers for software distribution.

 LOLBAS reference: ftp.exe (Windows FTP client, legacy tool)
 Note: FTP is a legacy protocol. Most modern environments use SFTP or HTTPS instead.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD


class FtpClient(BaseCMD):

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
        super(FtpClient, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'FtpClient'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ftpclient >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ftpclient >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] FtpClient Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the FTP server using 'server'
        3: Set the username using 'username'
        4: Set the remote path using 'remote_path'
        5: Complete the interaction using 'complete'
        """
        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.server = ''
        self.username = 'anonymous'
        self.remote_path = ''

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    #######################################################################
    # FtpClient Console Commands
    #######################################################################

    def do_new(self, arg):
        """
        Start a new FtpClient interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'FtpClient_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] {}_{}".format("FtpClient", str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_server(self, arg):
        """
        Set the FTP server hostname or IP address
        Example: server ftp.internal.corp
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new FtpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.server = arg
                print(self.cl.green("[*] FTP server set to: {}".format(self.server)))
            else:
                print(self.cl.red("[!] <ERROR> Please supply a server hostname or IP address."))


    def do_username(self, arg):
        """
        Set the FTP username (default: anonymous)
        Example: username ftpuser
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new FtpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.username = arg
                print(self.cl.green("[*] FTP username set to: {}".format(self.username)))
            else:
                print(self.cl.red("[!] <ERROR> Please supply a username."))


    def do_remote_path(self, arg):
        """
        Set the remote directory to navigate to after login
        Example: remote_path /pub/software
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new FtpClient Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            if arg:
                self.remote_path = arg
                print(self.cl.green("[*] Remote path set to: {}".format(self.remote_path)))
            else:
                print(self.cl.red("[!] <ERROR> Please supply a remote path."))


    def do_assigned(self, arg):
        """
        Get the current list of assigned FtpClient settings
        """
        print("[?] Currently Assigned FtpClient Settings")
        print("[>] Server      : {}".format(self.server if self.server else "Not set"))
        print("[>] Username    : {}".format(self.username))
        print("[>] Remote Path : {}".format(self.remote_path if self.remote_path else "Not set"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.server:
                self.create_autoIT_block()
                # now reset the tracking values and prompt
                self.complete_task()
                self.server = ''
                self.username = 'anonymous'
                self.remote_path = ''
            else:
                print(self.cl.red("[!] You need to assign a server in order to complete this task"))
        else:
            print(self.cl.red("[!] You need to start a new FtpClient Interaction first"))


    ######################################################################
    # FtpClient AutoIT Block Definition
    #######################################################################

    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('FtpClient_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_ftpclient() +
            self.ftp_commands_block() +
            self.close_ftpclient()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        this function sets the various object attributes in the same way
        that the interactive mode does
        """

        print("[%] Setting attributes from JSON Profile")
        # This snippet takes the keys ignoring the first key which is task and then shows
        # what should be set in the kwargs parsing.
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.server = kwargs["server"]
            self.username = kwargs.get("username", "anonymous")
            self.remote_path = kwargs.get("remote_path", "")

            print(f"[*] Setting the server attribute      : {self.server}")
            print(f"[*] Setting the username attribute    : {self.username}")
            print(f"[*] Setting the remote_path attribute : {self.remote_path}")

        except KeyError as e:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, missing key: {}".format(e)))

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------------- >
        ;         FtpClient Interaction
        ;   LOLBAS: ftp.exe - legacy FTP client
        ; < ----------------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "FtpClient_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_ftpclient(self):
        """
        Opens CMD via Win+R and launches ftp.exe against the target server,
        then handles the login prompt by typing the username and password.
        """

        _open_ftpclient = """

        Func FtpClient_{counter}()

            ; Creates an FtpClient Interaction using the built-in Windows ftp.exe
            ; LOLBAS: ftp.exe - Legitimate use: legacy FTP server access

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send("ftp {server}{enter}")
            ; Wait for the CMD/ftp window to become active
            WinWaitActive("[CLASS:ConsoleWindowClass]", "", 10)
            SendKeepActive("[CLASS:ConsoleWindowClass]")

            ; Wait for the login prompt and enter the username
            sleep(3000)
            Send("{username}{enter}")
            sleep(2000)
            ; Enter the password (anonymous FTP convention uses an email as password)
            Send("anonymous@{server}{enter}")

        """.format(
            counter=str(self.csh.counter.current()),
            server=self._escape_send(self.server),
            enter="{ENTER}",
            username=self._escape_send(self.username)
        )

        return textwrap.dedent(_open_ftpclient)


    def ftp_commands_block(self):
        """
        Issues FTP commands after login: navigate to remote_path if set,
        then list directory contents, print working directory, and quit.
        """

        typing_text = '\n'
        typing_text += '; Issue FTP commands after successful login\n'

        # Navigate to the remote path if one was specified
        if self.remote_path:
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
            typing_text += 'Send("cd {}{}")\n'.format(
                self._escape_send(self.remote_path), '{ENTER}'
            )

        # List directory contents
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += 'Send("dir{ENTER}")\n'

        # Print working directory
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += 'Send("pwd{ENTER}")\n'

        # Quit the FTP session
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += 'Send("bye{ENTER}")\n'

        typing_text += '; Reset Focus\n'
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    def close_ftpclient(self):
        """
        Closes the FtpClient function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
