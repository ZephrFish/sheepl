
# LOLBAS: wmic.exe — Legitimate use: IT support system information queries (deprecated in Win11 21H1+)

# #######################################################################
#
#  Task : WmicQuery Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of wmic.exe to query system information
 such as OS version, hardware details, running processes, and installed
 software. Note: wmic.exe is deprecated in Windows 11 build 21H1+ but
 remains present on many enterprise systems.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class WmicQuery(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(WmicQuery, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WmicQuery'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wmicquery >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wmicquery >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Default wmic query
        self.wmic_query = "os get Caption,Version,BuildNumber"

        self.introduction = """
        ----------------------------------
        [!] WmicQuery Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the wmic query using 'query'
        3: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  WmicQuery Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WmicQuery interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WmicQuery_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_query(self, query):
        """
        Set the wmic query string to execute.
        Default: os get Caption,Version,BuildNumber
        Examples:
            query os get Caption,Version,BuildNumber
            query process list brief
            query product get Name,Version
            query cpu get Name,NumberOfCores
        """
        if self.taskstarted:
            if query:
                self.wmic_query = query
                print(self.cl.green("[*] WMIC query set to: {}".format(self.wmic_query)))
            else:
                print(self.cl.yellow("[*] No query supplied, using default: {}".format(self.wmic_query)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new WmicQuery Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the currently assigned wmic query
        """
        print(self.cl.green("[?] Currently Assigned WMIC Query"))
        print("[>] {}".format(self.wmic_query))


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

        # reset query to default for next interaction
        self.wmic_query = "os get Caption,Version,BuildNumber"


    ######################################################################
    # WmicQuery AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WmicQuery_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.wmic_query_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            query : the wmic query string to execute
                    e.g. "os get Caption,Version,BuildNumber"
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "query" in kwargs:
            self.wmic_query = kwargs["query"]
        print(f"[*] Setting the wmic_query attribute : {self.wmic_query}")

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
        ; <      WmicQuery Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "WmicQuery_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens CMD via Win+R run dialogue
        """

        _open_commandshell = """

        Func WmicQuery_{}()

            ; Opens CMD to run wmic query

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
    # WMIC Query Block

    def wmic_query_block(self):
        """
        Sends the wmic command and exits the shell
        """

        query_text = '\n'
        query_text += 'Send("wmic ' + self._escape_send(self.wmic_query) + '{ENTER}")\n'
        query_text += 'sleep({})\n'.format(random.randint(3000, 10000))
        query_text += "Send('exit{ENTER}')\n"
        query_text += "; Reset Focus\n"
        query_text += 'SendKeepActive("")'

        return textwrap.indent(query_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the WmicQuery function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
