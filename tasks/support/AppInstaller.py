
# LOLBAS: AppInstaller.exe — Legitimate use: installing AppX/MSIX applications from a URI source

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of AppInstaller.exe to install or load an
 AppX/MSIX application package from a remote URL via the ms-appinstaller
 URI handler. The package is fetched and cached in INetCache.

 Requires a target_url parameter pointing to a .msix or .appx package.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class AppInstaller(BaseCMD):
    """
    # LOLBAS: AppInstaller.exe — Legitimate use: installing AppX/MSIX packages via ms-appinstaller URI

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(AppInstaller, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'AppInstaller'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > appinstaller >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > appinstaller >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the .msix/.appx package to install
        self.target_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] AppInstaller Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the package URL using 'target_url <url>'
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
    #  AppInstaller Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new AppInstaller interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'AppInstaller_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_url(self, target_url):
        """
        Set the URL of the AppX/MSIX package to install via AppInstaller.
        Example: target_url https://example.com/myapp.msix
        """
        if target_url:
            if self.taskstarted:
                self.target_url = target_url.strip()
                print(self.cl.green("[*] Target URL set to: {}".format(self.target_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AppInstaller Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a package URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned AppInstaller configuration
        """
        print(self.cl.green("[?] Currently Assigned AppInstaller Configuration"))
        print("[>] Target URL : {}".format(self.target_url if self.target_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.target_url:
                print(self.cl.red("[!] <ERROR> Please set a target_url before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.target_url = None


    ######################################################################
    # AppInstaller AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('AppInstaller_' + current_counter, self.create_autoit_function())


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
            target_url : str — URL of the .msix/.appx package to install
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_url = kwargs.get("target_url", None)
        if self.target_url:
            print(f"[*] Setting target_url attribute : {self.target_url}")
        else:
            print("[!] <ERROR> No target_url provided — AppInstaller task requires a package URL.")
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
        ; <      AppInstaller Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "AppInstaller_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func AppInstaller_{}()

            ; Creates an AppInstaller Interaction via CMD

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
        Builds the AppInstaller command to type into the CMD window.
        Launches the ms-appinstaller URI handler with the target package URL.
        """
        typing_text = '\n'

        # Invoke AppInstaller via the ms-appinstaller URI handler
        install_cmd = 'start ms-appinstaller://?source={}'.format(self.target_url)
        typing_text += 'Send("' + self._escape_send(install_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the AppInstaller AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
