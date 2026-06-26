
# #######################################################################
#
#  Task : MakeCab Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of makecab.exe for creating cabinet archive
 files from log files or driver packages for support ticket submission
 and deployment workflows.

"""

# LOLBAS: makecab.exe — Legitimate use: log file compression for support ticket submission

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MakeCab(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: makecab.exe — Legitimate use: log file compression for support ticket submission
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MakeCab, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MakeCab'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > makecab >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > makecab >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.source = 'C:\\Windows\\Logs\\CBS\\CBS.log'
        self.dest = ''

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] MakeCab Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source file using 'source'
        3: Optionally set the destination using 'dest'
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
    #  MakeCab Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MakeCab interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MakeCab_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source(self, arg):
        """
        Set the path of the file to compress into a cabinet archive.
        Default: C:\\Windows\\Logs\\CBS\\CBS.log
        Example: source C:\\Windows\\Logs\\CBS\\CBS.log
        """
        if self.taskstarted:
            if arg:
                self.source = arg
                print(self.cl.green("[*] Source file set to: {}".format(self.source)))
            else:
                print(self.cl.green("[*] Using default source file: {}".format(self.source)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new MakeCab Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_dest(self, arg):
        """
        Set the destination path for the output cabinet (.cab) file.
        If not set, defaults to the source path with a .cab extension.
        Example: dest C:\\Temp\\CBS.cab
        """
        if self.taskstarted:
            if arg:
                self.dest = arg
                print(self.cl.green("[*] Destination set to: {}".format(self.dest)))
            else:
                print(self.cl.green("[*] Destination will default to source path with .cab extension"))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new MakeCab Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current MakeCab task settings
        """
        print(self.cl.green("[?] Currently Assigned MakeCab Settings"))
        print("[>] Source : {}".format(self.source))
        effective_dest = self.dest if self.dest else self._default_dest()
        print("[>] Dest   : {}".format(effective_dest))


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

        # reset task-specific variables for next interaction
        self.source = 'C:\\Windows\\Logs\\CBS\\CBS.log'
        self.dest = ''


    ######################################################################
    # MakeCab AutoIT Block Definition
    #######################################################################


    def _default_dest(self):
        """
        Derives the default destination path by appending .cab to the source path.
        """
        return self.source + '.cab'


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MakeCab_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_makecab()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads source and dest from kwargs.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source = kwargs.get("source", 'C:\\Windows\\Logs\\CBS\\CBS.log')
        print(f"[*] Setting the source attribute : {self.source}")

        self.dest = kwargs.get("dest", '')
        print(f"[*] Setting the dest attribute : {self.dest}")

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      MakeCab Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "MakeCab_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for the makecab command
        """

        _open_commandshell = """

        Func MakeCab_{}()

            ; Creates a MakeCab Interaction via CMD

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
        Builds the makecab command:
          makecab <source> <dest>
        where dest defaults to source path with .cab extension if not set.
        """
        typing_text = '\n'

        dest = self.dest if self.dest else self._default_dest()
        escaped_source = self._escape_send(self.source)
        escaped_dest = self._escape_send(dest)

        makecab_cmd = 'makecab {} {}'.format(escaped_source, escaped_dest)
        typing_text += 'Send("{}{}")\n'.format(makecab_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_makecab(self):
        """
        Closes the MakeCab function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
