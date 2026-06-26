
# LOLBAS: bash.exe — Legitimate use: running shell commands via Windows Subsystem for Linux (WSL)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of bash.exe (WSL) to run a shell command
 on Windows 10 / Windows 11 systems where WSL is installed.

 Takes a required shell_command parameter — the command to pass to bash -c.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Bash(BaseCMD):
    """
    # LOLBAS: bash.exe — Legitimate use: running shell commands via Windows Subsystem for Linux (WSL)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Bash, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Bash'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > bash >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > bash >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Shell command to execute via bash -c
        self.shell_command = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Bash (WSL) Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the shell command using 'shell_command <cmd>'
        3: Complete the interaction using 'complete'
        ----------------------------------
        Requires Windows Subsystem for Linux (WSL) to be installed.
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Bash Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Bash interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Bash_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_shell_command(self, shell_command):
        """
        Set the shell command to execute via bash.exe -c.
        Example: shell_command ls -la /mnt/c/Users
        """
        if shell_command:
            if self.taskstarted:
                self.shell_command = shell_command.strip()
                print(self.cl.green("[*] Shell command set to: {}".format(self.shell_command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Bash Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a shell command."))


    def do_assigned(self, arg):
        """
        Get the current assigned Bash configuration
        """
        print(self.cl.green("[?] Currently Assigned Bash Configuration"))
        print("[>] Shell Command : {}".format(self.shell_command if self.shell_command else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.shell_command:
                print(self.cl.red("[!] <ERROR> A shell_command must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.shell_command = None


    ######################################################################
    # Bash AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Bash_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_bash()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            shell_command : str — the shell command to pass to bash.exe -c
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.shell_command = kwargs.get("shell_command", None)
        if self.shell_command:
            print(f"[*] Setting shell_command attribute : {self.shell_command}")
        else:
            print("[!] <ERROR> No shell_command provided — this task requires a shell_command.")
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
        ; <      Bash (WSL) Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Bash_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Bash_{}()

            ; Creates a Bash (WSL) Interaction via CMD

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
        Builds the bash.exe command to type into the CMD window.
        Runs: bash.exe -c "<shell_command>"
        """
        typing_text = '\n'

        bash_cmd = 'bash.exe -c "{}"'.format(self.shell_command)
        typing_text += 'Send("' + self._escape_send(bash_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_bash(self):
        """
        Closes the Bash AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
