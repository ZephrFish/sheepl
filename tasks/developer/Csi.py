
# #######################################################################
#
#  Task : Csi Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of csi.exe — C# Interactive REPL
 included with Visual Studio (Roslyn). Executes a C# script file (.cs)
 directly without prior compilation.

 DEVELOPER-ONLY: Requires Visual Studio (Roslyn toolchain) to be installed.
 Default path: C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\MSBuild\\15.0\\Bin\\Roslyn\\csi.exe

 the master script will already define the typing speed as part of the master declarations
"""

# LOLBAS: csi.exe — Legitimate use: running C# script files via the Visual Studio Roslyn REPL
# DEVELOPER-ONLY: Requires Visual Studio with Roslyn components installed

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Csi(BaseCMD):
    """
    # LOLBAS: csi.exe — Legitimate use: running C# script files via the Visual Studio Roslyn REPL
    # DEVELOPER-ONLY: Requires Visual Studio with Roslyn components installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Csi, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Csi'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > csi >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > csi >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Path to the .cs script file to execute
        self.script = None

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Csi Interaction.
        DEVELOPER-ONLY: Requires Visual Studio (Roslyn) to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the C# script file using 'script <path.cs>'
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
    #  Csi Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Csi interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Csi_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_script(self, arg):
        """
        Set the path to the C# script file (.cs) to execute with csi.exe.
        Example: script C:\\Users\\dev\\scripts\\hello.cs
        """
        if arg:
            if self.taskstarted:
                self.script = arg.strip()
                print(self.cl.green("[*] Script file set to: {}".format(self.script)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Csi Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .cs script file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Csi configuration
        """
        print(self.cl.green("[?] Currently Assigned Csi Configuration"))
        print("[>] Script  : {}".format(self.script if self.script else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.script:
                print(self.cl.red("[!] <ERROR> A script file (.cs) must be set before completing."))
                print(self.cl.red("[-] Use 'script <path>' to set the C# script file."))
                return None
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.script = None


    ######################################################################
    # Csi AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Csi_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_csi()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            script : str — path to the .cs script file to execute with csi.exe (required)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.script = kwargs.get("script", None)
        print(f"[*] Setting the script attribute : {self.script}")

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
        ; <      Csi Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Csi_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Csi_{}()

            ; Creates a Csi Interaction via CMD
            ; LOLBAS: csi.exe — Legitimate use: running C# script files via the Visual Studio Roslyn REPL
            ; DEVELOPER-ONLY: Requires Visual Studio with Roslyn components installed

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
        Builds the csi.exe command to type into the CMD window:
          csi.exe <script.cs>
        """
        typing_text = '\n'

        csi_cmd = 'csi.exe {}'.format(self._escape_send(self.script))
        typing_text += 'Send("' + csi_cmd + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_csi(self):
        """
        Closes the Csi AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
