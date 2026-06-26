
# #######################################################################
#
#  Task : ProblemStepsRecorder Interaction
#
# #######################################################################

# LOLBAS: psr.exe — Legitimate use: IT support documentation and helpdesk ticket creation
# Note: /gui 0 (hidden recording) is a detection indicator — this task uses /gui 1 (visible)

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT support use of psr.exe (Problem Steps Recorder),
 a built-in Windows tool for capturing user actions as annotated screenshots
 saved to a ZIP archive.

 Legitimate use cases: IT support staff documenting reproduction steps for bug
 reports, end users recording issues for helpdesk tickets, IT training documentation.

 The recording session starts with /start, runs for a configurable duration, then
 stops with /stop. Using /gui 1 keeps the recorder toolbar visible — consistent with
 legitimate IT support activity.
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class ProblemStepsRecorder(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    Simulates IT support use of psr.exe to record and document problem steps.
    Output is saved as a ZIP file containing annotated screenshots and an HTML log.
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ProblemStepsRecorder, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ProblemStepsRecorder'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > psr >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > psr >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Set boolean switch to confirm if this can be used as a subtask
        self.subtask = False

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] ProblemStepsRecorder Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the output ZIP path using 'output <path>'  (default: C:\\Users\\Public\\steps.zip)
        3: Toggle screenshots using 'screenshots'         (default: True)
        4: Set max screenshots using 'max_screenshots <N>'(default: 25)
        5: Set recording duration using 'record_time <s>' (default: 30 seconds)
        6: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # Path to save the ZIP output file
        self.output_path = 'C:\\Users\\Public\\steps.zip'
        # Whether to capture screenshots (/sc 1 or /sc 0)
        self.screenshots = True
        # Maximum number of screenshots to capture
        self.max_screenshots = 25
        # Number of seconds to record before stopping
        self.record_time = 30

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  ProblemStepsRecorder Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ProblemStepsRecorder interaction block
        """
        if self.check_task_started():
            # Reset per-block state to defaults
            self.output_path = 'C:\\Users\\Public\\steps.zip'
            self.screenshots = True
            self.max_screenshots = 25
            self.record_time = 30
            print("[!] Starting : 'ProblemStepsRecorder_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : ProblemStepsRecorder_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_output(self, arg):
        """
        Set the output path for the ZIP file produced by psr.exe.
        Default: C:\\Users\\Public\\steps.zip
        Example: output C:\\Temp\\issue_recording.zip
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new ProblemStepsRecorder Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return
        if arg:
            self.output_path = arg.strip()
            print(self.cl.green("[*] Output path set to: {}".format(self.output_path)))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a file path for the output ZIP."))


    def do_screenshots(self, arg):
        """
        Toggle whether psr.exe captures screenshots (/sc 1 or /sc 0).
        Default: True (screenshots enabled).
        Example: screenshots
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new ProblemStepsRecorder Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return
        self.screenshots = not self.screenshots
        state = "enabled" if self.screenshots else "disabled"
        print(self.cl.green("[*] Screenshots {}.".format(state)))


    def do_max_screenshots(self, arg):
        """
        Set the maximum number of screenshots psr.exe will capture (/maxsc N).
        Default: 25
        Example: max_screenshots 50
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new ProblemStepsRecorder Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return
        try:
            value = int(arg.strip())
            if value < 1:
                raise ValueError
            self.max_screenshots = value
            print(self.cl.green("[*] Max screenshots set to: {}".format(self.max_screenshots)))
        except (ValueError, AttributeError):
            print(self.cl.red("[!] <ERROR> Please provide a positive integer for max_screenshots."))


    def do_record_time(self, arg):
        """
        Set the number of seconds psr.exe will record before being stopped.
        Default: 30 seconds
        Example: record_time 60
        """
        if not self.taskstarted:
            print(self.cl.red("[!] <ERROR> You need to start a new ProblemStepsRecorder Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
            return
        try:
            value = int(arg.strip())
            if value < 1:
                raise ValueError
            self.record_time = value
            print(self.cl.green("[*] Record time set to: {} seconds".format(self.record_time)))
        except (ValueError, AttributeError):
            print(self.cl.red("[!] <ERROR> Please provide a positive integer number of seconds."))


    def do_assigned(self, arg):
        """
        Show the currently assigned ProblemStepsRecorder settings
        """
        print(self.cl.green("[?] Currently Assigned ProblemStepsRecorder Settings"))
        print("[>] Output Path      : {}".format(self.output_path))
        print("[>] Screenshots      : {}".format(self.screenshots))
        print("[>] Max Screenshots  : {}".format(self.max_screenshots))
        print("[>] Record Time (s)  : {}".format(self.record_time))


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

        # Reset per-block state to defaults
        self.output_path = 'C:\\Users\\Public\\steps.zip'
        self.screenshots = True
        self.max_screenshots = 25
        self.record_time = 30


    ######################################################################
    # ProblemStepsRecorder AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block.
        csh.add_tasks takes two positional arguments:
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ProblemStepsRecorder_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.run_psr_start() +
            self.wait_for_recording() +
            self.run_psr_stop() +
            self.close_psr()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys: output, screenshots, max_screenshots, record_time
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.output_path = kwargs.get("output", "C:\\Users\\Public\\steps.zip")
        print(f"[*] Setting output_path attribute : {self.output_path}")

        self.screenshots = bool(kwargs.get("screenshots", True))
        print(f"[*] Setting screenshots attribute : {self.screenshots}")

        self.max_screenshots = int(kwargs.get("max_screenshots", 25))
        print(f"[*] Setting max_screenshots attribute : {self.max_screenshots}")

        self.record_time = int(kwargs.get("record_time", 30))
        print(f"[*] Setting record_time attribute : {self.record_time}")

        # Once attributes are set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """

        function_declaration = """
        ; < ----------------------------------- >
        ; <      ProblemStepsRecorder Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "ProblemStepsRecorder_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function — launch psr.exe /start directly via Run()

    def run_psr_start(self):
        """
        Launches psr.exe with /start and configured options.
        Uses /gui 1 so the recorder toolbar is visible — consistent with legitimate
        IT support activity. /gui 0 (hidden recording) is a detection indicator.
        """
        sc_flag = '1' if self.screenshots else '0'

        _run_psr_start = """

        Func ProblemStepsRecorder_{counter}()

            ; LOLBAS: psr.exe — IT support staff documenting issue reproduction steps
            ; /gui 1 keeps the recorder toolbar visible (legitimate use indicator)
            ; Launches psr.exe to start recording with visible GUI
            Run('psr.exe /start /output "{output}" /sc {sc} /maxsc {maxsc} /gui 1')
            ; Wait briefly for psr.exe to initialise and begin recording
            Sleep(2000)

        """.format(
            counter=self.csh.counter.current(),
            output=self.output_path,
            sc=sc_flag,
            maxsc=self.max_screenshots
        )

        return textwrap.dedent(_run_psr_start)


    # --------------------------------------------------->
    # Wait Block — simulates the recording period

    def wait_for_recording(self):
        """
        Sleeps for the configured record_time (converted to milliseconds)
        to simulate an IT support technician or end user reproducing the issue
        while psr.exe captures the steps.
        """
        sleep_ms = self.record_time * 1000

        _wait_block = """
            ; Simulate reproducing the issue — psr.exe records steps during this period
            Sleep({sleep_ms})

        """.format(sleep_ms=sleep_ms)

        return textwrap.dedent(_wait_block)


    # --------------------------------------------------->
    # Stop Block — sends psr.exe /stop

    def run_psr_stop(self):
        """
        Launches psr.exe with /stop to end the recording session.
        psr.exe saves the annotated screenshot ZIP to the configured output path.
        """
        _run_psr_stop = """
            ; Stop the recording — psr.exe writes the ZIP output file and closes
            Run('psr.exe /stop')
            ; Wait for psr.exe to finish writing the output ZIP
            Sleep(2000)

        """

        return textwrap.dedent(_run_psr_stop)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_psr(self):
        """
        Closes the ProblemStepsRecorder function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
