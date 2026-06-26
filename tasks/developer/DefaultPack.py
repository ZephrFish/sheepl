
# LOLBAS: DefaultPack.EXE — Legitimate use: Bing default search provider installer bundled with Microsoft software downloads
# DEVELOPER-ONLY: Requires DefaultPack.EXE from Microsoft software bundle (e.g. Office installer side-download)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user invocation of DefaultPack.EXE, which is
 bundled alongside certain Microsoft software downloads and is used
 to configure Bing as the default search provider.

 Takes an optional target_binary parameter; if absent runs DefaultPack.EXE
 without a /C argument to perform the default browser/search configuration.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DefaultPack(BaseCMD):
    """
    # LOLBAS: DefaultPack.EXE — Legitimate use: Bing default search provider installer bundled with Microsoft software downloads

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DefaultPack, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DefaultPack'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > defaultpack >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > defaultpack >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional target binary to execute via /C argument
        self.target_binary = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DefaultPack Interaction.
        NOTE: Requires DefaultPack.EXE at C:\\Program Files (x86)\\Microsoft\\DefaultPack\\DefaultPack.exe
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a target binary to invoke via 'target_binary <path>'
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
    #  DefaultPack Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DefaultPack interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DefaultPack_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_binary(self, target_binary):
        """
        Optionally set a target binary path to pass to DefaultPack.EXE via the /C argument.
        If not set, DefaultPack.EXE is run without arguments (default search config).
        Example: target_binary C:\\Windows\\System32\\calc.exe
        """
        if target_binary:
            if self.taskstarted:
                self.target_binary = target_binary.strip()
                print(self.cl.green("[*] Target binary set to: {}".format(self.target_binary)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DefaultPack Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target binary path."))


    def do_assigned(self, arg):
        """
        Get the current assigned DefaultPack configuration
        """
        print(self.cl.green("[?] Currently Assigned DefaultPack Configuration"))
        print("[>] Target Binary : {}".format(self.target_binary if self.target_binary else "(not set — will run DefaultPack.EXE without arguments)"))


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
        self.target_binary = None


    ######################################################################
    # DefaultPack AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DefaultPack_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_defaultpack()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            target_binary : str — full path to a binary to invoke via DefaultPack.EXE /C
                                  if absent, DefaultPack.EXE is run without arguments
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_binary = kwargs.get("target_binary", None)
        if self.target_binary:
            print(f"[*] Setting target_binary attribute : {self.target_binary}")
        else:
            print("[*] No target_binary provided — will run DefaultPack.EXE without arguments")

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
        ; <      DefaultPack Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DefaultPack_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DefaultPack_{}()

            ; Creates a DefaultPack Interaction via CMD

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
        Builds the DefaultPack command to type into the CMD window.
        Runs DefaultPack.EXE from its standard installation path.
        If target_binary is set, passes it via the /C argument.
        """
        typing_text = '\n'

        defaultpack_exe = '"C:\\Program Files (x86)\\Microsoft\\DefaultPack\\DefaultPack.exe"'

        if self.target_binary:
            run_cmd = '{} /C:"{}"'.format(defaultpack_exe, self.target_binary)
        else:
            run_cmd = defaultpack_exe

        typing_text += 'Send("' + self._escape_send(run_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_defaultpack(self):
        """
        Closes the DefaultPack AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
