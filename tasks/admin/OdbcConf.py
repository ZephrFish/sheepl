
# LOLBAS: odbcconf.exe — Legitimate use: managing ODBC drivers and data source names (DSNs) on Windows

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of odbcconf.exe to install an ODBC driver
 and configure a system DSN, as commonly performed by database administrators
 when provisioning database connectivity on Windows workstations or servers.

 Takes optional driver_name, driver_dll, and dsn_name parameters.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class OdbcConf(BaseCMD):
    """
    # LOLBAS: odbcconf.exe — Legitimate use: installing ODBC drivers and configuring system DSNs

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(OdbcConf, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'OdbcConf'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > odbcconf >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > odbcconf >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # ODBC driver name and DLL to install
        self.driver_name = None
        # DSN name to configure
        self.dsn_name = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] OdbcConf Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the ODBC driver name using 'driver_name <name>'
        3: Set the DSN name using 'dsn_name <name>'
        4: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  OdbcConf Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new OdbcConf interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'OdbcConf_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_driver_name(self, driver_name):
        """
        Set the ODBC driver name to install.
        This is the friendly name registered in the Windows ODBC manager.
        Example: driver_name SQL Server Native Client 11.0
        """
        if driver_name:
            if self.taskstarted:
                self.driver_name = driver_name.strip()
                print(self.cl.green("[*] Driver name set to: {}".format(self.driver_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new OdbcConf Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a driver name."))


    def do_dsn_name(self, dsn_name):
        """
        Set the system DSN name to configure after driver installation.
        Example: dsn_name CorpDatabase
        """
        if dsn_name:
            if self.taskstarted:
                self.dsn_name = dsn_name.strip()
                print(self.cl.green("[*] DSN name set to: {}".format(self.dsn_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new OdbcConf Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DSN name."))


    def do_assigned(self, arg):
        """
        Get the current assigned OdbcConf configuration
        """
        print(self.cl.green("[?] Currently Assigned OdbcConf Configuration"))
        print("[>] Driver Name : {}".format(self.driver_name if self.driver_name else "(not set — will use default: CorpSQLDriver)"))
        print("[>] DSN Name    : {}".format(self.dsn_name if self.dsn_name else "(not set — will use default: CorpDSN)"))


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
        self.driver_name = None
        self.dsn_name = None


    ######################################################################
    # OdbcConf AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('OdbcConf_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_odbcconf()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Optional JSON keys:
            driver_name : str — friendly name for the ODBC driver to install
                                defaults to 'CorpSQLDriver' if absent
            dsn_name    : str — system DSN name to configure
                                defaults to 'CorpDSN' if absent
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.driver_name = kwargs.get("driver_name", None)
        if self.driver_name:
            print(f"[*] Setting driver_name attribute : {self.driver_name}")
        else:
            print("[*] No driver_name provided — will use default: CorpSQLDriver")

        self.dsn_name = kwargs.get("dsn_name", None)
        if self.dsn_name:
            print(f"[*] Setting dsn_name attribute : {self.dsn_name}")
        else:
            print("[*] No dsn_name provided — will use default: CorpDSN")

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
        ; <      OdbcConf Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "OdbcConf_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func OdbcConf_{}()

            ; Creates an OdbcConf Interaction via CMD

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
        Builds the odbcconf.exe commands to type into the CMD window.
        Installs an ODBC driver and configures a system DSN using
        odbcconf INSTALLDRIVER and configsysdsn — the standard administrative workflow.
        """

        # Apply defaults if not supplied interactively or via JSON
        driver = self.driver_name if self.driver_name else 'CorpSQLDriver'
        dsn = self.dsn_name if self.dsn_name else 'CorpDSN'

        typing_text = '\n'

        # Install the ODBC driver by registering it with Windows
        install_cmd = 'odbcconf INSTALLDRIVER "{}|Driver=sqlncli11.dll|APILevel=2"'.format(driver)
        typing_text += 'Send("' + self._escape_send(install_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Configure a system DSN bound to the installed driver
        config_cmd = 'odbcconf configsysdsn "{}" "DSN={}"'.format(driver, dsn)
        typing_text += 'Send("' + self._escape_send(config_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_odbcconf(self):
        """
        Closes the OdbcConf AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
