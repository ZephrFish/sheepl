
# LOLBAS: rcsi.exe — Legitimate use: running C# scripts non-interactively via the Roslyn scripting engine
# DEVELOPER-ONLY: requires Visual Studio or the Roslyn SDK to be installed (rcsi.exe ships with VS)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of rcsi.exe to execute C# script files (.csx)
 non-interactively from the command line.

 Takes a required csx_script parameter specifying the path to the .csx file to run.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Rcsi(BaseCMD):
    """
    # LOLBAS: rcsi.exe — Legitimate use: executing C# script (.csx) files non-interactively
    # DEVELOPER-ONLY: requires Visual Studio or the Roslyn SDK to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Rcsi, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Rcsi'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > rcsi >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > rcsi >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .csx script file to execute
        self.csx_script = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Rcsi Interaction.
        [!] DEVELOPER-ONLY: requires Visual Studio / Roslyn SDK (rcsi.exe).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the path to a .csx script using 'csx_script <path>'
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
    #  Rcsi Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Rcsi interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Rcsi_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_csx_script(self, csx_script):
        """
        Set the path to the .csx C# script file to execute.
        Example: csx_script C:\\Scripts\\hello.csx
        """
        if csx_script:
            if self.taskstarted:
                self.csx_script = csx_script.strip()
                print(self.cl.green("[*] CSX script path set to: {}".format(self.csx_script)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rcsi Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .csx script file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Rcsi configuration
        """
        print(self.cl.green("[?] Currently Assigned Rcsi Configuration"))
        print("[>] CSX Script : {}".format(self.csx_script if self.csx_script else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.csx_script:
                print(self.cl.red("[!] <ERROR> csx_script must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.csx_script = None


    ######################################################################
    # Rcsi AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Rcsi_' + current_counter, self.create_autoit_function())


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
            csx_script : str — full path to the .csx C# script file to execute
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.csx_script = kwargs.get("csx_script", None)
        if self.csx_script:
            print(f"[*] Setting csx_script attribute : {self.csx_script}")
        else:
            print("[!] <ERROR> csx_script is required for Rcsi task.")

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
        ; <      Rcsi Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Rcsi_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Rcsi_{}()

            ; Creates an Rcsi Interaction via CMD

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
        Builds the rcsi.exe command to type into the CMD window.
        Executes the specified .csx C# script file non-interactively.
        """
        typing_text = '\n'

        # Run the specified .csx script with rcsi.exe
        rcsi_cmd = 'rcsi.exe {}'.format(self.csx_script)
        typing_text += 'Send("' + self._escape_send(rcsi_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Rcsi AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
