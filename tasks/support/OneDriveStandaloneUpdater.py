
# LOLBAS: OneDriveStandaloneUpdater.exe — Legitimate use: updating OneDrive client configuration and settings from Microsoft's servers

# #######################################################################
#
#  Task : OneDriveStandaloneUpdater Interaction
#
# #######################################################################


r"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of OneDriveStandaloneUpdater.exe to fetch
 OneDrive update configuration from a URL stored in the registry key
 HKCU\Software\Microsoft\OneDrive\UpdateOfficeConfig\UpdateRingSettingURLFromOC.

 The updater downloads configuration to:
 %localappdata%\OneDrive\StandaloneUpdater\PreSignInSettingsConfig.json

 Takes optional registry_url and ring parameters for the update config URL
 and update ring setting respectively.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class OneDriveStandaloneUpdater(BaseCMD):
    """
    # LOLBAS: OneDriveStandaloneUpdater.exe — Legitimate use: updating OneDrive client configuration and settings from Microsoft's servers

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(OneDriveStandaloneUpdater, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'OneDriveStandaloneUpdater'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > onedrivestandaloneupdater >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > onedrivestandaloneupdater >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Registry URL for the OneDrive update config
        self.registry_url = None
        # Update ring (e.g. Production, Insider, Enterprise)
        self.update_ring = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] OneDriveStandaloneUpdater Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Optionally set an update config URL using 'registry_url <url>'
        3: Optionally set an update ring using 'update_ring <ring>'
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
    #  OneDriveStandaloneUpdater Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new OneDriveStandaloneUpdater interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'OneDriveStandaloneUpdater_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_registry_url(self, registry_url):
        """
        Optionally set the update config URL to write into the registry before running the updater.
        This is the value for HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig\\UpdateRingSettingURLFromOC
        Example: registry_url https://g.live.com/odclientsettings/ring.xml
        """
        if registry_url:
            if self.taskstarted:
                self.registry_url = registry_url.strip()
                print(self.cl.green("[*] Registry URL set to: {}".format(self.registry_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new OneDriveStandaloneUpdater Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a registry URL."))


    def do_update_ring(self, update_ring):
        """
        Optionally set the OneDrive update ring (e.g. Production, Insider, Enterprise).
        Written to HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig\\ODSUUpdateXMLUrlFromOC
        Example: update_ring Production
        """
        if update_ring:
            if self.taskstarted:
                self.update_ring = update_ring.strip()
                print(self.cl.green("[*] Update ring set to: {}".format(self.update_ring)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new OneDriveStandaloneUpdater Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an update ring value."))


    def do_assigned(self, arg):
        """
        Get the current assigned OneDriveStandaloneUpdater configuration
        """
        print(self.cl.green("[?] Currently Assigned OneDriveStandaloneUpdater Configuration"))
        print("[>] Registry URL  : {}".format(self.registry_url if self.registry_url else "(not set — skipping registry write)"))
        print("[>] Update Ring   : {}".format(self.update_ring if self.update_ring else "(not set — skipping ring write)"))


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
        self.registry_url = None
        self.update_ring = None


    ######################################################################
    # OneDriveStandaloneUpdater AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('OneDriveStandaloneUpdater_' + current_counter, self.create_autoit_function())


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
            registry_url : str — URL to write into UpdateRingSettingURLFromOC registry value
            update_ring  : str — update ring string (e.g. Production, Insider, Enterprise)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.registry_url = kwargs.get("registry_url", None)
        if self.registry_url:
            print(f"[*] Setting registry_url attribute : {self.registry_url}")
        else:
            print("[*] No registry_url provided — skipping registry write")

        self.update_ring = kwargs.get("update_ring", None)
        if self.update_ring:
            print(f"[*] Setting update_ring attribute : {self.update_ring}")
        else:
            print("[*] No update_ring provided — skipping ring write")

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
        ; <      OneDriveStandaloneUpdater Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "OneDriveStandaloneUpdater_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func OneDriveStandaloneUpdater_{}()

            ; Creates an OneDriveStandaloneUpdater Interaction via CMD

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
        Builds the OneDriveStandaloneUpdater commands to type into the CMD window.
        Optionally writes registry keys before triggering the updater, then runs
        OneDriveStandaloneUpdater.exe with no arguments to fetch the update config.
        """
        typing_text = '\n'

        # Optionally prime the registry with a URL
        if self.registry_url:
            reg_url_cmd = (
                'reg add "HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig" '
                '/v UpdateRingSettingURLFromOC /t REG_SZ /d {} /f'.format(self.registry_url)
            )
            typing_text += 'Send("' + self._escape_send(reg_url_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

            # ODSUUpdateXMLUrlFromOC and UpdateXMLUrlFromOC must also be non-empty
            reg_ods_cmd = (
                'reg add "HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig" '
                '/v ODSUUpdateXMLUrlFromOC /t REG_SZ /d {} /f'.format(self.registry_url)
            )
            typing_text += 'Send("' + self._escape_send(reg_ods_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

            reg_xml_cmd = (
                'reg add "HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig" '
                '/v UpdateXMLUrlFromOC /t REG_SZ /d {} /f'.format(self.registry_url)
            )
            typing_text += 'Send("' + self._escape_send(reg_xml_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

            # Set UpdateOfficeConfigTimestamp to a large QWORD so the cache is valid
            reg_ts_cmd = (
                'reg add "HKCU\\Software\\Microsoft\\OneDrive\\UpdateOfficeConfig" '
                '/v UpdateOfficeConfigTimestamp /t REG_QWORD /d 99999999999 /f'
            )
            typing_text += 'Send("' + self._escape_send(reg_ts_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Optionally set update ring
        if self.update_ring:
            reg_ring_cmd = (
                'reg add "HKCU\\Software\\Microsoft\\OneDrive" '
                '/v UpdateRing /t REG_SZ /d {} /f'.format(self.update_ring)
            )
            typing_text += 'Send("' + self._escape_send(reg_ring_cmd) + '{ENTER}")\n'
            typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        # Run the updater — use the most common install location
        run_cmd = (
            '"%LOCALAPPDATA%\\Microsoft\\OneDrive\\OneDriveStandaloneUpdater.exe"'
        )
        typing_text += 'Send("' + self._escape_send(run_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(5000, 15000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the OneDriveStandaloneUpdater AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
