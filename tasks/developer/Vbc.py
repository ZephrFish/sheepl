
# LOLBAS: vbc.exe — Legitimate use: compile Visual Basic .NET source files using the .NET Framework compiler
# DEVELOPER-ONLY: requires .NET Framework (vbc.exe ships with .NET Framework, not always present without developer tooling)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of vbc.exe to compile a Visual Basic
 .NET source file into an executable using the .NET Framework compiler.

 Takes a source_file parameter (absolute path to a .vb file).
 Optionally accepts a reference_dll to compile with an additional assembly reference.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Vbc(BaseCMD):
    """
    # LOLBAS: vbc.exe — Legitimate use: compile Visual Basic .NET source files using the .NET Framework compiler

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Vbc, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Vbc'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > vbc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > vbc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the Visual Basic source file to compile
        self.source_file = None
        # Optional additional assembly reference DLL
        self.reference_dll = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Vbc Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source file path using 'source_file <absolute_path_to_.vb>'
        3: Optionally set an assembly reference using 'reference_dll <DllName.dll>'
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
    #  Vbc Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Vbc interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Vbc_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source_file(self, source_file):
        """
        Set the absolute path to the Visual Basic source file to compile.
        Example: source_file C:\\Dev\\HelloWorld.vb
        """
        if source_file:
            if self.taskstarted:
                self.source_file = source_file.strip()
                print(self.cl.green("[*] Source file set to: {}".format(self.source_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Vbc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .vb source file."))


    def do_reference_dll(self, reference_dll):
        """
        Optionally set an assembly reference DLL to include during compilation.
        Example: reference_dll Microsoft.VisualBasic.dll
        """
        if reference_dll:
            if self.taskstarted:
                self.reference_dll = reference_dll.strip()
                print(self.cl.green("[*] Reference DLL set to: {}".format(self.reference_dll)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Vbc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Vbc configuration
        """
        print(self.cl.green("[?] Currently Assigned Vbc Configuration"))
        print("[>] Source File   : {}".format(self.source_file if self.source_file else "(not set)"))
        print("[>] Reference DLL : {}".format(self.reference_dll if self.reference_dll else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.source_file:
                print(self.cl.red("[!] <ERROR> source_file is required. Set it with 'source_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.source_file = None
        self.reference_dll = None


    ######################################################################
    # Vbc AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Vbc_' + current_counter, self.create_autoit_function())


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
            source_file  : str — absolute path to the .vb source file to compile

        Optional JSON keys:
            reference_dll : str — assembly reference DLL name (e.g. Microsoft.VisualBasic.dll)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source_file = kwargs.get("source_file", None)
        if self.source_file:
            print(f"[*] Setting source_file attribute : {self.source_file}")
        else:
            print("[!] <ERROR> source_file is required for Vbc task.")
            return

        self.reference_dll = kwargs.get("reference_dll", None)
        if self.reference_dll:
            print(f"[*] Setting reference_dll attribute : {self.reference_dll}")
        else:
            print("[*] No reference_dll provided — compiling with /target:exe only")

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
        ; <      Vbc Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Vbc_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Vbc_{}()

            ; Creates a Vbc Interaction via CMD

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
        Builds the vbc.exe compile commands to type into the CMD window.
        Always compiles the source file to an executable.
        If reference_dll is set, also compiles with that assembly reference.
        """
        typing_text = '\n'

        # Compile source file to executable using /target:exe
        compile_cmd = 'vbc.exe /target:exe {}'.format(self.source_file)
        typing_text += 'Send("' + self._escape_send(compile_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Optionally compile with an additional assembly reference
        if self.reference_dll:
            ref_cmd = 'vbc.exe -reference:{} {}'.format(self.reference_dll, self.source_file)
            typing_text += 'Send("' + self._escape_send(ref_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Vbc AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
