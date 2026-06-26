
# LOLBAS: mshta.exe — Legitimate use: opening and running HTML Applications (.hta) for IT admin tools

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of mshta.exe to open and execute local
 HTML Application (.hta) files, which are used by administrators for
 deployment wizards, configuration panels, and on-premises tools.

 Takes a required hta_path parameter pointing to a local .hta file.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Mshta(BaseCMD):
    """
    # LOLBAS: mshta.exe — Legitimate use: opening local HTML Application (.hta) files for admin tools

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Mshta, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Mshta'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mshta >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mshta >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the local .hta file to open
        self.hta_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Mshta Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the path to the .hta file using 'hta_path <path>'
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
    #  Mshta Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Mshta interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Mshta_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_hta_path(self, hta_path):
        """
        Set the path to the local .hta file to open with mshta.exe.
        Example: hta_path C:\\Tools\\admin_panel.hta
        """
        if hta_path:
            if self.taskstarted:
                self.hta_path = hta_path.strip()
                print(self.cl.green("[*] HTA path set to: {}".format(self.hta_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Mshta Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to an .hta file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Mshta configuration
        """
        print(self.cl.green("[?] Currently Assigned Mshta Configuration"))
        print("[>] HTA Path : {}".format(self.hta_path if self.hta_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.hta_path:
                print(self.cl.red("[!] <ERROR> You must set an hta_path before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.hta_path = None


    ######################################################################
    # Mshta AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Mshta_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_mshta()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            hta_path : str — path to the local .hta file to open with mshta.exe
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.hta_path = kwargs.get("hta_path", None)
        if self.hta_path:
            print(f"[*] Setting hta_path attribute : {self.hta_path}")
        else:
            print("[!] <ERROR> No hta_path provided — this is required for Mshta.")
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
        ; <      Mshta Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Mshta_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Mshta_{}()

            ; Creates a Mshta Interaction via CMD

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
        Builds the mshta command to type into the CMD window.
        Opens the specified local .hta file with mshta.exe.
        """
        typing_text = '\n'

        # Run mshta.exe against the specified local .hta file
        mshta_cmd = 'mshta.exe {}'.format(self.hta_path)
        typing_text += 'Send("' + self._escape_send(mshta_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_mshta(self):
        """
        Closes the Mshta AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
