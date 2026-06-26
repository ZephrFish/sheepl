
# LOLBAS: wbemtest.exe — Legitimate use: WMI repository connectivity testing and diagnostics

# #######################################################################
#
#  Task : WbemTest Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of wbemtest.exe to open and
 browse the Windows Management Instrumentation (WMI) repository for
 system diagnostics and connectivity testing.

 Legitimate use cases:
   - IT staff querying WMI for system diagnostics
   - Troubleshooting WMI repository issues
   - Testing WMI namespace connectivity
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


DEFAULT_NAMESPACE = "root\\cimv2"
DEFAULT_BROWSE_TIME = 15


class WbemTest(BaseCMD):
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
        super(WbemTest, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'WbemTest'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > wbemtest >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > wbemtest >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific defaults
        self.namespace = DEFAULT_NAMESPACE
        self.browse_time = DEFAULT_BROWSE_TIME

        self.introduction = """
        ----------------------------------
        [!] WbemTest Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the WMI namespace using 'namespace'   (default: root\\cimv2)
        3: Set browse time using 'browse_time'       (seconds, default: 15)
        4: Show assigned settings using 'assigned'
        5: Complete the interaction using 'complete'
        ----------------------------------
        Common WMI namespaces:
          root\\cimv2          Standard hardware/OS classes (default)
          root\\default        Default WMI repository root
          root\\security       Security-related WMI classes
          root\\microsoftiisv2 IIS management classes
        """

        self.indent_space = '    '

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  WbemTest Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new WbemTest interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'WbemTest_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_namespace(self, namespace):
        """
        Set the WMI namespace for wbemtest to connect to.
        Default: root\\cimv2
        Examples:
            namespace root\\cimv2
            namespace root\\default
            namespace root\\security
            namespace root\\microsoftiisv2
        """
        if namespace:
            if self.taskstarted:
                self.namespace = namespace.strip()
                print(self.cl.green("[*] Namespace set to: {}".format(self.namespace)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new WbemTest Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No namespace supplied, using default: {}".format(self.namespace)))


    def do_browse_time(self, browse_time):
        """
        Set how long (in seconds) to keep wbemtest open before closing.
        Default: 15 seconds
        Example:
            browse_time 30
        """
        if browse_time:
            if self.taskstarted:
                try:
                    self.browse_time = int(browse_time.strip())
                    print(self.cl.green("[*] Browse time set to: {} seconds".format(self.browse_time)))
                except ValueError:
                    print(self.cl.red("[!] <ERROR> browse_time must be an integer number of seconds."))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new WbemTest Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No browse time supplied, using default: {} seconds".format(self.browse_time)))


    def do_assigned(self, arg):
        """
        Show the currently assigned namespace and browse time
        """
        print(self.cl.green("[?] Currently Assigned WbemTest Settings"))
        print("[>] Namespace   : {}".format(self.namespace))
        print("[>] Browse time : {} seconds".format(self.browse_time))


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

        # reset to defaults for next interaction
        self.namespace = DEFAULT_NAMESPACE
        self.browse_time = DEFAULT_BROWSE_TIME


    ######################################################################
    # WbemTest AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('WbemTest_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_wbemtest() +
            self.close_wbemtest()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            namespace   : the WMI namespace to connect to (default: root\\cimv2)
                          e.g. "root\\\\default", "root\\\\security"
            browse_time : seconds to keep wbemtest open (default: 15)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "namespace" in kwargs:
            self.namespace = kwargs["namespace"].strip()
        print(f"[*] Setting the namespace attribute : {self.namespace}")

        if "browse_time" in kwargs:
            try:
                self.browse_time = int(kwargs["browse_time"])
            except (ValueError, TypeError):
                print(self.cl.yellow("[!] Invalid browse_time, using default: {}".format(DEFAULT_BROWSE_TIME)))
                self.browse_time = DEFAULT_BROWSE_TIME
        print(f"[*] Setting the browse_time attribute : {self.browse_time} seconds")

        # once these have all been set, push the task on the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block


    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ------------------------------------------ >
        ;           WbemTest Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "WbemTest_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_wbemtest(self):
        """
        Opens wbemtest.exe via Win+R, waits for the WMI Tester dialog to appear,
        then sleeps for browse_time to simulate diagnostic browsing.
        The close block sends Alt+F4 to dismiss the dialog.
        """

        # Convert seconds to milliseconds for AutoIT Sleep()
        browse_time_ms = self.browse_time * 1000

        _open_wbemtest = """

        Func WbemTest_{}()

            ; Opens wbemtest.exe for WMI namespace: {}
            ; LOLBAS: wbemtest.exe — Legitimate use: WMI repository connectivity testing and diagnostics

            Send("#r")
            ; Wait for the Run dialogue window to appear
            WinWaitActive("Run", "", 10)
            ; Launch wbemtest
            Send('wbemtest{}')
            ; Wait for the WMI Tester dialog to become active
            WinWaitActive("Windows Management Instrumentation Tester", "", 10)
            SendKeepActive("Windows Management Instrumentation Tester")

            ; Simulate IT administrator browsing the WMI repository for diagnostics
            Sleep({})

        """.format(
            self.csh.counter.current(),
            self.namespace,
            "{ENTER}",
            browse_time_ms
        )

        return textwrap.dedent(_open_wbemtest)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_wbemtest(self):
        """
        Closes the wbemtest dialog with Alt+F4 and resets focus
        """

        end_func = """

        ; Close the wbemtest dialog
        Send("!{F4}")
        ; Reset Focus
        SendKeepActive("")

        EndFunc

        """

        return textwrap.dedent(end_func)
