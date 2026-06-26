
# LOLBAS: provlaunch.exe — Legitimate use: launching provisioning commands defined in the registry

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates administrative use of provlaunch.exe to execute a provisioning
 command registered under HKLM\SOFTWARE\Microsoft\Provisioning\Commands.

 The operator provides a registry key name, a subkey name, and the commandline
 to register. The task creates the required registry structure via reg.exe,
 invokes provlaunch.exe with the key name, and cleans up automatically
 (the registry keys are removed by provlaunch after successful execution).

 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Provlaunch(BaseCMD):
    """
    # LOLBAS: provlaunch.exe — Legitimate use: executing provisioning commands stored in the registry

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Provlaunch, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Provlaunch'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > provlaunch >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > provlaunch >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Registry key name under HKLM\SOFTWARE\Microsoft\Provisioning\Commands
        self.key_name = None
        # Subkey name (first level below key_name)
        self.subkey_name = None
        # Command to register and execute
        self.commandline = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Provlaunch Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the registry key name using 'key_name <name>'
        3: Set the subkey name using 'subkey_name <name>'
        4: Set the commandline to register using 'commandline <cmd>'
        5: Complete the interaction using 'complete'
        ----------------------------------
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Provlaunch Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Provlaunch interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Provlaunch_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_key_name(self, key_name):
        """
        Set the registry key name for the provisioning command.
        This becomes HKLM\SOFTWARE\Microsoft\Provisioning\Commands\<key_name>
        Example: key_name ProvisioningTask
        """
        if key_name:
            if self.taskstarted:
                self.key_name = key_name.strip()
                print(self.cl.green("[*] Key name set to: {}".format(self.key_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Provlaunch Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a registry key name."))


    def do_subkey_name(self, subkey_name):
        """
        Set the subkey name (first level below key_name).
        Example: subkey_name entry1
        """
        if subkey_name:
            if self.taskstarted:
                self.subkey_name = subkey_name.strip()
                print(self.cl.green("[*] Subkey name set to: {}".format(self.subkey_name)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Provlaunch Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a subkey name."))


    def do_commandline(self, commandline):
        """
        Set the commandline value to register under the provisioning key.
        Example: commandline notepad.exe
        """
        if commandline:
            if self.taskstarted:
                self.commandline = commandline.strip()
                print(self.cl.green("[*] Commandline set to: {}".format(self.commandline)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Provlaunch Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a commandline value."))


    def do_assigned(self, arg):
        """
        Get the current assigned Provlaunch configuration
        """
        print(self.cl.green("[?] Currently Assigned Provlaunch Configuration"))
        print("[>] Key Name    : {}".format(self.key_name if self.key_name else "(not set)"))
        print("[>] Subkey Name : {}".format(self.subkey_name if self.subkey_name else "(not set)"))
        print("[>] Commandline : {}".format(self.commandline if self.commandline else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.key_name:
                self.key_name = 'ProvisioningTask'
            if not self.subkey_name:
                self.subkey_name = 'entry1'
            if not self.commandline:
                self.commandline = 'notepad.exe'
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.key_name = None
        self.subkey_name = None
        self.commandline = None


    ######################################################################
    # Provlaunch AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Provlaunch_' + current_counter, self.create_autoit_function())


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
            key_name    : str — registry key name under Provisioning\Commands
                                defaults to 'ProvisioningTask'
            subkey_name : str — first-level subkey name, defaults to 'entry1'
            commandline : str — command to register and execute, defaults to 'notepad.exe'
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.key_name = kwargs.get("key_name", "ProvisioningTask")
        self.subkey_name = kwargs.get("subkey_name", "entry1")
        self.commandline = kwargs.get("commandline", "notepad.exe")

        print(f"[*] Setting key_name attribute    : {self.key_name}")
        print(f"[*] Setting subkey_name attribute : {self.subkey_name}")
        print(f"[*] Setting commandline attribute  : {self.commandline}")

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
        ; <      Provlaunch Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Provlaunch_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Provlaunch_{}()

            ; Creates a Provlaunch Interaction via CMD

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
        Builds the provlaunch commands to type into the CMD window.
        Creates the required registry structure, invokes provlaunch.exe,
        then waits for the launched process. Registry keys are automatically
        removed by provlaunch after successful execution.
        """
        typing_text = '\n'

        # Build the base registry path
        base_path = r'HKLM\SOFTWARE\Microsoft\Provisioning\Commands'

        # reg.exe add — first level: create key_name\subkey_name with altitude value
        reg_cmd1 = 'reg.exe add {}\\{}\\{} /v altitude /t REG_DWORD /d 0 /f'.format(
            base_path,
            self._escape_send(self.key_name),
            self._escape_send(self.subkey_name)
        )
        typing_text += 'Send("' + reg_cmd1 + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # reg.exe add — second level: create subkey_name\entry with Commandline value
        reg_cmd2 = 'reg add {}\\{}\\{}\\entry /v Commandline /d {} /f'.format(
            base_path,
            self._escape_send(self.key_name),
            self._escape_send(self.subkey_name),
            self._escape_send(self.commandline)
        )
        typing_text += 'Send("' + reg_cmd2 + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # invoke provlaunch.exe with the key name
        provlaunch_cmd = 'provlaunch.exe {}'.format(self._escape_send(self.key_name))
        typing_text += 'Send("' + provlaunch_cmd + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Provlaunch AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
