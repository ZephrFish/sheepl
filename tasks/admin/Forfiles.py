
# LOLBAS: forfiles.exe — Legitimate use: automated file cleanup and age-based file auditing

# #######################################################################
#
#  Task : Forfiles Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT/admin use of forfiles.exe to perform batch
 file processing based on age and extension criteria. Common use cases
 include automated old log cleanup, finding files older than N days for
 archiving, and auditing files by age across a directory tree.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Forfiles(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Forfiles, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Forfiles'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > forfiles >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > forfiles >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific defaults
        self.search_path = 'C:\\Windows\\Temp'
        self.days_old = 30
        self.extension = '*.log'
        self.file_action = 'list'

        self.introduction = """
        ----------------------------------
        [!] Forfiles Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the search path using 'path'
        3: Set the age threshold using 'days'
        4: Set the file extension using 'extension'
        5: Set the action using 'action' (list or delete)
        6: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Forfiles Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Forfiles interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Forfiles_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_path(self, path):
        """
        Set the directory path to search with forfiles.
        Default: C:\\Windows\\Temp
        Example:
            path C:\\Windows\\Temp
            path C:\\Logs
        """
        if self.taskstarted:
            if path:
                self.search_path = path
                print(self.cl.green("[*] Search path set to: {}".format(self.search_path)))
            else:
                print(self.cl.yellow("[*] No path supplied, using default: {}".format(self.search_path)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Forfiles Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_days(self, days):
        """
        Set the minimum file age in days. Files older than this value will be matched.
        Default: 30
        Example:
            days 30
            days 90
        """
        if self.taskstarted:
            if days:
                try:
                    self.days_old = int(days)
                    print(self.cl.green("[*] Days threshold set to: {}".format(self.days_old)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> Days must be an integer value."))
            else:
                print(self.cl.yellow("[*] No value supplied, using default: {}".format(self.days_old)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Forfiles Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_extension(self, extension):
        """
        Set the file extension pattern to match.
        Default: *.log
        Example:
            extension *.log
            extension *.tmp
            extension *.bak
        """
        if self.taskstarted:
            if extension:
                self.extension = extension
                print(self.cl.green("[*] Extension set to: {}".format(self.extension)))
            else:
                print(self.cl.yellow("[*] No extension supplied, using default: {}".format(self.extension)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Forfiles Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_action(self, action):
        """
        Set the action to perform on matched files.
        Options:
            list   - echo filename and date (safe, read-only audit)
            delete - delete matched files (destructive cleanup)
        Default: list
        Example:
            action list
            action delete
        """
        if self.taskstarted:
            valid_actions = ['list', 'delete']
            if action:
                if action.lower() in valid_actions:
                    self.file_action = action.lower()
                    print(self.cl.green("[*] Action set to: {}".format(self.file_action)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid action. Choose from: {}".format(', '.join(valid_actions))))
            else:
                print(self.cl.yellow("[*] No action supplied, using default: {}".format(self.file_action)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Forfiles Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the currently assigned Forfiles settings
        """
        print(self.cl.green("[?] Currently Assigned Forfiles Settings"))
        print("[>] Search Path : {}".format(self.search_path))
        print("[>] Days Old    : {}".format(self.days_old))
        print("[>] Extension   : {}".format(self.extension))
        print("[>] Action      : {}".format(self.file_action))


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

        # reset attributes to defaults for next interaction
        self.search_path = 'C:\\Windows\\Temp'
        self.days_old = 30
        self.extension = '*.log'
        self.file_action = 'list'


    ######################################################################
    # Forfiles AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Forfiles_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.forfiles_command_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            path      : directory to search (default: C:\\Windows\\Temp)
            days      : files older than N days (default: 30)
            extension : file extension pattern to match (default: *.log)
            action    : "list" to echo filenames, "delete" to remove files (default: list)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "path" in kwargs:
            self.search_path = kwargs["path"]
        print(f"[*] Setting the search_path attribute : {self.search_path}")

        if "days" in kwargs:
            self.days_old = int(kwargs["days"])
        print(f"[*] Setting the days_old attribute : {self.days_old}")

        if "extension" in kwargs:
            self.extension = kwargs["extension"]
        print(f"[*] Setting the extension attribute : {self.extension}")

        if "action" in kwargs:
            self.file_action = kwargs["action"]
        print(f"[*] Setting the file_action attribute : {self.file_action}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      Forfiles Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Forfiles_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens CMD via Win+R run dialogue
        """

        _open_commandshell = """

        Func Forfiles_{}()

            ; Opens CMD to run forfiles batch file processing

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
    # Forfiles Command Block

    def forfiles_command_block(self):
        """
        Builds and sends the forfiles command based on configured action,
        then exits the shell.

        list action:
            forfiles /p <path> /s /m <extension> /d -<days> /c "cmd /c echo @file @fdate"

        delete action:
            forfiles /p <path> /s /m <extension> /d -<days> /c "cmd /c del @file"
        """

        if self.file_action == 'delete':
            cmd_string = (
                'forfiles /p {path} /s /m {ext} /d -{days} /c "cmd /c del @file"'.format(
                    path=self.search_path,
                    ext=self.extension,
                    days=self.days_old,
                )
            )
        else:
            # default: list
            cmd_string = (
                'forfiles /p {path} /s /m {ext} /d -{days} /c "cmd /c echo @file @fdate"'.format(
                    path=self.search_path,
                    ext=self.extension,
                    days=self.days_old,
                )
            )

        command_text = '\n'
        command_text += 'Send("' + self._escape_send(cmd_string) + '{ENTER}")\n'
        command_text += 'sleep({})\n'.format(random.randint(3000, 15000))
        command_text += "Send('exit{ENTER}')\n"
        command_text += "; Reset Focus\n"
        command_text += 'SendKeepActive("")'

        return textwrap.indent(command_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the Forfiles function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
