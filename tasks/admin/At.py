
# LOLBAS: at.exe — Legitimate use: scheduling periodic administrative tasks on Windows 7 and older

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of at.exe to schedule periodic administrative
 tasks on Windows 7 and older systems. Supports scheduling a command to run
 at a specific time, optionally on a recurring daily basis.

 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class At(BaseCMD):
    """
    # LOLBAS: at.exe — Legitimate use: scheduling periodic administrative tasks (Windows 7 and older)

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(At, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'At'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > at >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > at >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific parameters
        self.schedule_time = None
        self.command = None
        self.recurring = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] At Interaction.
        Note: at.exe is only available on Windows 7 and older systems.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the time to schedule the task using 'schedule_time <HH:MM>'
        3: Set the command to run using 'command <cmd>'
        4: Optionally enable daily recurrence using 'recurring'
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
    #  At Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new At interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'At_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_schedule_time(self, schedule_time):
        """
        Set the time at which to schedule the task (24-hour format HH:MM).
        Example: schedule_time 09:00
        """
        if schedule_time:
            if self.taskstarted:
                self.schedule_time = schedule_time.strip()
                print(self.cl.green("[*] Schedule time set to: {}".format(self.schedule_time)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new At Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a time in HH:MM format."))


    def do_command(self, command):
        """
        Set the command to be scheduled for execution.
        Example: command notepad.exe
        """
        if command:
            if self.taskstarted:
                self.command = command.strip()
                print(self.cl.green("[*] Command set to: {}".format(self.command)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new At Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a command to schedule."))


    def do_recurring(self, arg):
        """
        Enable daily recurrence for the scheduled task (/every:m,t,w,th,f,s,su).
        Example: recurring
        """
        if self.taskstarted:
            self.recurring = True
            print(self.cl.green("[*] Recurring daily schedule enabled."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new At Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current assigned At configuration
        """
        print(self.cl.green("[?] Currently Assigned At Configuration"))
        print("[>] Schedule Time : {}".format(self.schedule_time if self.schedule_time else "(not set)"))
        print("[>] Command       : {}".format(self.command if self.command else "(not set)"))
        print("[>] Recurring     : {}".format("yes" if self.recurring else "no"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.schedule_time:
                print(self.cl.red("[!] <ERROR> Please set a schedule time using 'schedule_time HH:MM'."))
                return
            if not self.command:
                print(self.cl.red("[!] <ERROR> Please set a command to run using 'command <cmd>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.schedule_time = None
        self.command = None
        self.recurring = False


    ######################################################################
    # At AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('At_' + current_counter, self.create_autoit_function())


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
            schedule_time : str — time in HH:MM format to schedule the task
            command       : str — command to be scheduled for execution

        Optional JSON keys:
            recurring     : bool — if True, schedule as a daily recurring task
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.schedule_time = kwargs.get("schedule_time", None)
        self.command = kwargs.get("command", None)
        self.recurring = kwargs.get("recurring", False)

        if self.schedule_time:
            print(f"[*] Setting schedule_time attribute : {self.schedule_time}")
        if self.command:
            print(f"[*] Setting command attribute : {self.command}")
        if self.recurring:
            print("[*] Recurring daily schedule enabled")

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
        ; <      At Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "At_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func At_{}()

            ; Creates an At Interaction via CMD

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
        Builds the at.exe commands to type into the CMD window.
        Schedules a command at the specified time, with optional daily recurrence.
        Also lists current scheduled tasks after creating the new one.
        """
        typing_text = '\n'

        # Build the at.exe scheduling command
        if self.recurring:
            at_cmd = 'at {} /every:m,t,w,th,f,s,su {}'.format(self.schedule_time, self.command)
        else:
            at_cmd = 'at {} {}'.format(self.schedule_time, self.command)

        typing_text += 'Send("' + self._escape_send(at_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # List all currently scheduled tasks to confirm
        typing_text += 'Send("' + self._escape_send('at') + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the At AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
