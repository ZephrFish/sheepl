
# LOLBAS: finger.exe — Legitimate use: querying user information from a remote host running the Finger service

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of finger.exe to query user information
 from a remote host running the Finger daemon/service.

 Takes a required remote_host parameter and an optional username parameter.
 If username is omitted, finger queries all logged-in users on the remote host.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Finger(BaseCMD):
    """
    # LOLBAS: finger.exe — Legitimate use: querying user information from a remote host running the Finger service

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Finger, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Finger'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > finger >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > finger >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Remote host to finger
        self.remote_host = None
        # Optional username to query; if absent queries all users
        self.username = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Finger Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the remote host using 'remote_host <hostname>'
        3: Optionally set a username using 'username <name>'
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
    #  Finger Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Finger interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Finger_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_remote_host(self, remote_host):
        """
        Set the remote host to query with finger.
        Example: remote_host fileserver.corp.local
        """
        if remote_host:
            if self.taskstarted:
                self.remote_host = remote_host.strip()
                print(self.cl.green("[*] Remote host set to: {}".format(self.remote_host)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Finger Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote host."))


    def do_username(self, username):
        """
        Optionally set a username to query on the remote host.
        If not set, finger will query all logged-in users.
        Example: username jsmith
        """
        if username:
            if self.taskstarted:
                self.username = username.strip()
                print(self.cl.green("[*] Username set to: {}".format(self.username)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Finger Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a username."))


    def do_assigned(self, arg):
        """
        Get the current assigned Finger configuration
        """
        print(self.cl.green("[?] Currently Assigned Finger Configuration"))
        print("[>] Remote Host : {}".format(self.remote_host if self.remote_host else "(not set)"))
        print("[>] Username    : {}".format(self.username if self.username else "(not set — will query all users)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.remote_host:
                print(self.cl.red("[!] <ERROR> A remote host is required. Use 'remote_host <hostname>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.remote_host = None
        self.username = None


    ######################################################################
    # Finger AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Finger_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_finger()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            remote_host : str — hostname or IP of the remote Finger server

        Optional JSON keys:
            username    : str — specific user to query; if absent queries all users
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.remote_host = kwargs.get("remote_host", None)
        if self.remote_host:
            print(f"[*] Setting remote_host attribute : {self.remote_host}")
        else:
            print("[!] <ERROR> No remote_host provided — this is required for Finger.")

        self.username = kwargs.get("username", None)
        if self.username:
            print(f"[*] Setting username attribute : {self.username}")
        else:
            print("[*] No username provided — will query all logged-in users on the remote host")

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
        ; <      Finger Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Finger_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Finger_{}()

            ; Creates a Finger Interaction via CMD

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
        Builds the finger command to type into the CMD window.
        If username is set, queries that specific user on the remote host.
        Otherwise queries all logged-in users on the remote host.
        """
        typing_text = '\n'

        if self.username:
            finger_cmd = 'finger {}@{}'.format(self.username, self.remote_host)
        else:
            finger_cmd = 'finger @{}'.format(self.remote_host)

        typing_text += 'Send("' + self._escape_send(finger_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_finger(self):
        """
        Closes the Finger AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
