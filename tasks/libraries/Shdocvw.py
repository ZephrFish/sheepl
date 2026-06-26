
# LOLBAS: shdocvw.dll — Legitimate use: opening URLs and web shortcuts via Shell Doc Object and Control Library
# #######################################################################
#
#  Task : Shdocvw Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of shdocvw.dll via rundll32.exe to open a
 URL or web shortcut (.url) file using the OpenURL exported function.
 This reflects normal shell behaviour for launching internet shortcuts.

 Takes a url_file parameter specifying the absolute path to a .url file.
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


class Shdocvw(BaseCMD):
    """
    # LOLBAS: shdocvw.dll — Legitimate use: opening URLs and web shortcuts via rundll32

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Shdocvw, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Shdocvw'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > shdocvw >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > shdocvw >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .url file to open
        self.url_file = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Shdocvw Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the .url file path using 'url_file <absolute_path>'
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
    #  Shdocvw Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Shdocvw interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Shdocvw_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_url_file(self, url_file):
        """
        Set the absolute path to the .url file to open via shdocvw.dll OpenURL.
        Example: url_file C:\\Users\\Public\\shortcut.url
        """
        if url_file:
            if self.taskstarted:
                self.url_file = url_file.strip()
                print(self.cl.green("[*] URL file path set to: {}".format(self.url_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Shdocvw Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an absolute path to a .url file."))


    def do_assigned(self, arg):
        """
        Get the current assigned Shdocvw configuration
        """
        print(self.cl.green("[?] Currently Assigned Shdocvw Configuration"))
        print("[>] URL File : {}".format(self.url_file if self.url_file else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.url_file:
                print(self.cl.red("[!] <ERROR> url_file must be set before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.url_file = None


    ######################################################################
    # Shdocvw AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Shdocvw_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_shdocvw()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            url_file : str — absolute path to the .url file to open via OpenURL
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.url_file = kwargs.get("url_file", None)
        if self.url_file:
            print(f"[*] Setting url_file attribute : {self.url_file}")
        else:
            print("[!] <ERROR> url_file is required for Shdocvw task.")
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
        ; <      Shdocvw Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Shdocvw_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Shdocvw_{}()

            ; Creates a Shdocvw Interaction via CMD

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
        Builds the rundll32 shdocvw.dll OpenURL command to type into the CMD window.
        Calls OpenURL with the specified .url file path.
        """
        typing_text = '\n'

        # rundll32.exe shdocvw.dll,OpenURL <url_file>
        run_cmd = 'rundll32.exe shdocvw.dll,OpenURL {}'.format(self.url_file)
        typing_text += 'Send("' + self._escape_send(run_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_shdocvw(self):
        """
        Closes the Shdocvw AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
