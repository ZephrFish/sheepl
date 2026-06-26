
# LOLBAS: Shell32.dll — Legitimate use: launching Control Panel applets and shell operations via rundll32

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of shell32.dll via rundll32.exe.
 Demonstrates the Control_RunDLL export (used by Control Panel applets)
 and the ShellExec_RunDLL export (used to launch executables via the shell).

 The dll_export parameter selects which export to invoke:
   Control_RunDLL   — opens a .cpl or .dll Control Panel applet
   ShellExec_RunDLL — launches an executable via the Windows shell

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Shell32(BaseCMD):
    """
    # LOLBAS: Shell32.dll — Legitimate use: launching Control Panel applets and shell operations via rundll32

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Shell32, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Shell32'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > shell32 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > shell32 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # dll export to invoke: Control_RunDLL or ShellExec_RunDLL
        self.dll_export = 'Control_RunDLL'
        # argument passed to the export (e.g. appwiz.cpl or calc.exe)
        self.target = 'appwiz.cpl'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Shell32 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the export function using 'dll_export <Control_RunDLL|ShellExec_RunDLL>'
        3: Set the target argument using 'target <appwiz.cpl|calc.exe|...>'
        4: Complete the interaction using 'complete'
        ----------------------------------
        Defaults: Control_RunDLL with appwiz.cpl (Add/Remove Programs)
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Shell32 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Shell32 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Shell32_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_dll_export(self, dll_export):
        """
        Set the shell32.dll export function to invoke via rundll32.
        Accepted values: Control_RunDLL, ShellExec_RunDLL
        Example: dll_export Control_RunDLL
        """
        if dll_export:
            if self.taskstarted:
                valid = ['Control_RunDLL', 'ShellExec_RunDLL']
                if dll_export.strip() in valid:
                    self.dll_export = dll_export.strip()
                    print(self.cl.green("[*] dll_export set to: {}".format(self.dll_export)))
                else:
                    print(self.cl.red("[!] <ERROR> Valid exports are: {}".format(', '.join(valid))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Shell32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a dll_export value."))


    def do_target(self, target):
        """
        Set the target argument passed to the dll export function.
        For Control_RunDLL use a .cpl name, e.g. appwiz.cpl, desk.cpl, inetcpl.cpl
        For ShellExec_RunDLL use an executable name, e.g. calc.exe, notepad.exe
        Example: target appwiz.cpl
        """
        if target:
            if self.taskstarted:
                self.target = target.strip()
                print(self.cl.green("[*] Target set to: {}".format(self.target)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Shell32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target value."))


    def do_assigned(self, arg):
        """
        Get the current assigned Shell32 configuration
        """
        print(self.cl.green("[?] Currently Assigned Shell32 Configuration"))
        print("[>] DLL Export : {}".format(self.dll_export))
        print("[>] Target     : {}".format(self.target))


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
        self.dll_export = 'Control_RunDLL'
        self.target = 'appwiz.cpl'


    ######################################################################
    # Shell32 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Shell32_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_shell32()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            dll_export : str — shell32.dll export to call (Control_RunDLL or ShellExec_RunDLL)
                               defaults to Control_RunDLL
            target     : str — argument passed to the export (e.g. appwiz.cpl or calc.exe)
                               defaults to appwiz.cpl
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.dll_export = kwargs.get("dll_export", "Control_RunDLL")
        self.target = kwargs.get("target", "appwiz.cpl")
        print(f"[*] Setting dll_export attribute : {self.dll_export}")
        print(f"[*] Setting target attribute     : {self.target}")

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
        ; <      Shell32 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Shell32_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Shell32_{}()

            ; Creates a Shell32 Interaction via CMD

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
        Builds the rundll32 shell32.dll command to type into the CMD window.
        Uses the configured dll_export and target to form the command.
        """
        typing_text = '\n'

        rundll_cmd = 'rundll32.exe shell32.dll,{} {}'.format(self.dll_export, self.target)
        typing_text += 'Send("' + self._escape_send(rundll_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_shell32(self):
        """
        Closes the Shell32 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
