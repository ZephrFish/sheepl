
# LOLBAS: te.exe — Legitimate use: running TAEF test suites (WSC or DLL) during development
# DEVELOPER-ONLY: Requires Microsoft Test Authoring and Execution Framework (TAEF) from the WDK/SDK

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of te.exe (Test Authoring and Execution Framework runner)
 to execute test suites stored in Windows Script Component (.wsc) files or DLL test modules.

 Takes a required test_file parameter (path to a .wsc or .dll test module).
 Optionally accepts a select_query to filter which tests to run via /select.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Te(BaseCMD):
    """
    # LOLBAS: te.exe — Legitimate use: running TAEF test suites (.wsc or .dll) during development
    # DEVELOPER-ONLY: Requires Microsoft Test Authoring and Execution Framework (TAEF) from the WDK/SDK

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Te, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Te'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > te >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > te >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .wsc or .dll test module to execute
        self.test_file = None
        # Optional /select query to filter specific tests
        self.select_query = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Te (TAEF) Interaction.
        [!] DEVELOPER-ONLY: Requires Microsoft Test Authoring and Execution Framework (TAEF).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the test file path using 'test_file <path>'
        3: Optionally filter tests using 'select_query <query>'
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
    #  Te Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Te interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Te_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_test_file(self, test_file):
        """
        Set the path to the .wsc or .dll test module to execute with te.exe.
        Example: test_file C:\\Tests\\MyTests.wsc
        Example: test_file C:\\Tests\\MyTestModule.dll
        """
        if test_file:
            if self.taskstarted:
                self.test_file = test_file.strip()
                print(self.cl.green("[*] Test file set to: {}".format(self.test_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Te Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a test file (.wsc or .dll)."))


    def do_select_query(self, select_query):
        """
        Optionally set a /select filter query to run specific tests.
        Example: select_query @Name='MyTest'
        """
        if select_query:
            if self.taskstarted:
                self.select_query = select_query.strip()
                print(self.cl.green("[*] Select query set to: {}".format(self.select_query)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Te Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a select query string."))


    def do_assigned(self, arg):
        """
        Get the current assigned Te configuration
        """
        print(self.cl.green("[?] Currently Assigned Te Configuration"))
        print("[>] Test File    : {}".format(self.test_file if self.test_file else "(not set)"))
        print("[>] Select Query : {}".format(self.select_query if self.select_query else "(not set — all tests will run)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.test_file:
                print(self.cl.red("[!] <ERROR> A test_file path is required before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.test_file = None
        self.select_query = None


    ######################################################################
    # Te AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Te_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_te()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            test_file    : str — path to the .wsc or .dll test module

        Optional JSON keys:
            select_query : str — /select filter query to run specific tests
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.test_file = kwargs.get("test_file", None)
        if self.test_file:
            print(f"[*] Setting test_file attribute : {self.test_file}")
        else:
            print("[!] No test_file provided — this is required for Te execution")

        self.select_query = kwargs.get("select_query", None)
        if self.select_query:
            print(f"[*] Setting select_query attribute : {self.select_query}")
        else:
            print("[*] No select_query provided — all tests in the module will run")

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
        ; <      Te (TAEF) Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Te_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Te_{}()

            ; Creates a Te (TAEF) Interaction via CMD

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
        Builds the te.exe command to type into the CMD window.
        Runs the specified test file, optionally filtered by a /select query.
        """
        typing_text = '\n'

        # Build the te.exe command
        te_cmd = 'te.exe {}'.format(self.test_file)
        if self.select_query:
            te_cmd += ' /select:{}'.format(self.select_query)

        typing_text += 'Send("' + self._escape_send(te_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_te(self):
        """
        Closes the Te AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
