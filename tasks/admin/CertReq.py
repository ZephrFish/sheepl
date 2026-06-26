
# LOLBAS: certreq.exe — Legitimate use: submitting and retrieving certificate requests from a CA
# #######################################################################
#
#  Task : CertReq Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT use of certreq.exe to submit a certificate
 signing request (CSR) file to a certificate authority (CA) endpoint
 and optionally save the response to a file.

 Takes a config_url (CA endpoint) and a request_file (local CSR path);
 optionally takes an output_file to save the CA response.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class CertReq(BaseCMD):
    """
    # LOLBAS: certreq.exe — Legitimate use: submitting certificate signing requests to a CA

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(CertReq, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'CertReq'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > certreq >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > certreq >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # CA URL endpoint (e.g. http://ca.internal/certsrv/mscep/mscep.dll)
        self.config_url = None
        # Path to local CSR / request file
        self.request_file = None
        # Optional file to save the CA response
        self.output_file = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CertReq Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the CA URL with 'config_url <url>'
        3: Set the request file path with 'request_file <path>'
        4: Optionally set an output file with 'output_file <path>'
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
    #  CertReq Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new CertReq interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'CertReq_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_config_url(self, config_url):
        """
        Set the CA configuration URL to submit the certificate request to.
        Example: config_url http://ca.corp.local/certsrv/mscep/mscep.dll
        """
        if config_url:
            if self.taskstarted:
                self.config_url = config_url.strip()
                print(self.cl.green("[*] Config URL set to: {}".format(self.config_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CertReq Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a CA URL."))


    def do_request_file(self, request_file):
        """
        Set the path to the local certificate request (CSR) file.
        Example: request_file C:\\Users\\user\\Documents\\request.req
        """
        if request_file:
            if self.taskstarted:
                self.request_file = request_file.strip()
                print(self.cl.green("[*] Request file set to: {}".format(self.request_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CertReq Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a request file path."))


    def do_output_file(self, output_file):
        """
        Optionally set a file path to save the CA response.
        Example: output_file C:\\Users\\user\\Documents\\response.txt
        """
        if output_file:
            if self.taskstarted:
                self.output_file = output_file.strip()
                print(self.cl.green("[*] Output file set to: {}".format(self.output_file)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new CertReq Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an output file path."))


    def do_assigned(self, arg):
        """
        Get the current assigned CertReq configuration
        """
        print(self.cl.green("[?] Currently Assigned CertReq Configuration"))
        print("[>] Config URL   : {}".format(self.config_url if self.config_url else "(not set)"))
        print("[>] Request File : {}".format(self.request_file if self.request_file else "(not set)"))
        print("[>] Output File  : {}".format(self.output_file if self.output_file else "(not set — response shown in terminal)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.config_url:
                print(self.cl.red("[!] <ERROR> config_url is required. Set it with 'config_url <url>'."))
                return
            if not self.request_file:
                print(self.cl.red("[!] <ERROR> request_file is required. Set it with 'request_file <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.config_url = None
        self.request_file = None
        self.output_file = None


    ######################################################################
    # CertReq AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('CertReq_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_certreq()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            config_url   : str — CA endpoint URL for -Post -config
            request_file : str — path to the local CSR / request file

        Optional JSON keys:
            output_file  : str — file path to save the CA response; if absent
                                 response is printed to the terminal
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.config_url = kwargs.get("config_url", None)
        self.request_file = kwargs.get("request_file", None)
        self.output_file = kwargs.get("output_file", None)

        if self.config_url:
            print(f"[*] Setting config_url attribute : {self.config_url}")
        if self.request_file:
            print(f"[*] Setting request_file attribute : {self.request_file}")
        if self.output_file:
            print(f"[*] Setting output_file attribute : {self.output_file}")
        else:
            print("[*] No output_file provided — CA response will be shown in terminal")

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
        ; <      CertReq Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "CertReq_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func CertReq_{}()

            ; Creates a CertReq Interaction via CMD

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
        Builds the certreq command to type into the CMD window.
        Submits the request file to the CA using -Post -config.
        If output_file is set, the CA response is saved to that path.
        """
        typing_text = '\n'

        # Build the certreq command
        if self.output_file:
            certreq_cmd = 'certreq -Post -config {} {} {}'.format(
                self.config_url, self.request_file, self.output_file
            )
        else:
            certreq_cmd = 'certreq -Post -config {} {}'.format(
                self.config_url, self.request_file
            )

        typing_text += 'Send("' + self._escape_send(certreq_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_certreq(self):
        """
        Closes the CertReq AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
