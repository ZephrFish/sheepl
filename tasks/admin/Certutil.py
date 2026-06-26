
# #######################################################################
#
#  Task : Certutil Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of certutil.exe for file hash verification
 and certificate store queries.

"""

# LOLBAS: certutil.exe — Legitimate use: file hash verification and certificate store queries

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Certutil(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: certutil.exe — Legitimate use: file hash verification and certificate store queries
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Certutil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Certutil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > certutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > certutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        self.target_file = 'C:\\Windows\\System32\\notepad.exe'
        self.query_store = False

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Certutil Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the target file using 'target_file'
        3: Optionally enable cert store query using 'query_store'
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
    #  Certutil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Certutil interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Certutil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_target_file(self, arg):
        """
        Set the path of the file to verify with SHA256.
        Default: C:\\Windows\\System32\\notepad.exe
        Example: target_file C:\\Windows\\System32\\calc.exe
        """
        if self.taskstarted:
            if arg:
                self.target_file = arg
                print(self.cl.green("[*] Target file set to: {}".format(self.target_file)))
            else:
                print(self.cl.green("[*] Using default target file: {}".format(self.target_file)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Certutil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_query_store(self, arg):
        """
        Enable querying the local certificate store (My).
        Pass 'true' to enable, 'false' to disable.
        Example: query_store true
        """
        if self.taskstarted:
            if arg.lower() in ('true', 'yes', '1'):
                self.query_store = True
                print(self.cl.green("[*] Certificate store query enabled (store: My)"))
            else:
                self.query_store = False
                print(self.cl.green("[*] Certificate store query disabled"))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Certutil Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current Certutil task settings
        """
        print(self.cl.green("[?] Currently Assigned Certutil Settings"))
        print("[>] Target file  : {}".format(self.target_file))
        print("[>] Query store  : {}".format(self.query_store))


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
        self.target_file = 'C:\\Windows\\System32\\notepad.exe'
        self.query_store = False


    ######################################################################
    # Certutil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Certutil_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_certutil()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads target_file and query_store from kwargs.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.target_file = kwargs.get("target_file", 'C:\\Windows\\System32\\notepad.exe')
        print(f"[*] Setting the target_file attribute : {self.target_file}")

        self.query_store = kwargs.get("query_store", False)
        print(f"[*] Setting the query_store attribute : {self.query_store}")

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
        ; <      Certutil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Certutil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for certutil commands
        """

        _open_commandshell = """

        Func Certutil_{}()

            ; Creates a Certutil Interaction via CMD

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
        Builds the certutil command sequence:
          certutil -hashfile <target_file> SHA256
          (optional) certutil -store My
          exit
        """
        typing_text = '\n'

        escaped_target = self._escape_send(self.target_file)
        hashfile_cmd = 'certutil -hashfile {} SHA256'.format(escaped_target)
        typing_text += 'Send("{}{}")\n'.format(hashfile_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        if self.query_store:
            typing_text += 'Send("certutil -store My{}")\n'.format('{ENTER}')
            typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_certutil(self):
        """
        Closes the Certutil function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
