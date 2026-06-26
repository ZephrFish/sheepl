
# LOLBAS: query.exe — Legitimate use: listing Remote Desktop Services sessions, users, and processes

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of query.exe (Remote Desktop Services MultiUser
 Query Utility) to list active RDS/terminal-server sessions, logged-on users,
 and running processes on the local machine.

 Supports the standard sub-commands: user, session, process.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Query(BaseCMD):
    """
    # LOLBAS: query.exe — Legitimate use: listing RDS sessions, users, and processes

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Query, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Query'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > query >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > query >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Sub-command: user, session, or process
        self.subcommand = 'user'

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Query Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set the sub-command using 'subcommand <user|session|process>'
           (default: user)
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
    #  Query Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Query interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Query_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_subcommand(self, subcommand):
        """
        Set the query.exe sub-command to run.
        Valid values: user, session, process
        Default: user
        Example: subcommand session
        """
        valid = ('user', 'session', 'process', 'termsession')
        if subcommand:
            if self.taskstarted:
                sub = subcommand.strip().lower()
                if sub in valid:
                    self.subcommand = sub
                    print(self.cl.green("[*] Sub-command set to: {}".format(self.subcommand)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid sub-command. Choose from: {}".format(', '.join(valid))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Query Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a sub-command (user, session, process)."))


    def do_assigned(self, arg):
        """
        Get the current assigned Query configuration
        """
        print(self.cl.green("[?] Currently Assigned Query Configuration"))
        print("[>] Sub-command : {}".format(self.subcommand))


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
        self.subcommand = 'user'


    ######################################################################
    # Query AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Query_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_query()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            subcommand : str — query.exe sub-command to run (user, session, process)
                               defaults to 'user' if absent
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.subcommand = kwargs.get("subcommand", "user")
        print(f"[*] Setting subcommand attribute : {self.subcommand}")

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
        ; <      Query Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Query_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Query_{}()

            ; Creates a Query Interaction via CMD

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
        Builds the query.exe command to type into the CMD window.
        Runs: query <subcommand>
        """
        typing_text = '\n'

        query_cmd = 'query {}'.format(self.subcommand)
        typing_text += 'Send("' + self._escape_send(query_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_query(self):
        """
        Closes the Query AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
