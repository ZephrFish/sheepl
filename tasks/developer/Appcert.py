
# LOLBAS: appcert.exe — Legitimate use: running Windows App Certification Kit tests on desktop applications
# DEVELOPER-ONLY: requires Windows Kits 10 / App Certification Kit install (C:\Program Files (x86)\Windows Kits\10\App Certification Kit\)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of appcert.exe to run Windows App Certification
 Kit tests against a desktop application executable and produce an XML report.

 Takes a setup_path parameter (absolute path to the .exe under test) and an
 optional report_path parameter for the XML output; defaults to a temp location.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Appcert(BaseCMD):
    """
    # LOLBAS: appcert.exe — Legitimate use: running Windows App Certification Kit tests on desktop applications
    # DEVELOPER-ONLY: requires Windows Kits 10 / App Certification Kit install

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Appcert, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Appcert'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > appcert >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > appcert >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the application executable to certify
        self.setup_path = None
        # Output path for the XML report
        self.report_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Appcert Interaction.
        [!] DEVELOPER-ONLY: requires Windows App Certification Kit (Windows Kits 10).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the path to the .exe to test using 'setup_path <absolute_path>'
        3: Optionally set the XML report output path using 'report_path <absolute_path>'
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
    #  Appcert Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Appcert interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Appcert_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_setup_path(self, setup_path):
        """
        Set the absolute path to the application executable (.exe) to certify.
        Example: setup_path C:\\MyApp\\MyApp.exe
        """
        if setup_path:
            if self.taskstarted:
                self.setup_path = setup_path.strip()
                print(self.cl.green("[*] Setup path set to: {}".format(self.setup_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Appcert Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an absolute path to the .exe file."))


    def do_report_path(self, report_path):
        """
        Optionally set the absolute path for the XML certification report output.
        If not set, defaults to C:\\Temp\\appcert_report.xml
        Example: report_path C:\\Reports\\certify_output.xml
        """
        if report_path:
            if self.taskstarted:
                self.report_path = report_path.strip()
                print(self.cl.green("[*] Report path set to: {}".format(self.report_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Appcert Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an absolute path for the XML report."))


    def do_assigned(self, arg):
        """
        Get the current assigned Appcert configuration
        """
        print(self.cl.green("[?] Currently Assigned Appcert Configuration"))
        print("[>] Setup Path  : {}".format(self.setup_path if self.setup_path else "(not set)"))
        print("[>] Report Path : {}".format(self.report_path if self.report_path else "(not set — will use C:\\Temp\\appcert_report.xml)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.setup_path:
                print(self.cl.red("[!] <ERROR> setup_path must be set before completing. Use 'setup_path <absolute_path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.setup_path = None
        self.report_path = None


    ######################################################################
    # Appcert AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Appcert_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_appcert()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            setup_path  : str — absolute path to the .exe to certify

        Optional JSON keys:
            report_path : str — absolute path for the XML report output
                                defaults to C:\\Temp\\appcert_report.xml
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.setup_path = kwargs.get("setup_path", None)
        self.report_path = kwargs.get("report_path", None)

        if self.setup_path:
            print(f"[*] Setting setup_path attribute : {self.setup_path}")
        else:
            print("[!] <ERROR> setup_path is required for Appcert task — skipping block.")
            return

        if self.report_path:
            print(f"[*] Setting report_path attribute : {self.report_path}")
        else:
            print("[*] No report_path provided — will use C:\\Temp\\appcert_report.xml")

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
        ; <      Appcert Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Appcert_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Appcert_{}()

            ; Creates an Appcert Interaction via CMD

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
        Builds the appcert command to type into the CMD window.
        Runs a Windows App Certification Kit test against the configured .exe
        and writes the XML report to the configured (or default) report path.
        """
        typing_text = '\n'

        # Resolve report path — default if none provided
        report = self.report_path if self.report_path else 'C:\\Temp\\appcert_report.xml'

        appcert_cmd = (
            'appcert.exe test -apptype desktop'
            ' -setuppath {}'
            ' -reportoutputpath {}'.format(self.setup_path, report)
        )

        typing_text += 'Send("' + self._escape_send(appcert_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_appcert(self):
        """
        Closes the Appcert AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
