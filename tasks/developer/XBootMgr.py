
# LOLBAS: xbootmgr.exe — Legitimate use: capturing Windows boot performance traces with the Windows Performance Toolkit
# DEVELOPER-ONLY: requires Windows Performance Toolkit (WPT) from the Windows ADK / Windows SDK install

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer/performance-engineer use of xbootmgr.exe
 to capture boot and standby performance traces using the Windows
 Performance Toolkit (WPT).

 Supports trace type selection (boot, hibernate, standby, shutdown,
 rebootCycle) and an optional output directory for the trace files.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class XBootMgr(BaseCMD):
    """
    # LOLBAS: xbootmgr.exe — Legitimate use: capturing Windows boot performance traces with the Windows Performance Toolkit
    # DEVELOPER-ONLY: requires Windows Performance Toolkit (WPT) from the Windows ADK / Windows SDK install

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(XBootMgr, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'XBootMgr'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > xbootmgr >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > xbootmgr >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Trace type: boot, hibernate, standby, shutdown, rebootCycle
        self.trace_type = 'boot'

        # Optional output directory for trace files
        self.output_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] XBootMgr Interaction.
        [!] DEVELOPER-ONLY: requires Windows Performance Toolkit (WPT).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set trace type using 'trace_type <boot|hibernate|standby|shutdown|rebootCycle>'
        3: Optionally set an output directory using 'output_dir <path>'
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
    #  XBootMgr Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new XBootMgr interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'XBootMgr_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_trace_type(self, trace_type):
        """
        Set the trace type for xbootmgr.
        Valid values: boot, hibernate, standby, shutdown, rebootCycle
        Example: trace_type boot
        """
        valid_types = ['boot', 'hibernate', 'standby', 'shutdown', 'rebootCycle']
        if trace_type:
            if self.taskstarted:
                trace_type = trace_type.strip()
                if trace_type in valid_types:
                    self.trace_type = trace_type
                    print(self.cl.green("[*] Trace type set to: {}".format(self.trace_type)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid trace type. Valid values: {}".format(', '.join(valid_types))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new XBootMgr Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a trace type."))


    def do_output_dir(self, output_dir):
        """
        Optionally set the output directory for trace files.
        Example: output_dir C:\\PerfTraces
        """
        if output_dir:
            if self.taskstarted:
                self.output_dir = output_dir.strip()
                print(self.cl.green("[*] Output directory set to: {}".format(self.output_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new XBootMgr Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned XBootMgr configuration
        """
        print(self.cl.green("[?] Currently Assigned XBootMgr Configuration"))
        print("[>] Trace Type  : {}".format(self.trace_type))
        print("[>] Output Dir  : {}".format(self.output_dir if self.output_dir else "(not set — default location)"))


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
        self.trace_type = 'boot'
        self.output_dir = None


    ######################################################################
    # XBootMgr AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('XBootMgr_' + current_counter, self.create_autoit_function())


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

        Optional JSON keys:
            trace_type : str — one of boot, hibernate, standby, shutdown, rebootCycle
                               defaults to 'boot' if absent
            output_dir : str — path to write trace output files
                               if absent, xbootmgr uses its default location
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.trace_type = kwargs.get("trace_type", "boot")
        print(f"[*] Setting trace_type attribute : {self.trace_type}")

        self.output_dir = kwargs.get("output_dir", None)
        if self.output_dir:
            print(f"[*] Setting output_dir attribute : {self.output_dir}")
        else:
            print("[*] No output_dir provided — xbootmgr will use its default location")

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
        ; <      XBootMgr Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "XBootMgr_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func XBootMgr_{}()

            ; Creates an XBootMgr Interaction via CMD

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
        Builds the xbootmgr command to type into the CMD window.
        Runs a performance trace using the configured trace type.
        Optionally specifies an output directory via -resultPath.
        """
        typing_text = '\n'

        # Build the xbootmgr command for a legitimate performance trace
        xbootmgr_cmd = 'xbootmgr.exe -trace {}'.format(self.trace_type)
        if self.output_dir:
            xbootmgr_cmd += ' -resultPath {}'.format(self.output_dir)

        typing_text += 'Send("' + self._escape_send(xbootmgr_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the XBootMgr AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
