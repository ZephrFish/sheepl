
# LOLBAS: Mshtml.dll — Legitimate use: printing HTML documents via rundll32 PrintHTML export

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of Mshtml.dll to print an HTML file using
 the PrintHTML export function via rundll32.exe.

 Takes a required html_path parameter pointing to the .html or .htm
 file to print.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Mshtml(BaseCMD):
    """
    # LOLBAS: Mshtml.dll — Legitimate use: printing HTML documents via the PrintHTML export

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Mshtml, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Mshtml'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mshtml >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mshtml >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the HTML file to print
        self.html_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Mshtml Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the HTML file to print using 'html_path <path>'
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
    #  Mshtml Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Mshtml interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Mshtml_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_html_path(self, html_path):
        """
        Set the path to the HTML file to print via Mshtml.dll PrintHTML.
        Example: html_path C:\\Users\\Public\\report.html
        """
        if html_path:
            if self.taskstarted:
                self.html_path = html_path.strip()
                print(self.cl.green("[*] HTML path set to: {}".format(self.html_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Mshtml Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to an HTML file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Mshtml configuration
        """
        print(self.cl.green("[?] Currently Assigned Mshtml Configuration"))
        print("[>] HTML Path : {}".format(self.html_path if self.html_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.html_path:
                print(self.cl.red("[!] <ERROR> html_path must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.html_path = None


    ######################################################################
    # Mshtml AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Mshtml_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_mshtml()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            html_path : str — absolute path to the HTML file to print
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.html_path = kwargs.get("html_path", None)
        if self.html_path:
            print(f"[*] Setting html_path attribute : {self.html_path}")
        else:
            print("[!] <ERROR> No html_path provided — this is required for Mshtml PrintHTML.")
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
        ; <      Mshtml Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Mshtml_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Mshtml_{}()

            ; Creates an Mshtml Interaction via CMD

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
        Builds the rundll32 Mshtml.dll,PrintHTML command to type into the CMD window.
        """
        typing_text = '\n'

        # Invoke Mshtml.dll PrintHTML via rundll32
        print_cmd = 'rundll32.exe Mshtml.dll,PrintHTML "{}"'.format(self.html_path)
        typing_text += 'Send("' + self._escape_send(print_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_mshtml(self):
        """
        Closes the Mshtml AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
