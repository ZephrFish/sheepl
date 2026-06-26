
# LOLBAS: msedge_proxy.exe — Legitimate use: launching Microsoft Edge browser processes
# #######################################################################
#
#  Task : MsedgeProxy Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of msedge_proxy.exe to open a URL in Microsoft Edge.
 The binary is the Edge browser process proxy, used to launch Edge with a target URL.

 Takes a target_url parameter; defaults to the Microsoft Edge new-tab page if absent.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsedgeProxy(BaseCMD):
    """
    # LOLBAS: msedge_proxy.exe — Legitimate use: launching Microsoft Edge browser processes

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsedgeProxy, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsedgeProxy'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msedge_proxy >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msedge_proxy >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target URL for msedge_proxy to open
        self.target_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsedgeProxy Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a target URL using 'target_url <url>'
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
    #  MsedgeProxy Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsedgeProxy interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsedgeProxy_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_url(self, target_url):
        """
        Optionally set a target URL for msedge_proxy to open.
        If not set, the Edge new-tab page will be opened.
        Example: target_url https://www.microsoft.com
        """
        if target_url:
            if self.taskstarted:
                self.target_url = target_url.strip()
                print(self.cl.green("[*] Target URL set to: {}".format(self.target_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsedgeProxy Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsedgeProxy configuration
        """
        print(self.cl.green("[?] Currently Assigned MsedgeProxy Configuration"))
        print("[>] Target URL : {}".format(self.target_url if self.target_url else "(not set — will open Edge new-tab page)"))


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
        self.target_url = None


    ######################################################################
    # MsedgeProxy AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsedgeProxy_' + current_counter, self.create_autoit_function())


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
            target_url : str — URL to open with msedge_proxy.exe
                               if absent, opens the Edge new-tab page
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_url = kwargs.get("target_url", None)
        if self.target_url:
            print(f"[*] Setting target_url attribute : {self.target_url}")
        else:
            print("[*] No target_url provided — will open Edge new-tab page")

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
        ; <      MsedgeProxy Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsedgeProxy_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsedgeProxy_{}()

            ; Creates a MsedgeProxy Interaction via CMD

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
        Builds the msedge_proxy command to type into the CMD window.
        Opens a URL (or the new-tab page if no URL was supplied).
        """
        typing_text = '\n'

        url = self.target_url if self.target_url else 'edge://newtab'
        msedge_cmd = '"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge_proxy.exe" {}'.format(url)
        typing_text += 'Send("' + self._escape_send(msedge_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MsedgeProxy AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
