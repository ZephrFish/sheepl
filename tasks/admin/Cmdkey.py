
# LOLBAS: cmdkey.exe — Legitimate use: listing and managing stored Windows credentials

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of cmdkey.exe to list stored user names
 and passwords / credentials on the host.

 Optionally adds a generic credential entry (e.g. for a file-share) and
 then lists all stored credentials.  The master script will already define
 the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Cmdkey(BaseCMD):
    """
    # LOLBAS: cmdkey.exe — Legitimate use: listing and managing stored Windows credentials

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Cmdkey, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Cmdkey'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cmdkey >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cmdkey >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional credential target to add before listing
        self.target = None
        self.username = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Cmdkey Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a credential target using 'target <hostname_or_ip>'
        3: Optionally set a username using 'username <user>'
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
    #  Cmdkey Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Cmdkey interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Cmdkey_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target(self, target):
        """
        Optionally set a target host or server name to store a credential for.
        If not set, only a /list will be performed.
        Example: target fileserver01
        """
        if target:
            if self.taskstarted:
                self.target = target.strip()
                print(self.cl.green("[*] Target set to: {}".format(self.target)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cmdkey Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target hostname or IP."))


    def do_username(self, username):
        """
        Optionally set the username for the stored credential.
        Only used when a target is also set.
        Example: username domainuser
        """
        if username:
            if self.taskstarted:
                self.username = username.strip()
                print(self.cl.green("[*] Username set to: {}".format(self.username)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cmdkey Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a username."))


    def do_assigned(self, arg):
        """
        Get the current assigned Cmdkey configuration
        """
        print(self.cl.green("[?] Currently Assigned Cmdkey Configuration"))
        print("[>] Target   : {}".format(self.target if self.target else "(not set — will only list credentials)"))
        print("[>] Username : {}".format(self.username if self.username else "(not set)"))


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
        self.target = None
        self.username = None


    ######################################################################
    # Cmdkey AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Cmdkey_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_cmdkey()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            target   : str — hostname or IP to store a generic credential for
            username : str — username for the stored credential (used with target)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target = kwargs.get("target", None)
        self.username = kwargs.get("username", None)

        if self.target:
            print(f"[*] Setting target attribute : {self.target}")
        else:
            print("[*] No target provided — will only list stored credentials")

        if self.username:
            print(f"[*] Setting username attribute : {self.username}")

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
        ; <      Cmdkey Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Cmdkey_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Cmdkey_{}()

            ; Creates a Cmdkey Interaction via CMD

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
        Builds the cmdkey commands to type into the CMD window.
        If target and username are set, adds a generic credential entry first.
        Always lists all stored credentials at the end.
        """
        typing_text = '\n'

        # Optionally add a generic stored credential for a target host
        if self.target and self.username:
            add_cmd = 'cmdkey /generic:{} /user:{} /pass:Password1'.format(
                self.target, self.username
            )
            typing_text += 'Send("' + self._escape_send(add_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Always list all stored credentials
        list_cmd = 'cmdkey /list'
        typing_text += 'Send("' + self._escape_send(list_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_cmdkey(self):
        """
        Closes the Cmdkey AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
