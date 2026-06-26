
# LOLBAS: PrintBrm.exe — Legitimate use: backup and restore Windows printer configurations
# #######################################################################
#
#  Task : PrintBrm Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of PrintBrm.exe to backup printer queues
 and configurations to a ZIP archive, or restore them from one.

 PrintBrm.exe resides at C:\Windows\System32\spool\tools\PrintBrm.exe
 and is used by administrators to migrate print spooler settings.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class PrintBrm(BaseCMD):
    """
    # LOLBAS: PrintBrm.exe — Legitimate use: backup and restore Windows printer configurations

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(PrintBrm, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PrintBrm'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > printbrm >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > printbrm >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Operation: 'backup' (-b) or 'restore' (-r)
        self.operation = 'backup'
        # Destination folder for backup, or source folder for restore
        self.target_dir = r'C:\PrinterBackup'
        # ZIP file path for backup output or restore input
        self.zip_file = r'C:\PrinterBackup\printers.zip'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] PrintBrm Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set operation with 'operation <backup|restore>'
        3: Set target folder with 'target_dir <path>'
        4: Set zip file path with 'zip_file <path>'
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
    #  PrintBrm Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new PrintBrm interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'PrintBrm_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_operation(self, operation):
        """
        Set the PrintBrm operation: 'backup' or 'restore'.
        Default is 'backup'.
        Example: operation backup
        Example: operation restore
        """
        if operation:
            if self.taskstarted:
                op = operation.strip().lower()
                if op in ('backup', 'restore'):
                    self.operation = op
                    print(self.cl.green("[*] Operation set to: {}".format(self.operation)))
                else:
                    print(self.cl.red("[!] <ERROR> Operation must be 'backup' or 'restore'."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new PrintBrm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an operation (backup or restore)."))


    def do_target_dir(self, target_dir):
        """
        Set the folder path used for backup source or restore destination.
        Default is C:\\PrinterBackup
        Example: target_dir C:\\PrinterBackup
        """
        if target_dir:
            if self.taskstarted:
                self.target_dir = target_dir.strip()
                print(self.cl.green("[*] Target directory set to: {}".format(self.target_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new PrintBrm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a target directory path."))


    def do_zip_file(self, zip_file):
        """
        Set the ZIP file path for the backup archive or restore source.
        Default is C:\\PrinterBackup\\printers.zip
        Example: zip_file C:\\PrinterBackup\\printers.zip
        """
        if zip_file:
            if self.taskstarted:
                self.zip_file = zip_file.strip()
                print(self.cl.green("[*] ZIP file path set to: {}".format(self.zip_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new PrintBrm Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a zip file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned PrintBrm configuration
        """
        print(self.cl.green("[?] Currently Assigned PrintBrm Configuration"))
        print("[>] Operation   : {}".format(self.operation))
        print("[>] Target Dir  : {}".format(self.target_dir))
        print("[>] ZIP File    : {}".format(self.zip_file))


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
        self.operation = 'backup'
        self.target_dir = r'C:\PrinterBackup'
        self.zip_file = r'C:\PrinterBackup\printers.zip'


    ######################################################################
    # PrintBrm AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PrintBrm_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_printbrm()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            operation  : str — 'backup' or 'restore' (default: 'backup')
            target_dir : str — folder path for backup source or restore destination
            zip_file   : str — path to the ZIP archive file
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.operation = kwargs.get("operation", "backup")
        self.target_dir = kwargs.get("target_dir", r'C:\PrinterBackup')
        self.zip_file = kwargs.get("zip_file", r'C:\PrinterBackup\printers.zip')

        print(f"[*] Setting operation attribute : {self.operation}")
        print(f"[*] Setting target_dir attribute : {self.target_dir}")
        print(f"[*] Setting zip_file attribute : {self.zip_file}")

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
        ; <      PrintBrm Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "PrintBrm_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func PrintBrm_{}()

            ; Creates a PrintBrm Interaction via CMD

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
        Builds the PrintBrm command to type into the CMD window.
        Runs either a backup (-b) or restore (-r) operation.
        """
        typing_text = '\n'

        if self.operation == 'backup':
            # Backup: PrintBrm -b -d <dir> -f <zip>
            cmd_str = r'C:\Windows\System32\spool\tools\PrintBrm.exe -b -d {} -f {}'.format(
                self.target_dir, self.zip_file
            )
        else:
            # Restore: PrintBrm -r -f <zip> -d <dir>
            cmd_str = r'C:\Windows\System32\spool\tools\PrintBrm.exe -r -f {} -d {}'.format(
                self.zip_file, self.target_dir
            )

        typing_text += 'Send("' + self._escape_send(cmd_str) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_printbrm(self):
        """
        Closes the PrintBrm AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
