
# LOLBAS: MsoHtmEd.exe — Legitimate use: Microsoft Office HTML editor component that fetches remote HTML content into INetCache

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of MsoHtmEd.exe, the Microsoft Office HTML
 editor component, to fetch a remote URL and cache it locally via
 INetCache — as it would when Office opens a remote HTML document.

 Takes a required remote_url parameter pointing to the HTML resource
 to retrieve.

 The master script will already define the typing speed as part of the
 master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsoHtmEd(BaseCMD):
    """
    # LOLBAS: MsoHtmEd.exe — Legitimate use: Microsoft Office HTML editor component that fetches remote HTML content into INetCache

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsoHtmEd, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsoHtmEd'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msohtmed >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msohtmed >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Remote URL to fetch via MsoHtmEd
        self.remote_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsoHtmEd Interaction.
        Simulates the Microsoft Office HTML editor component fetching a
        remote HTML resource into INetCache.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the remote URL using 'remote_url <url>'
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
    #  MsoHtmEd Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsoHtmEd interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsoHtmEd_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_remote_url(self, remote_url):
        """
        Set the remote URL for MsoHtmEd to fetch.
        The binary will download the resource and place it in INetCache.
        Example: remote_url http://intranet.corp.local/template.html
        """
        if remote_url:
            if self.taskstarted:
                self.remote_url = remote_url.strip()
                print(self.cl.green("[*] Remote URL set to: {}".format(self.remote_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsoHtmEd Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsoHtmEd configuration
        """
        print(self.cl.green("[?] Currently Assigned MsoHtmEd Configuration"))
        print("[>] Remote URL : {}".format(self.remote_url if self.remote_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.remote_url:
                print(self.cl.red("[!] <ERROR> A remote URL is required. Set it with 'remote_url <url>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.remote_url = None


    ######################################################################
    # MsoHtmEd AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsoHtmEd_' + current_counter, self.create_autoit_function())


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
            remote_url : str — remote HTTP/HTTPS URL for MsoHtmEd to fetch
                               (resource is cached in INetCache)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.remote_url = kwargs.get("remote_url", None)
        if self.remote_url:
            print(f"[*] Setting remote_url attribute : {self.remote_url}")
        else:
            print("[!] <ERROR> No remote_url provided — this task requires a URL.")
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
        ; <      MsoHtmEd Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsoHtmEd_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsoHtmEd_{}()

            ; Creates a MsoHtmEd Interaction via CMD

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
        Builds the MsoHtmEd command to type into the CMD window.
        Invokes MsoHtmEd.exe with the remote URL so Office fetches
        and caches the remote HTML resource via INetCache.
        """
        typing_text = '\n'

        # Run MsoHtmEd with the remote URL — Office will fetch and cache it
        msohtmed_cmd = 'MsoHtmEd.exe {}'.format(self.remote_url)
        typing_text += 'Send("' + self._escape_send(msohtmed_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MsoHtmEd AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
