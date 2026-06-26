
# LOLBAS: unregmp2.exe — Legitimate use: Windows Media Player setup utility to show or hide WMP

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrative use of unregmp2.exe to manage
 the Windows Media Player installation state on a Windows system.

 Supports /ShowWMP to re-enable Windows Media Player (default) or
 /HideWMP to suppress it, as an administrator would during OS hardening
 or feature management.

 The master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Unregmp2(BaseCMD):
    """
    # LOLBAS: unregmp2.exe — Legitimate use: managing Windows Media Player installation state

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Unregmp2, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Unregmp2'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > unregmp2 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > unregmp2 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Action: either 'show' or 'hide'
        self.wmp_action = 'show'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Unregmp2 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the WMP action using 'wmp_action show' or 'wmp_action hide'
           Default action is 'show' (/ShowWMP)
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
    #  Unregmp2 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Unregmp2 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Unregmp2_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_wmp_action(self, action):
        """
        Set the Windows Media Player action to perform.
        Use 'show' to run /ShowWMP (default) or 'hide' to run /HideWMP.
        Example: wmp_action show
        Example: wmp_action hide
        """
        if action:
            action = action.strip().lower()
            if action in ('show', 'hide'):
                if self.taskstarted:
                    self.wmp_action = action
                    print(self.cl.green("[*] WMP action set to: {}".format(self.wmp_action)))
                else:
                    print(self.cl.red("[!] <ERROR> You need to start a new Unregmp2 Interaction."))
                    print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            else:
                print(self.cl.red("[!] <ERROR> Action must be 'show' or 'hide'."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an action: 'show' or 'hide'."))


    def do_assigned(self, arg):
        """
        Get the current assigned Unregmp2 configuration
        """
        print(self.cl.green("[?] Currently Assigned Unregmp2 Configuration"))
        flag = '/ShowWMP' if self.wmp_action == 'show' else '/HideWMP'
        print("[>] WMP Action : {} ({})".format(self.wmp_action, flag))


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
        self.wmp_action = 'show'


    ######################################################################
    # Unregmp2 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Unregmp2_' + current_counter, self.create_autoit_function())


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
            wmp_action : str — 'show' (default) to run /ShowWMP, or 'hide' to run /HideWMP
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.wmp_action = kwargs.get("wmp_action", "show").strip().lower()
        if self.wmp_action not in ('show', 'hide'):
            self.wmp_action = 'show'
        print(f"[*] Setting wmp_action attribute : {self.wmp_action}")

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
        ; <      Unregmp2 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Unregmp2_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Unregmp2_{}()

            ; Creates an Unregmp2 Interaction via CMD

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
        Builds the unregmp2.exe command to type into the CMD window.
        Uses /ShowWMP or /HideWMP depending on the configured wmp_action.
        """
        typing_text = '\n'

        flag = '/ShowWMP' if self.wmp_action == 'show' else '/HideWMP'
        unregmp2_cmd = 'unregmp2.exe {}'.format(flag)
        typing_text += 'Send("' + self._escape_send(unregmp2_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Unregmp2 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
