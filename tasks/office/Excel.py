
# #######################################################################
#
#  Task : Excel Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Opens Microsoft Excel, types data into cells, then closes.

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import cmd
import random
import textwrap

from utils.base.base_cmd_class import BaseCMD
from utils.typing import TypeWriter


class Excel(BaseCMD):

    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : complete_task()       > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        super(Excel, self).__init__(csh, cl)

        self.taskname = 'Excel'
        self.csh = csh
        self.cl = cl

        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > excel >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > excel >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt
        self.subtask = False
        self.typing_threshold = None

        self.introduction = """
        ----------------------------------
        [!] Excel Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Add data rows using 'data cell1, cell2, cell3'
        3: Load rows from CSV using 'data_file'
        4: Complete the interaction using 'complete'
        """

        self.indent_space = '    '
        self.rows = []

        if not self.csh.json_parsing:
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    ########################################################################
    # Excel Console Commands
    ########################################################################


    def do_new(self, arg):
        """
        Start a new Excel interaction
        """
        if self.check_task_started():
            print("[!] Starting : 'Excel_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue("[*] Excel_{}".format(str(self.csh.counter.current()))) + "\n" + self.baseprompt


    def do_data(self, row):
        """
        Add a row of comma-separated cell values
        example: data Sales, Q1, 12500, EMEA
        """
        if row:
            if self.taskstarted:
                cells = [c.strip() for c in row.split(',')]
                self.rows.append(cells)
                print(self.cl.green("[*] Row added: {}".format(cells)))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Excel interaction first with 'new'."))


    def do_data_file(self, input_file):
        """
        Load rows from a CSV file, one row per line
        example: data_file spreadsheet_data.csv
        """
        if input_file:
            if self.taskstarted:
                try:
                    with open(input_file) as f:
                        for line in f.readlines():
                            cells = [c.strip() for c in line.rstrip('\n').split(',')]
                            self.rows.append(cells)
                    print(self.cl.green("[*] Loaded {} rows from {}".format(len(self.rows), input_file)))
                except OSError as e:
                    print("[!] Error reading file : {} ({})".format(self.cl.red(input_file), e))
            else:
                print(self.cl.red("[!] <ERROR> Start a new Excel interaction first with 'new'."))


    def do_typing_threshold(self, threshold):
        """
        Set typing realism level: epic / good / average / poor
        Use 'none' to revert to simple Send().
        example: typing_threshold average
        """
        valid = ['epic', 'good', 'average', 'poor', 'none']
        if threshold.lower() in valid:
            self.typing_threshold = None if threshold.lower() == 'none' else threshold.lower()
            print(self.cl.green("[*] Typing threshold set to: {}".format(threshold.lower())))
        else:
            print(self.cl.red("[!] Invalid threshold. Choose from: {}".format(', '.join(valid))))


    def do_assigned(self, arg):
        """
        Show currently assigned data rows
        """
        print(self.cl.green("[?] Currently Assigned Rows"))
        if self.rows:
            for i, row in enumerate(self.rows):
                print("[>] Row {} : {}".format(i + 1, row))
        else:
            print("[>] No rows currently assigned")


    def do_complete(self, arg):
        """
        Complete the Excel interaction and generate the AutoIT block
        """
        if self.taskstarted:
            if self.rows:
                self.create_autoIT_block()
                self.complete_task()
                self.rows = []
            else:
                print("{} No data rows assigned. Use 'data' to add rows.".format(self.cl.red("[!]")))
        else:
            print(self.cl.red("[!] Start a new Excel interaction first with 'new'."))


    ########################################################################
    # Excel AutoIT Block Definition
    ########################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Excel_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_excel() +
            self.type_data() +
            self.close_excel()
        )
        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and build out task variables when using JSON profiles
        Each row in 'data' is a list of cell values: [["col1", "col2"], ["val1", "val2"]]
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        try:
            self.rows = kwargs["data"]
            self.typing_threshold = kwargs.get("typing_threshold", None)
            print(f"[*] Loaded {len(self.rows)} rows")

        except KeyError as e:
            print(self.cl.red("[!] Error setting JSON Profile attributes, missing key: {}".format(e)))

        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ------------------------------------------ >
        ;              Excel Interaction
        ; < ------------------------------------------ >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Excel_{}()".format(str(self.csh.counter.current()))

        return textwrap.dedent(function_declaration)


    def open_excel(self):

        _open_excel = """

        Func Excel_{}()

            ; Creates an Excel Interaction

            Send("#r")
            WinWaitActive("Run", "", 10)
            Send("excel{}")
            ; Wait for Excel to open with a blank workbook
            Sleep(4000)
            WinWaitActive("[CLASS:XLMAIN]", "", 20)
            SendKeepActive("[CLASS:XLMAIN]")
            Sleep(1000)

            ; Dismiss any startup screen or wizard if present
            Send("{{ESC}}")
            Sleep(500)

        """.format(str(self.csh.counter.current()), "{ENTER}")

        return textwrap.dedent(_open_excel)


    def type_data(self):
        """
        Generates the AutoIT block for typing data into cells
        """
        typing_text = '\n'

        for row in self.rows:
            for i, cell in enumerate(row):
                if self.typing_threshold:
                    tw = TypeWriter(threshold=self.typing_threshold)
                    typing_text += tw.generate(cell) + '\n'
                else:
                    typing_text += 'Send("{}")\n'.format(self._escape_send(cell))

                # Tab between cells, Enter at end of row
                if i < len(row) - 1:
                    typing_text += 'Send("{TAB}")\n'
                else:
                    typing_text += 'Send("{ENTER}")\n'

            typing_text += 'Sleep({})\n'.format(random.randint(500, 3000))

        return textwrap.indent(typing_text, self.indent_space)


    def close_excel(self):
        """
        Saves and closes the Excel function declaration
        """
        end_func = """

        ; Save with Ctrl+S, then close without saving the dialog prompt
        Sleep(1000)
        Send("^s")
        Sleep(2000)
        ; Dismiss save dialog (we're just simulating, no real file needed)
        Send("{ESC}")
        Sleep(500)
        Send("!{F4}")
        Sleep(1000)
        ; Don't save prompt - select Don't Save
        Send("{TAB}{ENTER}")
        SendKeepActive("")

        EndFunc

        """
        return textwrap.dedent(end_func)
