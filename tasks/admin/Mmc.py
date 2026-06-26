
# LOLBAS: mmc.exe — Legitimate use: IT administration via management console snap-ins
# SERVER-ONLY snap-ins: servermanager.msc, dns.msc, dsa.msc, dhcpmgmt.msc require server roles

# #######################################################################
#
#  Task : Mmc Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT administrator use of mmc.exe to open Windows
 management console snap-ins such as Computer Management, Device Manager,
 Services, Event Viewer, Group Policy, and others.

 Snap-in options:
   compmgmt.msc    - Computer Management (common on client and server)
   devmgmt.msc     - Device Manager
   services.msc    - Services console
   eventvwr.msc    - Event Viewer
   gpedit.msc      - Local Group Policy Editor (Pro/Server only)
   diskmgmt.msc    - Disk Management
   certlm.msc      - Local Computer Certificates
   servermanager.msc - Server Manager (SERVER-ONLY)
   dns.msc         - DNS Manager (SERVER-ONLY: requires DNS Server role)
   dsa.msc         - Active Directory Users and Computers (SERVER-ONLY: requires AD DS role)
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


# Valid snap-ins and their human-readable descriptions
SNAP_INS = {
    "compmgmt.msc":      "Computer Management (client + server)",
    "devmgmt.msc":       "Device Manager",
    "services.msc":      "Services console",
    "eventvwr.msc":      "Event Viewer",
    "gpedit.msc":        "Local Group Policy Editor (Pro/Server only)",
    "diskmgmt.msc":      "Disk Management",
    "certlm.msc":        "Local Computer Certificates",
    # SERVER-ONLY snap-ins below — require appropriate server roles
    "servermanager.msc": "Server Manager (SERVER-ONLY)",
    "dns.msc":           "DNS Manager (SERVER-ONLY: DNS Server role required)",
    "dsa.msc":           "Active Directory Users and Computers (SERVER-ONLY: AD DS role required)",
}

DEFAULT_SNAP_IN = "compmgmt.msc"
DEFAULT_BROWSE_TIME = 10


class Mmc(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Mmc, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Mmc'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > mmc >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > mmc >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific defaults
        self.snap_in = DEFAULT_SNAP_IN
        self.browse_time = DEFAULT_BROWSE_TIME

        self.introduction = """
        ----------------------------------
        [!] Mmc Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the snap-in using 'snap_in'   (e.g. compmgmt.msc)
        3: Set browse time using 'browse_time' (seconds, default 10)
        4: Complete the interaction using 'complete'
        ----------------------------------
        Available snap-ins:
          compmgmt.msc      Computer Management
          devmgmt.msc       Device Manager
          services.msc      Services console
          eventvwr.msc      Event Viewer
          gpedit.msc        Local Group Policy (Pro/Server only)
          diskmgmt.msc      Disk Management
          certlm.msc        Local Computer Certificates
          servermanager.msc Server Manager          [SERVER-ONLY]
          dns.msc           DNS Manager             [SERVER-ONLY]
          dsa.msc           AD Users and Computers  [SERVER-ONLY]
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
    #  Mmc Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Mmc interaction
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Mmc_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_snap_in(self, snap_in):
        """
        Set the MMC snap-in (msc file) to open.
        Default: compmgmt.msc
        Examples:
            snap_in compmgmt.msc
            snap_in services.msc
            snap_in eventvwr.msc
            snap_in devmgmt.msc
            snap_in gpedit.msc
            snap_in diskmgmt.msc
            snap_in certlm.msc
            snap_in servermanager.msc   [SERVER-ONLY]
            snap_in dns.msc             [SERVER-ONLY]
            snap_in dsa.msc             [SERVER-ONLY]
        """
        if snap_in:
            if self.taskstarted:
                snap_in = snap_in.strip().lower()
                if snap_in in SNAP_INS:
                    self.snap_in = snap_in
                    description = SNAP_INS[snap_in]
                    print(self.cl.green("[*] Snap-in set to: {} ({})".format(self.snap_in, description)))
                    # Warn if server-only snap-in selected
                    if "SERVER-ONLY" in description:
                        print(self.cl.yellow("[!] Note: {} is a SERVER-ONLY snap-in and requires the appropriate server role.".format(snap_in)))
                else:
                    print(self.cl.red("[!] Unknown snap-in: {}".format(snap_in)))
                    print(self.cl.yellow("[-] Valid options: {}".format(", ".join(SNAP_INS.keys()))))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Mmc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No snap-in supplied, using default: {}".format(self.snap_in)))


    def do_browse_time(self, browse_time):
        """
        Set how long (in seconds) to keep the management console open before closing.
        Default: 10 seconds
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
                print(self.cl.red("[!] <ERROR> You need to start a new Mmc Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.yellow("[*] No browse time supplied, using default: {} seconds".format(self.browse_time)))


    def do_assigned(self, arg):
        """
        Show the currently assigned snap-in and browse time
        """
        print(self.cl.green("[?] Currently Assigned Mmc Settings"))
        print("[>] Snap-in     : {}  ({})".format(self.snap_in, SNAP_INS.get(self.snap_in, "unknown")))
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
        self.snap_in = DEFAULT_SNAP_IN
        self.browse_time = DEFAULT_BROWSE_TIME


    ######################################################################
    # Mmc AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Mmc_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_mmc() +
            self.close_mmc()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        JSON keys:
            snap_in     : the msc snap-in to open (default: compmgmt.msc)
                          e.g. "services.msc", "eventvwr.msc", "devmgmt.msc"
            browse_time : seconds to keep the console open (default: 10)
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        if "snap_in" in kwargs:
            snap_in = kwargs["snap_in"].strip().lower()
            if snap_in in SNAP_INS:
                self.snap_in = snap_in
            else:
                print(self.cl.yellow("[!] Unknown snap-in '{}', falling back to default: {}".format(snap_in, DEFAULT_SNAP_IN)))
                self.snap_in = DEFAULT_SNAP_IN
        print(f"[*] Setting the snap_in attribute : {self.snap_in}")

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
        ; < ----------------------------------- >
        ; <         Mmc Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Mmc_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_mmc(self):
        """
        Opens the MMC snap-in via Win+R run dialogue, waits for the window,
        sleeps for browse_time, then the close block sends Alt+F4.
        """

        # Convert seconds to milliseconds for AutoIT Sleep()
        browse_time_ms = self.browse_time * 1000

        _open_mmc = """

        Func Mmc_{}()

            ; Opens MMC snap-in: {}
            ; LOLBAS: mmc.exe — Legitimate use: IT administration via management console snap-ins

            Send("#r")
            ; Wait 10 seconds for the Run dialogue window to appear.
            WinWaitActive("Run", "", 10)
            ; Launch mmc with the specified snap-in
            Send('mmc {}{}')
            ; Wait for the MMC window to become active (class: MMCMainFrame)
            WinWaitActive("[CLASS:MMCMainFrame]", "", 15)
            SendKeepActive("[CLASS:MMCMainFrame]")

            ; Simulate administrator browsing the console
            Sleep({})

        """.format(
            self.csh.counter.current(),
            self.snap_in,
            self.snap_in,
            "{ENTER}",
            browse_time_ms
        )

        return textwrap.dedent(_open_mmc)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_mmc(self):
        """
        Closes the MMC management console with Alt+F4 and resets focus
        """

        end_func = """

        ; Close the MMC window
        Send("!{F4}")
        ; Reset Focus
        SendKeepActive("")

        EndFunc

        """

        return textwrap.dedent(end_func)
