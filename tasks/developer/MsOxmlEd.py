# LOLBAS: msoxmled.exe — Legitimate use: opening XML documents via Microsoft Office XML Editor
# DEVELOPER-ONLY: requires Microsoft Office installation (Office 14/16 shared component)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of msoxmled.exe to open an XML document from a URL,
 as would occur when a developer or Office user opens a remote XML file for
 editing via the Microsoft Office XML Editor shared component.

 Takes a required xml_url parameter specifying the remote XML document to open.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class MsOxmlEd(BaseCMD):
    """
    # LOLBAS: msoxmled.exe — Legitimate use: opening XML documents via Microsoft Office XML Editor
    # DEVELOPER-ONLY: requires Microsoft Office installation (Office 14/16 shared component)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(MsOxmlEd, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'MsOxmlEd'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msoxmled >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msoxmled >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the remote XML document to open
        self.xml_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] MsOxmlEd Interaction.
        [!] DEVELOPER-ONLY: requires Microsoft Office installation.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the remote XML URL using 'xml_url <url>'
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
    #  MsOxmlEd Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new MsOxmlEd interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'MsOxmlEd_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_xml_url(self, xml_url):
        """
        Set the remote URL of the XML document to open with msoxmled.exe.
        Example: xml_url http://intranet.corp.local/schemas/config.xml
        """
        if xml_url:
            if self.taskstarted:
                self.xml_url = xml_url.strip()
                print(self.cl.green("[*] XML URL set to: {}".format(self.xml_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new MsOxmlEd Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a remote XML URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned MsOxmlEd configuration
        """
        print(self.cl.green("[?] Currently Assigned MsOxmlEd Configuration"))
        print("[>] XML URL : {}".format(self.xml_url if self.xml_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.xml_url:
                print(self.cl.red("[!] <ERROR> xml_url is required. Set it with 'xml_url <url>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.xml_url = None


    ######################################################################
    # MsOxmlEd AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('MsOxmlEd_' + current_counter, self.create_autoit_function())


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
            xml_url : str — remote URL of the XML document to open with msoxmled.exe
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.xml_url = kwargs.get("xml_url", None)
        if self.xml_url:
            print(f"[*] Setting xml_url attribute : {self.xml_url}")
        else:
            print("[!] <ERROR> xml_url is required for MsOxmlEd task.")
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
        ; <      MsOxmlEd Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "MsOxmlEd_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func MsOxmlEd_{}()

            ; Creates a MsOxmlEd Interaction via CMD

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
        Builds the msoxmled command to type into the CMD window.
        Opens a remote XML document using the /verb open switch.
        """
        typing_text = '\n'

        # Open remote XML document with msoxmled.exe using /verb open
        open_cmd = 'msoxmled.exe /verb open {}'.format(self.xml_url)
        typing_text += 'Send("' + self._escape_send(open_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the MsOxmlEd AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
