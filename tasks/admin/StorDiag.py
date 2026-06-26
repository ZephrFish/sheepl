
# LOLBAS: stordiag.exe — Legitimate use: collecting storage diagnostics for troubleshooting
# #######################################################################
#
#  Task : StorDiag Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of stordiag.exe to run Windows storage
 diagnostics. Stordiag launches system tools (schtasks.exe,
 systeminfo.exe, fltmc.exe) as part of its normal diagnostic routine.

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


class StorDiag(BaseCMD):
    """
    # LOLBAS: stordiag.exe — Legitimate use: collecting storage diagnostics for troubleshooting

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(StorDiag, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'StorDiag'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > stordiag >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > stordiag >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional output directory for diagnostic results
        self.output_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] StorDiag Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set an output directory using 'output_dir <path>'
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
    #  StorDiag Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new StorDiag interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'StorDiag_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_output_dir(self, output_dir):
        """
        Optionally set an output directory for stordiag diagnostic results.
        If not set, stordiag runs without an explicit output path.
        Example: output_dir C:\\Temp\\StorDiagOutput
        """
        if output_dir:
            if self.taskstarted:
                self.output_dir = output_dir.strip()
                print(self.cl.green("[*] Output directory set to: {}".format(self.output_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new StorDiag Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned StorDiag configuration
        """
        print(self.cl.green("[?] Currently Assigned StorDiag Configuration"))
        print("[>] Output Dir : {}".format(self.output_dir if self.output_dir else "(not set — stordiag runs with default output)"))


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
        self.output_dir = None


    ######################################################################
    # StorDiag AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('StorDiag_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_stordiag()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            output_dir : str — path to write stordiag output files
                               if absent, stordiag runs without an explicit output path
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.output_dir = kwargs.get("output_dir", None)
        if self.output_dir:
            print(f"[*] Setting output_dir attribute : {self.output_dir}")
        else:
            print("[*] No output_dir provided — stordiag will run with default behaviour")

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
        ; <      StorDiag Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "StorDiag_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func StorDiag_{}()

            ; Creates a StorDiag Interaction via CMD

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
        Builds the stordiag commands to type into the CMD window.
        Runs stordiag.exe to collect storage diagnostic information.
        If output_dir is set, passes it as the output path argument.
        """
        typing_text = '\n'

        if self.output_dir:
            diag_cmd = 'stordiag.exe -out {}'.format(self.output_dir)
        else:
            diag_cmd = 'stordiag.exe'

        typing_text += 'Send("' + self._escape_send(diag_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_stordiag(self):
        """
        Closes the StorDiag AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
