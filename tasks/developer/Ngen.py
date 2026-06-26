
# LOLBAS: ngen.exe — Legitimate use: compiling .NET assemblies to native images to improve startup performance
# DEVELOPER-ONLY: requires .NET Framework installed (C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ngen.exe)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer/IT use of ngen.exe to compile a .NET assembly
 into a native image, improving application startup performance.

 Takes an optional assembly_path parameter; if absent uses a common .NET
 managed assembly path as a default.

 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Ngen(BaseCMD):
    """
    # LOLBAS: ngen.exe — Legitimate use: compiling .NET assemblies to native images to improve startup performance
    # DEVELOPER-ONLY: requires .NET Framework installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Ngen, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Ngen'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ngen >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ngen >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional assembly path to compile with ngen
        self.assembly_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Ngen Interaction.
        [!] DEVELOPER-ONLY: requires .NET Framework installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a specific assembly path using 'assembly_path <path>'
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
    #  Ngen Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Ngen interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Ngen_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assembly_path(self, assembly_path):
        """
        Optionally set a specific .NET assembly path to compile with ngen.
        If not set, a common default managed assembly will be used.
        Example: assembly_path C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clrjit.dll
        """
        if assembly_path:
            if self.taskstarted:
                self.assembly_path = assembly_path.strip()
                print(self.cl.green("[*] Assembly path set to: {}".format(self.assembly_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Ngen Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an assembly path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Ngen configuration
        """
        print(self.cl.green("[?] Currently Assigned Ngen Configuration"))
        print("[>] Assembly Path : {}".format(self.assembly_path if self.assembly_path else "(not set — will use default assembly)"))


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
        self.assembly_path = None


    ######################################################################
    # Ngen AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Ngen_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_ngen()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            assembly_path : str — full path to a .NET managed assembly to compile
                                  if absent, a common default assembly is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.assembly_path = kwargs.get("assembly_path", None)
        if self.assembly_path:
            print(f"[*] Setting assembly_path attribute : {self.assembly_path}")
        else:
            print("[*] No assembly_path provided — will compile default .NET assembly")

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
        ; <      Ngen Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Ngen_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Ngen_{}()

            ; Creates an Ngen Interaction via CMD

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
        Builds the ngen commands to type into the CMD window.
        Compiles the specified assembly (or a sensible default) to a native image.
        Optionally queries the native image cache with 'display'.
        """
        typing_text = '\n'

        # Determine the assembly to compile
        if self.assembly_path:
            target = self.assembly_path
        else:
            target = 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\System.Management.dll'

        ngen_exe = 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\ngen.exe'

        # Run ngen install to compile the assembly to a native image
        install_cmd = '{} install "{}"'.format(ngen_exe, target)
        typing_text += 'Send("' + self._escape_send(install_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Display the native image cache to confirm the install
        display_cmd = '{} display'.format(ngen_exe)
        typing_text += 'Send("' + self._escape_send(display_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_ngen(self):
        """
        Closes the Ngen AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
