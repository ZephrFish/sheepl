
# LOLBAS: rundll32.exe — Legitimate use: loading and executing functions from DLL files
# #######################################################################
#
#  Task : Rundll32 Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of rundll32.exe to invoke exported functions
 from system DLLs (e.g. PrintUIEntry for printer management, or
 Control_RunDLL for Control Panel applets).

 Takes a dll_name and entry_point parameter; optionally accepts dll_args
 for arguments passed after the entry point.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Rundll32(BaseCMD):
    """
    # LOLBAS: rundll32.exe — Legitimate use: loading and executing functions from DLL files

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Rundll32, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Rundll32'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > rundll32 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > rundll32 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # DLL name (just the filename, e.g. printui.dll) — no full path needed for System32 DLLs
        self.dll_name = None
        # Exported entry point to call
        self.entry_point = None
        # Optional arguments passed after the entry point
        self.dll_args = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Rundll32 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the DLL filename using 'dll_name <name>'
           e.g. dll_name printui.dll
        3: Set the entry point using 'entry_point <function>'
           e.g. entry_point PrintUIEntry
        4: Optionally pass arguments using 'dll_args <args>'
           e.g. dll_args /il
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
    #  Rundll32 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Rundll32 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Rundll32_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_dll_name(self, dll_name):
        """
        Set the DLL filename to load (just the filename, not full path).
        System32 DLLs do not need a path prefix.
        Example: dll_name printui.dll
        """
        if dll_name:
            if self.taskstarted:
                self.dll_name = dll_name.strip()
                print(self.cl.green("[*] DLL name set to: {}".format(self.dll_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rundll32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL filename."))


    def do_entry_point(self, entry_point):
        """
        Set the exported entry point function to call within the DLL.
        Example: entry_point PrintUIEntry
        """
        if entry_point:
            if self.taskstarted:
                self.entry_point = entry_point.strip()
                print(self.cl.green("[*] Entry point set to: {}".format(self.entry_point)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rundll32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an entry point function name."))


    def do_dll_args(self, dll_args):
        """
        Optionally set arguments to pass after the entry point.
        Example: dll_args /il
        """
        if dll_args:
            if self.taskstarted:
                self.dll_args = dll_args.strip()
                print(self.cl.green("[*] DLL args set to: {}".format(self.dll_args)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rundll32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide arguments for the DLL entry point."))


    def do_assigned(self, arg):
        """
        Get the current assigned Rundll32 configuration
        """
        print(self.cl.green("[?] Currently Assigned Rundll32 Configuration"))
        print("[>] DLL Name    : {}".format(self.dll_name if self.dll_name else "(not set)"))
        print("[>] Entry Point : {}".format(self.entry_point if self.entry_point else "(not set)"))
        print("[>] DLL Args    : {}".format(self.dll_args if self.dll_args else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.dll_name:
                self.dll_name = 'printui.dll'
                print(self.cl.yellow("[*] No DLL name set — defaulting to printui.dll"))
            if not self.entry_point:
                self.entry_point = 'PrintUIEntry'
                print(self.cl.yellow("[*] No entry point set — defaulting to PrintUIEntry"))
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.dll_name = None
        self.entry_point = None
        self.dll_args = None


    ######################################################################
    # Rundll32 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Rundll32_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_rundll32()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            dll_name    : str — DLL filename (e.g. printui.dll)
            entry_point : str — exported function name (e.g. PrintUIEntry)

        Optional JSON keys:
            dll_args    : str — arguments to pass after the entry point
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.dll_name = kwargs.get("dll_name", "printui.dll")
        self.entry_point = kwargs.get("entry_point", "PrintUIEntry")
        self.dll_args = kwargs.get("dll_args", None)

        print(f"[*] Setting dll_name attribute    : {self.dll_name}")
        print(f"[*] Setting entry_point attribute : {self.entry_point}")
        if self.dll_args:
            print(f"[*] Setting dll_args attribute    : {self.dll_args}")
        else:
            print("[*] No dll_args provided")

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
        ; <      Rundll32 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Rundll32_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Rundll32_{}()

            ; Creates a Rundll32 Interaction via CMD

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
        Builds the rundll32 command to type into the CMD window.
        Constructs: rundll32.exe <dll_name>,<entry_point> [dll_args]
        """
        typing_text = '\n'

        # Build the rundll32 command
        if self.dll_args:
            cmd_str = 'rundll32.exe {},{} {}'.format(self.dll_name, self.entry_point, self.dll_args)
        else:
            cmd_str = 'rundll32.exe {},{}'.format(self.dll_name, self.entry_point)

        typing_text += 'Send("' + self._escape_send(cmd_str) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_rundll32(self):
        """
        Closes the Rundll32 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
