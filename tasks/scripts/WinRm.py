
# LOLBAS: winrm.vbs — Legitimate use: querying WMI process and system information via WinRM
# #######################################################################
#
#  Task : WinRm Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of winrm.vbs (cscript) to query WMI
 class information via Windows Remote Management (WinRM).

 Runs: cscript //nologo C:\\Windows\\System32\\winrm.vbs get wmicimv2/Win32_Process?Handle=<pid> -format:pretty

 Takes an optional process_handle parameter (PID); defaults to 4 (System).
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WinRm(BaseCMD):
    """
    # LOLBAS: winrm.vbs — Legitimate use: querying WMI process and system information via WinRM

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WinRm, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WinRm'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > winrm >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > winrm >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional process handle (PID) to query; defaults to 4 (System)
        self.process_handle = '4'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] WinRm Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a process handle (PID) using 'process_handle <pid>'
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
    #  WinRm Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WinRm interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WinRm_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_process_handle(self, process_handle):
        """
        Optionally set the WMI process handle (PID) to query.
        If not set, defaults to 4 (the System process).
        Example: process_handle 1234
        """
        if process_handle:
            if self.taskstarted:
                self.process_handle = process_handle.strip()
                print(self.cl.green("[*] Process handle set to: {}".format(self.process_handle)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new WinRm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a process handle (PID)."))


    def do_assigned(self, arg):
        """
        Get the current assigned WinRm configuration
        """
        print(self.cl.green("[?] Currently Assigned WinRm Configuration"))
        print("[>] Process Handle : {}".format(self.process_handle))


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
        self.process_handle = '4'


    ######################################################################
    # WinRm AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WinRm_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_winrm()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            process_handle : str — WMI process handle (PID) to query
                                   if absent, defaults to 4 (System)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.process_handle = kwargs.get("process_handle", "4")
        print(f"[*] Setting process_handle attribute : {self.process_handle}")

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
        ; <      WinRm Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "WinRm_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func WinRm_{}()

            ; Creates a WinRm Interaction via CMD

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
        Builds the winrm.vbs cscript command to type into the CMD window.
        Queries a WMI Win32_Process instance by handle (PID) via WinRM.
        """
        typing_text = '\n'

        # Query Win32_Process via winrm.vbs using cscript
        winrm_cmd = 'cscript //nologo C:\\Windows\\System32\\winrm.vbs get wmicimv2/Win32_Process?Handle={} -format:pretty'.format(self.process_handle)
        typing_text += 'Send("' + self._escape_send(winrm_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_winrm(self):
        """
        Closes the WinRm AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
