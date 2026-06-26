
# LOLBAS: conhost.exe — Legitimate use: hosting console windows as a parent process for CLI tools

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of conhost.exe to launch a command with conhost.exe
 as the parent process. Takes an optional command parameter; if absent runs
 a simple directory listing to demonstrate normal conhost usage.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Conhost(BaseCMD):
    """
    # LOLBAS: conhost.exe — Legitimate use: hosting console windows as a parent process for CLI tools

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Conhost, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Conhost'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > conhost >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > conhost >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional command to run under conhost.exe
        self.command = None
        # Whether to use --headless flag to hide child process window
        self.headless = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Conhost Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a command to run using 'command <cmd>'
        3: Optionally set headless mode using 'headless'
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
    #  Conhost Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Conhost interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Conhost_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_command(self, command):
        """
        Optionally set a command to run via conhost.exe.
        If not set, a simple directory listing (dir) will be used.
        Example: command dir C:\\Windows\\System32
        """
        if command:
            if self.taskstarted:
                self.command = command.strip()
                print(self.cl.green("[*] Command set to: {}".format(self.command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Conhost Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a command to run."))


    def do_headless(self, arg):
        """
        Toggle the --headless flag for conhost.exe.
        When enabled, the child process window is hidden.
        Example: headless
        """
        if self.taskstarted:
            self.headless = not self.headless
            state = "enabled" if self.headless else "disabled"
            print(self.cl.green("[*] Headless mode {}.".format(state)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Conhost Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned Conhost configuration
        """
        print(self.cl.green("[?] Currently Assigned Conhost Configuration"))
        print("[>] Command  : {}".format(self.command if self.command else "(not set — will run 'dir')"))
        print("[>] Headless : {}".format(self.headless))


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
        self.command = None
        self.headless = False


    ######################################################################
    # Conhost AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Conhost_' + current_counter, self.create_autoit_function())


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

        Optional JSON keys:
            command  : str  — command to run via conhost.exe
                              if absent, defaults to 'dir'
            headless : bool — if True, use --headless flag to hide child window
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.command = kwargs.get("command", None)
        self.headless = kwargs.get("headless", False)

        if self.command:
            print(f"[*] Setting command attribute : {self.command}")
        else:
            print("[*] No command provided — will default to 'dir'")

        print(f"[*] Headless mode : {self.headless}")

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
        ; <      Conhost Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Conhost_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Conhost_{}()

            ; Creates a Conhost Interaction via CMD

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
        Builds the conhost.exe command to type into the CMD window.
        Uses --headless flag if enabled. Defaults to running 'dir' if no command set.
        """
        typing_text = '\n'

        # Build the child command — default to dir listing if not specified
        child_cmd = self.command if self.command else 'dir'

        # Build the full conhost invocation
        if self.headless:
            conhost_cmd = 'conhost.exe --headless {}'.format(child_cmd)
        else:
            conhost_cmd = 'conhost.exe {}'.format(child_cmd)

        typing_text += 'Send("' + self._escape_send(conhost_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Conhost AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
