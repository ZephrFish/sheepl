
# LOLBAS: explorer.exe — Legitimate use: managing files and launching applications via Windows Explorer

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of explorer.exe to browse a folder path or
 open an application via explorer's /root switch, as a normal user would
 when navigating the filesystem or launching a program through Explorer.

 Takes an optional target_path parameter specifying the folder or executable
 to open; if absent, launches Explorer with no arguments (opens default view).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Explorer(BaseCMD):
    """
    # LOLBAS: explorer.exe — Legitimate use: managing files and launching applications via Windows Explorer

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Explorer, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Explorer'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > explorer >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > explorer >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional target path to open (folder or executable)
        self.target_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Explorer Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a folder or file path using 'target_path <path>'
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
    #  Explorer Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Explorer interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Explorer_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_path(self, target_path):
        """
        Optionally set a folder path or executable path for Explorer to open.
        If not set, Explorer launches with no arguments (opens default file browser view).
        Example: target_path C:\\Users\\Public\\Documents
        Example: target_path C:\\Windows\\notepad.exe
        """
        if target_path:
            if self.taskstarted:
                self.target_path = target_path.strip()
                print(self.cl.green("[*] Target path set to: {}".format(self.target_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Explorer Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Explorer configuration
        """
        print(self.cl.green("[?] Currently Assigned Explorer Configuration"))
        print("[>] Target Path : {}".format(self.target_path if self.target_path else "(not set — will open default Explorer view)"))


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
        self.target_path = None


    ######################################################################
    # Explorer AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Explorer_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_explorer()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            target_path : str — folder or executable path to open with Explorer
                                if absent, Explorer is launched with no arguments
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_path = kwargs.get("target_path", None)
        if self.target_path:
            print(f"[*] Setting target_path attribute : {self.target_path}")
        else:
            print("[*] No target_path provided — will open default Explorer view")

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
        ; <      Explorer Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Explorer_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Explorer_{}()

            ; Creates an Explorer Interaction via CMD

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
        Builds the explorer.exe command to type into the CMD window.
        If target_path is set, opens Explorer with /root pointing to that path.
        Otherwise launches Explorer with no arguments for a default file browser view.
        """
        typing_text = '\n'

        if self.target_path:
            explorer_cmd = 'explorer.exe /root,"{}"'.format(self.target_path)
        else:
            explorer_cmd = 'explorer.exe'

        typing_text += 'Send("' + self._escape_send(explorer_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_explorer(self):
        """
        Closes the Explorer AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
