
# LOLBAS: Visio.exe — Legitimate use: opening Microsoft Visio diagram files including remote URLs

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of Visio.exe to open a Visio diagram file
 (.vsd / .vsdx) from a specified URL or UNC path, as a normal office
 worker would when clicking a diagram link from an intranet or SharePoint.

 Takes a required remote_url parameter pointing to a .vsd or .vsdx file.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Visio(BaseCMD):
    """
    # LOLBAS: Visio.exe — Legitimate use: opening Visio diagram files from local or remote URLs

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Visio, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Visio'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > visio >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > visio >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Remote URL or UNC path to a Visio diagram file
        self.remote_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Visio Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the diagram URL with 'remote_url <url>'
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
    #  Visio Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Visio interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Visio_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_remote_url(self, remote_url):
        """
        Set the URL or UNC path to the Visio diagram file to open.
        Example: remote_url http://intranet.corp/diagrams/network.vsdx
        Example: remote_url \\\\fileserver\\share\\diagrams\\topology.vsd
        """
        if remote_url:
            if self.taskstarted:
                self.remote_url = remote_url.strip()
                print(self.cl.green("[*] Remote URL set to: {}".format(self.remote_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Visio Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a URL or file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Visio configuration
        """
        print(self.cl.green("[?] Currently Assigned Visio Configuration"))
        print("[>] Remote URL : {}".format(self.remote_url if self.remote_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.remote_url:
                print(self.cl.red("[!] <ERROR> You need to set a remote_url before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.remote_url = None


    ######################################################################
    # Visio AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Visio_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_visio()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            remote_url : str — URL or UNC path to a .vsd / .vsdx diagram file
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.remote_url = kwargs.get("remote_url", None)
        if self.remote_url:
            print(f"[*] Setting remote_url attribute : {self.remote_url}")
        else:
            print("[!] No remote_url provided — task cannot be created")
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
        ; <      Visio Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Visio_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Visio_{}()

            ; Creates a Visio Interaction via CMD

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
        Builds the Visio command to type into the CMD window.
        Launches Visio.exe with the supplied remote URL to open a diagram.
        """
        typing_text = '\n'

        visio_cmd = 'Visio.exe {}'.format(self.remote_url)
        typing_text += 'Send("' + self._escape_send(visio_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_visio(self):
        """
        Closes the Visio AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
