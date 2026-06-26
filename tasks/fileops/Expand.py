
# #######################################################################
#
#  Task : Expand Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of expand.exe for extracting cabinet (.cab)
 files — common when IT staff deploy Windows updates, drivers, or patches.

"""

# LOLBAS: expand.exe — Legitimate use: extracting Windows driver and update cabinet files

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Expand(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: expand.exe — Legitimate use: extracting Windows driver and update cabinet files
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Expand, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Expand'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > expand >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > expand >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.source = 'C:\\Windows\\System32\\cabinet.cab'
        self.dest = 'C:\\Temp\\expanded'
        self.list_only = False

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Expand Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the source cabinet file using 'source'
        3: Set the destination directory using 'dest'
        4: Optionally list contents only using 'list_only'
        5: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Expand Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Expand interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Expand_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_source(self, arg):
        """
        Set the path to the .cab file to expand.
        Default: C:\\Windows\\System32\\cabinet.cab
        Example: source C:\\Updates\\windows10.0-kb5000000.cab
        """
        if self.taskstarted:
            if arg:
                self.source = arg
                print(self.cl.green("[*] Source cabinet file set to: {}".format(self.source)))
            else:
                print(self.cl.green("[*] Using default source cabinet file: {}".format(self.source)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Expand Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_dest(self, arg):
        """
        Set the destination directory for extracted files.
        Default: C:\\Temp\\expanded
        Example: dest C:\\Drivers\\extracted
        """
        if self.taskstarted:
            if arg:
                self.dest = arg
                print(self.cl.green("[*] Destination directory set to: {}".format(self.dest)))
            else:
                print(self.cl.green("[*] Using default destination directory: {}".format(self.dest)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Expand Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_list_only(self, arg):
        """
        If enabled, list the contents of the cabinet file without extracting (expand -D).
        Pass 'true' to enable, 'false' to disable.
        Example: list_only true
        """
        if self.taskstarted:
            if arg.lower() in ('true', 'yes', '1'):
                self.list_only = True
                print(self.cl.green("[*] List-only mode enabled (expand -D <source>)"))
            else:
                self.list_only = False
                print(self.cl.green("[*] List-only mode disabled; will extract files"))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Expand Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current Expand task settings
        """
        print(self.cl.green("[?] Currently Assigned Expand Settings"))
        print("[>] Source (.cab) : {}".format(self.source))
        print("[>] Destination   : {}".format(self.dest))
        print("[>] List only     : {}".format(self.list_only))


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
        self.source = 'C:\\Windows\\System32\\cabinet.cab'
        self.dest = 'C:\\Temp\\expanded'
        self.list_only = False


    ######################################################################
    # Expand AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Expand_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_expand()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads source, dest, and list_only from kwargs.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.source = kwargs.get("source", 'C:\\Windows\\System32\\cabinet.cab')
        print(f"[*] Setting the source attribute : {self.source}")

        self.dest = kwargs.get("dest", 'C:\\Temp\\expanded')
        print(f"[*] Setting the dest attribute : {self.dest}")

        self.list_only = kwargs.get("list_only", False)
        print(f"[*] Setting the list_only attribute : {self.list_only}")

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
        ; <      Expand Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Expand_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for expand commands
        """

        _open_commandshell = """

        Func Expand_{}()

            ; Creates an Expand Interaction via CMD

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
        Builds the expand command:
          list_only : expand -D <source>
          extract   : expand <source> -F:* <dest>
        """
        typing_text = '\n'

        escaped_source = self._escape_send(self.source)

        if self.list_only:
            expand_cmd = 'expand -D {}'.format(escaped_source)
        else:
            escaped_dest = self._escape_send(self.dest)
            expand_cmd = 'expand {} -F:* {}'.format(escaped_source, escaped_dest)

        typing_text += 'Send("{}{}")\n'.format(expand_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_expand(self):
        """
        Closes the Expand function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
