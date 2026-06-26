
# LOLBAS: vsls-agent.exe — Legitimate use: Visual Studio Live Share collaboration agent
# DEVELOPER-ONLY: Requires Visual Studio with Live Share extension installed

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of vsls-agent.exe, the Visual Studio
 Live Share collaboration agent. Loads an agent extension DLL via the
 --agentExtensionPath parameter, as used during legitimate Live Share sessions.

 Takes a required extension_path parameter pointing to the Live Share agent
 extension DLL. The binary is typically located under the Visual Studio
 installation directory.

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class VslsAgent(BaseCMD):
    """
    # LOLBAS: vsls-agent.exe — Legitimate use: Visual Studio Live Share collaboration agent
    # DEVELOPER-ONLY: Requires Visual Studio with Live Share extension installed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(VslsAgent, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'VslsAgent'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > vsls-agent >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > vsls-agent >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the agent extension DLL loaded via --agentExtensionPath
        self.extension_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] VslsAgent Interaction.
        [!] DEVELOPER-ONLY: Requires Visual Studio with Live Share installed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the extension DLL path using 'extension_path <path>'
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
    #  VslsAgent Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new VslsAgent interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'VslsAgent_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_extension_path(self, extension_path):
        """
        Set the path to the agent extension DLL to load via --agentExtensionPath.
        This is the DLL that vsls-agent.exe will load as part of a Live Share session.
        Example: extension_path C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Professional\\Common7\\IDE\\Extensions\\Microsoft\\LiveShare\\Agent\\Microsoft.VisualStudio.LiveShare.Agent.dll
        """
        if extension_path:
            if self.taskstarted:
                self.extension_path = extension_path.strip()
                print(self.cl.green("[*] Extension path set to: {}".format(self.extension_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new VslsAgent Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an extension DLL path."))


    def do_assigned(self, arg):
        """
        Get the current assigned VslsAgent configuration
        """
        print(self.cl.green("[?] Currently Assigned VslsAgent Configuration"))
        print("[>] Extension Path : {}".format(self.extension_path if self.extension_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.extension_path:
                print(self.cl.red("[!] <ERROR> extension_path is required. Set it with 'extension_path <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.extension_path = None


    ######################################################################
    # VslsAgent AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('VslsAgent_' + current_counter, self.create_autoit_function())


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
            extension_path : str — absolute path to the agent extension DLL
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.extension_path = kwargs.get("extension_path", None)
        if self.extension_path:
            print(f"[*] Setting extension_path attribute : {self.extension_path}")
        else:
            print("[!] <ERROR> extension_path is required for VslsAgent task.")
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
        ; <      VslsAgent Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "VslsAgent_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func VslsAgent_{}()

            ; Creates a VslsAgent Interaction via CMD

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
        Builds the vsls-agent command to type into the CMD window.
        Invokes vsls-agent.exe with --agentExtensionPath to load the
        specified Live Share extension DLL.
        """
        typing_text = '\n'

        # Build the vsls-agent command with the extension path
        vsls_cmd = 'vsls-agent.exe --agentExtensionPath {}'.format(self.extension_path)
        typing_text += 'Send("' + self._escape_send(vsls_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the VslsAgent AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
