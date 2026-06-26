
# #######################################################################
#
#  Task : Teams Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Opens Microsoft Teams, navigates to a channel or chat, and sends a message.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD
from utils.typing import TypeWriter


class Teams(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(Teams, self).__init__(csh, cl)

        self.taskname = 'Teams'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > teams >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > teams >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False
        self.typing_threshold = None

        self.introduction = """
        ----------------------------------
        [!] Teams Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set channel or chat name using 'channel'
        3: Add messages using 'message'
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '
        self.channel = ''
        self.messages = []

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # Teams Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new Teams interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'Teams_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] Teams_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_channel(self, channel):
        """
        Set the channel or person name to navigate to via Teams search
        example: channel General
        example: channel John Smith
        """
        if channel:
            if self.taskstarted:
                self.channel = channel
                print(self.cl.green("[*] Channel/chat set to: {}".format(channel)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Teams interaction first with 'new'."))


    def do_message(self, text):
        """
        Add a message to send
        example: message Hey team, standup in 5 minutes
        """
        if text:
            if self.taskstarted:
                self.messages.append(text)
                print(self.cl.green("[*] Message added: {}".format(text)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Teams interaction first with 'new'."))


    def do_typing_threshold(self, threshold):
        """
        Set typing realism level: epic / good / average / poor
        Use 'none' to revert to simple Send().
        example: typing_threshold average
        """
        valid = ['epic', 'good', 'average', 'poor', 'none']
        if threshold.lower() in valid:
            self.typing_threshold = None if threshold.lower() == 'none' else threshold.lower()
            print(self.cl.green("[*] Typing threshold set to: {}".format(threshold.lower())))
        else:
            print(self.cl.red("[!] Invalid threshold. Choose from: {}".format(', '.join(valid))))


    def do_assigned(self, arg):
        """
        Show currently assigned Teams settings
        """
        print(self.cl.green("[?] Current Teams Settings"))
        print("[>] Channel  : {}".format(self.channel or "Not set"))
        print("[>] Messages : {}".format(len(self.messages)))
        for msg in self.messages:
            print("    [>] {}".format(msg))


    def do_complete(self, arg):
        """
        Complete the Teams interaction and generate the AutoIT block
        """
        if self.taskstarted:
            if self.channel and self.messages:
                self.create_autoIT_block()
                self.complete_task()
                self.channel = ''
                self.messages = []
            else:
                print("{} Channel and at least one message must be set before completing".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new Teams interaction first with 'new'."))


    ########################################################################
    # Teams AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Teams_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_teams() +
            self.navigate_and_message() +
            self.close_teams()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.channel = kwargs["channel"]
            self.messages = kwargs["messages"]
            self.typing_threshold = kwargs.get("typing_threshold", None)

            print(f"[*] Channel  : {self.channel}")
            print(f"[*] Messages : {len(self.messages)}")

        except KeyError as e:
            print(self.cl.red("[!] Error setting JSON Profile attributes, missing key: {}".format(e)))

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ------------------------------------------ >
        ;             Teams Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Teams_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_teams(self):

        _open_teams = """

        Func Teams_{}()

            ; Creates a Teams Interaction

            Send("#r")
            WinWaitActive("Run", "", 10)
            Send("msteams{}")
            ; Wait for Teams window to appear
            WinWaitActive("[CLASS:Chrome_WidgetWin_1]", "", 25)
            SendKeepActive("[CLASS:Chrome_WidgetWin_1]")
            ; Allow Teams to fully load
            Sleep(4000)

        """.format(str(self.csh.counter.current()), "{ENTER}")

        return textwrap.dedent(_open_teams)


    def navigate_and_message(self):
        """
        Generates the AutoIT block for navigating to a channel and sending messages
        """
        typing_text = '\n'

        # Use Ctrl+F (search) to navigate to the channel or person
        typing_text += 'Send("^f")\n'
        typing_text += 'Sleep(1000)\n'

        if self.typing_threshold:
            tw = TypeWriter(threshold=self.typing_threshold)
            typing_text += tw.generate(self._escape_send(self.channel)) + '\n'
        else:
            typing_text += 'Send("{}")\n'.format(self._escape_send(self.channel))

        typing_text += 'Sleep(1500)\n'
        typing_text += 'Send("{ENTER}")\n'
        typing_text += 'Sleep(2000)\n'

        # Type and send each message
        for msg in self.messages:
            escaped = self._escape_send(msg)
            if self.typing_threshold:
                tw = TypeWriter(threshold=self.typing_threshold)
                typing_text += tw.generate_command(escaped, indent='') + '\n'
            else:
                typing_text += 'Send("' + escaped + '{ENTER}")\n'
            typing_text += 'Sleep({})\n'.format(random.randint(3000, 15000))

        return textwrap.indent(typing_text, self.indent_space)


    def close_teams(self):
        """
        Closes the Teams function declaration
        """
        end_func = """

        ; Reset focus
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
