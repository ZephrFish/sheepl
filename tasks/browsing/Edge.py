
# #######################################################################
#
#  Task : Edge Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Opens Microsoft Edge and navigates to a destination URL.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Edge(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(Edge, self).__init__(csh, cl)

        self.taskname = 'Edge'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > edge >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > edge >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.introduction = """
        ----------------------------------
        [!] Edge Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the destination URL using 'url'
        3: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        self.destination_url = ''

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # Edge Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new Edge interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'Edge_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] Edge_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_url(self, destination):
        """
        Set the destination URL for Edge to navigate to
        """
        if destination:
            if self.taskstarted:
                self.destination_url = destination
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Edge Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        """
        if self.taskstarted:
            if self.destination_url:
                self.create_autoIT_block()
                self.complete_task()
            else:
                print("{} There is currently no URL assigned".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new Edge interaction first with 'new'."))


    ########################################################################
    # Edge AutoIT Block Definition
    ########################################################################

    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Edge_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_edge() +
            self.close_edge()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.destination_url = kwargs["destination_url"]
        print(f"[*] Setting the destination_url attribute : {self.destination_url}")

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ------------------------------------------ >
        ;              Edge Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Edge_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_edge(self):

        _open_edge = """

        Func Edge_{}()

            ; Creates an Edge Interaction

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('msedge {}{}')
            ; Wait for Edge window to appear
            WinWaitActive("[CLASS:Chrome_WidgetWin_1]", "", 15)
            SendKeepActive("[CLASS:Chrome_WidgetWin_1]")
            ; Simulate browsing time
            Sleep(20000)

        """.format(
            str(self.csh.counter.current()),
            self._escape_send(self.destination_url),
            "{ENTER}"
        )

        return textwrap.dedent(_open_edge)


    def close_edge(self):
        """
        Closes the Edge application function declaration
        """
        end_func = """

        ; Close the Edge window
        Send("!{F4}")
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
