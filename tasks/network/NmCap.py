
# LOLBAS: nmcap.exe — Legitimate use: packet capture for network diagnostics using Microsoft Network Monitor 3.x
# DEVELOPER-ONLY: Requires Microsoft Network Monitor 3.x installation (not inbox)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrator use of nmcap.exe to capture network
 traffic on all adapters and save to a .cap file for diagnostics.

 Requires Microsoft Network Monitor 3.x to be installed.
 Takes an output_file parameter for the capture destination path and an
 optional duration in seconds for auto-termination.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class NmCap(BaseCMD):
    """
    # LOLBAS: nmcap.exe — Legitimate use: packet capture for network diagnostics using Microsoft Network Monitor 3.x
    # DEVELOPER-ONLY: Requires Microsoft Network Monitor 3.x installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(NmCap, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'NmCap'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > nmcap >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > nmcap >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Capture output file path (.cap)
        self.output_file = None
        # Optional duration in seconds for auto-termination (None = no auto-terminate)
        self.duration = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] NmCap Interaction.
        Requires Microsoft Network Monitor 3.x installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the capture output file using 'output_file <path>'
        3: Optionally set capture duration in seconds using 'duration <seconds>'
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
    #  NmCap Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new NmCap interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'NmCap_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_output_file(self, output_file):
        """
        Set the path for the capture output file (.cap format).
        Example: output_file C:\\Temp\\capture.cap
        """
        if output_file:
            if self.taskstarted:
                self.output_file = output_file.strip()
                print(self.cl.green("[*] Output file set to: {}".format(self.output_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new NmCap Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path (e.g. C:\\Temp\\capture.cap)."))


    def do_duration(self, duration):
        """
        Optionally set the capture duration in seconds for auto-termination.
        Example: duration 30
        If not set, the capture will run until manually stopped.
        """
        if duration:
            if self.taskstarted:
                try:
                    self.duration = int(duration.strip())
                    print(self.cl.green("[*] Duration set to: {} seconds".format(self.duration)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> Duration must be an integer number of seconds."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new NmCap Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a duration in seconds."))


    def do_assigned(self, arg):
        """
        Get the current assigned NmCap configuration
        """
        print(self.cl.green("[?] Currently Assigned NmCap Configuration"))
        print("[>] Output File : {}".format(self.output_file if self.output_file else "(not set)"))
        print("[>] Duration    : {}".format("{} seconds".format(self.duration) if self.duration else "(not set — manual stop)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.output_file:
                print(self.cl.red("[!] <ERROR> Please set an output file path using 'output_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.output_file = None
        self.duration = None


    ######################################################################
    # NmCap AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('NmCap_' + current_counter, self.create_autoit_function())


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
            output_file : str — path to the .cap output file (e.g. C:\\Temp\\capture.cap)

        Optional JSON keys:
            duration    : int — capture duration in seconds for auto-termination
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.output_file = kwargs.get("output_file", None)
        if self.output_file:
            print(f"[*] Setting output_file attribute : {self.output_file}")
        else:
            print("[!] No output_file provided — this is required for NmCap")

        self.duration = kwargs.get("duration", None)
        if self.duration:
            print(f"[*] Setting duration attribute : {self.duration} seconds")
        else:
            print("[*] No duration provided — capture will run until manually stopped")

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
        ; <      NmCap Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "NmCap_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func NmCap_{}()

            ; Creates a NmCap Interaction via CMD

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
        Builds the nmcap command to type into the CMD window.
        Captures traffic on all adapters, saves to the specified .cap file.
        If duration is set, adds /TerminateWhen /TimeAfter for auto-stop.
        """
        typing_text = '\n'

        # Build the nmcap command
        nmcap_cmd = 'nmcap.exe /network * /capture /file {}'.format(self.output_file)
        if self.duration:
            nmcap_cmd += ' /TerminateWhen /TimeAfter {} seconds'.format(self.duration)

        typing_text += 'Send("' + self._escape_send(nmcap_cmd) + '{ENTER}")\n'

        # Sleep for capture duration + buffer, or a fixed wait if no duration set
        if self.duration:
            wait_ms = (self.duration * 1000) + random.randint(2000, 5000)
        else:
            wait_ms = random.randint(2000, 5000)
        typing_text += 'sleep({})\n'.format(wait_ms)

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the NmCap AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
