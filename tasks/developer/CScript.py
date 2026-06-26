
# #######################################################################
#
#  Task : CScript Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of cscript.exe to run Windows Script Host
 scripts in console (headless) mode — VBScript WMI queries, AD queries,
 legacy automation, and disk management scripts.

 Takes a script path (required) and optional arguments to pass to the script.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class CScript(BaseCMD):
    """
    # LOLBAS: cscript.exe — Legitimate use: headless VBScript/JScript execution for IT automation

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(CScript, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'CScript'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cscript >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cscript >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the .vbs or .js script to execute
        self.script = None
        # Optional arguments to pass to the script
        self.script_args = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CScript Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the script path using 'script <path>'
        3: Optionally set script arguments using 'args <arguments>'
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
    #  CScript Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new CScript interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'CScript_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_script(self, script):
        """
        Set the path to the VBScript or JScript file to execute.
        Example: script C:\\Scripts\\query_ad.vbs
        Example: script C:\\Scripts\\disk_report.js
        """
        if script:
            if self.taskstarted:
                self.script = script.strip()
                print(self.cl.green("[*] Script set to: {}".format(self.script)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CScript Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a .vbs or .js script."))


    def do_args(self, args):
        """
        Optionally set arguments to pass to the script.
        Example: args /server:DC01 /output:C:\\Logs\\result.txt
        """
        if args:
            if self.taskstarted:
                self.script_args = args.strip()
                print(self.cl.green("[*] Script args set to: {}".format(self.script_args)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CScript Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide arguments to pass to the script."))


    def do_assigned(self, arg):
        """
        Get the current assigned CScript configuration
        """
        print(self.cl.green("[?] Currently Assigned CScript Configuration"))
        print("[>] Script : {}".format(self.script if self.script else "(not set)"))
        print("[>] Args   : {}".format(self.script_args if self.script_args else "(none)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if self.script:
                self.create_autoIT_block()
            else:
                print("{} There is no script assigned".format(self.cl.red("[!]")))
                print("{} Assign a script path using 'script <path>'".format(self.cl.red("[-]")))
                return None

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.script = None
        self.script_args = None


    ######################################################################
    # CScript AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('CScript_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_cscript()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            script : str — path to the .vbs or .js script to execute

        Optional JSON keys:
            args   : str — arguments to pass to the script
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.script = kwargs.get("script", None)
        self.script_args = kwargs.get("args", None)

        if self.script:
            print(f"[*] Setting script attribute : {self.script}")
        else:
            print("[!] No script provided — skipping CScript task")
            return

        if self.script_args:
            print(f"[*] Setting script_args attribute : {self.script_args}")
        else:
            print("[*] No args provided — script will run without additional arguments")

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
        ; <      CScript Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "CScript_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func CScript_{}()

            ; Creates a CScript Interaction via CMD

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
        Builds the cscript command to type into the CMD window.
        Uses //Nologo to suppress the Windows Script Host banner.
        Appends optional script_args if set.
        """
        typing_text = '\n'

        # Build the cscript command: cscript //Nologo <script> [args]
        if self.script_args:
            cscript_cmd = 'cscript //Nologo {} {}'.format(self.script, self.script_args)
        else:
            cscript_cmd = 'cscript //Nologo {}'.format(self.script)

        typing_text += 'Send("' + self._escape_send(cscript_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_cscript(self):
        """
        Closes the CScript AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
