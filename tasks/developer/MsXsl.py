
# LOLBAS: msxsl.exe — Legitimate use: applying XSL stylesheets to transform XML documents
# DEVELOPER-ONLY: msxsl.exe is part of the Microsoft XML Core Services SDK and must be downloaded separately

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of msxsl.exe to perform XSL transformations
 on local XML files, producing transformed output. This is a common workflow when
 developing or testing XSLT stylesheets against XML data.

 Requires an input XML file path and an XSL stylesheet path.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsXsl(BaseCMD):
    """
    # LOLBAS: msxsl.exe — Legitimate use: applying XSL stylesheets to transform XML documents
    # DEVELOPER-ONLY: msxsl.exe must be downloaded separately as part of the Microsoft XML Core Services SDK

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsXsl, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsXsl'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msxsl >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msxsl >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.xml_file = None
        self.xsl_file = None
        self.output_file = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsXsl Interaction.
        [!] DEVELOPER-ONLY: msxsl.exe must be installed separately (Microsoft XML Core Services SDK).
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the input XML file path using 'xml_file <path>'
        3: Set the XSL stylesheet path using 'xsl_file <path>'
        4: Optionally set an output file path using 'output_file <path>'
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
    #  MsXsl Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsXsl interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsXsl_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_xml_file(self, xml_file):
        """
        Set the path to the input XML file to transform.
        Example: xml_file C:\\data\\input.xml
        """
        if xml_file:
            if self.taskstarted:
                self.xml_file = xml_file.strip()
                print(self.cl.green("[*] XML file set to: {}".format(self.xml_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsXsl Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to an XML file."))


    def do_xsl_file(self, xsl_file):
        """
        Set the path to the XSL stylesheet to apply.
        Example: xsl_file C:\\data\\transform.xsl
        """
        if xsl_file:
            if self.taskstarted:
                self.xsl_file = xsl_file.strip()
                print(self.cl.green("[*] XSL file set to: {}".format(self.xsl_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsXsl Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to an XSL stylesheet file."))


    def do_output_file(self, output_file):
        """
        Optionally set the output file path for the transformed result.
        If not set, output is printed to the console.
        Example: output_file C:\\data\\output.xml
        """
        if output_file:
            if self.taskstarted:
                self.output_file = output_file.strip()
                print(self.cl.green("[*] Output file set to: {}".format(self.output_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsXsl Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsXsl configuration
        """
        print(self.cl.green("[?] Currently Assigned MsXsl Configuration"))
        print("[>] XML File    : {}".format(self.xml_file if self.xml_file else "(not set)"))
        print("[>] XSL File    : {}".format(self.xsl_file if self.xsl_file else "(not set)"))
        print("[>] Output File : {}".format(self.output_file if self.output_file else "(not set — output to console)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.xml_file:
                print(self.cl.red("[!] <ERROR> Please set an XML file path using 'xml_file <path>'."))
                return
            if not self.xsl_file:
                print(self.cl.red("[!] <ERROR> Please set an XSL stylesheet path using 'xsl_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.xml_file = None
        self.xsl_file = None
        self.output_file = None


    ######################################################################
    # MsXsl AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsXsl_' + current_counter, self.create_autoit_function())


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
            xml_file : str — path to the input XML file
            xsl_file : str — path to the XSL stylesheet
        Optional JSON keys:
            output_file : str — path to write transformed output (omit to print to console)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.xml_file = kwargs.get("xml_file", None)
        self.xsl_file = kwargs.get("xsl_file", None)
        self.output_file = kwargs.get("output_file", None)

        if self.xml_file:
            print(f"[*] Setting xml_file attribute : {self.xml_file}")
        if self.xsl_file:
            print(f"[*] Setting xsl_file attribute : {self.xsl_file}")
        if self.output_file:
            print(f"[*] Setting output_file attribute : {self.output_file}")

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
        ; <      MsXsl Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsXsl_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsXsl_{}()

            ; Creates an MsXsl Interaction via CMD

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
        Builds the msxsl command to type into the CMD window.
        Transforms the specified XML file using the specified XSL stylesheet.
        Optionally writes output to a file using -o flag.
        """
        typing_text = '\n'

        # Build the msxsl command
        if self.output_file:
            msxsl_cmd = 'msxsl.exe {} {} -o {}'.format(
                self.xml_file, self.xsl_file, self.output_file
            )
        else:
            msxsl_cmd = 'msxsl.exe {} {}'.format(self.xml_file, self.xsl_file)

        typing_text += 'Send("' + self._escape_send(msxsl_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MsXsl AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
