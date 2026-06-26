
# LOLBAS: url.dll — Legitimate use: opening URLs and local file paths via the shell protocol handler

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of url.dll via rundll32.exe to open a local
 file path using the FileProtocolHandler export, which is a standard
 Windows shell mechanism for launching files by protocol URI.

 Takes a target_path parameter specifying the file to open.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Url(BaseCMD):
    """
    # LOLBAS: url.dll — Legitimate use: opening local files via FileProtocolHandler export

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Url, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Url'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > url >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > url >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Target path to open via FileProtocolHandler
        self.target_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Url.dll Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the file path to open using 'target_path <path>'
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
    #  Url Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Url interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Url_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_path(self, target_path):
        """
        Set the local file path to open via url.dll FileProtocolHandler.
        Example: target_path C:\\Users\\Public\\document.pdf
        """
        if target_path:
            if self.taskstarted:
                self.target_path = target_path.strip()
                print(self.cl.green("[*] Target path set to: {}".format(self.target_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Url Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Url configuration
        """
        print(self.cl.green("[?] Currently Assigned Url Configuration"))
        print("[>] Target Path : {}".format(self.target_path if self.target_path else "(not set — will use default notepad path)"))


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
        self.target_path = None


    ######################################################################
    # Url AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Url_' + current_counter, self.create_autoit_function())


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
            target_path : str — local file path to open via FileProtocolHandler
                                if absent, opens notepad.exe as a benign default
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_path = kwargs.get("target_path", None)
        if self.target_path:
            print(f"[*] Setting target_path attribute : {self.target_path}")
        else:
            print("[*] No target_path provided — will open notepad.exe as default")

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
        ; <      Url.dll Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Url_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Url_{}()

            ; Creates a Url.dll Interaction via CMD

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
        Builds the rundll32 url.dll command to type into the CMD window.
        Uses FileProtocolHandler to open a local file path.
        Falls back to notepad.exe if no target_path is provided.
        """
        typing_text = '\n'

        # Determine the file to open — fall back to a benign default
        target = self.target_path if self.target_path else 'C:\\Windows\\System32\\notepad.exe'

        rundll_cmd = 'rundll32.exe url.dll,FileProtocolHandler {}'.format(target)
        typing_text += 'Send("' + self._escape_send(rundll_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Url AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
