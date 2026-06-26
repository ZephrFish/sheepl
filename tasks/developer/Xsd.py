
# LOLBAS: xsd.exe — Legitimate use: generating XML schema definition files from XDR or XML data sources
# DEVELOPER-ONLY: Requires Windows SDK installation (ships with Visual Studio / Windows SDK)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of xsd.exe to generate XML Schema Definition
 (.xsd) files or C#/VB.NET class files from existing XML or XDR schema sources.
 Included with the Windows Software Development Kit (SDK).

 Takes an input_file parameter specifying the XML or XDR file to process,
 and an optional /outputdir to control where generated files are written.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Xsd(BaseCMD):
    """
    # LOLBAS: xsd.exe — Legitimate use: generating XML schema definition files from XDR or XML data sources
    # DEVELOPER-ONLY: Requires Windows SDK installation (ships with Visual Studio / Windows SDK)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Xsd, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Xsd'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > xsd >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > xsd >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Input file (XML or XDR) to process
        self.input_file = None
        # Optional output directory for generated files
        self.output_dir = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Xsd Interaction.
        [!] DEVELOPER-ONLY: Requires Windows SDK installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the input XML/XDR file using 'input_file <path>'
        3: Optionally set an output directory using 'output_dir <path>'
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
    #  Xsd Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Xsd interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Xsd_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_input_file(self, input_file):
        """
        Set the input XML or XDR file for xsd.exe to process.
        Example: input_file C:\\schemas\\data.xml
        Example: input_file C:\\schemas\\schema.xdr
        """
        if input_file:
            if self.taskstarted:
                self.input_file = input_file.strip()
                print(self.cl.green("[*] Input file set to: {}".format(self.input_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Xsd Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an input file path."))


    def do_output_dir(self, output_dir):
        """
        Optionally set the output directory for generated schema/class files.
        If not set, output is written to the current directory.
        Example: output_dir C:\\schemas\\output
        """
        if output_dir:
            if self.taskstarted:
                self.output_dir = output_dir.strip()
                print(self.cl.green("[*] Output directory set to: {}".format(self.output_dir)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Xsd Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output directory path."))


    def do_assigned(self, arg):
        """
        Get the current assigned Xsd configuration
        """
        print(self.cl.green("[?] Currently Assigned Xsd Configuration"))
        print("[>] Input File  : {}".format(self.input_file if self.input_file else "(not set)"))
        print("[>] Output Dir  : {}".format(self.output_dir if self.output_dir else "(not set — current directory)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.input_file:
                print(self.cl.red("[!] <ERROR> An input file is required. Use 'input_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.input_file = None
        self.output_dir = None


    ######################################################################
    # Xsd AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Xsd_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_xsd()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            input_file : str — path to the XML or XDR file to process with xsd.exe

        Optional JSON keys:
            output_dir : str — directory where generated files are written
                               if absent, output goes to current directory
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.input_file = kwargs.get("input_file", None)
        if self.input_file:
            print(f"[*] Setting input_file attribute : {self.input_file}")
        else:
            print("[!] No input_file provided — this is required for xsd.exe")

        self.output_dir = kwargs.get("output_dir", None)
        if self.output_dir:
            print(f"[*] Setting output_dir attribute : {self.output_dir}")
        else:
            print("[*] No output_dir provided — output will go to current directory")

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
        ; <      Xsd Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Xsd_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Xsd_{}()

            ; Creates an Xsd Interaction via CMD

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
        Builds the xsd.exe command to type into the CMD window.
        Processes the supplied input XML/XDR file to generate a schema,
        optionally writing output to the specified directory.
        """
        typing_text = '\n'

        # Build the xsd.exe command
        xsd_cmd = 'xsd.exe {}'.format(self.input_file)
        if self.output_dir:
            xsd_cmd += ' /outputdir:{}'.format(self.output_dir)

        typing_text += 'Send("' + self._escape_send(xsd_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_xsd(self):
        """
        Closes the Xsd AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
