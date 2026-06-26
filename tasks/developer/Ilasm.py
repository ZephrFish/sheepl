
# LOLBAS: ilasm.exe — Legitimate use: compile IL/C# intermediate language source files to .exe or .dll
# DEVELOPER-ONLY: Requires .NET Framework (typically installed with Visual Studio or Windows SDK)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of ilasm.exe to compile Intermediate
 Language (IL) source files into .exe or .dll assemblies using the .NET
 Framework's IL Assembler.

 Takes a source_file parameter (path to a .txt or .il file containing IL
 code) and an optional output_type ('exe' or 'dll', default 'exe').
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


class Ilasm(BaseCMD):
    """
    # LOLBAS: ilasm.exe — Legitimate use: compile IL source files to .exe or .dll assemblies

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Ilasm, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Ilasm'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ilasm >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ilasm >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # IL source file to compile
        self.source_file = None
        # Output type: exe or dll
        self.output_type = 'exe'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Ilasm Interaction.
        [!] DEVELOPER-ONLY: Requires .NET Framework ilasm.exe
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the IL source file path using 'source_file <path>'
        3: Optionally set the output type using 'output_type <exe|dll>'
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
    #  Ilasm Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Ilasm interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Ilasm_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source_file(self, source_file):
        """
        Set the path to the IL source file to compile.
        Accepts a .txt or .il file containing IL assembly code.
        Example: source_file C:\\Users\\dev\\hello_world.txt
        """
        if source_file:
            if self.taskstarted:
                self.source_file = source_file.strip()
                print(self.cl.green("[*] Source file set to: {}".format(self.source_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Ilasm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a source file path."))


    def do_output_type(self, output_type):
        """
        Set the output type for the compiled assembly.
        Valid options: exe (default) or dll
        Example: output_type dll
        """
        if output_type:
            if self.taskstarted:
                output_type = output_type.strip().lower()
                if output_type in ('exe', 'dll'):
                    self.output_type = output_type
                    print(self.cl.green("[*] Output type set to: {}".format(self.output_type)))
                else:
                    print(self.cl.red("[!] <ERROR> output_type must be 'exe' or 'dll'."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Ilasm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output type (exe or dll)."))


    def do_assigned(self, arg):
        """
        Get the current assigned Ilasm configuration
        """
        print(self.cl.green("[?] Currently Assigned Ilasm Configuration"))
        print("[>] Source File  : {}".format(self.source_file if self.source_file else "(not set)"))
        print("[>] Output Type  : {}".format(self.output_type))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.source_file:
                print(self.cl.red("[!] <ERROR> source_file must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.source_file = None
        self.output_type = 'exe'


    ######################################################################
    # Ilasm AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Ilasm_' + current_counter, self.create_autoit_function())


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
            source_file : str — path to the IL source file to compile

        Optional JSON keys:
            output_type : str — 'exe' or 'dll' (default: 'exe')
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source_file = kwargs.get("source_file", None)
        if self.source_file:
            print(f"[*] Setting source_file attribute : {self.source_file}")
        else:
            print("[!] <ERROR> source_file is required for Ilasm task.")
            return

        self.output_type = kwargs.get("output_type", "exe").strip().lower()
        print(f"[*] Setting output_type attribute : {self.output_type}")

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
        ; <      Ilasm Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Ilasm_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Ilasm_{}()

            ; Creates an Ilasm Interaction via CMD

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
        Builds the ilasm command to type into the CMD window.
        Compiles the specified IL source file to the selected output type.
        """
        typing_text = '\n'

        # Build the ilasm command: ilasm.exe <source_file> /<output_type>
        ilasm_cmd = 'ilasm.exe {} /{}'.format(self.source_file, self.output_type)
        typing_text += 'Send("' + self._escape_send(ilasm_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Ilasm AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
