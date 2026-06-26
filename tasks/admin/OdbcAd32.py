
# LOLBAS: odbcad32.exe — Legitimate use: open ODBC Data Source Administrator to inspect configured DSNs and drivers

# #######################################################################
#
#  Task : OdbcAd32 Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of odbcad32.exe to open the ODBC Data Source
 Administrator GUI and browse configured User or System data sources and
 installed ODBC drivers.

 Takes an optional tab parameter to select which tab to view
 (UserDSN, SystemDSN, or Drivers); defaults to UserDSN.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class OdbcAd32(BaseCMD):
    """
    # LOLBAS: odbcad32.exe — Legitimate use: open ODBC Data Source Administrator to inspect configured DSNs and drivers

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(OdbcAd32, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'OdbcAd32'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > odbcad32 >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > odbcad32 >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Which tab to select: UserDSN, SystemDSN, or Drivers
        self.tab = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] OdbcAd32 Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a tab to view using 'tab <UserDSN|SystemDSN|Drivers>'
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
    #  OdbcAd32 Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new OdbcAd32 interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'OdbcAd32_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_tab(self, tab):
        """
        Optionally set which tab to navigate to in the ODBC Administrator window.
        Accepted values: UserDSN, SystemDSN, Drivers
        If not set, the window is opened and closed without changing tabs.
        Example: tab SystemDSN
        """
        valid_tabs = ('UserDSN', 'SystemDSN', 'Drivers')
        if tab:
            if self.taskstarted:
                if tab.strip() in valid_tabs:
                    self.tab = tab.strip()
                    print(self.cl.green("[*] Tab set to: {}".format(self.tab)))
                else:
                    print(self.cl.red("[!] <ERROR> Tab must be one of: {}".format(', '.join(valid_tabs))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new OdbcAd32 Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a tab name (UserDSN, SystemDSN, or Drivers)."))


    def do_assigned(self, arg):
        """
        Get the current assigned OdbcAd32 configuration
        """
        print(self.cl.green("[?] Currently Assigned OdbcAd32 Configuration"))
        print("[>] Tab : {}".format(self.tab if self.tab else "(not set — window will open then close)"))


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
        self.tab = None


    ######################################################################
    # OdbcAd32 AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('OdbcAd32_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_toolwindow() +
            self.text_typing_block() +
            self.close_odbcad32()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            tab : str — tab to navigate to: UserDSN, SystemDSN, or Drivers
                        if absent, the window is opened and closed without tab navigation
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.tab = kwargs.get("tab", None)
        if self.tab:
            print(f"[*] Setting tab attribute : {self.tab}")
        else:
            print("[*] No tab provided — will open ODBC Administrator and close")

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
        ; <      OdbcAd32 Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "OdbcAd32_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_toolwindow(self):
        """
        Opens the ODBC Data Source Administrator GUI via Win+R run dialogue
        """

        _open_toolwindow = """

        Func OdbcAd32_{}()

            ; Launches the ODBC Data Source Administrator GUI

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Launch odbcad32.exe
            Send('odbcad32.exe{}')
            ; Wait for the ODBC Data Source Administrator window
            WinWaitActive("ODBC Data Source Administrator", "", 15)

        """.format(self.csh.counter.current(), "{ENTER}")

        return textwrap.dedent(_open_toolwindow)


    # --------------------------------------------------->
    # Typing Output

    def text_typing_block(self):
        """
        Navigates the ODBC Administrator window.
        If a tab is configured, clicks through to that tab by sending Ctrl+Tab keystrokes.
        Always closes the window with Alt+F4 after a short dwell.
        """
        tab_order = ('UserDSN', 'SystemDSN', 'FileDSN', 'Drivers', 'Tracing', 'ConnectionPooling', 'About')

        typing_text = '\n'

        # Dwell briefly on the default (first) tab
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        if self.tab and self.tab in tab_order:
            tab_index = tab_order.index(self.tab)
            for _ in range(tab_index):
                typing_text += 'Send("^{TAB}")\n'
                typing_text += 'sleep({})\n'.format(random.randint(500, 1500))
            # Dwell on the chosen tab
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Close the GUI with Alt+F4
        typing_text += 'Send("!{F4}")\n'
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_odbcad32(self):
        """
        Closes the OdbcAd32 AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
