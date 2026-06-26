
# LOLBAS: control.exe — Legitimate use: launch Control Panel items (.cpl applets) on Windows

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of control.exe to open Windows Control Panel
 applets directly by .cpl filename or by canonical panel name.

 Takes an optional cpl_item parameter specifying which applet to open.
 If absent, opens the Control Panel root window.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Control(BaseCMD):
    """
    # LOLBAS: control.exe — Legitimate use: launch Control Panel items (.cpl applets) on Windows

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Control, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Control'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > control >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > control >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional Control Panel item / .cpl filename to open
        self.cpl_item = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Control Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a Control Panel applet using 'cpl_item <name>'
           Examples: appwiz.cpl  desk.cpl  inetcpl.cpl  timedate.cpl
           If not set, the Control Panel root window is opened.
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
    #  Control Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Control interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Control_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_cpl_item(self, cpl_item):
        """
        Optionally set a Control Panel applet (.cpl) to open with control.exe.
        If not set, the Control Panel root window is opened.
        Example: cpl_item appwiz.cpl
        Example: cpl_item desk.cpl
        Example: cpl_item timedate.cpl
        """
        if cpl_item:
            if self.taskstarted:
                self.cpl_item = cpl_item.strip()
                print(self.cl.green("[*] CPL item set to: {}".format(self.cpl_item)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Control Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a .cpl filename or leave blank for the root panel."))


    def do_assigned(self, arg):
        """
        Get the current assigned Control configuration
        """
        print(self.cl.green("[?] Currently Assigned Control Configuration"))
        print("[>] CPL Item : {}".format(self.cpl_item if self.cpl_item else "(not set — will open Control Panel root)"))


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
        self.cpl_item = None


    ######################################################################
    # Control AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Control_' + current_counter, self.create_autoit_function())


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
            cpl_item : str — .cpl filename to open with control.exe
                             e.g. "appwiz.cpl", "desk.cpl", "timedate.cpl"
                             if absent, opens the Control Panel root window
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.cpl_item = kwargs.get("cpl_item", None)
        if self.cpl_item:
            print(f"[*] Setting cpl_item attribute : {self.cpl_item}")
        else:
            print("[*] No cpl_item provided — will open Control Panel root window")

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
        ; <      Control Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Control_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Control_{}()

            ; Creates a Control Interaction via CMD

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
        Builds the control.exe command to type into the CMD window.
        Opens the specified .cpl applet, or the Control Panel root if none set.
        """
        typing_text = '\n'

        if self.cpl_item:
            control_cmd = 'control.exe {}'.format(self.cpl_item)
        else:
            control_cmd = 'control.exe'

        typing_text += 'Send("' + self._escape_send(control_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Control AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
