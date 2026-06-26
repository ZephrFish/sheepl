
# LOLBAS: Runscripthelper.exe — Legitimate use: execute a PowerShell diagnostic script via the Windows telemetry client helper

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of Runscripthelper.exe to invoke a PowerShell
 script (stored with a .txt extension) through the Windows telemetry client
 helper binary, using the 'surfacecheck' verb.

 Requires: script_path (absolute path to the .txt PowerShell script) and
           working_folder (absolute path to the working directory).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class RunScriptHelper(BaseCMD):
    """
    # LOLBAS: Runscripthelper.exe — Legitimate use: execute a PowerShell diagnostic script via the Windows telemetry client helper

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(RunScriptHelper, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'RunScriptHelper'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > runscripthelper >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > runscripthelper >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.script_path = None
        self.working_folder = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] RunScriptHelper Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the PowerShell script path (.txt) using 'script_path <path>'
        3: Set the working folder using 'working_folder <path>'
        4: Complete the interaction using 'complete'
        ----------------------------------
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  RunScriptHelper Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new RunScriptHelper interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'RunScriptHelper_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_script_path(self, script_path):
        """
        Set the absolute path to the PowerShell script file (.txt extension).
        Example: script_path C:\\Diagnostics\\telemetry_check.txt
        """
        if script_path:
            if self.taskstarted:
                self.script_path = script_path.strip()
                print(self.cl.green("[*] Script path set to: {}".format(self.script_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RunScriptHelper Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide the absolute path to the script file."))


    def do_working_folder(self, working_folder):
        """
        Set the absolute path to the working folder for the script execution.
        Example: working_folder C:\\Diagnostics
        """
        if working_folder:
            if self.taskstarted:
                self.working_folder = working_folder.strip()
                print(self.cl.green("[*] Working folder set to: {}".format(self.working_folder)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RunScriptHelper Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide the absolute path to the working folder."))


    def do_assigned(self, arg):
        """
        Get the current assigned RunScriptHelper configuration
        """
        print(self.cl.green("[?] Currently Assigned RunScriptHelper Configuration"))
        print("[>] Script Path    : {}".format(self.script_path if self.script_path else "(not set)"))
        print("[>] Working Folder : {}".format(self.working_folder if self.working_folder else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.script_path:
                print(self.cl.red("[!] <ERROR> script_path is required. Set it with 'script_path <path>'."))
                return
            if not self.working_folder:
                print(self.cl.red("[!] <ERROR> working_folder is required. Set it with 'working_folder <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.script_path = None
        self.working_folder = None


    ######################################################################
    # RunScriptHelper AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('RunScriptHelper_' + current_counter, self.create_autoit_function())


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
            script_path    : str — absolute path to the PowerShell .txt script
            working_folder : str — absolute path to the working directory
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.script_path = kwargs.get("script_path", None)
        self.working_folder = kwargs.get("working_folder", None)

        if self.script_path:
            print(f"[*] Setting script_path attribute : {self.script_path}")
        else:
            print("[!] <ERROR> No script_path provided — this is required.")

        if self.working_folder:
            print(f"[*] Setting working_folder attribute : {self.working_folder}")
        else:
            print("[!] <ERROR> No working_folder provided — this is required.")

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
        ; <      RunScriptHelper Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "RunScriptHelper_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func RunScriptHelper_{}()

            ; Creates a RunScriptHelper Interaction via CMD

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
        Builds the runscripthelper.exe command to type into the CMD window.
        Uses the 'surfacecheck' verb to execute the PowerShell script (.txt)
        in the specified working folder.
        """
        typing_text = '\n'

        # Build the runscripthelper command using the surfacecheck verb
        rsh_cmd = 'runscripthelper.exe surfacecheck \\\\?\\{} {}'.format(
            self.script_path, self.working_folder
        )
        typing_text += 'Send("' + self._escape_send(rsh_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the RunScriptHelper AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
