
# LOLBAS: AgentExecutor.exe — Legitimate use: Intune Management Extension executing PowerShell scripts on managed devices

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate Intune managed device behaviour of AgentExecutor.exe
 spawning powershell.exe to execute a PowerShell script with ExecutionPolicy
 Bypass, as performed by the Microsoft Intune Management Extension.

 Takes a ps1_path parameter pointing to the PowerShell script to execute.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class AgentExecutor(BaseCMD):
    """
    # LOLBAS: AgentExecutor.exe — Legitimate use: Intune Management Extension executing PowerShell scripts on managed devices

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(AgentExecutor, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'AgentExecutor'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > agentexecutor >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > agentexecutor >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the PowerShell script to execute
        self.ps1_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] AgentExecutor Interaction.
            Simulates Intune Management Extension executing a PowerShell script.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the PowerShell script path using 'ps1_path <path>'
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
    #  AgentExecutor Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new AgentExecutor interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'AgentExecutor_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_ps1_path(self, ps1_path):
        """
        Set the absolute path to the PowerShell script (.ps1) to execute.
        Example: ps1_path C:\\Temp\\MyScript.ps1
        """
        if ps1_path:
            if self.taskstarted:
                self.ps1_path = ps1_path.strip()
                print(self.cl.green("[*] PS1 path set to: {}".format(self.ps1_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AgentExecutor Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .ps1 script."))


    def do_assigned(self, arg):
        """
        Get the current assigned AgentExecutor configuration
        """
        print(self.cl.green("[?] Currently Assigned AgentExecutor Configuration"))
        print("[>] PS1 Path : {}".format(self.ps1_path if self.ps1_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.ps1_path:
                print(self.cl.red("[!] <ERROR> Please set a ps1_path before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.ps1_path = None


    ######################################################################
    # AgentExecutor AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('AgentExecutor_' + current_counter, self.create_autoit_function())


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
            ps1_path : str — absolute path to the PowerShell script to execute
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.ps1_path = kwargs.get("ps1_path", None)
        if self.ps1_path:
            print(f"[*] Setting ps1_path attribute : {self.ps1_path}")
        else:
            print("[!] <ERROR> No ps1_path provided — this is required for AgentExecutor.")
            return

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
        ; <      AgentExecutor Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "AgentExecutor_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func AgentExecutor_{}()

            ; Creates an AgentExecutor Interaction via CMD

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
        Builds the AgentExecutor command to type into the CMD window.
        Invokes AgentExecutor.exe with -powershell flag to execute a PS1 script,
        mirroring how the Intune Management Extension launches scripts on managed devices.
        """
        typing_text = '\n'

        # Build the AgentExecutor command using standard Intune log path conventions
        # Log paths mirror what the Intune Management Extension generates automatically
        log1 = self.ps1_path + '.1.log'
        log2 = self.ps1_path + '.2.log'
        log3 = self.ps1_path + '.3.log'
        ps_dir = 'C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0'

        agent_cmd = (
            '"C:\\Program Files (x86)\\Microsoft Intune Management Extension\\AgentExecutor.exe"'
            ' -powershell "{}" "{}" "{}" "{}" 60000 "{}" 0 1'.format(
                self.ps1_path, log1, log2, log3, ps_dir
            )
        )

        typing_text += 'Send("' + self._escape_send(agent_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the AgentExecutor AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
