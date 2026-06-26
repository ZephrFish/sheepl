
# LOLBAS: Squirrel.exe — Legitimate use: updating Nuget/Squirrel-packaged applications (e.g. Microsoft Teams)
# #######################################################################
#
#  Task : Squirrel Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of Squirrel.exe to check for and download
 updates for a Nuget/Squirrel-packaged application such as Microsoft Teams.

 Squirrel.exe is shipped with Microsoft Teams and similar Squirrel-packaged
 apps. It contacts a remote update URL, reads a RELEASES manifest file, and
 downloads the latest Nuget package.

 Requires: Microsoft Teams (or another Squirrel-packaged app) installed.

 Parameters
     update_url : str  — URL of the Squirrel update feed (must serve a RELEASES file)

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Squirrel(BaseCMD):
    """
    # LOLBAS: Squirrel.exe — Legitimate use: updating Nuget/Squirrel-packaged applications

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Squirrel, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Squirrel'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > squirrel >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > squirrel >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the remote update feed (must serve a RELEASES file)
        self.update_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Squirrel Interaction.
            Squirrel.exe updates Nuget/Squirrel-packaged apps (e.g. Microsoft Teams).
            Requires Microsoft Teams or another Squirrel-packaged application to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the remote update feed URL using 'update_url <url>'
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
    #  Squirrel Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Squirrel interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Squirrel_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_update_url(self, update_url):
        """
        Set the remote Squirrel update feed URL.
        Squirrel.exe will fetch the RELEASES file from this URL and download the package.
        Example: update_url https://update.example.com/myapp
        """
        if update_url:
            if self.taskstarted:
                self.update_url = update_url.strip()
                print(self.cl.green("[*] Update URL set to: {}".format(self.update_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Squirrel Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an update URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned Squirrel configuration
        """
        print(self.cl.green("[?] Currently Assigned Squirrel Configuration"))
        print("[>] Update URL : {}".format(self.update_url if self.update_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.update_url:
                print(self.cl.red("[!] <ERROR> An update URL must be set before completing."))
                print(self.cl.red("[!] <ERROR> Use 'update_url <url>' to set it."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.update_url = None


    ######################################################################
    # Squirrel AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Squirrel_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_squirrel()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            update_url : str  — URL of the remote Squirrel update feed (must serve a RELEASES file)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.update_url = kwargs.get("update_url", None)
        if self.update_url:
            print(f"[*] Setting update_url attribute : {self.update_url}")
        else:
            print("[!] <ERROR> No update_url provided — cannot build Squirrel task.")
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
        ; <      Squirrel Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Squirrel_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Squirrel_{}()

            ; Creates a Squirrel Interaction via CMD

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
        Builds the Squirrel.exe command to type into the CMD window.
        Uses --download to fetch the remote Nuget package without executing it,
        which represents a legitimate update check/download workflow.
        """
        typing_text = '\n'

        # Squirrel.exe lives in the Teams (or other app) install directory
        squirrel_path = r'%LOCALAPPDATA%\Microsoft\Teams\current\Squirrel.exe'
        download_cmd = '{} --download {}'.format(squirrel_path, self.update_url)
        typing_text += 'Send("' + self._escape_send(download_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_squirrel(self):
        """
        Closes the Squirrel AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
