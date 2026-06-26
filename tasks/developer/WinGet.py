
# #######################################################################
#
#  Task : WinGet Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT/developer use of winget.exe (Windows Package Manager)
 for software inventory, package installation, and upgrade management.

"""

# LOLBAS: winget.exe — Legitimate use: software inventory and package management (Win10 1809+)

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WinGet(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: winget.exe — Legitimate use: software inventory and package management (Win10 1809+)
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WinGet, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WinGet'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > winget >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > winget >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # action: search | install | list | upgrade  (default: list)
        self.action = 'list'
        # package name or ID used with search/install actions
        self.package = ''

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] WinGet Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action'   (search / install / list / upgrade)
        3: Set the package using 'package' (required for search / install)
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
    #  WinGet Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WinGet interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WinGet_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, arg):
        """
        Set the winget action to perform.
        Valid options: search, install, list, upgrade
        Default: list
        Example: action search
        """
        valid_actions = ['search', 'install', 'list', 'upgrade']
        if self.taskstarted:
            if arg and arg.lower() in valid_actions:
                self.action = arg.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new WinGet Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_package(self, arg):
        """
        Set the package name or ID to use with search or install actions.
        Example: package Microsoft.VisualStudioCode
        """
        if self.taskstarted:
            if arg:
                self.package = arg
                print(self.cl.green("[*] Package set to: {}".format(self.package)))
            else:
                print(self.cl.red("[!] <ERROR> You must supply a package name or ID."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new WinGet Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current WinGet task settings
        """
        print(self.cl.green("[?] Currently Assigned WinGet Settings"))
        print("[>] Action  : {}".format(self.action))
        print("[>] Package : {}".format(self.package if self.package else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.action in ('search', 'install') and not self.package:
                print(self.cl.red("[!] <ERROR> Action '{}' requires a package to be set.".format(self.action)))
                print(self.cl.red("[-] Use 'package <name>' to specify the package."))
                return None
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific variables for next interaction
        self.action = 'list'
        self.package = ''


    ######################################################################
    # WinGet AutoIT Block Definition
    #######################################################################


    def _build_winget_command(self):
        """
        Constructs the winget command string based on self.action and self.package.
        """
        if self.action == 'search':
            return 'winget search {}'.format(self.package)
        elif self.action == 'install':
            return 'winget install --accept-package-agreements --accept-source-agreements {}'.format(self.package)
        elif self.action == 'list':
            return 'winget list'
        elif self.action == 'upgrade':
            return 'winget upgrade'
        else:
            return 'winget list'


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WinGet_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_winget()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads action and package from kwargs.
        JSON keys: action, package
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", "list")
        print(f"[*] Setting the action attribute : {self.action}")

        self.package = kwargs.get("package", "")
        print(f"[*] Setting the package attribute : {self.package}")

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      WinGet Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "WinGet_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for the winget command
        """

        _open_commandshell = """

        Func WinGet_{}()

            ; Creates a WinGet Interaction via CMD

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
        Builds the winget command and emits AutoIT Send statements.
        """
        typing_text = '\n'

        winget_cmd = self._build_winget_command()
        escaped_cmd = self._escape_send(winget_cmd)

        typing_text += 'Send("{}{}")\n'.format(escaped_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_winget(self):
        """
        Closes the WinGet function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
