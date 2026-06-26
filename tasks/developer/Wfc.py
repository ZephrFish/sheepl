
# LOLBAS: wfc.exe — Legitimate use: compiling XOML workflow definition files into assemblies
# DEVELOPER-ONLY: Requires Windows SDK (NETFX 4.8 Tools) installed at
#   C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\wfc.exe


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of wfc.exe (Workflow Command-line Compiler)
 to compile a XOML workflow definition file into a .NET assembly.

 Takes a required xoml_path parameter pointing to the .xoml file to compile.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Wfc(BaseCMD):
    """
    # LOLBAS: wfc.exe — Legitimate use: compiling XOML workflow definition files into assemblies
    # DEVELOPER-ONLY: Requires Windows SDK (NETFX 4.8 Tools)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Wfc, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Wfc'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wfc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wfc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .xoml file to compile
        self.xoml_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Wfc (Workflow Command-line Compiler) Interaction.
        [!] DEVELOPER-ONLY: Requires Windows SDK (NETFX 4.8 Tools).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the XOML file path using 'xoml_path <path>'
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
    #  Wfc Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Wfc interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Wfc_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_xoml_path(self, xoml_path):
        """
        Set the path to the XOML workflow definition file to compile.
        Example: xoml_path C:\\Workflows\\MyWorkflow.xoml
        """
        if xoml_path:
            if self.taskstarted:
                self.xoml_path = xoml_path.strip()
                print(self.cl.green("[*] XOML path set to: {}".format(self.xoml_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Wfc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .xoml file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Wfc configuration
        """
        print(self.cl.green("[?] Currently Assigned Wfc Configuration"))
        print("[>] XOML Path : {}".format(self.xoml_path if self.xoml_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.xoml_path:
                print(self.cl.red("[!] <ERROR> xoml_path must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.xoml_path = None


    ######################################################################
    # Wfc AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Wfc_' + current_counter, self.create_autoit_function())


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
            xoml_path : str — absolute path to the .xoml workflow file to compile
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.xoml_path = kwargs.get("xoml_path", None)
        if self.xoml_path:
            print(f"[*] Setting xoml_path attribute : {self.xoml_path}")
        else:
            print("[!] <ERROR> xoml_path is required for Wfc task.")
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
        ; <      Wfc Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Wfc_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Wfc_{}()

            ; Creates a Wfc Interaction via CMD

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
        Builds the wfc.exe command to type into the CMD window.
        Compiles the specified .xoml workflow definition file.
        """
        typing_text = '\n'

        wfc_path = r'"C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\wfc.exe"'
        compile_cmd = '{} {}'.format(wfc_path, self.xoml_path)
        typing_text += 'Send("' + self._escape_send(compile_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Wfc AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
