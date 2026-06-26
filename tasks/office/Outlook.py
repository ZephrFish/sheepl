
# #######################################################################
#
#  Task : Outlook Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Opens Outlook, composes an email, and sends it.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD
from utils.typing import TypeWriter


class Outlook(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(Outlook, self).__init__(csh, cl)

        self.taskname = 'Outlook'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > outlook >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > outlook >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False
        self.typing_threshold = None

        self.introduction = """
        ----------------------------------
        [!] Outlook Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set recipient using 'to'
        3: Set subject using 'subject'
        4: Set body using 'body' or 'body_file'
        5: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        self.recipient = ''
        self.subject = ''
        self.body_lines = []

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # Outlook Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new Outlook interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'Outlook_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] Outlook_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_to(self, recipient):
        """
        Set the recipient email address
        example: to user@domain.com
        """
        if recipient:
            if self.taskstarted:
                self.recipient = recipient
                print(self.cl.green("[*] Recipient set to: {}".format(recipient)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Outlook interaction first with 'new'."))


    def do_subject(self, subject):
        """
        Set the email subject line
        example: subject Weekly Status Update
        """
        if subject:
            if self.taskstarted:
                self.subject = subject
                print(self.cl.green("[*] Subject set to: {}".format(subject)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Outlook interaction first with 'new'."))


    def do_body(self, text):
        """
        Add a line of body text to the email
        example: body Please find attached the weekly report.
        """
        if text:
            if self.taskstarted:
                self.body_lines.append(text)
                print(self.cl.green("[*] Body line added: {}".format(text)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Outlook interaction first with 'new'."))


    def do_body_file(self, input_file):
        """
        Load body text from a file, one line per Send()
        example: body_file email_body.txt
        """
        if input_file:
            if self.taskstarted:
                try:
                    with open(input_file) as f:
                        for line in f.readlines():
                            self.body_lines.append(line.rstrip('\n'))
                except OSError as e:
                    print("[!] Error reading file : {} ({})".format(self.cl.red(input_file), e))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Outlook interaction first with 'new'."))


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
        Show current Outlook interaction settings
        """
        print(self.cl.green("[?] Current Outlook Settings"))
        print("[>] Recipient : {}".format(self.recipient or "Not set"))
        print("[>] Subject   : {}".format(self.subject or "Not set"))
        print("[>] Body lines: {}".format(len(self.body_lines)))


    def do_complete(self, arg):
        """
        Complete the Outlook interaction and generate the AutoIT block
        """
        if self.taskstarted:
            if self.recipient and self.subject:
                self.create_autoIT_block()
                self.complete_task()
                self.recipient = ''
                self.subject = ''
                self.body_lines = []
            else:
                print("{} Recipient and Subject must be set before completing".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new Outlook interaction first with 'new'."))


    ########################################################################
    # Outlook AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Outlook_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_outlook() +
            self.compose_email() +
            self.close_outlook()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.recipient = kwargs["to"]
            self.subject = kwargs["subject"]
            self.body_lines = kwargs.get("body", [])
            self.typing_threshold = kwargs.get("typing_threshold", None)

            print(f"[*] Recipient  : {self.recipient}")
            print(f"[*] Subject    : {self.subject}")
            print(f"[*] Body lines : {len(self.body_lines)}")

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
        ;             Outlook Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Outlook_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_outlook(self):

        _open_outlook = """

        Func Outlook_{}()

            ; Creates an Outlook Interaction

            Send("#r")
            WinWaitActive("Run", "", 10)
            Send("outlook{}")
            ; Wait for Outlook main window
            WinWaitActive("[CLASS:rctrl_renwnd32]", "", 20)
            SendKeepActive("[CLASS:rctrl_renwnd32]")
            Sleep(2000)

            ; Open a new email compose window
            Send("^n")
            Sleep(1500)

        """.format(str(self.csh.counter.current()), "{ENTER}")

        return textwrap.dedent(_open_outlook)


    def compose_email(self):
        """
        Generates the AutoIT block for filling in and sending the email
        """
        typing_text = '\n'

        if self.typing_threshold:
            tw = TypeWriter(threshold=self.typing_threshold)
            typing_text += tw.generate(self._escape_send(self.recipient)) + '\n'
        else:
            typing_text += 'Send("{}")\n'.format(self._escape_send(self.recipient))

        # Tab past Cc to Subject
        typing_text += 'Send("{TAB}{TAB}")\n'
        typing_text += 'Sleep({})\n'.format(random.randint(500, 1500))

        if self.typing_threshold:
            tw = TypeWriter(threshold=self.typing_threshold)
            typing_text += tw.generate(self._escape_send(self.subject)) + '\n'
        else:
            typing_text += 'Send("{}")\n'.format(self._escape_send(self.subject))

        # Tab into body area
        typing_text += 'Send("{TAB}")\n'
        typing_text += 'Sleep({})\n'.format(random.randint(500, 1500))

        for line in self.body_lines:
            escaped = self._escape_send(line)
            if self.typing_threshold:
                tw = TypeWriter(threshold=self.typing_threshold)
                typing_text += tw.generate(escaped) + '\n'
                typing_text += 'Send("{ENTER}")\n'
            else:
                typing_text += 'Send("' + escaped + '{ENTER}")\n'
            typing_text += 'Sleep({})\n'.format(random.randint(1000, 5000))

        # Send the email with Alt+S
        typing_text += 'Sleep({})\n'.format(random.randint(500, 2000))
        typing_text += 'Send("!s")\n'
        typing_text += 'Sleep(2000)\n'

        return textwrap.indent(typing_text, self.indent_space)


    def close_outlook(self):
        """
        Closes the Outlook function declaration
        """
        end_func = """

        ; Close Outlook
        Send("!{F4}")
        Sleep(1000)
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
