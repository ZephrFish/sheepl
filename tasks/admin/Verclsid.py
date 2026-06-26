
# LOLBAS: verclsid.exe — Legitimate use: verifying COM objects before instantiation by Windows Explorer

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of verclsid.exe to verify a COM object
 before it is instantiated by Windows Explorer.

 Takes an optional clsid parameter representing the COM object CLSID
 to verify. If not set, a common shell CLSID is used as a default.

 The master script will already define the typing speed as part of the
 master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Verclsid(BaseCMD):
    """
    # LOLBAS: verclsid.exe — Legitimate use: verifying COM objects before instantiation by Windows Explorer

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Verclsid, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Verclsid'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > verclsid >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > verclsid >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Optional CLSID to verify — defaults to the Shell Folder CLSID if not set
        self.clsid = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Verclsid Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set a CLSID to verify using 'clsid <{CLSID}>'
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
    #  Verclsid Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Verclsid interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Verclsid_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_clsid(self, clsid):
        """
        Optionally set a specific COM object CLSID to verify.
        If not set, the Shell Folder CLSID {20D04FE0-3AEA-1069-A2D8-08002B30309D} is used.
        Example: clsid {20D04FE0-3AEA-1069-A2D8-08002B30309D}
        """
        if clsid:
            if self.taskstarted:
                self.clsid = clsid.strip()
                print(self.cl.green("[*] CLSID set to: {}".format(self.clsid)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Verclsid Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a CLSID value."))


    def do_assigned(self, arg):
        """
        Get the current assigned Verclsid configuration
        """
        print(self.cl.green("[?] Currently Assigned Verclsid Configuration"))
        print("[>] CLSID : {}".format(self.clsid if self.clsid else "(not set — will use Shell Folder CLSID)"))


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
        self.clsid = None


    ######################################################################
    # Verclsid AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Verclsid_' + current_counter, self.create_autoit_function())


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

        Optional JSON keys:
            clsid : str — CLSID of the COM object to verify with /S /C
                          if absent, the Shell Folder CLSID is used
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.clsid = kwargs.get("clsid", None)
        if self.clsid:
            print(f"[*] Setting clsid attribute : {self.clsid}")
        else:
            print("[*] No CLSID provided — will use Shell Folder CLSID")

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
        ; <      Verclsid Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Verclsid_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Verclsid_{}()

            ; Creates a Verclsid Interaction via CMD

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
        Builds the verclsid command to type into the CMD window.
        Uses the provided CLSID or defaults to the Shell Folder CLSID.
        Runs with /S (silent) and /C (verify CLSID).
        """
        typing_text = '\n'

        target_clsid = self.clsid if self.clsid else '{20D04FE0-3AEA-1069-A2D8-08002B30309D}'
        verify_cmd = 'verclsid.exe /S /C {}'.format(target_clsid)
        typing_text += 'Send("' + self._escape_send(verify_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Verclsid AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
