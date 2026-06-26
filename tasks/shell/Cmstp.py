
# LOLBAS: cmstp.exe — Legitimate use: silently installing a Connection Manager service profile (.inf)

# #######################################################################
#
#  Task : Cmstp Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of cmstp.exe to silently install a
 Connection Manager (VPN) service profile from a local .INF file.

 Takes a required inf_path parameter pointing to the local .INF profile.
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


class Cmstp(BaseCMD):
    """
    # LOLBAS: cmstp.exe — Legitimate use: silently installing a Connection Manager service profile (.inf)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Cmstp, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Cmstp'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cmstp >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cmstp >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the local Connection Manager .INF profile to install
        self.inf_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Cmstp Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the local .INF profile path using 'inf_path <path>'
        3: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Cmstp Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Cmstp interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Cmstp_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_inf_path(self, inf_path):
        """
        Set the local path to the Connection Manager .INF profile to install.
        Example: inf_path C:\\Profiles\\corp_vpn.inf
        """
        if inf_path:
            if self.taskstarted:
                self.inf_path = inf_path.strip()
                print(self.cl.green("[*] INF profile path set to: {}".format(self.inf_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cmstp Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .INF profile."))


    def do_assigned(self, arg):
        """
        Get the current assigned Cmstp configuration
        """
        print(self.cl.green("[?] Currently Assigned Cmstp Configuration"))
        print("[>] INF Path : {}".format(self.inf_path if self.inf_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.inf_path:
                print(self.cl.red("[!] <ERROR> inf_path must be set before completing. Use 'inf_path <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.inf_path = None


    ######################################################################
    # Cmstp AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Cmstp_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_cmstp()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            inf_path : str — local path to the Connection Manager .INF profile
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.inf_path = kwargs.get("inf_path", None)
        if self.inf_path:
            print(f"[*] Setting inf_path attribute : {self.inf_path}")
        else:
            print("[!] <ERROR> No inf_path provided — this is required for Cmstp.")
            return

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
        ; <      Cmstp Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Cmstp_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Cmstp_{}()

            ; Creates a Cmstp Interaction via CMD

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
        Builds the cmstp command to type into the CMD window.
        Silently installs the specified .INF Connection Manager profile.
        """
        typing_text = '\n'

        # Silently install the CM profile without creating a desktop icon
        install_cmd = 'cmstp.exe /ni /s {}'.format(self.inf_path)
        typing_text += 'Send("' + self._escape_send(install_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_cmstp(self):
        """
        Closes the Cmstp AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
