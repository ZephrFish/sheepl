
# #######################################################################
#
#  Task : BitsAdmin Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of bitsadmin.exe to list and monitor
 Background Intelligent Transfer Service (BITS) transfer jobs.

 Takes an optional job_name parameter; if absent lists all active jobs.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class BitsAdmin(BaseCMD):
    """
    # LOLBAS: bitsadmin.exe — Legitimate use: monitoring Windows Update and BITS transfer jobs

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(BitsAdmin, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'BitsAdmin'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > bitsadmin >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > bitsadmin >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional job name to monitor a specific BITS job
        self.job_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] BitsAdmin Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a specific job to monitor using 'job_name <name>'
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
    #  BitsAdmin Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new BitsAdmin interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'BitsAdmin_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_job_name(self, job_name):
        """
        Optionally set a specific BITS job name to monitor.
        If not set, all active jobs will be listed.
        Example: job_name WUClient-SelfUpdate-ActiveX
        """
        if job_name:
            if self.taskstarted:
                self.job_name = job_name.strip()
                print(self.cl.green("[*] Job name set to: {}".format(self.job_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new BitsAdmin Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a job name."))


    def do_assigned(self, arg):
        """
        Get the current assigned BitsAdmin configuration
        """
        print(self.cl.green("[?] Currently Assigned BitsAdmin Configuration"))
        print("[>] Job Name : {}".format(self.job_name if self.job_name else "(not set — will list all jobs)"))


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

        # reset task-specific state for the next interaction
        self.job_name = None


    ######################################################################
    # BitsAdmin AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('BitsAdmin_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_bitsadmin()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            job_name : str — name of a specific BITS job to query with /info
                             if absent, only /list /allusers /verbose is run
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.job_name = kwargs.get("job_name", None)
        if self.job_name:
            print(f"[*] Setting job_name attribute : {self.job_name}")
        else:
            print("[*] No job_name provided — will list all active BITS jobs")

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
        ; <      BitsAdmin Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "BitsAdmin_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func BitsAdmin_{}()

            ; Creates a BitsAdmin Interaction via CMD

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
        Builds the bitsadmin commands to type into the CMD window.
        Always lists all jobs with /list /allusers /verbose.
        If job_name is set, also queries that specific job with /info.
        """
        typing_text = '\n'

        # Always list all active BITS jobs verbosely
        list_cmd = 'bitsadmin /list /allusers /verbose'
        typing_text += 'Send("' + self._escape_send(list_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        # Optionally query a specific job by name
        if self.job_name:
            info_cmd = 'bitsadmin /info {}'.format(self.job_name)
            typing_text += 'Send("' + self._escape_send(info_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_bitsadmin(self):
        """
        Closes the BitsAdmin AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
