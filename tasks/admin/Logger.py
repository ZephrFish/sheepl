
# LOLBAS: logger.exe — Legitimate use: launch process logging via Windows Kits debugger tool
# DEVELOPER-ONLY: Requires Windows Kits (WDK/SDK) installation; logger.exe ships with Debugging Tools for Windows

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of logger.exe to run a command under
 the Windows Kits process logger for diagnostic tracing.

 Takes a command parameter specifying the executable to launch under logger.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Logger(BaseCMD):
    """
    # LOLBAS: logger.exe — Legitimate use: launch process logging via Windows Kits debugger tool
    # DEVELOPER-ONLY: Requires Windows Kits (WDK/SDK) installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Logger, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Logger'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > logger >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > logger >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Command to run under logger — defaults to a benign system tool
        self.command = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Logger Interaction.
        [!] DEVELOPER-ONLY: Requires Windows Kits (Debugging Tools for Windows).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the command to run using 'command <cmd>'
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
    #  Logger Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Logger interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Logger_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_command(self, command):
        """
        Set the command to run under logger.exe.
        Example: command notepad.exe
        Example: command cmd.exe /c ipconfig
        """
        if command:
            if self.taskstarted:
                self.command = command.strip()
                print(self.cl.green("[*] Command set to: {}".format(self.command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Logger Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a command to run."))


    def do_assigned(self, arg):
        """
        Get the current assigned Logger configuration
        """
        print(self.cl.green("[?] Currently Assigned Logger Configuration"))
        print("[>] Command : {}".format(self.command if self.command else "(not set — will default to notepad.exe)"))


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


    ######################################################################
    # Logger AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Logger_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_logger()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            command : str — the command to run under logger.exe
                            if absent, defaults to notepad.exe
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.command = kwargs.get("command", None)
        if self.command:
            print(f"[*] Setting command attribute : {self.command}")
        else:
            print("[*] No command provided — will default to notepad.exe")

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
        ; <      Logger Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Logger_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Logger_{}()

            ; Creates a Logger Interaction via CMD

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
        Builds the logger.exe command to type into the CMD window.
        Runs the configured command (or notepad.exe by default) under logger.exe.
        """
        typing_text = '\n'

        # Resolve command — default to notepad.exe if not set
        target_cmd = self.command if self.command else 'notepad.exe'

        # Use the RUN subcommand to launch target under logger.exe for tracing
        logger_cmd = 'logger.exe RUN "{}"'.format(target_cmd)
        typing_text += 'Send("' + self._escape_send(logger_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_logger(self):
        """
        Closes the Logger AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
