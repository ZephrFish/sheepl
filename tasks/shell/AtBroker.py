
# LOLBAS: AtBroker.exe — Legitimate use: starting registered Assistive Technology (AT) services

# #######################################################################
#
#  Task : AtBroker Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of ATBroker.exe to start a registered
 Assistive Technology (AT) service on Windows. ATBroker is the helper
 binary for Windows Assistive Technology and lives in System32.

 Takes a required at_name parameter specifying the registered AT to start.
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


class AtBroker(BaseCMD):
    """
    # LOLBAS: AtBroker.exe — Legitimate use: starting registered Assistive Technology (AT) services

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(AtBroker, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'AtBroker'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > atbroker >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > atbroker >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Name of the registered AT to start (e.g. 'narrator', 'magnifier')
        self.at_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] AtBroker Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the Assistive Technology name using 'at_name <name>'
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
    #  AtBroker Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new AtBroker interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'AtBroker_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_at_name(self, at_name):
        """
        Set the registered Assistive Technology name to start.
        Example: at_name narrator
        Example: at_name magnifier
        """
        if at_name:
            if self.taskstarted:
                self.at_name = at_name.strip()
                print(self.cl.green("[*] AT name set to: {}".format(self.at_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new AtBroker Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an Assistive Technology name."))


    def do_assigned(self, arg):
        """
        Get the current assigned AtBroker configuration
        """
        print(self.cl.green("[?] Currently Assigned AtBroker Configuration"))
        print("[>] AT Name : {}".format(self.at_name if self.at_name else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.at_name:
                print(self.cl.red("[!] <ERROR> You must set an AT name using 'at_name <name>' before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.at_name = None


    ######################################################################
    # AtBroker AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('AtBroker_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_atbroker()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            at_name : str — name of the registered Assistive Technology to start
                            e.g. 'narrator', 'magnifier', 'osk'
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.at_name = kwargs.get("at_name", None)
        if self.at_name:
            print(f"[*] Setting at_name attribute : {self.at_name}")
        else:
            print("[!] <ERROR> No at_name provided — cannot build AtBroker task")
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
        ; <      AtBroker Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "AtBroker_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func AtBroker_{}()

            ; Creates an AtBroker Interaction via CMD

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
        Builds the ATBroker command to type into the CMD window.
        Starts the named registered Assistive Technology via ATBroker.exe /start.
        """
        typing_text = '\n'

        # Start the registered AT using ATBroker /start
        at_cmd = 'ATBroker.exe /start {}'.format(self.at_name)
        typing_text += 'Send("' + self._escape_send(at_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_atbroker(self):
        """
        Closes the AtBroker AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
