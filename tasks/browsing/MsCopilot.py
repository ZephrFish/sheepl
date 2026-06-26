# LOLBAS: mscopilot.exe — Legitimate use: launching Microsoft Copilot AI assistant app

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user interaction with mscopilot.exe,
 the Microsoft Copilot desktop application bundled with Windows 11.

 Launches the Copilot app via CMD using the --no-startup-window flag
 to open the application without an initial splash screen, then closes it.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsCopilot(BaseCMD):
    """
    # LOLBAS: mscopilot.exe — Legitimate use: launching Microsoft Copilot AI assistant app

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsCopilot, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsCopilot'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mscopilot >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mscopilot >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional flag: disable GPU sandbox (useful in virtualised environments)
        self.no_gpu_sandbox = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsCopilot Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally disable GPU sandbox using 'no_gpu_sandbox'
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
    #  MsCopilot Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsCopilot interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsCopilot_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_no_gpu_sandbox(self, arg):
        """
        Enable the --disable-gpu-sandbox flag when launching mscopilot.exe.
        Useful in virtualised or sandboxed lab environments.
        Example: no_gpu_sandbox
        """
        if self.taskstarted:
            self.no_gpu_sandbox = True
            print(self.cl.green("[*] GPU sandbox will be disabled for mscopilot.exe launch."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new MsCopilot Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsCopilot configuration
        """
        print(self.cl.green("[?] Currently Assigned MsCopilot Configuration"))
        print("[>] No GPU Sandbox : {}".format(self.no_gpu_sandbox))


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
        self.no_gpu_sandbox = False


    ######################################################################
    # MsCopilot AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsCopilot_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_mscopilot()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            no_gpu_sandbox : bool — if True, adds --disable-gpu-sandbox to the launch command
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.no_gpu_sandbox = kwargs.get("no_gpu_sandbox", False)
        if self.no_gpu_sandbox:
            print("[*] Setting no_gpu_sandbox attribute : True")
        else:
            print("[*] no_gpu_sandbox not set — launching without --disable-gpu-sandbox")

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
        ; <      MsCopilot Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsCopilot_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsCopilot_{}()

            ; Creates a MsCopilot Interaction via CMD

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
        Builds the mscopilot.exe command to type into the CMD window.
        Launches Copilot with --no-startup-window; optionally adds --disable-gpu-sandbox.
        Kills the process after a short dwell time to simulate a user closing the app.
        """
        typing_text = '\n'

        # Build the launch command
        launch_cmd = '"C:\\Program Files (x86)\\Microsoft\\Copilot\\Application\\mscopilot.exe" --no-startup-window'
        if self.no_gpu_sandbox:
            launch_cmd += ' --disable-gpu-sandbox'

        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(4000, 8000))

        # Kill the Copilot process to clean up (mirrors real-world admin behaviour)
        kill_cmd = 'taskkill /f /im mscopilot.exe'
        typing_text += 'Send("' + self._escape_send(kill_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_mscopilot(self):
        """
        Closes the MsCopilot AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
