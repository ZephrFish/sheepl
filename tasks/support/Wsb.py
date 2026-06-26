
# LOLBAS: wsb.exe — Legitimate use: managing Windows Sandbox sessions from the host CLI

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of wsb.exe (Windows Sandbox CLI) to start a sandbox
 session with an optional mapped folder for file sharing, then execute a command
 inside the sandbox via the exec subcommand.

 Takes an optional mapped_folder parameter; if absent starts a basic sandbox session.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Wsb(BaseCMD):
    """
    # LOLBAS: wsb.exe — Legitimate use: managing Windows Sandbox sessions from the host CLI

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Wsb, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Wsb'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wsb >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wsb >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional host folder to map into the sandbox
        self.mapped_folder = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Wsb Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a host folder to share into the sandbox using 'mapped_folder <path>'
        3: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Wsb Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Wsb interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Wsb_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_mapped_folder(self, mapped_folder):
        """
        Optionally set a host folder path to share into the Windows Sandbox.
        If not set, a basic sandbox session will be started with no mapped folders.
        Example: mapped_folder C:\\Users\\Public\\SandboxShare
        """
        if mapped_folder:
            if self.taskstarted:
                self.mapped_folder = mapped_folder.strip()
                print(self.cl.green("[*] Mapped folder set to: {}".format(self.mapped_folder)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Wsb Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a folder path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Wsb configuration
        """
        print(self.cl.green("[?] Currently Assigned Wsb Configuration"))
        print("[>] Mapped Folder : {}".format(self.mapped_folder if self.mapped_folder else "(not set — basic sandbox start)"))


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
        self.mapped_folder = None


    ######################################################################
    # Wsb AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Wsb_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_wsb()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            mapped_folder : str — absolute path to a host folder to share into the sandbox
                                  if absent, a basic 'wsb start' is executed
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.mapped_folder = kwargs.get("mapped_folder", None)
        if self.mapped_folder:
            print(f"[*] Setting mapped_folder attribute : {self.mapped_folder}")
        else:
            print("[*] No mapped_folder provided — will run a basic sandbox session")

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
        ; <      Wsb Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Wsb_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Wsb_{}()

            ; Creates a Wsb Interaction via CMD

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
        Builds the wsb commands to type into the CMD window.
        If mapped_folder is set, starts the sandbox with an inline XML config that
        maps the specified host folder. Otherwise runs a plain 'wsb start'.
        """
        typing_text = '\n'

        if self.mapped_folder:
            # Build inline XML config with a MappedFolder — legitimate file-sharing use case
            xml_config = (
                '<Configuration>'
                '<MappedFolders>'
                '<MappedFolder>'
                '<HostFolder>{}</HostFolder>'
                '<ReadOnly>true</ReadOnly>'
                '</MappedFolder>'
                '</MappedFolders>'
                '</Configuration>'
            ).format(self.mapped_folder)
            start_cmd = 'wsb start --config "{}"'.format(xml_config)
        else:
            start_cmd = 'wsb start'

        typing_text += 'Send("' + self._escape_send(start_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # List active sandbox sessions to confirm it started
        list_cmd = 'wsb list'
        typing_text += 'Send("' + self._escape_send(list_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_wsb(self):
        """
        Closes the Wsb AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
