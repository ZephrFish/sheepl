
# LOLBAS: ieadvpack.dll — Legitimate use: INF-based component registration via rundll32 LaunchINFSection

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrative use of ieadvpack.dll via rundll32 to
 install or register a local INF file using the LaunchINFSection export.
 This mirrors the pattern used by Windows component setup routines.

 Takes an inf_path parameter pointing to a local .inf file to process.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class IeAdvpack(BaseCMD):
    """
    # LOLBAS: ieadvpack.dll — Legitimate use: INF-based component registration via rundll32 LaunchINFSection

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(IeAdvpack, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'IeAdvpack'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ieadvpack >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ieadvpack >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the local INF file to process
        self.inf_path = None
        # Optional section name (defaults to DefaultInstall_SingleUser if not set)
        self.section_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] IeAdvpack Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the INF file path using 'inf_path <path>'
        3: Optionally set a section name using 'section_name <name>'
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
    #  IeAdvpack Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new IeAdvpack interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'IeAdvpack_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_inf_path(self, inf_path):
        """
        Set the absolute path to the local INF file to process.
        Example: inf_path C:\\Windows\\inf\\msmsgs.inf
        """
        if inf_path:
            if self.taskstarted:
                self.inf_path = inf_path.strip()
                print(self.cl.green("[*] INF path set to: {}".format(self.inf_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new IeAdvpack Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an INF file path."))


    def do_section_name(self, section_name):
        """
        Optionally set the INF section name to invoke.
        Defaults to DefaultInstall_SingleUser if not set.
        Example: section_name DefaultInstall
        """
        if section_name:
            if self.taskstarted:
                self.section_name = section_name.strip()
                print(self.cl.green("[*] Section name set to: {}".format(self.section_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new IeAdvpack Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a section name."))


    def do_assigned(self, arg):
        """
        Get the current assigned IeAdvpack configuration
        """
        print(self.cl.green("[?] Currently Assigned IeAdvpack Configuration"))
        print("[>] INF Path     : {}".format(self.inf_path if self.inf_path else "(not set)"))
        print("[>] Section Name : {}".format(self.section_name if self.section_name else "(not set — defaults to DefaultInstall_SingleUser)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.inf_path:
                print(self.cl.red("[!] <ERROR> You must set an INF path before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.inf_path = None
        self.section_name = None


    ######################################################################
    # IeAdvpack AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('IeAdvpack_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_ieadvpack()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            inf_path     : str — absolute path to the local INF file to process

        Optional JSON keys:
            section_name : str — INF section to invoke (defaults to DefaultInstall_SingleUser)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.inf_path = kwargs.get("inf_path", None)
        if self.inf_path:
            print(f"[*] Setting inf_path attribute : {self.inf_path}")
        else:
            print("[!] <ERROR> No inf_path provided — this is required for IeAdvpack.")

        self.section_name = kwargs.get("section_name", None)
        if self.section_name:
            print(f"[*] Setting section_name attribute : {self.section_name}")
        else:
            print("[*] No section_name provided — will use DefaultInstall_SingleUser")

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
        ; <      IeAdvpack Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "IeAdvpack_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func IeAdvpack_{}()

            ; Creates an IeAdvpack Interaction via CMD

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
        Builds the rundll32 ieadvpack.dll command to type into the CMD window.
        Uses LaunchINFSection to process the specified local INF file.
        """
        typing_text = '\n'

        # Build the section argument — use provided section or default
        section = self.section_name if self.section_name else 'DefaultInstall_SingleUser'

        # rundll32 ieadvpack.dll,LaunchINFSection <inf_path>,<section>,1,
        rundll_cmd = 'rundll32.exe ieadvpack.dll,LaunchINFSection {},{},1,'.format(
            self.inf_path, section
        )
        typing_text += 'Send("' + self._escape_send(rundll_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_ieadvpack(self):
        """
        Closes the IeAdvpack AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
