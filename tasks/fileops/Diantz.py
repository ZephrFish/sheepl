
# LOLBAS: diantz.exe — Legitimate use: compressing files into cabinet (.cab) archives

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of diantz.exe to compress a local file into a
 cabinet (.cab) archive. Diantz is the Windows cabinet compression utility
 (functionally equivalent to makecab.exe).

 Requires a source_file path and a destination cab file path.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Diantz(BaseCMD):
    """
    # LOLBAS: diantz.exe — Legitimate use: compressing files into cabinet (.cab) archives

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Diantz, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Diantz'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > diantz >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > diantz >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Source file to compress
        self.source_file = None
        # Destination cabinet file
        self.dest_cab = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Diantz Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source file to compress using 'source_file <path>'
        3: Set the destination CAB file using 'dest_cab <path>'
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
    #  Diantz Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Diantz interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Diantz_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source_file(self, source_file):
        """
        Set the path of the file to compress into a CAB archive.
        Example: source_file C:\\Users\\User\\Documents\\report.txt
        """
        if source_file:
            if self.taskstarted:
                self.source_file = source_file.strip()
                print(self.cl.green("[*] Source file set to: {}".format(self.source_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Diantz Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a source file path."))


    def do_dest_cab(self, dest_cab):
        """
        Set the destination path for the output CAB file.
        Example: dest_cab C:\\Users\\User\\Documents\\archive.cab
        """
        if dest_cab:
            if self.taskstarted:
                self.dest_cab = dest_cab.strip()
                print(self.cl.green("[*] Destination CAB set to: {}".format(self.dest_cab)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Diantz Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a destination CAB file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Diantz configuration
        """
        print(self.cl.green("[?] Currently Assigned Diantz Configuration"))
        print("[>] Source File : {}".format(self.source_file if self.source_file else "(not set)"))
        print("[>] Destination CAB : {}".format(self.dest_cab if self.dest_cab else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.source_file:
                print(self.cl.red("[!] <ERROR> source_file is required. Set it with 'source_file <path>'."))
                return
            if not self.dest_cab:
                print(self.cl.red("[!] <ERROR> dest_cab is required. Set it with 'dest_cab <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.source_file = None
        self.dest_cab = None


    ######################################################################
    # Diantz AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Diantz_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_diantz()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            source_file : str — path to the file to compress
            dest_cab    : str — path for the output CAB file
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source_file = kwargs.get("source_file", None)
        self.dest_cab = kwargs.get("dest_cab", None)

        if self.source_file:
            print(f"[*] Setting source_file attribute : {self.source_file}")
        else:
            print("[!] <ERROR> No source_file provided — this is required.")

        if self.dest_cab:
            print(f"[*] Setting dest_cab attribute : {self.dest_cab}")
        else:
            print("[!] <ERROR> No dest_cab provided — this is required.")

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
        ; <      Diantz Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Diantz_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Diantz_{}()

            ; Creates a Diantz Interaction via CMD

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
        Builds the diantz command to type into the CMD window.
        Compresses the source file into the destination CAB archive.
        """
        typing_text = '\n'

        # Build the diantz compress command
        diantz_cmd = 'diantz.exe {} {}'.format(self.source_file, self.dest_cab)
        typing_text += 'Send("' + self._escape_send(diantz_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_diantz(self):
        """
        Closes the Diantz AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
