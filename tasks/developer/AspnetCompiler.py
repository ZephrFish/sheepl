
# LOLBAS: aspnet_compiler.exe — Legitimate use: pre-compiling ASP.NET web applications to catch build errors
# DEVELOPER-ONLY: Requires .NET Framework 4.x installed (aspnet_compiler.exe lives under Framework/Framework64 paths)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of aspnet_compiler.exe to pre-compile
 an ASP.NET web application from a source directory to an output directory.
 This is standard practice to validate markup and code-behind files before
 deployment without needing a full Visual Studio build.

 Takes a source_path and output_path parameter; if absent uses safe defaults.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class AspnetCompiler(BaseCMD):
    """
    # LOLBAS: aspnet_compiler.exe — Legitimate use: pre-compiling ASP.NET web applications to catch build errors
    # DEVELOPER-ONLY: Requires .NET Framework 4.x installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(AspnetCompiler, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'AspnetCompiler'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > aspnet_compiler >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > aspnet_compiler >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Source directory containing the ASP.NET application to compile
        self.source_path = None
        # Output directory where compiled output will be written
        self.output_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] AspnetCompiler Interaction.
        [!] DEVELOPER-ONLY: Requires .NET Framework 4.x installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the ASP.NET source directory using 'source_path <path>'
        3: Set the compiled output directory using 'output_path <path>'
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
    #  AspnetCompiler Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new AspnetCompiler interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'AspnetCompiler_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source_path(self, source_path):
        """
        Set the source directory containing the ASP.NET web application to compile.
        Example: source_path C:\\inetpub\\wwwroot\\myapp
        """
        if source_path:
            if self.taskstarted:
                self.source_path = source_path.strip()
                print(self.cl.green("[*] Source path set to: {}".format(self.source_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AspnetCompiler Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a source path."))


    def do_output_path(self, output_path):
        """
        Set the output directory where compiled files will be written.
        Example: output_path C:\\inetpub\\wwwroot\\myapp_compiled
        """
        if output_path:
            if self.taskstarted:
                self.output_path = output_path.strip()
                print(self.cl.green("[*] Output path set to: {}".format(self.output_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AspnetCompiler Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output path."))


    def do_assigned(self, arg):
        """
        Get the current assigned AspnetCompiler configuration
        """
        print(self.cl.green("[?] Currently Assigned AspnetCompiler Configuration"))
        print("[>] Source Path : {}".format(self.source_path if self.source_path else "(not set — will use default sample path)"))
        print("[>] Output Path : {}".format(self.output_path if self.output_path else "(not set — will use default sample path)"))


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
        self.source_path = None
        self.output_path = None


    ######################################################################
    # AspnetCompiler AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('AspnetCompiler_' + current_counter, self.create_autoit_function())


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

        Optional JSON keys:
            source_path : str — path to the ASP.NET source directory to compile
            output_path : str — path where compiled output will be written
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source_path = kwargs.get("source_path", None)
        self.output_path = kwargs.get("output_path", None)

        if self.source_path:
            print(f"[*] Setting source_path attribute : {self.source_path}")
        else:
            print("[*] No source_path provided — will use default sample path")

        if self.output_path:
            print(f"[*] Setting output_path attribute : {self.output_path}")
        else:
            print("[*] No output_path provided — will use default sample path")

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
        ; <      AspnetCompiler Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "AspnetCompiler_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func AspnetCompiler_{}()

            ; Creates an AspnetCompiler Interaction via CMD

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
        Builds the aspnet_compiler commands to type into the CMD window.
        Uses supplied source_path and output_path, or safe defaults if absent.
        Compiles an ASP.NET web application to catch build-time errors before deployment.
        """
        typing_text = '\n'

        # Resolve paths — fall back to sensible developer defaults
        src = self.source_path if self.source_path else r'C:\inetpub\wwwroot\myapp'
        out = self.output_path if self.output_path else r'C:\inetpub\wwwroot\myapp_compiled'

        # Build the aspnet_compiler command:
        #   -v none       : virtual path (none for file-system-based compilation)
        #   -p <src>      : physical source path
        #   -f            : force overwrite of output directory
        #   <out>         : output directory
        #   -u            : allow the compiled output to be updated (updatable compilation)
        compile_cmd = (
            r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_compiler.exe'
            ' -v none -p {} -f {} -u'.format(src, out)
        )

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
        Closes the AspnetCompiler AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
