
# LOLBAS: scp.exe — Legitimate use: copying files to or from a remote host over SSH

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of scp.exe to copy a file to a remote host
 over SSH (Secure Copy Protocol), as bundled with Windows OpenSSH.

 Requires a remote_host, remote_user, local_file, and remote_path to be
 set before completing the task.
 The master script will already define the typing speed as part of the
 master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Scp(BaseCMD):
    """
    # LOLBAS: scp.exe — Legitimate use: copying files to a remote host over SSH

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Scp, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Scp'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > scp >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > scp >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.remote_host = None
        self.remote_user = None
        self.local_file = None
        self.remote_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Scp Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set source file using 'local_file <path>'
        3: Set remote user using 'remote_user <username>'
        4: Set remote host using 'remote_host <hostname>'
        5: Set remote destination using 'remote_path <path>'
        6: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Scp Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Scp interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Scp_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_local_file(self, local_file):
        """
        Set the local file path to copy to the remote host.
        Example: local_file C:\\Users\\user\\documents\\report.pdf
        """
        if local_file:
            if self.taskstarted:
                self.local_file = local_file.strip()
                print(self.cl.green("[*] Local file set to: {}".format(self.local_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Scp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a local file path."))


    def do_remote_user(self, remote_user):
        """
        Set the remote SSH username.
        Example: remote_user administrator
        """
        if remote_user:
            if self.taskstarted:
                self.remote_user = remote_user.strip()
                print(self.cl.green("[*] Remote user set to: {}".format(self.remote_user)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Scp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote username."))


    def do_remote_host(self, remote_host):
        """
        Set the remote hostname or IP address to copy the file to.
        Example: remote_host 192.168.1.50
        """
        if remote_host:
            if self.taskstarted:
                self.remote_host = remote_host.strip()
                print(self.cl.green("[*] Remote host set to: {}".format(self.remote_host)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Scp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote host."))


    def do_remote_path(self, remote_path):
        """
        Set the destination path on the remote host.
        Example: remote_path /home/administrator/uploads/
        """
        if remote_path:
            if self.taskstarted:
                self.remote_path = remote_path.strip()
                print(self.cl.green("[*] Remote path set to: {}".format(self.remote_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Scp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote destination path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Scp configuration
        """
        print(self.cl.green("[?] Currently Assigned Scp Configuration"))
        print("[>] Local File   : {}".format(self.local_file if self.local_file else "(not set)"))
        print("[>] Remote User  : {}".format(self.remote_user if self.remote_user else "(not set)"))
        print("[>] Remote Host  : {}".format(self.remote_host if self.remote_host else "(not set)"))
        print("[>] Remote Path  : {}".format(self.remote_path if self.remote_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.local_file or not self.remote_user or not self.remote_host or not self.remote_path:
                print(self.cl.red("[!] <ERROR> local_file, remote_user, remote_host, and remote_path must all be set."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.local_file = None
        self.remote_user = None
        self.remote_host = None
        self.remote_path = None


    ######################################################################
    # Scp AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Scp_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_scp()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            local_file  : str — local file path to copy
            remote_user : str — SSH username on the remote host
            remote_host : str — remote hostname or IP address
            remote_path : str — destination path on the remote host
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.local_file = kwargs.get("local_file", None)
        self.remote_user = kwargs.get("remote_user", None)
        self.remote_host = kwargs.get("remote_host", None)
        self.remote_path = kwargs.get("remote_path", None)

        if self.local_file:
            print(f"[*] Setting local_file attribute : {self.local_file}")
        if self.remote_user:
            print(f"[*] Setting remote_user attribute : {self.remote_user}")
        if self.remote_host:
            print(f"[*] Setting remote_host attribute : {self.remote_host}")
        if self.remote_path:
            print(f"[*] Setting remote_path attribute : {self.remote_path}")

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
        ; <      Scp Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Scp_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Scp_{}()

            ; Creates an Scp Interaction via CMD

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
        Builds the scp command to type into the CMD window.
        Copies local_file to remote_user@remote_host:remote_path using scp.exe.
        The -o StrictHostKeyChecking=no flag avoids an interactive host-key prompt.
        """
        typing_text = '\n'

        scp_cmd = 'scp.exe -o StrictHostKeyChecking=no {} {}@{}:{}'.format(
            self.local_file,
            self.remote_user,
            self.remote_host,
            self.remote_path
        )
        typing_text += 'Send("' + self._escape_send(scp_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_scp(self):
        """
        Closes the Scp AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
