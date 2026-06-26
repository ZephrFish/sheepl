
# LOLBAS: Dfshim.dll — Legitimate use: launching ClickOnce applications via rundll32

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of dfshim.dll to open a ClickOnce application
 from a URL using rundll32 and the ShOpenVerbApplication export.

 Takes a required app_url parameter pointing to the ClickOnce manifest (.application).
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Dfshim(BaseCMD):
    """
    # LOLBAS: Dfshim.dll — Legitimate use: launching ClickOnce applications via rundll32

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Dfshim, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Dfshim'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > dfshim >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > dfshim >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the ClickOnce application manifest
        self.app_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Dfshim Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the ClickOnce application URL using 'app_url <url>'
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
    #  Dfshim Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Dfshim interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Dfshim_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_app_url(self, app_url):
        """
        Set the URL of the ClickOnce application manifest to launch.
        Example: app_url http://example.com/app/MyApp.application
        """
        if app_url:
            if self.taskstarted:
                self.app_url = app_url.strip()
                print(self.cl.green("[*] App URL set to: {}".format(self.app_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Dfshim Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a ClickOnce application URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned Dfshim configuration
        """
        print(self.cl.green("[?] Currently Assigned Dfshim Configuration"))
        print("[>] App URL : {}".format(self.app_url if self.app_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.app_url:
                print(self.cl.red("[!] <ERROR> app_url must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.app_url = None


    ######################################################################
    # Dfshim AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Dfshim_' + current_counter, self.create_autoit_function())


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
            app_url : str — URL to the ClickOnce application manifest (.application)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.app_url = kwargs.get("app_url", None)
        if self.app_url:
            print(f"[*] Setting app_url attribute : {self.app_url}")
        else:
            print("[!] <ERROR> app_url is required for Dfshim task")
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
        ; <      Dfshim Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Dfshim_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Dfshim_{}()

            ; Creates a Dfshim Interaction via CMD

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
        Builds the rundll32 dfshim command to type into the CMD window.
        Uses ShOpenVerbApplication export to launch a ClickOnce app from a URL.
        """
        typing_text = '\n'

        # Launch ClickOnce application via dfshim.dll ShOpenVerbApplication
        run_cmd = 'rundll32.exe dfshim.dll,ShOpenVerbApplication {}'.format(self.app_url)
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
        Closes the Dfshim AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
