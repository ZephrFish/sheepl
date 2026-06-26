
# LOLBAS: Powerpnt.exe — Legitimate use: opening Microsoft PowerPoint presentations

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate user activity with powerpnt.exe (Microsoft PowerPoint).
 Opens PowerPoint with a specified local presentation file, waits briefly,
 then closes the application.

 Takes a required presentation_path parameter pointing to a local .pptx file.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class PowerPnt(BaseCMD):
    """
    # LOLBAS: Powerpnt.exe — Legitimate use: opening Microsoft PowerPoint presentations

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(PowerPnt, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PowerPnt'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > powerpnt >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > powerpnt >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the local PowerPoint presentation to open
        self.presentation_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] PowerPnt Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the presentation file to open using 'presentation_path <path>'
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
    #  PowerPnt Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new PowerPnt interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'PowerPnt_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_presentation_path(self, presentation_path):
        """
        Set the local path to the PowerPoint presentation file to open.
        Example: presentation_path C:\\Users\\user\\Documents\\quarterly_report.pptx
        """
        if presentation_path:
            if self.taskstarted:
                self.presentation_path = presentation_path.strip()
                print(self.cl.green("[*] Presentation path set to: {}".format(self.presentation_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new PowerPnt Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a path to a PowerPoint file."))


    def do_assigned(self, arg):
        """
        Get the current assigned PowerPnt configuration
        """
        print(self.cl.green("[?] Currently Assigned PowerPnt Configuration"))
        print("[>] Presentation Path : {}".format(self.presentation_path if self.presentation_path else "(not set — PowerPoint will open to start screen)"))


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
        self.presentation_path = None


    ######################################################################
    # PowerPnt AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PowerPnt_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.text_typing_block() +
            self.close_powerpnt()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            presentation_path : str — local path to a .pptx file to open
                                      if absent, PowerPoint opens to the start screen
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.presentation_path = kwargs.get("presentation_path", None)
        if self.presentation_path:
            print(f"[*] Setting presentation_path attribute : {self.presentation_path}")
        else:
            print("[*] No presentation_path provided — PowerPoint will open to the start screen")

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
        ; <      PowerPnt Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "PowerPnt_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens PowerPoint via Win+R run dialogue, optionally with a presentation file.
        Waits for the PowerPoint window to become active.
        """

        if self.presentation_path:
            run_cmd = 'powerpnt.exe "{}"'.format(self.presentation_path)
        else:
            run_cmd = 'powerpnt.exe'

        _open_toolwindow = """

        Func PowerPnt_{}()

            ; Opens PowerPoint via the Run dialogue

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            Send('{}')
            ; Wait for PowerPoint to load
            WinWaitActive("PowerPoint", "", 20)
            sleep({})

        """.format(
            self.csh.counter.current(),
            self._escape_send(run_cmd) + "{ENTER}",
            random.randint(3000, 8000)
        )

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Typing Output

    def text_typing_block(self):
        """
        Simulates brief user activity in PowerPoint then closes the application.
        """
        typing_text = '\n'

        # Brief pause to simulate reading the presentation
        typing_text += 'sleep({})\n'.format(random.randint(3000, 10000))

        # Close PowerPoint with Alt+F4
        typing_text += 'Send("!{F4}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(1000, 3000))

        # Handle potential "Save changes?" dialog — dismiss without saving
        typing_text += '; Dismiss any save dialog without saving\n'
        typing_text += 'Send("n")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_powerpnt(self):
        """
        Closes the PowerPnt AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
