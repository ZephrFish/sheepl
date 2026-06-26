
# LOLBAS: msedgewebview2.exe — Legitimate use: launching Edge WebView2 to render embedded web content in applications

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of msedgewebview2.exe to launch the Microsoft Edge
 WebView2 browser control and render a web URL.  Takes an optional url
 parameter; if absent a generic local help page is opened.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsedgeWebview2(BaseCMD):
    """
    # LOLBAS: msedgewebview2.exe — Legitimate use: launching Edge WebView2 to render embedded web content in applications

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsedgeWebview2, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsedgeWebview2'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msedgewebview2 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msedgewebview2 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional URL to open via msedgewebview2
        self.url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsedgeWebview2 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a URL to open using 'url <url>'
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
    #  MsedgeWebview2 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsedgeWebview2 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsedgeWebview2_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_url(self, url):
        """
        Optionally set a URL to open via msedgewebview2.
        If not set, a default about:blank page is used.
        Example: url https://intranet.example.com/help
        """
        if url:
            if self.taskstarted:
                self.url = url.strip()
                print(self.cl.green("[*] URL set to: {}".format(self.url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsedgeWebview2 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsedgeWebview2 configuration
        """
        print(self.cl.green("[?] Currently Assigned MsedgeWebview2 Configuration"))
        print("[>] URL : {}".format(self.url if self.url else "(not set — will use about:blank)"))


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
        self.url = None


    ######################################################################
    # MsedgeWebview2 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsedgeWebview2_' + current_counter, self.create_autoit_function())


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
            url : str — URL to open via msedgewebview2
                        if absent, about:blank is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.url = kwargs.get("url", None)
        if self.url:
            print(f"[*] Setting url attribute : {self.url}")
        else:
            print("[*] No url provided — will use about:blank")

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
        ; <      MsedgeWebview2 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsedgeWebview2_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsedgeWebview2_{}()

            ; Creates a MsedgeWebview2 Interaction via CMD

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
        Builds the msedgewebview2 command to type into the CMD window.
        Launches msedgewebview2.exe with a URL argument to simulate
        legitimate embedded browser usage by an application.
        """
        typing_text = '\n'

        target_url = self.url if self.url else 'about:blank'

        # Launch msedgewebview2 with the target URL — simulates an app opening WebView2
        launch_cmd = 'msedgewebview2.exe "{}"'.format(target_url)
        typing_text += 'Send("' + self._escape_send(launch_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MsedgeWebview2 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
