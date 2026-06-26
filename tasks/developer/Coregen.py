
# LOLBAS: coregen.exe — Legitimate use: generating CoreCLR native images for .NET assemblies (Microsoft Silverlight)
# DEVELOPER-ONLY: requires Microsoft Silverlight to be installed; coregen.exe is bundled with Silverlight

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of coregen.exe (Microsoft CoreCLR Native Image Generator)
 to generate a native image for a .NET assembly name. coregen.exe is located within the
 Microsoft Silverlight installation directory and is signed by Microsoft.

 Takes an assembly_name parameter (required) which is passed to coregen.exe.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Coregen(BaseCMD):
    """
    # LOLBAS: coregen.exe — Legitimate use: generating CoreCLR native images for .NET assemblies
    # DEVELOPER-ONLY: requires Microsoft Silverlight installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Coregen, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Coregen'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > coregen >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > coregen >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Assembly name to generate a native image for
        self.assembly_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Coregen Interaction.
        [!] DEVELOPER-ONLY: Requires Microsoft Silverlight installation.
        [!] coregen.exe — Microsoft CoreCLR Native Image Generator.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the assembly name using 'assembly_name <name>'
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
    #  Coregen Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Coregen interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Coregen_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assembly_name(self, assembly_name):
        """
        Set the .NET assembly name to pass to coregen.exe for native image generation.
        Example: assembly_name mscorlib
        """
        if assembly_name:
            if self.taskstarted:
                self.assembly_name = assembly_name.strip()
                print(self.cl.green("[*] Assembly name set to: {}".format(self.assembly_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Coregen Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an assembly name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Coregen configuration
        """
        print(self.cl.green("[?] Currently Assigned Coregen Configuration"))
        print("[>] Assembly Name : {}".format(self.assembly_name if self.assembly_name else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.assembly_name:
                print(self.cl.red("[!] <ERROR> assembly_name must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.assembly_name = None


    ######################################################################
    # Coregen AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Coregen_' + current_counter, self.create_autoit_function())


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
            assembly_name : str — name of the .NET assembly to pass to coregen.exe
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.assembly_name = kwargs.get("assembly_name", None)
        if self.assembly_name:
            print(f"[*] Setting assembly_name attribute : {self.assembly_name}")
        else:
            print("[!] <ERROR> assembly_name is required for Coregen task.")
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
        ; <      Coregen Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Coregen_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Coregen_{}()

            ; Creates a Coregen Interaction via CMD

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
        Builds the coregen.exe command to type into the CMD window.
        Runs coregen.exe with the specified assembly name to generate a native image.
        """
        typing_text = '\n'

        # Navigate to the Silverlight directory and run coregen for the assembly
        silverlight_dir = r'C:\Program Files (x86)\Microsoft Silverlight\5.1.50918.0'
        cd_cmd = 'cd /d "{}"'.format(silverlight_dir)
        typing_text += 'Send("' + self._escape_send(cd_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        coregen_cmd = 'coregen.exe {}'.format(self.assembly_name)
        typing_text += 'Send("' + self._escape_send(coregen_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Coregen AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
