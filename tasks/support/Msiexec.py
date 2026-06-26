
# LOLBAS: msiexec.exe — Legitimate use: software deployment via Windows Installer packages

# #######################################################################
#
#  Task : Msiexec Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT/user use of msiexec.exe for installing,
 uninstalling, or querying Windows Installer packages. Common IT
 scenarios include deploying software via MSI packages, removing
 applications, and auditing installed software via wmic.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Msiexec(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Msiexec, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Msiexec'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msiexec >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msiexec >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific defaults
        # action: "install", "uninstall", or "query"
        self.action = "query"
        # package: path to .msi file for install/uninstall, or product name for query
        self.package = ""
        # passive: use /passive flag for minimal UI (True by default)
        self.passive = True

        self.introduction = """
        ----------------------------------
        [!] Msiexec Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action' (install / uninstall / query)
        3: Set the package using 'package' (path to .msi or product name)
        4: Toggle passive mode using 'passive'
        5: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Msiexec Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Msiexec interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Msiexec_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, action):
        """
        Set the msiexec action to perform.
        Options: install, uninstall, query
        Default: query
        Examples:
            action install
            action uninstall
            action query
        """
        valid_actions = ['install', 'uninstall', 'query']
        if self.taskstarted:
            if action.lower() in valid_actions:
                self.action = action.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msiexec Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_package(self, package):
        """
        Set the package path or product name.
        For install/uninstall: path to the .msi file
        For query: (optional) product name filter
        Examples:
            package C:\\installers\\app.msi
            package 7-Zip
        """
        if self.taskstarted:
            if package:
                self.package = package
                print(self.cl.green("[*] Package set to: {}".format(self.package)))
            else:
                print(self.cl.yellow("[*] No package supplied."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msiexec Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_passive(self, arg):
        """
        Toggle passive mode (minimal UI during install/uninstall).
        Default: True (passive mode enabled)
        """
        if self.taskstarted:
            self.passive = not self.passive
            state = "enabled" if self.passive else "disabled"
            print(self.cl.green("[*] Passive mode {}.".format(state)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Msiexec Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the currently assigned Msiexec settings
        """
        print(self.cl.green("[?] Currently Assigned Msiexec Settings"))
        print("[>] Action  : {}".format(self.action))
        print("[>] Package : {}".format(self.package if self.package else "(none)"))
        print("[>] Passive : {}".format(self.passive))


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

        # reset task-specific attributes for next interaction
        self.action = "query"
        self.package = ""
        self.passive = True


    ######################################################################
    # Msiexec AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Msiexec_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.msiexec_command_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            action  : "install", "uninstall", or "query" (default: "query")
            package : path to .msi file for install/uninstall, or product name for query
            passive : boolean, use /passive flag for minimal UI (default: true)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "action" in kwargs:
            self.action = kwargs["action"]
        print(f"[*] Setting the action attribute : {self.action}")

        if "package" in kwargs:
            self.package = kwargs["package"]
        print(f"[*] Setting the package attribute : {self.package}")

        if "passive" in kwargs:
            self.passive = bool(kwargs["passive"])
        print(f"[*] Setting the passive attribute : {self.passive}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      Msiexec Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Msiexec_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens CMD via Win+R run dialogue
        """

        _open_commandshell = """

        Func Msiexec_{}()

            ; Opens CMD to run msiexec command

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
    # Msiexec Command Block

    def _build_msiexec_command(self):
        """
        Constructs the appropriate msiexec or wmic command string
        based on the configured action, package, and passive flag.
        """
        ui_flag = "/passive" if self.passive else "/quiet"

        if self.action == "install":
            package = self.package if self.package else "C:\\installers\\package.msi"
            return "msiexec /i {} {}".format(package, ui_flag)

        elif self.action == "uninstall":
            package = self.package if self.package else "C:\\installers\\package.msi"
            return "msiexec /x {} {}".format(package, ui_flag)

        else:
            # query: use wmic to enumerate installed products
            # wmic is the standard tool for querying MSI-installed software
            if self.package:
                return 'wmic product where "Name like \'%{}%\'" get Name,Version,Vendor'.format(self.package)
            else:
                return "wmic product get Name,Version,Vendor"

    def msiexec_command_block(self):
        """
        Sends the msiexec/wmic command and exits the shell
        """

        command = self._build_msiexec_command()

        cmd_text = '\n'
        cmd_text += 'Send("' + self._escape_send(command) + '{ENTER}")\n'
        cmd_text += 'sleep({})\n'.format(random.randint(3000, 15000))
        cmd_text += "Send('exit{ENTER}')\n"
        cmd_text += "; Reset Focus\n"
        cmd_text += 'SendKeepActive("")'

        return textwrap.indent(cmd_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the Msiexec function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
