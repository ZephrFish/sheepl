
# LOLBAS: desk.cpl — Legitimate use: Desktop Settings Control Panel, launching screen savers via rundll32

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of desk.cpl via rundll32.exe to invoke the
 InstallScreenSaver function, which opens a .scr file as a screen saver
 through the Desktop Settings Control Panel library.

 Requires a screen_saver_path parameter pointing to a local .scr file.
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


class Desk(BaseCMD):
    """
    # LOLBAS: desk.cpl — Legitimate use: launching screen savers via the Desktop Settings Control Panel

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Desk, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Desk'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > desk >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > desk >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .scr screen saver file to install
        self.screen_saver_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Desk (desk.cpl) Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the screen saver path using 'screen_saver_path <path>'
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
    #  Desk Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Desk interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Desk_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_screen_saver_path(self, screen_saver_path):
        """
        Set the path to the .scr screen saver file to install.
        Example: screen_saver_path C:\\Windows\\System32\\Bubbles.scr
        """
        if screen_saver_path:
            if self.taskstarted:
                self.screen_saver_path = screen_saver_path.strip()
                print(self.cl.green("[*] Screen saver path set to: {}".format(self.screen_saver_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Desk Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a screen saver path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Desk configuration
        """
        print(self.cl.green("[?] Currently Assigned Desk Configuration"))
        print("[>] Screen Saver Path : {}".format(self.screen_saver_path if self.screen_saver_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.screen_saver_path:
                print(self.cl.red("[!] <ERROR> Please set a screen saver path using 'screen_saver_path'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.screen_saver_path = None


    ######################################################################
    # Desk AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Desk_' + current_counter, self.create_autoit_function())


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
            screen_saver_path : str — path to the .scr file to install via InstallScreenSaver
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.screen_saver_path = kwargs.get("screen_saver_path", None)
        if self.screen_saver_path:
            print(f"[*] Setting screen_saver_path attribute : {self.screen_saver_path}")
        else:
            print("[!] <ERROR> No screen_saver_path provided — this task requires a .scr file path.")
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
        ; <      Desk (desk.cpl) Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Desk_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Desk_{}()

            ; Creates a Desk (desk.cpl) Interaction via CMD

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
        Builds the rundll32 desk.cpl InstallScreenSaver command to type into the CMD window.
        """
        typing_text = '\n'

        # Invoke InstallScreenSaver via rundll32 and desk.cpl
        desk_cmd = 'rundll32.exe desk.cpl,InstallScreenSaver {}'.format(self.screen_saver_path)
        typing_text += 'Send("' + self._escape_send(desk_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Desk AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
