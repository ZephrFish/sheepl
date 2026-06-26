
# LOLBAS: cdb.exe — Legitimate use: attaching to a process for debugging with Windows Debugging Tools
# DEVELOPER-ONLY: requires Windows Debugging Tools (Windows Kits) to be installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of cdb.exe (CDB Console Debugger) to
 attach to a running process by name and inspect it, then detach cleanly.

 Takes a process_name parameter (default: notepad.exe).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Cdb(BaseCMD):
    """
    # LOLBAS: cdb.exe — Legitimate use: attaching to a process for debugging with Windows Debugging Tools
    # DEVELOPER-ONLY: requires Windows Debugging Tools (Windows Kits) to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Cdb, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Cdb'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cdb >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cdb >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Process name to attach the debugger to
        self.process_name = 'notepad.exe'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Cdb Interaction.
            DEVELOPER-ONLY: requires Windows Debugging Tools (Windows Kits) installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the process to attach to using 'process_name <name>'
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
    #  Cdb Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Cdb interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Cdb_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_process_name(self, process_name):
        """
        Set the name of the process to attach the debugger to.
        Default is notepad.exe.
        Example: process_name notepad.exe
        """
        if process_name:
            if self.taskstarted:
                self.process_name = process_name.strip()
                print(self.cl.green("[*] Process name set to: {}".format(self.process_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cdb Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Cdb configuration
        """
        print(self.cl.green("[?] Currently Assigned Cdb Configuration"))
        print("[>] Process Name : {}".format(self.process_name))


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


    ######################################################################
    # Cdb AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Cdb_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_cdb()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            process_name : str — name of the process to attach cdb.exe to
                                 defaults to notepad.exe if absent
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.process_name = kwargs.get("process_name", "notepad.exe")
        print(f"[*] Setting process_name attribute : {self.process_name}")

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
        ; <      Cdb Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Cdb_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Cdb_{}()

            ; Creates a Cdb Interaction via CMD

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
        Builds the cdb.exe command to type into the CMD window.
        Attaches to the specified process with -pd (non-invasive attach),
        lists loaded modules, then detaches and exits.
        """
        typing_text = '\n'

        # Attach to the target process non-invasively, list modules, then detach
        cdb_cmd = 'cdb.exe -pd -pn {}'.format(self.process_name)
        typing_text += 'Send("' + self._escape_send(cdb_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Inside the cdb prompt: list loaded modules then quit
        typing_text += 'Send("' + self._escape_send('lm') + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += 'Send("' + self._escape_send('q') + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(1000, 3000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_cdb(self):
        """
        Closes the Cdb AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
