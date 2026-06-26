
# LOLBAS: DeviceCredentialDeployment.exe — Legitimate use: conceal a console window by grabbing its handle and hiding it

# #######################################################################
#
#  Task : DeviceCredentialDeployment Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrative use of DeviceCredentialDeployment.exe,
 which grabs the console window handle and sets it to hidden.  This behaviour
 is representative of T1564 (Hide Artifacts) and is useful as a red-team
 baseline artefact on Windows 10 endpoints.

 The binary takes no meaningful arguments; the task simply executes it from
 a CMD shell and allows an optional sleep dwell time before exiting.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DeviceCredentialDeployment(BaseCMD):
    """
    # LOLBAS: DeviceCredentialDeployment.exe — Legitimate use: conceal a console window by setting it to hidden

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DeviceCredentialDeployment, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DeviceCredentialDeployment'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > devicecredentialdeployment >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > devicecredentialdeployment >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DeviceCredentialDeployment Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  DeviceCredentialDeployment Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DeviceCredentialDeployment interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DeviceCredentialDeployment_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_assigned(self, arg):
        """
        Get the current assigned DeviceCredentialDeployment configuration
        """
        print(self.cl.green("[?] Currently Assigned DeviceCredentialDeployment Configuration"))
        print("[>] No configurable parameters — binary will be executed as-is")


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


    ######################################################################
    # DeviceCredentialDeployment AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DeviceCredentialDeployment_' + current_counter, self.create_autoit_function())


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

        No additional JSON keys are required for this task.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

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
        ; <      DeviceCredentialDeployment Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DeviceCredentialDeployment_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DeviceCredentialDeployment_{}()

            ; Creates a DeviceCredentialDeployment Interaction via CMD

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
        Builds the DeviceCredentialDeployment command to type into the CMD window.
        Executes the binary in-place, then exits the shell.
        """
        typing_text = '\n'

        # Execute DeviceCredentialDeployment.exe — grabs console handle and hides window
        run_cmd = 'DeviceCredentialDeployment.exe'
        typing_text += 'Send("' + self._escape_send(run_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the DeviceCredentialDeployment AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
