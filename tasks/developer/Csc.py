
# #######################################################################
#
#  Task : Csc Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of csc.exe — C# compiler.
 Compiles a C# source file using the .NET Framework C# compiler.

 the master script will already define the typing speed as part of the master declarations
"""

# LOLBAS: csc.exe — Legitimate use: C# source compilation (.NET Framework compiler)
# csc.exe location: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import os
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Csc(BaseCMD):
    """
    # LOLBAS: csc.exe — Legitimate use: C# source compilation (.NET Framework compiler)
    # csc.exe location: C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Csc, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Csc'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > csc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > csc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Path to .cs source file to compile
        self.source = None
        # Output executable path (default: same dir as source with .exe extension)
        self.output = None
        # Compilation target type: exe, library, winexe
        self.target = 'exe'

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Csc Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source file using 'source <path.cs>'
        3: Optionally set output path using 'output <path.exe>'
        4: Optionally set target type using 'target <exe|library|winexe>'
        5: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Csc Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Csc interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Csc_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source(self, arg):
        """
        Set the path to the C# source file (.cs) to compile.
        Example: source C:\\Users\\dev\\project\\Program.cs
        """
        if arg:
            if self.taskstarted:
                self.source = arg.strip()
                print(self.cl.green("[*] Source file set to: {}".format(self.source)))
                # Auto-derive default output path if not already set
                if not self.output:
                    base, _ = os.path.splitext(self.source)
                    self.output = base + '.exe'
                    print(self.cl.green("[*] Default output path derived: {}".format(self.output)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Csc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .cs source file."))


    def do_output(self, arg):
        """
        Set the output executable path.
        Defaults to the same directory as the source file with a .exe extension.
        Example: output C:\\Users\\dev\\project\\Program.exe
        """
        if arg:
            if self.taskstarted:
                self.output = arg.strip()
                print(self.cl.green("[*] Output path set to: {}".format(self.output)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Csc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output path."))


    def do_target(self, arg):
        """
        Set the compilation target type.
        Valid values: exe, library, winexe
        Default: exe
        Example: target library
        """
        valid_targets = ['exe', 'library', 'winexe']
        if arg:
            if self.taskstarted:
                if arg.strip().lower() in valid_targets:
                    self.target = arg.strip().lower()
                    print(self.cl.green("[*] Target type set to: {}".format(self.target)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid target type. Choose from: {}".format(', '.join(valid_targets))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Csc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target type: {}".format(', '.join(valid_targets))))


    def do_assigned(self, arg):
        """
        Get the current assigned Csc configuration
        """
        print(self.cl.green("[?] Currently Assigned Csc Configuration"))
        print("[>] Source  : {}".format(self.source if self.source else "(not set)"))
        print("[>] Output  : {}".format(self.output if self.output else "(not set)"))
        print("[>] Target  : {}".format(self.target))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.source:
                print(self.cl.red("[!] <ERROR> A source file (.cs) must be set before completing."))
                print(self.cl.red("[-] Use 'source <path>' to set the C# source file."))
                return None
            # Ensure output is derived if still None
            if not self.output:
                base, _ = os.path.splitext(self.source)
                self.output = base + '.exe'
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.source = None
        self.output = None
        self.target = 'exe'


    ######################################################################
    # Csc AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Csc_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_csc()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            source : str — path to the .cs source file to compile (required)
            output : str — output executable path (optional, defaults to source path with .exe)
            target : str — compilation target type: exe, library, winexe (optional, default: exe)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source = kwargs.get("source", None)
        print(f"[*] Setting the source attribute : {self.source}")

        # Derive default output from source if not provided
        default_output = None
        if self.source:
            base, _ = os.path.splitext(self.source)
            default_output = base + '.exe'

        self.output = kwargs.get("output", default_output)
        print(f"[*] Setting the output attribute : {self.output}")

        self.target = kwargs.get("target", "exe")
        print(f"[*] Setting the target attribute : {self.target}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      Csc Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Csc_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Csc_{}()

            ; Creates a Csc Interaction via CMD
            ; LOLBAS: csc.exe — Legitimate use: C# source compilation (.NET Framework compiler)
            ; csc.exe location: C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe

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
        Builds the csc.exe compilation command:
          csc /out:<output> /target:<target> <source>
        """
        typing_text = '\n'

        escaped_output = self._escape_send(self.output)
        escaped_source = self._escape_send(self.source)
        csc_cmd = 'csc /out:{} /target:{} {}'.format(escaped_output, self.target, escaped_source)
        typing_text += 'Send("' + csc_cmd + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_csc(self):
        """
        Closes the Csc AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
