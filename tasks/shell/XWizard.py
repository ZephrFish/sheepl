
# LOLBAS: xwizard.exe — Legitimate use: running registered COM wizard classes via the Windows Extensible Wizard host

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of xwizard.exe (Windows Extensible Wizard host process)
 to invoke a registered COM wizard class by GUID.

 Takes a required class_guid parameter (the COM class GUID to run) and an optional
 suppress_ui flag to add /taero /u switches that suppress error dialogs on Windows 10+.

 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class XWizard(BaseCMD):
    """
    # LOLBAS: xwizard.exe — Legitimate use: running registered COM wizard classes via the Windows Extensible Wizard host

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(XWizard, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'XWizard'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > xwizard >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > xwizard >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # COM class GUID to run with RunWizard
        self.class_guid = None
        # Whether to add /taero /u flags (suppresses error dialogs on Windows 10+)
        self.suppress_ui = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] XWizard Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set a registered COM class GUID using 'class_guid <GUID>'
        3: Optionally suppress UI errors using 'suppress_ui'
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
    #  XWizard Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new XWizard interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'XWizard_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_class_guid(self, class_guid):
        """
        Set the COM class GUID to invoke via xwizard RunWizard.
        This must be a GUID registered under HKCR\\CLSID or the user registry.
        Example: class_guid {7940acf8-60ba-4213-a7c3-f3b400ee266d}
        """
        if class_guid:
            if self.taskstarted:
                self.class_guid = class_guid.strip()
                print(self.cl.green("[*] Class GUID set to: {}".format(self.class_guid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new XWizard Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a COM class GUID."))


    def do_suppress_ui(self, arg):
        """
        Toggle the /taero /u flags that suppress error dialogs on Windows 10+.
        These flags prevent an error message box from appearing when the wizard
        class exits, which is the normal behaviour for background wizard invocations.
        Example: suppress_ui
        """
        if self.taskstarted:
            self.suppress_ui = not self.suppress_ui
            state = "enabled" if self.suppress_ui else "disabled"
            print(self.cl.green("[*] UI suppression ({}/taero /u) is now: {}".format("{", state)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new XWizard Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned XWizard configuration
        """
        print(self.cl.green("[?] Currently Assigned XWizard Configuration"))
        print("[>] Class GUID   : {}".format(self.class_guid if self.class_guid else "(not set)"))
        print("[>] Suppress UI  : {}".format(self.suppress_ui))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.class_guid:
                print(self.cl.red("[!] <ERROR> class_guid must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.class_guid = None
        self.suppress_ui = False


    ######################################################################
    # XWizard AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('XWizard_' + current_counter, self.create_autoit_function())


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
            class_guid  : str  — COM class GUID to pass to RunWizard
                                 e.g. "{7940acf8-60ba-4213-a7c3-f3b400ee266d}"

        Optional JSON keys:
            suppress_ui : bool — if true, adds /taero /u flags (default: false)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.class_guid = kwargs.get("class_guid", None)
        if self.class_guid:
            print(f"[*] Setting class_guid attribute : {self.class_guid}")
        else:
            print("[!] No class_guid provided — this task requires a COM class GUID")

        self.suppress_ui = kwargs.get("suppress_ui", False)
        print(f"[*] Setting suppress_ui attribute : {self.suppress_ui}")

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
        ; <      XWizard Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "XWizard_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func XWizard_{}()

            ; Creates an XWizard Interaction via CMD

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
        Builds the xwizard command to type into the CMD window.
        Runs RunWizard with the specified COM class GUID.
        Optionally adds /taero /u to suppress error dialogs on Windows 10+.
        """
        typing_text = '\n'

        if self.suppress_ui:
            xwizard_cmd = 'xwizard RunWizard /taero /u {}'.format(self.class_guid)
        else:
            xwizard_cmd = 'xwizard RunWizard {}'.format(self.class_guid)

        typing_text += 'Send("' + self._escape_send(xwizard_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the XWizard AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
