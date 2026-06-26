
# #######################################################################
#
#  Task : SchTasks Interaction
#
# #######################################################################

# LOLBAS: schtasks.exe — Legitimate use: task auditing and scheduling maintenance jobs

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of schtasks.exe for listing or creating scheduled tasks.
 IT admins use this for auditing existing tasks or setting up maintenance schedules
 such as backups and cleanups.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class SchTasks(BaseCMD):
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
        super(SchTasks, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'SchTasks'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > schtasks >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > schtasks >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.introduction = """
        ----------------------------------
        [!] SchTasks Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the action using 'action' (query or create)
        3: If creating, set task details using 'task_name', 'task_command', 'schedule'
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Default action is query (list tasks)
        self.action = 'query'
        self.task_name = ''
        self.task_command = ''
        self.schedule = 'daily'

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    #######################################################################
    #  SchTasks Console Commands
    #######################################################################

    def do_new(self, arg):
        """
        This command creates a new SchTasks interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'SchTasks_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)

    def do_action(self, arg):
        """
        Set the schtasks action.
        Valid values: query (list tasks) or create (create a new task)
        Default is 'query'.
        Example: action query
        Example: action create
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SchTasks Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        valid_actions = ['query', 'create']
        if arg.lower() in valid_actions:
            self.action = arg.lower()
            print(self.cl.green("[*] Action set to: {}".format(self.action)))
        else:
            print(self.cl.red("[!] Invalid action. Choose from: {}".format(', '.join(valid_actions))))

    def do_task_name(self, arg):
        """
        Set the scheduled task name (used when action=create).
        Example: task_name DailyBackup
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SchTasks Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        if arg:
            self.task_name = arg
            print(self.cl.green("[*] Task name set to: {}".format(self.task_name)))
        else:
            print(self.cl.red("[!] <ERROR> You need to provide a task name."))

    def do_task_command(self, arg):
        """
        Set the command to be scheduled (used when action=create).
        Example: task_command C:\\Scripts\\backup.bat
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SchTasks Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        if arg:
            self.task_command = arg
            print(self.cl.green("[*] Task command set to: {}".format(self.task_command)))
        else:
            print(self.cl.red("[!] <ERROR> You need to provide a task command."))

    def do_schedule(self, arg):
        """
        Set the schedule frequency (used when action=create).
        Valid values: daily, weekly, monthly
        Default is 'daily'.
        Example: schedule weekly
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new SchTasks Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        valid_schedules = ['daily', 'weekly', 'monthly']
        if arg.lower() in valid_schedules:
            self.schedule = arg.lower()
            print(self.cl.green("[*] Schedule set to: {}".format(self.schedule)))
        else:
            print(self.cl.red("[!] Invalid schedule. Choose from: {}".format(', '.join(valid_schedules))))

    def do_assigned(self, arg):
        """
        Get the currently assigned SchTasks configuration
        """
        print(self.cl.green("[?] Currently Assigned SchTasks Configuration"))
        print("[>] Action       : {}".format(self.action))
        if self.action == 'create':
            print("[>] Task Name    : {}".format(self.task_name if self.task_name else "Not set"))
            print("[>] Task Command : {}".format(self.task_command if self.task_command else "Not set"))
            print("[>] Schedule     : {}".format(self.schedule))

    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if self.action == 'create':
                if not self.task_name:
                    print(self.cl.red("[!] <ERROR> You need to set a task name using 'task_name'."))
                    return
                if not self.task_command:
                    print(self.cl.red("[!] <ERROR> You need to set a task command using 'task_command'."))
                    return
            self.create_autoIT_block()
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new SchTasks Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific variables for next interaction
        self.action = 'query'
        self.task_name = ''
        self.task_command = ''
        self.schedule = 'daily'

    ######################################################################
    # SchTasks AutoIT Block Definition
    #######################################################################

    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('SchTasks_' + current_counter, self.create_autoit_function())

    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.schtasks_command_block() +
            self.close_schtasks()
        )

        return autoIT_script

    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        this function sets the various object attributes in the same way
        that the interactive mode does

        JSON keys: action, task_name, task_command, schedule
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.action = kwargs.get("action", "query")
            print(f"[*] Setting the action attribute : {self.action}")

            if self.action == 'create':
                self.task_name = kwargs["task_name"]
                self.task_command = kwargs["task_command"]
                self.schedule = kwargs.get("schedule", "daily")
                print(f"[*] Setting the task_name attribute : {self.task_name}")
                print(f"[*] Setting the task_command attribute : {self.task_command}")
                print(f"[*] Setting the schedule attribute : {self.schedule}")

        except KeyError as e:
            print(self.cl.red("[!] Error Setting JSON Profile attributes, missing key: {}".format(e)))

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
        ; <        SchTasks Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "SchTasks_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)

    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func SchTasks_{}()

            ; Opens a command shell to run schtasks.exe

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
    # SchTasks Command Block

    def schtasks_command_block(self):
        """
        Builds the schtasks.exe command based on the configured action
        """
        typing_text = '\n'

        if self.action == 'query':
            # List all scheduled tasks in LIST format with verbose output
            schtasks_cmd = 'schtasks /query /fo LIST /v'
            typing_text += 'Send("' + self._escape_send(schtasks_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        elif self.action == 'create':
            # SERVER-ONLY: Use /s <remote_host> flag for remote task creation (server administration)
            schtasks_cmd = 'schtasks /create /tn "{}" /tr "{}" /sc {} /f'.format(
                self.task_name,
                self.task_command,
                self.schedule
            )
            typing_text += 'Send("' + self._escape_send(schtasks_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(3000, 8000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)

    # --------------------------------------------------->
    # Close AutoIT Function

    def close_schtasks(self):
        """
        Closes the SchTasks function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
