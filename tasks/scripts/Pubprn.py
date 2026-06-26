
# LOLBAS: pubprn.vbs — Legitimate use: publishing a shared printer to Active Directory
# SERVER-ONLY: Requires Active Directory and Windows Server print services to publish printers

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of pubprn.vbs to publish a shared printer
 to Active Directory. pubprn.vbs is a Windows Script Host script located
 in C:\\Windows\\System32\\Printing_Admin_Scripts\\en-US\\ used by sysadmins
 to automate printer publishing in domain environments.

 Requires a print server hostname and a shared printer name.
 NOTE: This task requires a Windows Server environment with Active Directory.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Pubprn(BaseCMD):
    """
    # LOLBAS: pubprn.vbs — Legitimate use: publishing a shared printer to Active Directory
    # SERVER-ONLY: Requires Active Directory and Windows Server print services

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Pubprn, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Pubprn'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > pubprn >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > pubprn >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.print_server = None
        self.printer_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Pubprn Interaction.
        [!] SERVER-ONLY: Requires Active Directory and Windows Server print services.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the print server using 'print_server <hostname>'
        3: Set the shared printer name using 'printer_name <name>'
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
    #  Pubprn Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Pubprn interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Pubprn_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_print_server(self, print_server):
        """
        Set the hostname of the print server that hosts the shared printer.
        Example: print_server printserver01
        """
        if print_server:
            if self.taskstarted:
                self.print_server = print_server.strip()
                print(self.cl.green("[*] Print server set to: {}".format(self.print_server)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Pubprn Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a print server hostname."))


    def do_printer_name(self, printer_name):
        """
        Set the name of the shared printer to publish to Active Directory.
        Example: printer_name HP_LaserJet_Floor2
        """
        if printer_name:
            if self.taskstarted:
                self.printer_name = printer_name.strip()
                print(self.cl.green("[*] Printer name set to: {}".format(self.printer_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Pubprn Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a printer name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Pubprn configuration
        """
        print(self.cl.green("[?] Currently Assigned Pubprn Configuration"))
        print("[>] Print Server  : {}".format(self.print_server if self.print_server else "(not set)"))
        print("[>] Printer Name  : {}".format(self.printer_name if self.printer_name else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.print_server:
                print(self.cl.red("[!] <ERROR> print_server is required. Set it with 'print_server <hostname>'."))
                return
            if not self.printer_name:
                print(self.cl.red("[!] <ERROR> printer_name is required. Set it with 'printer_name <name>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.print_server = None
        self.printer_name = None


    ######################################################################
    # Pubprn AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Pubprn_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_pubprn()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            print_server : str — hostname of the print server
            printer_name : str — shared printer name to publish to AD
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.print_server = kwargs.get("print_server", None)
        self.printer_name = kwargs.get("printer_name", None)

        if self.print_server:
            print(f"[*] Setting print_server attribute : {self.print_server}")
        else:
            print("[!] <ERROR> print_server is required for Pubprn task")

        if self.printer_name:
            print(f"[*] Setting printer_name attribute : {self.printer_name}")
        else:
            print("[!] <ERROR> printer_name is required for Pubprn task")

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
        ; <      Pubprn Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Pubprn_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Pubprn_{}()

            ; Creates a Pubprn Interaction via CMD

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
        Builds the cscript pubprn.vbs command to type into the CMD window.
        Publishes the specified shared printer to Active Directory.
        """
        typing_text = '\n'

        # Build the pubprn.vbs command to publish the printer to AD
        pubprn_cmd = (
            'cscript //nologo C:\\Windows\\System32\\Printing_Admin_Scripts\\en-US\\pubprn.vbs '
            '\\\\{} "LDAP:"'.format(self.print_server)
        )
        typing_text += 'Send("' + self._escape_send(pubprn_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_pubprn(self):
        """
        Closes the Pubprn AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
