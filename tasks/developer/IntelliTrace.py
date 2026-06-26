
# LOLBAS: IntelliTrace.exe — Legitimate use: collecting diagnostic trace files for Visual Studio debugging
# DEVELOPER-ONLY: Requires Visual Studio 2022 installation (Community, Professional, or Enterprise)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of IntelliTrace.exe to launch an application
 under diagnostic tracing using a collection plan, generating an .iTrace log file
 for post-mortem debugging in Visual Studio.

 Takes a target_exe parameter (the executable to trace) and an optional output_dir
 for the trace file; defaults to C:\\Users\\Public\\Logs if absent.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class IntelliTrace(BaseCMD):
    """
    # LOLBAS: IntelliTrace.exe — Legitimate use: collecting diagnostic trace files for Visual Studio debugging
    # DEVELOPER-ONLY: Requires Visual Studio 2022 installation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(IntelliTrace, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'IntelliTrace'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > intellitrace >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > intellitrace >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target executable to launch under IntelliTrace
        self.target_exe = None
        # Directory to write the .iTrace output file
        self.output_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] IntelliTrace Interaction.
            DEVELOPER-ONLY: Requires Visual Studio 2022.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the executable to trace using 'target_exe <path>'
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
    #  IntelliTrace Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new IntelliTrace interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'IntelliTrace_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_exe(self, target_exe):
        """
        Set the executable to launch and trace with IntelliTrace.
        Example: target_exe C:\\Windows\\System32\\notepad.exe
        """
        if target_exe:
            if self.taskstarted:
                self.target_exe = target_exe.strip()
                print(self.cl.green("[*] Target executable set to: {}".format(self.target_exe)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new IntelliTrace Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target executable path."))


    def do_output_dir(self, output_dir):
        """
        Optionally set the directory for the .iTrace output file.
        If not set, defaults to C:\\Users\\Public\\Logs.
        Example: output_dir C:\\Users\\Public\\Logs
        """
        if output_dir:
            if self.taskstarted:
                self.output_dir = output_dir.strip()
                print(self.cl.green("[*] Output directory set to: {}".format(self.output_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new IntelliTrace Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned IntelliTrace configuration
        """
        print(self.cl.green("[?] Currently Assigned IntelliTrace Configuration"))
        print("[>] Target Executable : {}".format(self.target_exe if self.target_exe else "(not set)"))
        print("[>] Output Directory  : {}".format(self.output_dir if self.output_dir else "(default: C:\\Users\\Public\\Logs)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_exe:
                self.target_exe = 'C:\\Windows\\System32\\notepad.exe'
                print(self.cl.yellow("[*] No target_exe set — defaulting to notepad.exe"))
            if not self.output_dir:
                self.output_dir = 'C:\\Users\\Public\\Logs'
                print(self.cl.yellow("[*] No output_dir set — defaulting to C:\\Users\\Public\\Logs"))
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_exe = None
        self.output_dir = None


    ######################################################################
    # IntelliTrace AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('IntelliTrace_' + current_counter, self.create_autoit_function())


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
            target_exe : str — full path to the executable to trace
                               defaults to C:\\Windows\\System32\\notepad.exe
            output_dir : str — directory for the .iTrace output file
                               defaults to C:\\Users\\Public\\Logs
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_exe = kwargs.get("target_exe", "C:\\Windows\\System32\\notepad.exe")
        self.output_dir = kwargs.get("output_dir", "C:\\Users\\Public\\Logs")
        print(f"[*] Setting target_exe attribute : {self.target_exe}")
        print(f"[*] Setting output_dir attribute : {self.output_dir}")

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
        ; <      IntelliTrace Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "IntelliTrace_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func IntelliTrace_{}()

            ; Creates an IntelliTrace Interaction via CMD

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
        Builds the IntelliTrace command to type into the CMD window.
        Launches the target executable under IntelliTrace with a collection plan,
        writing the .iTrace diagnostic log to the specified output directory.
        """
        typing_text = '\n'

        # Resolve the output directory
        out_dir = self.output_dir if self.output_dir else 'C:\\Users\\Public\\Logs'
        target = self.target_exe if self.target_exe else 'C:\\Windows\\System32\\notepad.exe'

        # Construct the IntelliTrace launch command using the full binary path
        # and the default collection plan bundled with Visual Studio 2022
        collection_plan = (
            '"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community'
            '\\Common7\\IDE\\CommonExtensions\\Microsoft\\IntelliTrace'
            '\\collection_plan.ASP.NET.default.xml"'
        )

        full_cmd = (
            '"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community'
            '\\Common7\\IDE\\CommonExtensions\\Microsoft\\IntelliTrace\\IntelliTrace.exe"'
            ' launch /cp:{} /f:"{}" "{}"'.format(collection_plan, out_dir, target)
        )

        typing_text += 'Send("' + self._escape_send(full_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the IntelliTrace AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
