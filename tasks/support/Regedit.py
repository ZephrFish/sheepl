
# LOLBAS: regedit.exe — Legitimate use: registry inspection and configuration export (IT admin)

# #######################################################################
#
#  Task : Regedit Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of regedit.exe to inspect
 Windows Registry keys, navigate to specific paths for troubleshooting,
 and optionally export registry keys to .reg files for backup or
 configuration documentation.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


DEFAULT_BROWSE_TIME = 10


class Regedit(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Regedit, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Regedit'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > regedit >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > regedit >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific defaults
        self.nav_key = ''
        self.browse_time = DEFAULT_BROWSE_TIME
        self.export_key = ''
        self.export_path = ''

        self.introduction = """
        ----------------------------------
        [!] Regedit Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set registry key to navigate to using 'nav_key'  (optional)
           Example: HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion
        3: Set browse time using 'browse_time'  (seconds to keep open, default 10)
        4: Set a registry key to export using 'export_key'  (optional)
           Example: HKEY_LOCAL_MACHINE\\SOFTWARE\\MyApp
        5: Set export file path using 'export_path'  (required if export_key set)
           Example: C:\\Temp\\myapp_backup.reg
        6: Complete the interaction using 'complete'
        ----------------------------------
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
    #  Regedit Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Regedit interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Regedit_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_nav_key(self, nav_key):
        """
        Set the registry key to navigate to using the Ctrl+G 'Go to Key' dialog.
        This is optional. If not set, regedit opens at its last visited location.
        Example:
            nav_key HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion
            nav_key HKEY_CURRENT_USER\\Software\\Microsoft\\Office
        """
        if nav_key:
            if self.taskstarted:
                self.nav_key = nav_key.strip()
                print(self.cl.green("[*] Registry key (nav) set to: {}".format(self.nav_key)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Regedit Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No nav_key supplied. Regedit will open at its default location."))


    def do_browse_time(self, browse_time):
        """
        Set how long (in seconds) to keep regedit open before closing.
        Default: 10 seconds
        Example:
            browse_time 20
        """
        if browse_time:
            if self.taskstarted:
                try:
                    self.browse_time = int(browse_time.strip())
                    print(self.cl.green("[*] Browse time set to: {} seconds".format(self.browse_time)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> browse_time must be an integer number of seconds."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Regedit Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No browse time supplied, using default: {} seconds".format(self.browse_time)))


    def do_export_key(self, export_key):
        """
        Set the registry key to export to a .reg file.
        This is optional. If set, export_path must also be set.
        The export is performed via 'regedit /e <path> <key>' through a separate Win+R dialog.
        Example:
            export_key HKEY_LOCAL_MACHINE\\SOFTWARE\\MyApp
            export_key HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\MyService
        """
        if export_key:
            if self.taskstarted:
                self.export_key = export_key.strip()
                print(self.cl.green("[*] Export key set to: {}".format(self.export_key)))
                if not self.export_path:
                    print(self.cl.yellow("[!] Remember to set 'export_path' before completing."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Regedit Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No export_key supplied. Registry export will be skipped."))


    def do_export_path(self, export_path):
        """
        Set the file path to save the exported .reg file.
        Only used when export_key is set.
        Example:
            export_path C:\\Temp\\myapp_backup.reg
            export_path C:\\Users\\Administrator\\Desktop\\hklm_software.reg
        """
        if export_path:
            if self.taskstarted:
                self.export_path = export_path.strip()
                print(self.cl.green("[*] Export path set to: {}".format(self.export_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Regedit Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No export_path supplied."))


    def do_assigned(self, arg):
        """
        Show the currently assigned Regedit settings
        """
        print(self.cl.green("[?] Currently Assigned Regedit Settings"))
        print("[>] Nav key     : {}".format(self.nav_key or "Not set (opens at default location)"))
        print("[>] Browse time : {} seconds".format(self.browse_time))
        print("[>] Export key  : {}".format(self.export_key or "Not set (no export)"))
        print("[>] Export path : {}".format(self.export_path or "Not set"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            # Validate: if export_key is set, export_path must also be set
            if self.export_key and not self.export_path:
                print(self.cl.red("[!] <ERROR> export_key is set but export_path is not. Set export_path first."))
                return

            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset to defaults for next interaction
        self.nav_key = ''
        self.browse_time = DEFAULT_BROWSE_TIME
        self.export_key = ''
        self.export_path = ''


    ######################################################################
    # Regedit AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Regedit_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_regedit() +
            self.close_regedit()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            nav_key     : registry key to navigate to via Ctrl+G (optional)
                          e.g. "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion"
            browse_time : seconds to keep regedit open (default: 10)
            export_key  : registry key to export to a .reg file (optional)
                          e.g. "HKEY_LOCAL_MACHINE\\SOFTWARE\\MyApp"
            export_path : file path for the exported .reg file (required if export_key set)
                          e.g. "C:\\Temp\\myapp_backup.reg"
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "nav_key" in kwargs:
            self.nav_key = kwargs["nav_key"].strip()
            print(f"[*] Setting the nav_key attribute : {self.nav_key}")

        if "browse_time" in kwargs:
            try:
                self.browse_time = int(kwargs["browse_time"])
            except (ValueError, TypeError):
                print(self.cl.yellow("[!] Invalid browse_time, using default: {}".format(DEFAULT_BROWSE_TIME)))
                self.browse_time = DEFAULT_BROWSE_TIME
        print(f"[*] Setting the browse_time attribute : {self.browse_time} seconds")

        if "export_key" in kwargs:
            self.export_key = kwargs["export_key"].strip()
            print(f"[*] Setting the export_key attribute : {self.export_key}")

        if "export_path" in kwargs:
            self.export_path = kwargs["export_path"].strip()
            print(f"[*] Setting the export_path attribute : {self.export_path}")

        # Validate export settings
        if self.export_key and not self.export_path:
            print(self.cl.yellow("[!] export_key is set but export_path is missing. Export will be skipped."))
            self.export_key = ''

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
        ; <         Regedit Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Regedit_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_regedit(self):
        """
        Opens regedit.exe via Win+R, optionally navigates to a registry key
        using Ctrl+G, sleeps for browse_time, and optionally runs a separate
        Win+R command to export a key before closing.
        """

        browse_time_ms = self.browse_time * 1000
        counter = str(self.csh.counter.current())

        # Build the optional navigation block
        nav_block = ""
        if self.nav_key:
            nav_block = """
            ; Navigate to the specified registry key using Ctrl+G (Go to Key)
            Send("^g")
            WinWaitActive("Go to Key", "", 10)
            Send("{}")
            Send("{{ENTER}}")
            """.format(self._escape_send(self.nav_key))

        # Build the optional export block
        export_block = ""
        if self.export_key and self.export_path:
            export_block = """
            ; Export the specified registry key to a .reg file via Win+R
            ; Using 'regedit /e <path> <key>' for a clean command-line export
            Send("#r")
            WinWaitActive("Run", "", 10)
            Send('regedit /e "{}" "{}"{{ENTER}}')
            ; Brief pause to allow the export to complete
            Sleep(2000)
            """.format(self._escape_send(self.export_path), self._escape_send(self.export_key))

        _open_regedit = """

        Func Regedit_{}()

            ; Simulates IT administrator use of Windows Registry Editor
            ; LOLBAS: regedit.exe — Legitimate use: registry inspection and configuration export (IT admin)

            ; Open regedit via Win+R run dialog
            Send("#r")
            WinWaitActive("Run", "", 10)
            Send("regedit{{ENTER}}")
            ; Wait for Registry Editor window to become active
            WinWaitActive("Registry Editor", "", 10)
            SendKeepActive("Registry Editor")
        {}
            ; Simulate IT administrator browsing registry keys
            Sleep({})
        {}
        """.format(counter, nav_block, browse_time_ms, export_block)

        return textwrap.dedent(_open_regedit)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_regedit(self):
        """
        Closes regedit with Alt+F4 and resets focus
        """

        end_func = """

        ; Close the Registry Editor window
        Send("!{F4}")
        ; Reset Focus
        SendKeepActive("")

        EndFunc

        """

        return textwrap.dedent(end_func)
