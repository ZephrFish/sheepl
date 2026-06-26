
# #######################################################################
#
#  Task : FileExplorer Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Opens Windows Explorer and browses to a specified path.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD


class FileExplorer(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(FileExplorer, self).__init__(csh, cl)

        self.taskname = 'FileExplorer'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > fileexplorer >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > fileexplorer >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] FileExplorer Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set path using 'path'  (supports UNC paths e.g. \\\\server\\share)
        3: Complete the interaction using 'complete'
        """

        self.indent_space = '    '
        self.browse_path = ''

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # FileExplorer Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new FileExplorer interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'FileExplorer_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] FileExplorer_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_path(self, path):
        """
        Set the path for Explorer to open
        Supports local paths and UNC paths
        example: path C:\\Users\\Public\\Documents
        example: path \\\\fileserver\\shared
        """
        if path:
            if self.taskstarted:
                self.browse_path = path
                print(self.cl.green("[*] Path set to: {}".format(path)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new FileExplorer interaction first with 'new'."))


    def do_assigned(self, arg):
        """
        Show the currently assigned path
        """
        print("[>] Path : {}".format(self.browse_path or "Not set"))


    def do_complete(self, arg):
        """
        Complete the FileExplorer interaction and generate the AutoIT block
        """
        if self.taskstarted:
            if self.browse_path:
                self.create_autoIT_block()
                self.complete_task()
                self.browse_path = ''
            else:
                print("{} No path set. Use 'path' to specify a directory.".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new FileExplorer interaction first with 'new'."))


    ########################################################################
    # FileExplorer AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('FileExplorer_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_fileexplorer() +
            self.close_fileexplorer()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.browse_path = kwargs["path"]
            print(f"[*] Path : {self.browse_path}")

        except KeyError as e:
            print(self.cl.red("[!] Error setting JSON Profile attributes, missing key: {}".format(e)))

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ------------------------------------------ >
        ;           FileExplorer Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "FileExplorer_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_fileexplorer(self):

        browse_time = random.randint(15000, 45000)

        _open_fileexplorer = """

        Func FileExplorer_{}()

            ; Creates a FileExplorer Interaction

            Send("#r")
            WinWaitActive("Run", "", 10)
            Send('explorer "{}"{{ENTER}}')
            ; Wait for Explorer window to appear
            WinWaitActive("[CLASS:CabinetWClass]", "", 15)
            SendKeepActive("[CLASS:CabinetWClass]")

            ; Simulate browsing time
            Sleep({})

        """.format(str(self.csh.counter.current()), self.browse_path, browse_time)

        return textwrap.dedent(_open_fileexplorer)


    def close_fileexplorer(self):
        """
        Closes the FileExplorer function declaration
        """
        end_func = """

        ; Close the Explorer window
        Send("!{F4}")
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
