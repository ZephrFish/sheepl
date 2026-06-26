
# LOLBAS: rasautou.exe — Legitimate use: loading a custom dialer DLL via the Windows Remote Access dialer
# NOTE: The -d and -p options are only available on Windows Vista, 7, 8, and 8.1. They were removed in Windows 10.

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates use of rasautou.exe to load a custom Remote Access dialer DLL
 and invoke a named export function, as supported on Windows Vista through 8.1.

 Requires a DLL path (-d) and an export function name (-p).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Rasautou(BaseCMD):
    """
    # LOLBAS: rasautou.exe — Legitimate use: loading a custom dialer DLL via the Windows Remote Access dialer

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    NOTE: The -d and -p flags were removed in Windows 10. This task targets Vista/7/8/8.1 only.
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Rasautou, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Rasautou'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > rasautou >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > rasautou >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # DLL path to load and export function name to invoke
        self.dll_path = None
        self.export_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Rasautou Interaction.
        NOTE: -d and -p options only available on Windows Vista, 7, 8, and 8.1.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the DLL path using 'dll_path <path>'
        3: Set the export function name using 'export_name <name>'
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
    #  Rasautou Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Rasautou interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Rasautou_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_dll_path(self, dll_path):
        """
        Set the path to the DLL to load via rasautou -d.
        Example: dll_path C:\\Users\\user\\dialer.dll
        """
        if dll_path:
            if self.taskstarted:
                self.dll_path = dll_path.strip()
                print(self.cl.green("[*] DLL path set to: {}".format(self.dll_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rasautou Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL path."))


    def do_export_name(self, export_name):
        """
        Set the name of the export function to invoke via rasautou -p.
        Example: export_name ConnectDLL
        """
        if export_name:
            if self.taskstarted:
                self.export_name = export_name.strip()
                print(self.cl.green("[*] Export name set to: {}".format(self.export_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Rasautou Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an export function name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Rasautou configuration
        """
        print(self.cl.green("[?] Currently Assigned Rasautou Configuration"))
        print("[>] DLL Path    : {}".format(self.dll_path if self.dll_path else "(not set)"))
        print("[>] Export Name : {}".format(self.export_name if self.export_name else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.dll_path:
                print(self.cl.red("[!] <ERROR> dll_path is required. Set it with 'dll_path <path>'."))
                return
            if not self.export_name:
                print(self.cl.red("[!] <ERROR> export_name is required. Set it with 'export_name <name>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.dll_path = None
        self.export_name = None


    ######################################################################
    # Rasautou AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Rasautou_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_rasautou()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            dll_path    : str — path to the DLL to load with rasautou -d
            export_name : str — name of the export function to call with rasautou -p
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.dll_path = kwargs.get("dll_path", None)
        self.export_name = kwargs.get("export_name", None)

        if self.dll_path:
            print(f"[*] Setting dll_path attribute : {self.dll_path}")
        else:
            print("[!] <ERROR> dll_path is required for Rasautou task.")

        if self.export_name:
            print(f"[*] Setting export_name attribute : {self.export_name}")
        else:
            print("[!] <ERROR> export_name is required for Rasautou task.")

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
        ; <      Rasautou Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Rasautou_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Rasautou_{}()

            ; Creates a Rasautou Interaction via CMD

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
        Builds the rasautou command to type into the CMD window.
        Loads the specified DLL and invokes the named export function.
        """
        typing_text = '\n'

        # Build the rasautou command: -a a -e e are required positional stubs
        rasautou_cmd = 'rasautou -d {} -p {} -a a -e e'.format(self.dll_path, self.export_name)
        typing_text += 'Send("' + self._escape_send(rasautou_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_rasautou(self):
        """
        Closes the Rasautou AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
