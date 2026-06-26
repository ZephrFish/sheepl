
# LOLBAS: wuauclt.exe — Legitimate use: triggering Windows Update detection and reporting update status
# #######################################################################
#
#  Task : Wuauclt Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of wuauclt.exe to detect Windows updates
 and report update status via the Windows Update client.

 Takes an optional update_server parameter to target a specific WSUS
 server path; if absent, triggers a standard update detection cycle.

 The master script will already define the typing speed as part of
 the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Wuauclt(BaseCMD):
    """
    # LOLBAS: wuauclt.exe — Legitimate use: triggering Windows Update detection and reporting update status

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Wuauclt, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Wuauclt'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wuauclt >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wuauclt >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional WSUS server path for targeted update detection
        self.update_server = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Wuauclt Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a WSUS server path using 'update_server <path>'
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
    #  Wuauclt Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Wuauclt interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Wuauclt_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_update_server(self, update_server):
        """
        Optionally set a WSUS server URL to target with /ResetAuthorization /DetectNow.
        If not set, a standard /DetectNow cycle is run.
        Example: update_server http://wsus.corp.local:8530
        """
        if update_server:
            if self.taskstarted:
                self.update_server = update_server.strip()
                print(self.cl.green("[*] Update server set to: {}".format(self.update_server)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Wuauclt Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a WSUS server URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned Wuauclt configuration
        """
        print(self.cl.green("[?] Currently Assigned Wuauclt Configuration"))
        print("[>] Update Server : {}".format(self.update_server if self.update_server else "(not set — will run /DetectNow only)"))


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
        self.update_server = None


    ######################################################################
    # Wuauclt AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Wuauclt_' + current_counter, self.create_autoit_function())


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
            update_server : str — WSUS server URL to target with /ResetAuthorization /DetectNow
                                  if absent, only /DetectNow is run
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.update_server = kwargs.get("update_server", None)
        if self.update_server:
            print(f"[*] Setting update_server attribute : {self.update_server}")
        else:
            print("[*] No update_server provided — will run standard /DetectNow cycle")

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
        ; <      Wuauclt Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Wuauclt_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Wuauclt_{}()

            ; Creates a Wuauclt Interaction via CMD

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
        Builds the wuauclt commands to type into the CMD window.
        Always triggers a standard update detection cycle with /DetectNow.
        If update_server is set, also runs /ResetAuthorization targeting that server.
        """
        typing_text = '\n'

        # Always trigger a standard Windows Update detection cycle
        detect_cmd = 'wuauclt /DetectNow'
        typing_text += 'Send("' + self._escape_send(detect_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Optionally target a specific WSUS server with reset authorization
        if self.update_server:
            reset_cmd = 'wuauclt /ResetAuthorization /DetectNow'
            typing_text += 'Send("' + self._escape_send(reset_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Wuauclt AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
