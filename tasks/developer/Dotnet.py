
# LOLBAS: dotnet.exe — Legitimate use: running .NET applications and F# interactive scripting
# DEVELOPER-ONLY: requires .NET SDK installed (C:\Program Files\dotnet\dotnet.exe)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of dotnet.exe to run compiled .NET DLL
 applications and optionally open an F# interactive (fsi) console session.

 Takes an optional dll_path parameter; if absent opens the F# interactive console.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Dotnet(BaseCMD):
    """
    # LOLBAS: dotnet.exe — Legitimate use: running .NET applications and F# interactive scripting
    # DEVELOPER-ONLY: requires .NET SDK installed (C:\\Program Files\\dotnet\\dotnet.exe)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Dotnet, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Dotnet'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dotnet >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dotnet >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional path to a .NET DLL to execute; if None, opens fsi console
        self.dll_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Dotnet Interaction.
        NOTE: Requires .NET SDK installed at C:\\Program Files\\dotnet\\dotnet.exe
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a .NET DLL path using 'dll_path <path>'
           (if not set, opens the F# interactive console instead)
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
    #  Dotnet Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Dotnet interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Dotnet_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_dll_path(self, dll_path):
        """
        Optionally set a path to a compiled .NET DLL to execute with dotnet.exe.
        If not set, the F# interactive console (dotnet fsi) will be opened instead.
        Example: dll_path C:\\Dev\\MyApp\\bin\\Release\\net6.0\\MyApp.dll
        """
        if dll_path:
            if self.taskstarted:
                self.dll_path = dll_path.strip()
                print(self.cl.green("[*] DLL path set to: {}".format(self.dll_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dotnet Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Dotnet configuration
        """
        print(self.cl.green("[?] Currently Assigned Dotnet Configuration"))
        print("[>] DLL Path : {}".format(self.dll_path if self.dll_path else "(not set — will open F# interactive console)"))


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
        self.dll_path = None


    ######################################################################
    # Dotnet AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Dotnet_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_dotnet()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            dll_path : str — path to a compiled .NET DLL to execute with dotnet.exe
                             if absent, opens the F# interactive console (dotnet fsi)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.dll_path = kwargs.get("dll_path", None)
        if self.dll_path:
            print(f"[*] Setting dll_path attribute : {self.dll_path}")
        else:
            print("[*] No dll_path provided — will open F# interactive console (dotnet fsi)")

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
        ; <      Dotnet Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Dotnet_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Dotnet_{}()

            ; Creates a Dotnet Interaction via CMD

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
        Builds the dotnet commands to type into the CMD window.
        If dll_path is set, executes the DLL via dotnet.exe.
        Otherwise, opens the F# interactive console (dotnet fsi) and exits it.
        """
        typing_text = '\n'

        if self.dll_path:
            # Run the specified .NET DLL application
            run_cmd = '"C:\\Program Files\\dotnet\\dotnet.exe" {}'.format(self.dll_path)
            typing_text += 'Send("' + self._escape_send(run_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        else:
            # Open F# interactive console session and exit cleanly
            fsi_cmd = '"C:\\Program Files\\dotnet\\dotnet.exe" fsi'
            typing_text += 'Send("' + self._escape_send(fsi_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
            # Type a simple F# expression then exit
            typing_text += 'Send("' + self._escape_send('printfn "Hello from F# interactive"') + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(1000, 3000))
            typing_text += 'Send("' + self._escape_send('#quit;;') + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(1000, 2000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_dotnet(self):
        """
        Closes the Dotnet AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
