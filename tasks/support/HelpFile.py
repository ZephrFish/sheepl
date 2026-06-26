
# #######################################################################
#
#  Task : HelpFile Interaction
#
# #######################################################################

# LOLBAS: hh.exe — Legitimate use: reading application and system documentation (.chm files)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user/IT use of hh.exe — opening CHM Windows Help files.
 Users and IT staff routinely open .chm files to read application help or
 product documentation.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import textwrap

from utils.base.base_cmd_class import BaseCMD


class HelpFile(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(HelpFile, self).__init__(csh, cl)

        self.taskname = 'HelpFile'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > helpfile >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > helpfile >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] HelpFile Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the CHM path using 'chm_path'  (default: C:\\Windows\\Help\\Windows.chm)
        3: Set the browse time using 'browse_time'  (default: 15 seconds)
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # Task-specific variables
        self.chm_path = 'C:\\Windows\\Help\\Windows.chm'
        self.browse_time = 15

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # HelpFile Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new HelpFile interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'HelpFile_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] HelpFile_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_chm_path(self, path):
        """
        Set the path to the CHM help file to open
        example: chm_path C:\\Windows\\Help\\Windows.chm
        example: chm_path C:\\Program Files\\App\\help.chm
        """
        if path:
            if self.taskstarted:
                self.chm_path = path
                print(self.cl.green("[*] CHM path set to: {}".format(path)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new HelpFile interaction first with 'new'."))
        else:
            print(self.cl.green("[*] Using default CHM path: {}".format(self.chm_path)))


    def do_browse_time(self, seconds):
        """
        Set the number of seconds to keep the help file open before closing
        example: browse_time 15
        """
        if seconds:
            if self.taskstarted:
                try:
                    self.browse_time = int(seconds)
                    print(self.cl.green("[*] Browse time set to: {} seconds".format(self.browse_time)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> browse_time must be an integer number of seconds."))
            else:
                print(self.cl.red("[!] <ERROR> Start a new HelpFile interaction first with 'new'."))
        else:
            print(self.cl.green("[*] Using default browse time: {} seconds".format(self.browse_time)))


    def do_assigned(self, arg):
        """
        Show the currently assigned HelpFile settings
        """
        print("[>] CHM Path    : {}".format(self.chm_path))
        print("[>] Browse Time : {} seconds".format(self.browse_time))


    def do_complete(self, arg):
        """
        Complete the HelpFile interaction and generate the AutoIT block
        """
        if self.taskstarted:
            if self.chm_path:
                self.create_autoIT_block()
                self.complete_task()
                # reset to defaults
                self.chm_path = 'C:\\Windows\\Help\\Windows.chm'
                self.browse_time = 15
            else:
                print("{} No CHM path set. Use 'chm_path' to specify a file.".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new HelpFile interaction first with 'new'."))


    ########################################################################
    # HelpFile AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('HelpFile_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_helpfile() +
            self.close_helpfile()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        Reads chm_path and browse_time from kwargs
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.chm_path = kwargs.get("chm_path", 'C:\\Windows\\Help\\Windows.chm')
            print(f"[*] CHM Path : {self.chm_path}")
        except KeyError as e:
            print(self.cl.red("[!] Error setting JSON Profile attributes, missing key: {}".format(e)))

        try:
            self.browse_time = int(kwargs.get("browse_time", 15))
            print(f"[*] Browse Time : {self.browse_time} seconds")
        except (KeyError, ValueError) as e:
            print(self.cl.red("[!] Error setting browse_time, using default 15 seconds: {}".format(e)))
            self.browse_time = 15

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ------------------------------------------ >
        ;           HelpFile Interaction
        ;   LOLBAS: hh.exe - Opening CHM help files
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "HelpFile_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_helpfile(self):
        """
        Opens the CHM help file via Win+R -> hh.exe <path>
        """
        browse_ms = self.browse_time * 1000

        _open_helpfile = """

        Func HelpFile_{counter}()

            ; Simulates a user opening a CHM Windows Help file via hh.exe
            ; Legitimate use: reading application and system documentation

            Send("#r")
            WinWaitActive("Run", "", 10)
            Send('hh.exe "{chm_path}"{{ENTER}}')

            ; Wait for the HTML Help viewer window to appear
            WinWaitActive("HTML Help", "", 10)
            SendKeepActive("HTML Help")

            ; Simulate reading/browsing the help file
            Sleep({browse_ms})

        """.format(
            counter=str(self.csh.counter.current()),
            chm_path=self._escape_send(self.chm_path),
            browse_ms=browse_ms
        )

        return textwrap.dedent(_open_helpfile)


    def close_helpfile(self):
        """
        Closes the HTML Help viewer and ends the function declaration
        """
        end_func = """

        ; Close the HTML Help viewer
        Send("!{F4}")
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
