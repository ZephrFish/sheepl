
# LOLBAS: mscopilot_proxy.exe — Legitimate use: proxy launcher component for Microsoft Copilot application

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of mscopilot_proxy.exe, the GPU/network proxy
 launcher bundled with the Microsoft Copilot desktop application on Windows 11.

 Launches the Copilot proxy with standard flags that suppress the startup
 window and disable the GPU sandbox, which reflects normal Copilot operation.

 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MscopilotProxy(BaseCMD):
    """
    # LOLBAS: mscopilot_proxy.exe — Legitimate use: proxy launcher component for Microsoft Copilot application

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MscopilotProxy, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MscopilotProxy'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mscopilot_proxy >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mscopilot_proxy >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional flags controlling proxy launch behaviour
        self.no_startup_window = True
        self.disable_gpu_sandbox = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MscopilotProxy Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally toggle flags using 'disable_gpu_sandbox'
        3: Review current settings with 'assigned'
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
    #  MscopilotProxy Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MscopilotProxy interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MscopilotProxy_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_disable_gpu_sandbox(self, arg):
        """
        Toggle whether --disable-gpu-sandbox is passed to mscopilot_proxy.exe.
        Default: off (flag not passed).
        Example: disable_gpu_sandbox
        """
        if self.taskstarted:
            self.disable_gpu_sandbox = not self.disable_gpu_sandbox
            state = "enabled" if self.disable_gpu_sandbox else "disabled"
            print(self.cl.green("[*] --disable-gpu-sandbox flag: {}".format(state)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new MscopilotProxy Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned MscopilotProxy configuration
        """
        print(self.cl.green("[?] Currently Assigned MscopilotProxy Configuration"))
        print("[>] --no-startup-window : {}".format(self.no_startup_window))
        print("[>] --disable-gpu-sandbox : {}".format(self.disable_gpu_sandbox))


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
        self.no_startup_window = True
        self.disable_gpu_sandbox = False


    ######################################################################
    # MscopilotProxy AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MscopilotProxy_' + current_counter, self.create_autoit_function())


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
            disable_gpu_sandbox : bool — if True, passes --disable-gpu-sandbox flag
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.disable_gpu_sandbox = kwargs.get("disable_gpu_sandbox", False)
        print(f"[*] Setting disable_gpu_sandbox attribute : {self.disable_gpu_sandbox}")

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
        ; <      MscopilotProxy Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MscopilotProxy_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MscopilotProxy_{}()

            ; Creates a MscopilotProxy Interaction via CMD

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
        Builds the mscopilot_proxy.exe command to type into the CMD window.
        Launches the Copilot proxy with --no-startup-window and optionally
        --disable-gpu-sandbox, reflecting normal Copilot desktop operation.
        """
        typing_text = '\n'

        copilot_path = r'"C:\Program Files (x86)\Microsoft\Copilot\Application\mscopilot_proxy.exe"'
        flags = '--no-startup-window'
        if self.disable_gpu_sandbox:
            flags += ' --disable-gpu-sandbox'

        launch_cmd = '{} {}'.format(copilot_path, flags)
        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MscopilotProxy AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
