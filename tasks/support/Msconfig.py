
# LOLBAS: msconfig.exe — Legitimate use: launching System Configuration to review startup programs and services

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT/support use of msconfig.exe (System Configuration)
 to open the tool and review startup settings or boot options.

 Msconfig is a built-in Windows troubleshooting utility; this task opens it
 via Win+R, optionally navigates to a named tab, waits briefly, and closes.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Msconfig(BaseCMD):
    """
    # LOLBAS: msconfig.exe — Legitimate use: opening System Configuration to inspect startup and services

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Msconfig, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Msconfig'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > msconfig >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > msconfig >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional tab to navigate to inside msconfig (e.g. "Services", "Startup", "Boot", "General")
        self.tab_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Msconfig Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a tab to navigate to using 'tab_name <name>'
           Valid tab names: General, Boot, Services, Startup, Tools
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
    #  Msconfig Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Msconfig interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Msconfig_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_tab_name(self, tab_name):
        """
        Optionally set a tab to navigate to inside System Configuration.
        Valid options: General, Boot, Services, Startup, Tools
        Example: tab_name Services
        """
        valid_tabs = ['General', 'Boot', 'Services', 'Startup', 'Tools']
        if tab_name:
            if self.taskstarted:
                tab = tab_name.strip()
                if tab in valid_tabs:
                    self.tab_name = tab
                    print(self.cl.green("[*] Tab name set to: {}".format(self.tab_name)))
                else:
                    print(self.cl.red("[!] <ERROR> Invalid tab name. Choose from: {}".format(', '.join(valid_tabs))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Msconfig Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a tab name."))


    def do_assigned(self, arg):
        """
        Get the current assigned Msconfig configuration
        """
        print(self.cl.green("[?] Currently Assigned Msconfig Configuration"))
        print("[>] Tab Name : {}".format(self.tab_name if self.tab_name else "(not set — will open on default tab)"))


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
        self.tab_name = None


    ######################################################################
    # Msconfig AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Msconfig_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.text_typing_block() +
            self.close_msconfig()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            tab_name : str — name of a System Configuration tab to navigate to
                             (General, Boot, Services, Startup, Tools)
                             if absent, the tool opens on the default General tab
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.tab_name = kwargs.get("tab_name", None)
        if self.tab_name:
            print(f"[*] Setting tab_name attribute : {self.tab_name}")
        else:
            print("[*] No tab_name provided — will open on default General tab")

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
        ; <      Msconfig Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Msconfig_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens msconfig.exe via Win+R run dialogue and waits for the tool window
        """

        _open_toolwindow = """

        Func Msconfig_{}()

            ; Opens System Configuration (msconfig.exe) via Win+R

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Launch msconfig.exe
            Send('msconfig.exe{}')
            ; Wait for System Configuration window
            WinWaitActive("System Configuration", "", 15)

        """.format(self.csh.counter.current(), "{ENTER}")

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Typing Output

    def text_typing_block(self):
        """
        Builds the interaction block for the msconfig GUI window.
        Optionally clicks a named tab, waits, then closes the window.
        """
        typing_text = '\n'

        # Brief pause after the window opens
        typing_text += 'sleep({})\n'.format(random.randint(2000, 4000))

        if self.tab_name:
            # Navigate to the requested tab by sending Ctrl+Tab until we find it
            # Simpler approach: click the tab by name using ControlClick with tab text
            typing_text += '; Navigate to {} tab\n'.format(self.tab_name)
            typing_text += 'ControlClick("System Configuration", "", "' + self._escape_send(self.tab_name) + '")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Close the System Configuration window with Alt+F4
        typing_text += "; Close System Configuration\n"
        typing_text += 'Send("!{F4}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(1000, 2000))
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_msconfig(self):
        """
        Closes the Msconfig AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
