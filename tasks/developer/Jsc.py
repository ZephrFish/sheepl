
# LOLBAS: Jsc.exe — Legitimate use: compiling JavaScript source files to .exe or .dll using the .NET JScript compiler
# DEVELOPER-ONLY: requires .NET Framework (v2.0 or v4.0) installed on the target system

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of jsc.exe (.NET JScript compiler) to
 compile a JavaScript source file into an executable or a library DLL.

 Accepts a js_file parameter (path to the .js source file) and an optional
 target_type parameter ('exe' or 'library'; defaults to 'exe').
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Jsc(BaseCMD):
    """
    # LOLBAS: Jsc.exe — Legitimate use: compiling JavaScript source files to .exe or .dll using the .NET JScript compiler
    # DEVELOPER-ONLY: requires .NET Framework (v2.0 or v4.0) installed on the target system

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Jsc, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Jsc'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > jsc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > jsc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the JavaScript source file to compile
        self.js_file = None
        # Output type: 'exe' (default) or 'library' (produces a DLL)
        self.target_type = 'exe'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Jsc Interaction.
        [!] DEVELOPER-ONLY: requires .NET Framework installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the JavaScript source file using 'js_file <path>'
        3: Optionally set the output type using 'target_type <exe|library>'
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
    #  Jsc Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Jsc interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Jsc_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_js_file(self, js_file):
        """
        Set the path to the JavaScript source file to compile.
        Example: js_file C:\\dev\\hello.js
        """
        if js_file:
            if self.taskstarted:
                self.js_file = js_file.strip()
                print(self.cl.green("[*] JavaScript file set to: {}".format(self.js_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Jsc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide the path to a .js file."))


    def do_target_type(self, target_type):
        """
        Set the compilation output type.
        Options: exe (default) or library (produces a DLL)
        Example: target_type library
        """
        if target_type:
            if self.taskstarted:
                target_type = target_type.strip().lower()
                if target_type in ('exe', 'library'):
                    self.target_type = target_type
                    print(self.cl.green("[*] Target type set to: {}".format(self.target_type)))
                else:
                    print(self.cl.red("[!] <ERROR> target_type must be 'exe' or 'library'."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Jsc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target type: exe or library."))


    def do_assigned(self, arg):
        """
        Get the current assigned Jsc configuration
        """
        print(self.cl.green("[?] Currently Assigned Jsc Configuration"))
        print("[>] JS File     : {}".format(self.js_file if self.js_file else "(not set)"))
        print("[>] Target Type : {}".format(self.target_type))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.js_file:
                print(self.cl.red("[!] <ERROR> You must set a JavaScript source file using 'js_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.js_file = None
        self.target_type = 'exe'


    ######################################################################
    # Jsc AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Jsc_' + current_counter, self.create_autoit_function())


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
            js_file     : str — path to the .js source file to compile

        Optional JSON keys:
            target_type : str — 'exe' (default) or 'library'
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.js_file = kwargs.get("js_file", None)
        if self.js_file:
            print(f"[*] Setting js_file attribute : {self.js_file}")
        else:
            print("[!] <ERROR> No js_file provided — this is required for Jsc.")

        self.target_type = kwargs.get("target_type", "exe").lower()
        print(f"[*] Setting target_type attribute : {self.target_type}")

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
        ; <      Jsc Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Jsc_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Jsc_{}()

            ; Creates a Jsc Interaction via CMD

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
        Builds the jsc.exe command to type into the CMD window.
        Compiles the given JavaScript file to an exe or library DLL.
        """
        typing_text = '\n'

        # Build the jsc command based on target type
        if self.target_type == 'library':
            jsc_cmd = 'jsc.exe /t:library {}'.format(self.js_file)
        else:
            jsc_cmd = 'jsc.exe {}'.format(self.js_file)

        typing_text += 'Send("' + self._escape_send(jsc_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Jsc AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
