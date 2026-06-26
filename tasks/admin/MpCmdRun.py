
# LOLBAS: MpCmdRun.exe — Legitimate use: managing Windows Defender settings and running antivirus scans

# #######################################################################
#
#  Task : MpCmdRun Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of MpCmdRun.exe to manage Windows Defender,
 run quick or full antivirus scans, and update signature definitions.

 Takes optional parameters for scan type and signature update; defaults
 to running a quick scan.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MpCmdRun(BaseCMD):
    """
    # LOLBAS: MpCmdRun.exe — Legitimate use: managing Windows Defender settings and running antivirus scans

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MpCmdRun, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MpCmdRun'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mpcmdrun >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mpcmdrun >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Scan type: 'quick' (default), 'full', or 'custom'
        self.scan_type = None
        # Whether to run a signature update before scanning
        self.update_sigs = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MpCmdRun Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set scan type using 'scan_type <quick|full>'
        3: Optionally enable signature update using 'update_sigs'
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
    #  MpCmdRun Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MpCmdRun interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MpCmdRun_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_scan_type(self, scan_type):
        """
        Optionally set the scan type: quick or full.
        Defaults to quick if not set.
        Example: scan_type quick
        Example: scan_type full
        """
        if scan_type:
            if self.taskstarted:
                scan_type = scan_type.strip().lower()
                if scan_type in ('quick', 'full'):
                    self.scan_type = scan_type
                    print(self.cl.green("[*] Scan type set to: {}".format(self.scan_type)))
                else:
                    print(self.cl.red("[!] <ERROR> Scan type must be 'quick' or 'full'."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MpCmdRun Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a scan type (quick or full)."))


    def do_update_sigs(self, arg):
        """
        Enable Windows Defender signature update before the scan.
        Example: update_sigs
        """
        if self.taskstarted:
            self.update_sigs = True
            print(self.cl.green("[*] Signature update enabled."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new MpCmdRun Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned MpCmdRun configuration
        """
        print(self.cl.green("[?] Currently Assigned MpCmdRun Configuration"))
        print("[>] Scan Type     : {}".format(self.scan_type if self.scan_type else "quick (default)"))
        print("[>] Update Sigs   : {}".format(self.update_sigs))


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
        self.scan_type = None
        self.update_sigs = False


    ######################################################################
    # MpCmdRun AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MpCmdRun_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_mpcmdrun()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            scan_type   : str  — 'quick' or 'full' (default: 'quick')
            update_sigs : bool — whether to update signatures before scanning
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.scan_type = kwargs.get("scan_type", None)
        if self.scan_type:
            print(f"[*] Setting scan_type attribute : {self.scan_type}")
        else:
            print("[*] No scan_type provided — will run a quick scan")

        self.update_sigs = kwargs.get("update_sigs", False)
        if self.update_sigs:
            print("[*] Signature update enabled")

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
        ; <      MpCmdRun Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MpCmdRun_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MpCmdRun_{}()

            ; Creates a MpCmdRun Interaction via CMD

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
        Builds the MpCmdRun commands to type into the CMD window.
        Optionally updates signatures, then runs a quick or full scan.
        """
        typing_text = '\n'

        # Optionally update Windows Defender signatures first
        if self.update_sigs:
            update_cmd = 'MpCmdRun.exe -SignatureUpdate'
            typing_text += 'Send("' + self._escape_send(update_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(5000, 15000))

        # Determine scan flag: -2 for quick scan (default), -1 for full scan
        if self.scan_type and self.scan_type == 'full':
            scan_cmd = 'MpCmdRun.exe -Scan -ScanType 1'
        else:
            scan_cmd = 'MpCmdRun.exe -Scan -ScanType 2'

        typing_text += 'Send("' + self._escape_send(scan_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_mpcmdrun(self):
        """
        Closes the MpCmdRun AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
