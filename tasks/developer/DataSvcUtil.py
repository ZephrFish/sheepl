
# LOLBAS: DataSvcUtil.exe — Legitimate use: generating WCF Data Services client proxy classes from an OData feed
# DEVELOPER-ONLY: Requires .NET Framework 3.5 (C:\Windows\Microsoft.NET\Framework64\v3.5\DataSvcUtil.exe)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate developer use of DataSvcUtil.exe to generate
 WCF Data Services client data service classes from an OData feed URI.

 Requires an output path and an OData service URI. The tool writes
 generated .cs/.vb proxy classes to the specified output file so a
 .NET client application can consume the data service.

 The master script will already define the typing speed as part of
 the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class DataSvcUtil(BaseCMD):
    """
    # LOLBAS: DataSvcUtil.exe — Legitimate use: generating WCF Data Services client proxy classes from an OData feed

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(DataSvcUtil, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'DataSvcUtil'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > datasvcutil >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > datasvcutil >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Parameters for DataSvcUtil
        self.output_path = None
        self.service_uri = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] DataSvcUtil Interaction.
        Generates WCF Data Services client proxy classes from an OData feed.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the output file path using 'output_path <path>'
        3: Set the OData service URI using 'service_uri <uri>'
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
    #  DataSvcUtil Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new DataSvcUtil interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'DataSvcUtil_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_output_path(self, output_path):
        """
        Set the output file path for the generated proxy class file.
        Example: output_path C:\\dev\\NorthwindClient.cs
        """
        if output_path:
            if self.taskstarted:
                self.output_path = output_path.strip()
                print(self.cl.green("[*] Output path set to: {}".format(self.output_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DataSvcUtil Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path."))


    def do_service_uri(self, service_uri):
        """
        Set the OData service URI to generate proxy classes from.
        Example: service_uri http://services.odata.org/Northwind/Northwind.svc/
        """
        if service_uri:
            if self.taskstarted:
                self.service_uri = service_uri.strip()
                print(self.cl.green("[*] Service URI set to: {}".format(self.service_uri)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new DataSvcUtil Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a service URI."))


    def do_assigned(self, arg):
        """
        Get the current assigned DataSvcUtil configuration
        """
        print(self.cl.green("[?] Currently Assigned DataSvcUtil Configuration"))
        print("[>] Output Path  : {}".format(self.output_path if self.output_path else "(not set)"))
        print("[>] Service URI  : {}".format(self.service_uri if self.service_uri else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.output_path:
                print(self.cl.red("[!] <ERROR> output_path is required. Set it with 'output_path <path>'."))
                return
            if not self.service_uri:
                print(self.cl.red("[!] <ERROR> service_uri is required. Set it with 'service_uri <uri>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.output_path = None
        self.service_uri = None


    ######################################################################
    # DataSvcUtil AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('DataSvcUtil_' + current_counter, self.create_autoit_function())


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
            output_path : str — absolute path for the generated proxy class file
            service_uri : str — OData service URI to consume
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.output_path = kwargs.get("output_path", None)
        self.service_uri = kwargs.get("service_uri", None)

        if self.output_path:
            print(f"[*] Setting output_path attribute : {self.output_path}")
        else:
            print("[!] <WARNING> No output_path provided — this is required for DataSvcUtil")

        if self.service_uri:
            print(f"[*] Setting service_uri attribute : {self.service_uri}")
        else:
            print("[!] <WARNING> No service_uri provided — this is required for DataSvcUtil")

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
        ; <      DataSvcUtil Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "DataSvcUtil_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func DataSvcUtil_{}()

            ; Creates a DataSvcUtil Interaction via CMD

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
        Builds the DataSvcUtil command to type into the CMD window.
        Runs DataSvcUtil.exe with /out and /uri flags to generate proxy classes.
        """
        typing_text = '\n'

        # Build the DataSvcUtil command using the .NET Framework path
        datasvcutil_cmd = (
            'C:\\Windows\\Microsoft.NET\\Framework64\\v3.5\\DataSvcUtil.exe'
            ' /out:{} /uri:{}'.format(self.output_path, self.service_uri)
        )

        typing_text += 'Send("' + self._escape_send(datasvcutil_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the DataSvcUtil AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
