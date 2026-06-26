
# LOLBAS: desktopimgdownldr.exe — Legitimate use: configure lockscreen or desktop background image via URL

# #######################################################################
#
#  Task : Desktopimgdownldr Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of desktopimgdownldr.exe to download and set
 a lockscreen image from a URL.  The binary reads the /lockscreenurl
 argument, downloads the remote image, and configures
 HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\PersonalizationCSP
 accordingly.

 Takes a lockscreen_url parameter pointing to a valid image file.
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


class Desktopimgdownldr(BaseCMD):
    """
    # LOLBAS: desktopimgdownldr.exe — Legitimate use: download and apply a lockscreen image

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Desktopimgdownldr, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Desktopimgdownldr'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > desktopimgdownldr >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > desktopimgdownldr >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # URL of the image to download and set as lockscreen
        self.lockscreen_url = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] Desktopimgdownldr Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the lockscreen image URL using 'lockscreen_url <url>'
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
    #  Desktopimgdownldr Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Desktopimgdownldr interaction block
        """
        if self.check_task_started():
            self.prompt = self.cl.blue(
                "[*] Current Task : 'Desktopimgdownldr_{}'".format(str(self.csh.counter.current()))
                + "\n" + self.baseprompt
            )


    def do_lockscreen_url(self, lockscreen_url):
        """
        Set the URL of the image to download and apply as the lockscreen.
        The URL should point to a reachable image file (e.g. PNG, JPG, BMP).
        Example: lockscreen_url https://example.com/lockscreen.jpg
        """
        if lockscreen_url:
            if self.taskstarted:
                self.lockscreen_url = lockscreen_url.strip()
                print(self.cl.green("[*] Lockscreen URL set to: {}".format(self.lockscreen_url)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new Desktopimgdownldr Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a lockscreen URL."))


    def do_assigned(self, arg):
        """
        Get the current assigned Desktopimgdownldr configuration
        """
        print(self.cl.green("[?] Currently Assigned Desktopimgdownldr Configuration"))
        print("[>] Lockscreen URL : {}".format(self.lockscreen_url if self.lockscreen_url else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.lockscreen_url:
                print(self.cl.red("[!] <ERROR> A lockscreen URL is required. Use 'lockscreen_url <url>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.lockscreen_url = None


    ######################################################################
    # Desktopimgdownldr AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Desktopimgdownldr_' + current_counter, self.create_autoit_function())


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
            lockscreen_url : str — URL of the image to download and apply as lockscreen
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.lockscreen_url = kwargs.get("lockscreen_url", None)
        if self.lockscreen_url:
            print(f"[*] Setting lockscreen_url attribute : {self.lockscreen_url}")
        else:
            print("[!] <ERROR> lockscreen_url is required for Desktopimgdownldr.")
            return

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
        ; <      Desktopimgdownldr Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "Desktopimgdownldr_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func Desktopimgdownldr_{}()

            ; Creates a Desktopimgdownldr Interaction via CMD

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
        Builds the desktopimgdownldr command to type into the CMD window.
        Sets SYSTEMROOT to a writable temp directory, then invokes
        desktopimgdownldr.exe with /lockscreenurl to download the image.
        """
        typing_text = '\n'

        # Set SYSTEMROOT to a writable temp path so the binary can write its output
        set_cmd = 'set "SYSTEMROOT=C:\\Windows\\Temp"'
        typing_text += 'Send("' + self._escape_send(set_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(500, 1500))

        # Run desktopimgdownldr with the supplied lockscreen URL
        dl_cmd = 'desktopimgdownldr.exe /lockscreenurl:{} /eventName:desktopimgdownldr'.format(
            self.lockscreen_url
        )
        typing_text += 'Send("' + self._escape_send(dl_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the Desktopimgdownldr AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
