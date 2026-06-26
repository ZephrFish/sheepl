
# LOLBAS: setupugc.exe — Legitimate use: Setup Unattend Generic Command Processor used during Windows deployment
# #######################################################################
#
#  Task : SetupUGC Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrative use of setupugc.exe to trigger
 unattended setup actions during Windows deployment workflows.

 The 'specialize' or 'auditUser' phase argument controls which
 RunSynchronous registry entries are executed. A registry path
 parameter specifies which command the registry key will point to
 (written before setupugc.exe is called).

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SetupUGC(BaseCMD):
    """
    # LOLBAS: setupugc.exe — Legitimate use: triggering unattended setup phases during Windows deployment

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SetupUGC, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SetupUGC'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > setupugc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > setupugc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Phase argument: 'specialize' or 'auditUser'
        self.phase = 'specialize'
        # Command to write to the registry RunSynchronous key before invoking setupugc
        self.reg_command = r'C:\Windows\System32\cmd.exe /c whoami'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] SetupUGC Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the setup phase using 'phase specialize' or 'phase auditUser'
        3: Set the command written to the registry key using 'reg_command <cmd>'
        4: Complete the interaction using 'complete'
        ----------------------------------
        Requires: Administrator privileges
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  SetupUGC Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new SetupUGC interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SetupUGC_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_phase(self, phase):
        """
        Set the setup phase argument passed to setupugc.exe.
        Valid values: specialize, auditUser
        Example: phase specialize
        """
        valid_phases = ['specialize', 'auditUser']
        if phase:
            if self.taskstarted:
                phase = phase.strip()
                if phase in valid_phases:
                    self.phase = phase
                    print(self.cl.green("[*] Phase set to: {}".format(self.phase)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid phase. Choose from: {}".format(', '.join(valid_phases))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SetupUGC Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a phase value (specialize or auditUser)."))


    def do_reg_command(self, reg_command):
        """
        Set the command path to write into the RunSynchronous registry key before calling setupugc.exe.
        Example: reg_command C:\\Windows\\System32\\cmd.exe /c whoami
        """
        if reg_command:
            if self.taskstarted:
                self.reg_command = reg_command.strip()
                print(self.cl.green("[*] Registry command set to: {}".format(self.reg_command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SetupUGC Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a command string."))


    def do_assigned(self, arg):
        """
        Get the current assigned SetupUGC configuration
        """
        print(self.cl.green("[?] Currently Assigned SetupUGC Configuration"))
        print("[>] Phase       : {}".format(self.phase))
        print("[>] Reg Command : {}".format(self.reg_command))


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
        self.phase = 'specialize'
        self.reg_command = r'C:\Windows\System32\cmd.exe /c whoami'


    ######################################################################
    # SetupUGC AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SetupUGC_' + current_counter, self.create_autoit_function())


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
            phase       : str — 'specialize' or 'auditUser' (default: 'specialize')
            reg_command : str — command written to RunSynchronous registry key
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.phase = kwargs.get("phase", "specialize")
        self.reg_command = kwargs.get("reg_command", r'C:\Windows\System32\cmd.exe /c whoami')

        print(f"[*] Setting phase attribute : {self.phase}")
        print(f"[*] Setting reg_command attribute : {self.reg_command}")

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
        ; <      SetupUGC Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "SetupUGC_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func SetupUGC_{}()

            ; Creates a SetupUGC Interaction via CMD

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
        Builds the setupugc.exe commands to type into the CMD window.
        First writes the command into the registry RunSynchronous key,
        then invokes setupugc.exe with the configured phase argument.
        """
        typing_text = '\n'

        # Write command into the RunSynchronous registry key
        reg_key = r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\UnattendSettings\Setup-Unattend-Settings\RunSynchronous\1'
        reg_add_cmd = 'reg add "{}" /v Path /d "{}" /f'.format(reg_key, self.reg_command)
        typing_text += 'Send("' + self._escape_send(reg_add_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Invoke setupugc.exe with the chosen phase
        setupugc_cmd = 'setupugc.exe {}'.format(self.phase)
        typing_text += 'Send("' + self._escape_send(setupugc_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the SetupUGC AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
