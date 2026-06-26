
# #######################################################################
#
#  Task : Msbuild Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of msbuild.exe for building .NET
 projects, solutions, and targets — as performed by developers, CI/CD
 agents, and release engineers.

"""

# LOLBAS: msbuild.exe — Legitimate use: .NET project compilation (requires Visual Studio or Build Tools)

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Msbuild(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: msbuild.exe — Legitimate use: .NET project compilation (requires Visual Studio or Build Tools)
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Msbuild, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Msbuild'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msbuild >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msbuild >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.project = ''
        self.configuration = 'Release'
        self.target = 'Build'
        self.verbosity = 'minimal'

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Msbuild Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the project file using 'project'
        3: Optionally set configuration using 'configuration' (default: Release)
        4: Optionally set the build target using 'target' (default: Build)
        5: Optionally set verbosity using 'verbosity' (default: minimal)
        6: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Msbuild Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Msbuild interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Msbuild_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_project(self, arg):
        """
        Set the path to the .csproj, .sln, or .targets file to build.
        Example: project C:\\src\\MyApp\\MyApp.sln
        """
        if self.taskstarted:
            if arg:
                self.project = arg
                print(self.cl.green("[*] Project set to: {}".format(self.project)))
            else:
                print(self.cl.red("[!] <ERROR> You must supply a project path."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msbuild Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_configuration(self, arg):
        """
        Set the build configuration: Debug or Release (default: Release).
        Example: configuration Debug
        """
        valid = ['Debug', 'Release']
        if self.taskstarted:
            if arg:
                if arg in valid:
                    self.configuration = arg
                    print(self.cl.green("[*] Configuration set to: {}".format(self.configuration)))
                else:
                    print(self.cl.red("[!] Invalid configuration. Choose from: {}".format(', '.join(valid))))
            else:
                print(self.cl.green("[*] Using default configuration: {}".format(self.configuration)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msbuild Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_target(self, arg):
        """
        Set the build target (default: Build).
        Common targets: Build, Clean, Rebuild
        Example: target Rebuild
        """
        if self.taskstarted:
            if arg:
                self.target = arg
                print(self.cl.green("[*] Target set to: {}".format(self.target)))
            else:
                print(self.cl.green("[*] Using default target: {}".format(self.target)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msbuild Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_verbosity(self, arg):
        """
        Set the verbosity level: minimal, normal, or detailed (default: minimal).
        Example: verbosity normal
        """
        valid = ['minimal', 'normal', 'detailed']
        if self.taskstarted:
            if arg:
                if arg.lower() in valid:
                    self.verbosity = arg.lower()
                    print(self.cl.green("[*] Verbosity set to: {}".format(self.verbosity)))
                else:
                    print(self.cl.red("[!] Invalid verbosity. Choose from: {}".format(', '.join(valid))))
            else:
                print(self.cl.green("[*] Using default verbosity: {}".format(self.verbosity)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msbuild Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current Msbuild task settings
        """
        print(self.cl.green("[?] Currently Assigned Msbuild Settings"))
        print("[>] Project       : {}".format(self.project))
        print("[>] Configuration : {}".format(self.configuration))
        print("[>] Target        : {}".format(self.target))
        print("[>] Verbosity     : {}".format(self.verbosity))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.project:
                self.create_autoIT_block()
            else:
                print("{} No project file has been set".format(self.cl.red("[!]")))
                print("{} Set a project path using 'project <path>'".format(self.cl.red("[-]")))
                return None

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific variables for next interaction
        self.project = ''
        self.configuration = 'Release'
        self.target = 'Build'
        self.verbosity = 'minimal'


    ######################################################################
    # Msbuild AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Msbuild_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_msbuild()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads project, configuration, target, and verbosity from kwargs.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.project = kwargs.get("project", '')
        print(f"[*] Setting the project attribute : {self.project}")

        self.configuration = kwargs.get("configuration", 'Release')
        print(f"[*] Setting the configuration attribute : {self.configuration}")

        self.target = kwargs.get("target", 'Build')
        print(f"[*] Setting the target attribute : {self.target}")

        self.verbosity = kwargs.get("verbosity", 'minimal')
        print(f"[*] Setting the verbosity attribute : {self.verbosity}")

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      Msbuild Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Msbuild_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for the msbuild command
        """

        _open_commandshell = """

        Func Msbuild_{}()

            ; Creates an Msbuild Interaction via CMD
            ; msbuild.exe path: C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\MSBuild\\Current\\Bin\\MSBuild.exe

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
        Builds the msbuild command:
          msbuild <project> /t:<target> /p:Configuration=<configuration> /v:<verbosity>
        Waits for the build to complete before exiting.
        """
        typing_text = '\n'

        escaped_project = self._escape_send(self.project)
        escaped_target = self._escape_send(self.target)
        escaped_configuration = self._escape_send(self.configuration)
        escaped_verbosity = self._escape_send(self.verbosity)

        msbuild_cmd = 'msbuild {} /t:{} /p:Configuration={} /v:{}'.format(
            escaped_project,
            escaped_target,
            escaped_configuration,
            escaped_verbosity
        )

        typing_text += 'Send("{}{}")\n'.format(msbuild_cmd, '{ENTER}')
        # Wait for the build to complete — builds can take significant time
        typing_text += '; Wait for msbuild to complete\n'
        typing_text += 'sleep({})\n'.format(random.randint(15000, 60000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_msbuild(self):
        """
        Closes the Msbuild function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
