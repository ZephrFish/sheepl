
# LOLBAS: PhotoViewer.dll — Legitimate use: opening and displaying image files via Windows Photo Viewer

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate use of PhotoViewer.dll via rundll32.exe to open and
 display a local image file using the Windows Photo Viewer ImageView_Fullscreen
 export function.

 Takes a required image_path parameter pointing to the local image to display.
 The master script will already define the typing speed as part of the master declarations.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class PhotoViewer(BaseCMD):
    """
    # LOLBAS: PhotoViewer.dll — Legitimate use: opening and displaying image files via Windows Photo Viewer

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(PhotoViewer, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'PhotoViewer'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > photoviewer >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > photoviewer >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the local image file to display
        self.image_path = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] PhotoViewer Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the local image path using 'image_path <path>'
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
    #  PhotoViewer Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new PhotoViewer interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'PhotoViewer_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_image_path(self, image_path):
        """
        Set the local path to the image file to open with Windows Photo Viewer.
        Example: image_path C:\\Users\\Public\\Pictures\\photo.jpg
        """
        if image_path:
            if self.taskstarted:
                self.image_path = image_path.strip()
                print(self.cl.green("[*] Image path set to: {}".format(self.image_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new PhotoViewer Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide an image path."))


    def do_assigned(self, arg):
        """
        Get the current assigned PhotoViewer configuration
        """
        print(self.cl.green("[?] Currently Assigned PhotoViewer Configuration"))
        print("[>] Image Path : {}".format(self.image_path if self.image_path else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.image_path:
                print(self.cl.red("[!] <ERROR> Please set an image path using 'image_path <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.image_path = None


    ######################################################################
    # PhotoViewer AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('PhotoViewer_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_photoviewer()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        Required JSON keys:
            image_path : str — local path to the image file to display with PhotoViewer
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.image_path = kwargs.get("image_path", None)
        if self.image_path:
            print(f"[*] Setting image_path attribute : {self.image_path}")
        else:
            print("[!] <ERROR> No image_path provided — required for PhotoViewer task")
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
        ; <      PhotoViewer Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "PhotoViewer_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func PhotoViewer_{}()

            ; Creates a PhotoViewer Interaction via CMD

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
        Builds the rundll32 command to open the image via PhotoViewer.dll
        """
        typing_text = '\n'

        # Use rundll32 to invoke PhotoViewer.dll's ImageView_Fullscreen export
        rundll_cmd = 'rundll32.exe PhotoViewer.dll,ImageView_Fullscreen {}'.format(self.image_path)
        typing_text += 'Send("' + self._escape_send(rundll_cmd) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_photoviewer(self):
        """
        Closes the PhotoViewer AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
