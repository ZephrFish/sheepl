
# LOLBAS: adplus.exe — Legitimate use: debugging tool for process memory dumps and crash analysis
# DEVELOPER-ONLY: Requires Windows Debugging Tools (Windows Kits SDK) to be installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of adplus.exe to create a memory dump
 of a running process for offline crash analysis and debugging.

 Takes an optional process_name parameter (default: notepad.exe) and an
 output_folder parameter (default: C:\\Dumps) for the dump output directory.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Adplus(BaseCMD):
    """
    # LOLBAS: adplus.exe — Legitimate use: creating process memory dumps via Windows Debugging Tools
    # DEVELOPER-ONLY: Requires Windows Kits SDK (Debugging Tools for Windows) to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Adplus, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Adplus'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > adplus >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > adplus >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional parameters for the adplus hang dump command
        self.process_name = 'notepad.exe'
        self.output_folder = 'C:\\Dumps'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Adplus Interaction.
        [!] DEVELOPER-ONLY: Requires Windows Debugging Tools (Windows Kits SDK).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the target process using 'process_name <name>'
        3: Optionally set the output folder using 'output_folder <path>'
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
    #  Adplus Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Adplus interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Adplus_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_process_name(self, process_name):
        """
        Set the name of the process to capture a hang dump from.
        Defaults to notepad.exe if not set.
        Example: process_name notepad.exe
        """
        if process_name:
            if self.taskstarted:
                self.process_name = process_name.strip()
                print(self.cl.green("[*] Process name set to: {}".format(self.process_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Adplus Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process name."))


    def do_output_folder(self, output_folder):
        """
        Set the output folder where the memory dump will be written.
        Defaults to C:\\Dumps if not set.
        Example: output_folder C:\\DebugOutput
        """
        if output_folder:
            if self.taskstarted:
                self.output_folder = output_folder.strip()
                print(self.cl.green("[*] Output folder set to: {}".format(self.output_folder)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Adplus Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output folder path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Adplus configuration
        """
        print(self.cl.green("[?] Currently Assigned Adplus Configuration"))
        print("[>] Process Name  : {}".format(self.process_name))
        print("[>] Output Folder : {}".format(self.output_folder))


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
        self.process_name = 'notepad.exe'
        self.output_folder = 'C:\\Dumps'


    ######################################################################
    # Adplus AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Adplus_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_adplus()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            process_name  : str — name of the running process to dump (default: notepad.exe)
            output_folder : str — path to write the dump output (default: C:\\Dumps)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.process_name = kwargs.get("process_name", "notepad.exe")
        self.output_folder = kwargs.get("output_folder", "C:\\Dumps")

        print(f"[*] Setting process_name attribute : {self.process_name}")
        print(f"[*] Setting output_folder attribute : {self.output_folder}")

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
        ; <      Adplus Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Adplus_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Adplus_{}()

            ; Creates an Adplus Interaction via CMD

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
        Builds the adplus hang dump command to type into the CMD window.
        Uses adplus -hang to capture a memory dump of the specified process
        and write it to the configured output folder.
        """
        typing_text = '\n'

        # Run adplus -hang dump against the target process
        dump_cmd = 'adplus.exe -hang -pn {} -o {} -quiet'.format(
            self.process_name, self.output_folder
        )
        typing_text += 'Send("' + self._escape_send(dump_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_adplus(self):
        """
        Closes the Adplus AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
