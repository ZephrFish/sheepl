
# #######################################################################
#
#  Task : Tar Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user use of tar.exe (Win10 build 17063+) for
 archiving files and extracting downloaded archives.

 Supports two actions:
   create  — compress source path into a .tar.gz archive at dest
   extract — extract archive at source into directory at dest

 the master script will already define the typing speed as part of the master declarations
"""

# LOLBAS: tar.exe — Legitimate use: file archiving and extraction (available Win10 build 17063+)

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Tar(BaseCMD):
    """
    # LOLBAS: tar.exe — Legitimate use: file archiving and extraction (available Win10 build 17063+)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Tar, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Tar'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > tar >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > tar >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific variables
        # action: "create" or "extract" (default: "create")
        self.action = 'create'
        # source: path/file to archive (create) or archive to extract (extract)
        self.source = None
        # dest: archive name for create, or directory for extract
        self.dest = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Tar Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the action using 'action <create|extract>'
        3: Set the source path using 'source <path>'
        4: Set the destination using 'dest <path>'
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
    #  Tar Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Tar interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Tar_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, action):
        """
        Set the tar action to perform.
        Valid values: create, extract
        Default: create
        Example: action extract
        """
        valid = ['create', 'extract']
        if action.strip().lower() in valid:
            if self.taskstarted:
                self.action = action.strip().lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Tar Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Invalid action '{}'. Choose from: {}".format(action, ', '.join(valid))))


    def do_source(self, source):
        """
        Set the source for the tar operation.
        For create: path or file to archive.
        For extract: path to the archive file to extract.
        Example: source C:\\Users\\user\\logs
        """
        if source:
            if self.taskstarted:
                self.source = source.strip()
                print(self.cl.green("[*] Source set to: {}".format(self.source)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Tar Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a source path."))


    def do_dest(self, dest):
        """
        Set the destination for the tar operation.
        For create: archive filename to create (e.g. archive.tar.gz).
        For extract: directory to extract files into.
        Example: dest C:\\Users\\user\\archive.tar.gz
        """
        if dest:
            if self.taskstarted:
                self.dest = dest.strip()
                print(self.cl.green("[*] Destination set to: {}".format(self.dest)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Tar Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a destination path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Tar configuration
        """
        print(self.cl.green("[?] Currently Assigned Tar Configuration"))
        print("[>] Action : {}".format(self.action))
        print("[>] Source : {}".format(self.source if self.source else "(not set)"))
        print("[>] Dest   : {}".format(self.dest if self.dest else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if self.source and self.dest:
                self.create_autoIT_block()
            else:
                print("{} Source and destination must both be set before completing.".format(self.cl.red("[!]")))
                print("{} Use 'source <path>' and 'dest <path>' to configure.".format(self.cl.red("[-]")))
                return None

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.action = 'create'
        self.source = None
        self.dest = None


    ######################################################################
    # Tar AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Tar_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_tar()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            action : str — "create" or "extract" (default: "create")
            source : str — source path/file to archive, or archive to extract
            dest   : str — archive name for create, or extract directory for extract
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", "create")
        self.source = kwargs.get("source")
        self.dest = kwargs.get("dest")

        print(f"[*] Setting action attribute : {self.action}")
        print(f"[*] Setting source attribute : {self.source}")
        print(f"[*] Setting dest attribute   : {self.dest}")

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
        ; <      Tar Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Tar_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Tar_{}()

            ; Creates a Tar Interaction via CMD

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
        Builds the tar command to type into the CMD window.
        create  : tar -czf <dest> <source>
        extract : tar -xf <source> -C <dest>
        """
        typing_text = '\n'

        if self.action == 'create':
            tar_cmd = 'tar -czf {} {}'.format(self.dest, self.source)
        else:
            tar_cmd = 'tar -xf {} -C {}'.format(self.source, self.dest)

        typing_text += 'Send("' + self._escape_send(tar_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_tar(self):
        """
        Closes the Tar AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
