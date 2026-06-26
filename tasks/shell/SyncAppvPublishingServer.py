
# LOLBAS: SyncAppvPublishingServer.exe — Legitimate use: querying App-V publishing servers in App-V deployments
# #######################################################################
#
#  Task : SyncAppvPublishingServer Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate App-V administrator use of SyncAppvPublishingServer.exe
 to query and synchronise App-V publishing server lists.

 Takes an optional server_url parameter representing the App-V publishing
 server URL to query; if absent a placeholder localhost URL is used.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SyncAppvPublishingServer(BaseCMD):
    """
    # LOLBAS: SyncAppvPublishingServer.exe — Legitimate use: querying App-V publishing servers in App-V deployments

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(SyncAppvPublishingServer, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SyncAppvPublishingServer'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > syncappvpublishingserver >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > syncappvpublishingserver >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional App-V publishing server URL
        self.server_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] SyncAppvPublishingServer Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a publishing server URL using 'server_url <url>'
        3: Complete the interaction using 'complete'
        ----------------------------------
        Note: SyncAppvPublishingServer.exe is used by App-V to query and
        synchronise App-V publishing server lists. This task simulates
        legitimate App-V administrator activity.
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  SyncAppvPublishingServer Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new SyncAppvPublishingServer interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SyncAppvPublishingServer_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_server_url(self, server_url):
        """
        Optionally set the App-V publishing server URL to query.
        If not set, a default localhost URL will be used.
        Example: server_url http://appv-server.corp.local:8080
        """
        if server_url:
            if self.taskstarted:
                self.server_url = server_url.strip()
                print(self.cl.green("[*] Server URL set to: {}".format(self.server_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new SyncAppvPublishingServer Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a server URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned SyncAppvPublishingServer configuration
        """
        print(self.cl.green("[?] Currently Assigned SyncAppvPublishingServer Configuration"))
        print("[>] Server URL : {}".format(self.server_url if self.server_url else "(not set — will use default localhost URL)"))


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
        self.server_url = None


    ######################################################################
    # SyncAppvPublishingServer AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SyncAppvPublishingServer_' + current_counter, self.create_autoit_function())


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
            server_url : str — App-V publishing server URL to query
                               if absent, a default localhost URL is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.server_url = kwargs.get("server_url", None)
        if self.server_url:
            print(f"[*] Setting server_url attribute : {self.server_url}")
        else:
            print("[*] No server_url provided — will use default localhost URL")

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
        ; <      SyncAppvPublishingServer Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "SyncAppvPublishingServer_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func SyncAppvPublishingServer_{}()

            ; Creates a SyncAppvPublishingServer Interaction via CMD

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
        Builds the SyncAppvPublishingServer commands to type into the CMD window.
        Queries the App-V publishing server using the provided or default URL.
        """
        typing_text = '\n'

        # Use provided server URL or fall back to a default localhost placeholder
        url = self.server_url if self.server_url else 'http://localhost:8080'

        sync_cmd = 'SyncAppvPublishingServer.exe "n;Get-AppvPublishingServer"'
        typing_text += 'Send("' + self._escape_send(sync_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the SyncAppvPublishingServer AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
