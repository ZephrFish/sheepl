
# #######################################################################
#
#  Task : Wscript Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of wscript.exe (Windows Script Host) to
 run VBScript (.vbs) and Windows Script Files (.wsf) — common in
 enterprise login scripts and legacy automation.

"""

# LOLBAS: wscript.exe — Legitimate use: VBScript and WSF automation scripts (common in enterprise login scripts)
# Note: wscript.exe runs scripts with a GUI (message boxes visible); use cscript.exe for headless execution

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Wscript(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # LOLBAS: wscript.exe — Legitimate use: VBScript and WSF automation scripts (common in enterprise login scripts)
    # Note: wscript.exe runs scripts with a GUI (message boxes visible); use cscript.exe for headless execution
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Wscript, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Wscript'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wscript >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wscript >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Path to the .vbs or .wsf script to execute
        self.script = ''
        # Optional arguments to pass to the script
        self.script_args = ''

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Wscript Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the script path using 'script'
        3: Optionally set script arguments using 'args'
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
    #  Wscript Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Wscript interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Wscript_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_script(self, arg):
        """
        Set the path to the .vbs or .wsf script to run with wscript.exe.
        Example: script C:\\Scripts\\login.vbs
        Example: script C:\\Scripts\\setup.wsf
        """
        if self.taskstarted:
            if arg:
                self.script = arg
                print(self.cl.green("[*] Script set to: {}".format(self.script)))
            else:
                print(self.cl.red("[!] <ERROR> Please provide a path to a .vbs or .wsf script."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Wscript Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_args(self, arg):
        """
        Set optional arguments to pass to the script.
        Example: args //T:30 //Nologo
        Example: args username domain
        """
        if self.taskstarted:
            self.script_args = arg
            if arg:
                print(self.cl.green("[*] Script arguments set to: {}".format(self.script_args)))
            else:
                print(self.cl.green("[*] Script arguments cleared (none will be passed)."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Wscript Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show current Wscript task settings
        """
        print(self.cl.green("[?] Currently Assigned Wscript Settings"))
        print("[>] Script path  : {}".format(self.script if self.script else "(not set)"))
        print("[>] Script args  : {}".format(self.script_args if self.script_args else "(none)"))


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
                print("{} No script path assigned.".format(self.cl.red("[!]")))
                print("{} Assign a script using 'script <path>'".format(self.cl.red("[-]")))
                return None

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific variables for next interaction
        self.script = ''
        self.script_args = ''


    ######################################################################
    # Wscript AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Wscript_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_wscript() +
            self.wait_for_completion() +
            self.close_wscript()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads script and args from kwargs.
        JSON keys: script, args
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.script = kwargs.get("script", '')
        print(f"[*] Setting the script attribute : {self.script}")

        self.script_args = kwargs.get("args", '')
        print(f"[*] Setting the script_args attribute : {self.script_args}")

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
        ; <      Wscript Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Wscript_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_wscript(self):
        """
        Opens a Run dialog (Win+R) and launches wscript.exe with the
        configured script path and optional arguments.
        """

        # Build the wscript run command: wscript.exe <script> [args]
        if self.script_args:
            run_command = 'wscript.exe {} {}'.format(self.script, self.script_args)
        else:
            run_command = 'wscript.exe {}'.format(self.script)

        escaped_command = self._escape_send(run_command)

        _open_wscript = """

        Func Wscript_{}()

            ; Launches wscript.exe to run a VBScript or WSF file via Win+R
            ; LOLBAS: wscript.exe — Legitimate use: VBScript and WSF automation scripts (common in enterprise login scripts)
            ; Note: wscript.exe runs scripts with a GUI (message boxes visible); use cscript.exe for headless execution

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Send the wscript.exe command with the script path and optional args
            Send('{}{}')

        """.format(self.csh.counter.current(), escaped_command, "{ENTER}")

        return textwrap.dedent(_open_wscript)


    # --------------------------------------------------->
    # Wait for Script Completion

    def wait_for_completion(self):
        """
        Waits for wscript.exe to complete or times out.
        wscript.exe does not leave a persistent window open — it runs and exits.
        We sleep to allow the script time to execute before moving on.
        """

        wait_text = '\n'
        wait_text += '; Wait for wscript.exe to complete (or time out after ~30 seconds)\n'
        wait_text += 'sleep({})\n'.format(random.randint(5000, 30000))
        wait_text += '; Reset Focus\n'
        wait_text += 'SendKeepActive("")'

        return textwrap.indent(wait_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_wscript(self):
        """
        Closes the Wscript function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
