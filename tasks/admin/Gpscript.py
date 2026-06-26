
# LOLBAS: gpscript.exe — Legitimate use: executing logon and startup scripts configured in Group Policy

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate administrative use of gpscript.exe to run
 Group Policy scripts (logon or startup) as configured by domain policy.

 Takes a required script_phase parameter ('logon' or 'startup').
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Gpscript(BaseCMD):
    """
    # LOLBAS: gpscript.exe — Legitimate use: executing logon and startup scripts configured in Group Policy

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Gpscript, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Gpscript'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > gpscript >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > gpscript >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Script phase: 'logon' or 'startup'
        self.script_phase = 'logon'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Gpscript Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the script phase using 'script_phase <logon|startup>'
        3: Complete the interaction using 'complete'
        ----------------------------------
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Gpscript Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Gpscript interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Gpscript_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_script_phase(self, script_phase):
        """
        Set the Group Policy script phase to execute.
        Valid values: logon, startup
        Example: script_phase logon
        Example: script_phase startup
        """
        if script_phase:
            if self.taskstarted:
                phase = script_phase.strip().lower()
                if phase in ('logon', 'startup'):
                    self.script_phase = phase
                    print(self.cl.green("[*] Script phase set to: {}".format(self.script_phase)))
                else:
                    print(self.cl.red("[!] <ERROR> Valid phases are 'logon' or 'startup'."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Gpscript Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a script phase (logon or startup)."))


    def do_assigned(self, arg):
        """
        Get the current assigned Gpscript configuration
        """
        print(self.cl.green("[?] Currently Assigned Gpscript Configuration"))
        print("[>] Script Phase : {}".format(self.script_phase))


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
        self.script_phase = 'logon'


    ######################################################################
    # Gpscript AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Gpscript_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_gpscript()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            script_phase : str — 'logon' or 'startup' (default: 'logon')
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        phase = kwargs.get("script_phase", "logon").strip().lower()
        if phase in ('logon', 'startup'):
            self.script_phase = phase
        else:
            self.script_phase = 'logon'
        print(f"[*] Setting script_phase attribute : {self.script_phase}")

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
        ; <      Gpscript Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Gpscript_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Gpscript_{}()

            ; Creates a Gpscript Interaction via CMD

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
        Builds the gpscript command to type into the CMD window.
        Runs the configured Group Policy script phase (logon or startup).
        """
        typing_text = '\n'

        gpscript_cmd = 'gpscript /{}'.format(self.script_phase)
        typing_text += 'Send("' + self._escape_send(gpscript_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_gpscript(self):
        """
        Closes the Gpscript AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
