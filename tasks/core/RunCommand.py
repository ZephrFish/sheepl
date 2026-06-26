
# #######################################################################
#
#  Task : RunCommand Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Takes a supplied text file for the Sheepl to type
 the master script will already define the typing speed as part of the master declarations

"""

__author__ = "Matt Lorentzen"
__license__ = "MIT"

import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class RunCommand(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(RunCommand, self).__init__(csh, cl)


        # Override the defined task name
        self.taskname = 'RunCommand'
        
        # current Sheepl Object
        # which might need to be renamed to Sheepl
        self.csh = csh
        # current colour object
        self.cl = cl
       
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > command >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > runcommand >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False

        # creating my own
        self.introduction = """
        ----------------------------------
        [!] RunCommand Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Basically anything that you want to pass to the run command
        3: If it spawns errors, you can clean them out with 'killwindow <title>'
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # List to hold commands for current interaction
        self.command = ''
               
        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking 
        # if we are parsing JSON
        
        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()

    ########################################################################
    # RunCommand Console Commands
    ########################################################################

    def do_new(self, arg):
        """
        Start a new RunCommand interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'RunCommand_{}'".format(str(self.csh.counter.current())))
            # OCD Line break
            print()
            self.prompt = self.cl.blue("[*] RunCommand_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_cmd(self, command):
        """
        This is the command to execute from the 'run' prompt
        """

        if command:
            if self.taskstarted:
                self.command = command
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new RunCommand Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Get the current list of assigned CMD commands
        """
        print(self.cl.green("[?] Currently Assigned Commands "))
        print("[>] {}".format(self.command))


    def do_complete(self, arg):
        """
        Creates the command call
        """

        if self.taskstarted:
            if self.command:
                self.create_autoIT_block()
                
                # now reset the tracking values and prompt
                self.complete_task()
                # reset the command
                self.command = ''

            else:
                print("{} There are currently no command assigned".format(self.cl.red("[!]")))
                print("{} Assign some commands using 'cmd <command>'".format(self.cl.red("[-]")))
                return None


    ########################################################################
    #  RunCommand AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
   
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('RunCommand_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_RunCommand() +
            self.close_RunCommand()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        this function sets the various object attributes in the same way
        that the interactive mode does
        """
    
        print("[%] Setting attributes from JSON Profile")
        # This snippet takes the keys ignoring the first key which is task and then shows
        # what should be set in the kwargs parsing. 
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")
        self.command = kwargs["cmd"][0]
        if len(kwargs["cmd"]) > 1:
            print(self.cl.red("[!] Multiple run entries are detected - only the first one will be used"))
        print(f"[*] Setting the command attribute : {self.command}")

        # once these have all been set in here, then self.create_autoIT_block() gets called which pushes the task on the stack
        self.create_autoIT_block()
           
    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        when using textwrap.dedent you need to add in the backslash
        to the start of the multiline
        """

        function_declaration = """
        ; < ------------------------------------ >
        ;         RunCommand Interaction
        ; < ------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "RunCommand_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_RunCommand(self):

        _open_runcommand = """

        Func RunCommand_{}()

            ; Creates a RunCommand Interaction

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; note this needs to be escaped
            Send('{}{}')

            ; add in a check to see if a not found window appears


        """.format(self.csh.counter.current(), self.command, '{ENTER}')

        return textwrap.dedent(_open_runcommand)



    def close_RunCommand(self):
        """
        Closes the RunCommand application function declaration
        """

        end_func = """

        WinClose("Run")
        EndFunc

        """

        return textwrap.dedent(end_func)


