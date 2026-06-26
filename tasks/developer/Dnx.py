
# LOLBAS: dnx.exe — Legitimate use: executing a local C# console application project via the .NET Execution Environment
# DEVELOPER-ONLY: requires .NET Core / ASP.NET 5 SDK (dnx.exe ships with the DNX runtime, not a default Windows install)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of dnx.exe to execute a C# project
 stored in a local console application folder. The folder must contain
 a 'Program.cs' entry point and a 'Project.json' manifest.

 Takes a required project_folder parameter (absolute path to the C# project).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Dnx(BaseCMD):
    """
    # LOLBAS: dnx.exe — Legitimate use: executing a local C# console application project
    # DEVELOPER-ONLY: requires .NET Core / ASP.NET 5 SDK (dnx.exe ships with the DNX runtime)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Dnx, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Dnx'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dnx >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dnx >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Absolute path to the C# project folder (must contain Program.cs and Project.json)
        self.project_folder = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Dnx Interaction.
        [!] DEVELOPER-ONLY: requires .NET Core / ASP.NET 5 SDK.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the project folder path using 'project_folder <path>'
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
    #  Dnx Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Dnx interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Dnx_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_project_folder(self, project_folder):
        """
        Set the absolute path to the C# project folder to execute.
        The folder must contain Program.cs and Project.json.
        Example: project_folder C:\\Users\\dev\\consoleapp
        """
        if project_folder:
            if self.taskstarted:
                self.project_folder = project_folder.strip()
                print(self.cl.green("[*] Project folder set to: {}".format(self.project_folder)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dnx Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a project folder path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Dnx configuration
        """
        print(self.cl.green("[?] Currently Assigned Dnx Configuration"))
        print("[>] Project Folder : {}".format(self.project_folder if self.project_folder else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.project_folder:
                print(self.cl.red("[!] <ERROR> project_folder must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.project_folder = None


    ######################################################################
    # Dnx AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Dnx_' + current_counter, self.create_autoit_function())


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
            project_folder : str — absolute path to the C# project folder containing
                                   Program.cs and Project.json
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.project_folder = kwargs.get("project_folder", None)
        if self.project_folder:
            print(f"[*] Setting project_folder attribute : {self.project_folder}")
        else:
            print("[!] <ERROR> No project_folder provided — this is required for Dnx.")
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
        ; <      Dnx Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Dnx_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Dnx_{}()

            ; Creates a Dnx Interaction via CMD

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
        Builds the dnx command to type into the CMD window.
        Navigates to the project folder then executes it with dnx.exe.
        """
        typing_text = '\n'

        # Change directory to the project folder first
        cd_cmd = 'cd /d {}'.format(self.project_folder)
        typing_text += 'Send("' + self._escape_send(cd_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Execute the project with dnx.exe (no path — on PATH after SDK install)
        typing_text += 'Send("dnx .{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Dnx AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
