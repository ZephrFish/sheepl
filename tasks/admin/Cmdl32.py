
# LOLBAS: cmdl32.exe — Legitimate use: downloading VPN configuration files via Microsoft Connection Manager

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of cmdl32.exe (Microsoft Connection Manager
 Auto-Download) to download a VPN configuration file from a URL specified
 in a local .cms configuration file.

 Takes a url parameter pointing to the remote resource and an optional
 config_dir parameter for the directory holding the .cms file.
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


class Cmdl32(BaseCMD):
    """
    # LOLBAS: cmdl32.exe — Legitimate use: downloading VPN configuration files via Microsoft Connection Manager

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Cmdl32, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Cmdl32'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cmdl32 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cmdl32 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the remote file to download (required)
        self.url = None
        # Directory containing the .cms config file (optional, defaults to %CD%)
        self.config_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Cmdl32 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the download URL using 'url <url>'
        3: Optionally set the config directory using 'config_dir <path>'
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
    #  Cmdl32 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Cmdl32 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Cmdl32_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_url(self, url):
        """
        Set the URL from which cmdl32 will download a file.
        This URL is embedded in the .cms config file passed to cmdl32.
        Example: url https://intranet.corp.local/vpn/update.bin
        """
        if url:
            if self.taskstarted:
                self.url = url.strip()
                print(self.cl.green("[*] URL set to: {}".format(self.url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cmdl32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a URL."))


    def do_config_dir(self, config_dir):
        """
        Optionally set the directory containing the .cms config file.
        Defaults to %CD% (current directory) if not set.
        Example: config_dir C:\\Users\\user\\vpnconfig
        """
        if config_dir:
            if self.taskstarted:
                self.config_dir = config_dir.strip()
                print(self.cl.green("[*] Config directory set to: {}".format(self.config_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Cmdl32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a config directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Cmdl32 configuration
        """
        print(self.cl.green("[?] Currently Assigned Cmdl32 Configuration"))
        print("[>] URL        : {}".format(self.url if self.url else "(not set)"))
        print("[>] Config Dir : {}".format(self.config_dir if self.config_dir else "(not set — will use %CD%)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.url:
                print(self.cl.red("[!] <ERROR> A URL must be set before completing. Use 'url <url>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.url = None
        self.config_dir = None


    ######################################################################
    # Cmdl32 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Cmdl32_' + current_counter, self.create_autoit_function())


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
            url        : str — URL to embed in the .cms config for cmdl32 to download from

        Optional JSON keys:
            config_dir : str — directory containing the .cms config file
                               (defaults to %CD% if absent)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.url = kwargs.get("url", None)
        if self.url:
            print(f"[*] Setting url attribute : {self.url}")
        else:
            print("[!] <ERROR> No url provided — this is required for Cmdl32.")
            return

        self.config_dir = kwargs.get("config_dir", None)
        if self.config_dir:
            print(f"[*] Setting config_dir attribute : {self.config_dir}")
        else:
            print("[*] No config_dir provided — will use %CD%")

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
        ; <      Cmdl32 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Cmdl32_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Cmdl32_{}()

            ; Creates a Cmdl32 Interaction via CMD

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
        Builds the cmdl32 command to type into the CMD window.
        Uses the /vpn /lan flags with the config directory containing a
        .cms file that references the target URL.
        """
        typing_text = '\n'

        # Determine config directory: use provided path or fall back to %CD%
        cfg_dir = self.config_dir if self.config_dir else '%CD%'

        # Build the cmdl32 command
        cmdl32_cmd = 'cmdl32 /vpn /lan {}'.format(cfg_dir)
        typing_text += 'Send("' + self._escape_send(cmdl32_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Cmdl32 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
