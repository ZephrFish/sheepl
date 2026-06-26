
# LOLBAS: WinProj.exe — Legitimate use: opening Microsoft Project files directly from a URL or file path
# DEVELOPER-ONLY: Requires Microsoft Office / Microsoft Project to be installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user use of WinProj.exe to open a Microsoft Project
 file from a UNC path or local file path, mimicking normal project management
 activity.

 Takes a required project_url parameter pointing to the .mpp file to open.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Winproj(BaseCMD):
    """
    # LOLBAS: WinProj.exe — Legitimate use: opening Microsoft Project files directly from a URL or file path
    # DEVELOPER-ONLY: Requires Microsoft Office / Microsoft Project to be installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Winproj, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Winproj'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > winproj >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > winproj >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL or file path to the project file to open
        self.project_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] WinProj Interaction.
            Requires Microsoft Project to be installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the project file URL or path using 'project_url <url>'
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
    #  Winproj Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Winproj interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Winproj_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_project_url(self, project_url):
        """
        Set the URL or file path for the Microsoft Project file to open.
        Example: project_url http://fileserver/shared/schedule.mpp
        Example: project_url \\\\fileserver\\projects\\q1plan.mpp
        """
        if project_url:
            if self.taskstarted:
                self.project_url = project_url.strip()
                print(self.cl.green("[*] Project URL set to: {}".format(self.project_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Winproj Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a project file URL or path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Winproj configuration
        """
        print(self.cl.green("[?] Currently Assigned Winproj Configuration"))
        print("[>] Project URL : {}".format(self.project_url if self.project_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.project_url:
                print(self.cl.red("[!] <ERROR> You must set a project_url before completing."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.project_url = None


    ######################################################################
    # Winproj AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Winproj_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_function()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            project_url : str — URL or file path to the .mpp project file to open
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.project_url = kwargs.get("project_url", None)
        if self.project_url:
            print(f"[*] Setting project_url attribute : {self.project_url}")
        else:
            print("[!] <ERROR> No project_url provided — this is required for Winproj.")
            return

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
        ; <      Winproj Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Winproj_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Winproj_{}()

            ; Creates a Winproj Interaction via CMD

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
        Builds the WinProj command to type into the CMD window.
        Opens the specified project file URL using WinProj.exe.
        """
        typing_text = '\n'

        # Launch WinProj with the project file URL
        winproj_cmd = 'WinProj.exe {}'.format(self.project_url)
        typing_text += 'Send("' + self._escape_send(winproj_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Winproj AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
