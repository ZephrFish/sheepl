
# #######################################################################
#
#  Task : Findstr Interaction
#
# #######################################################################

# LOLBAS: findstr.exe — Legitimate use: log analysis and configuration file searching

"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate IT staff use of findstr.exe to search text within files.
 Common scenarios include searching log files for errors, grepping source code,
 and locating configuration values in admin directories.

 JSON keys:
   search_string      : string to search for (required)
   path               : directory or file to search (default: C:\\Windows\\Logs)
   recursive          : boolean, adds /S flag to search subdirectories (default: true)
   case_insensitive   : boolean, adds /I flag for case-insensitive search (default: true)
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Findstr(BaseCMD):
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
        super(Findstr, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Findstr'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > findstr >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > findstr >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Task-specific state
        self.search_string = ""
        self.search_path = "C:\\Windows\\Logs"
        self.recursive = True
        self.case_insensitive = True

        self.introduction = """
        ----------------------------------
        [!] Findstr Interaction.
        Type help or ? to list commands.
        ----------------------------------
        1: Start a new block using 'new'
        2: Set the search string using 'search_string'
        3: Set the search path using 'path'
           Default: C:\\Windows\\Logs
        4: Toggle recursive search using 'recursive'
           Default: True (adds /S flag)
        5: Toggle case-insensitive search using 'case_insensitive'
           Default: True (adds /I flag)
        6: Review current settings using 'assigned'
        7: Complete the interaction using 'complete'
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
    #  Findstr Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Findstr interaction block
        """
        # method from parent class BaseCMD
        if self.check_task_started():
            print("[!] Starting : 'Findstr_{}'".format(str(self.csh.counter.current())))
            print()
            self.prompt = self.cl.blue(
                "[*] Current Task : Findstr_{}".format(str(self.csh.counter.current()))
            ) + "\n" + self.baseprompt


    def do_search_string(self, arg):
        """
        Set the string to search for with findstr.
        Example: search_string error

        This value is passed directly to findstr as the search pattern.
        """
        arg = arg.strip()
        if not arg:
            print(self.cl.green("[?] Current search string: '{}'".format(self.search_string)))
            return

        self.search_string = arg
        print(self.cl.green("[*] Search string set to: '{}'".format(self.search_string)))


    def do_path(self, arg):
        """
        Set the directory or file to search.
        Default: C:\\Windows\\Logs

        Example: path C:\\inetpub\\logs
        Example: path C:\\Windows\\System32\\drivers\\etc\\hosts
        """
        if self.taskstarted:
            arg = arg.strip()
            if not arg:
                print(self.cl.green("[?] Current search path: '{}'".format(self.search_path)))
                return
            self.search_path = arg
            print(self.cl.green("[*] Search path set to: '{}'".format(self.search_path)))
        else:
            print(self.cl.red("[!] <ERROR> Start a new Findstr interaction first with 'new'."))


    def do_recursive(self, arg):
        """
        Toggle recursive subdirectory search (/S flag).
        Default: True

        Example: recursive true
        Example: recursive false
        """
        arg = arg.strip().lower()
        if not arg:
            print(self.cl.green("[?] Recursive search: {}".format(self.recursive)))
            return

        if arg in ('true', '1', 'yes', 'on'):
            self.recursive = True
            print(self.cl.green("[*] Recursive search enabled (/S flag will be included)"))
        elif arg in ('false', '0', 'no', 'off'):
            self.recursive = False
            print(self.cl.green("[*] Recursive search disabled (/S flag will be omitted)"))
        else:
            print(self.cl.red("[!] Invalid value '{}'. Use true or false.".format(arg)))


    def do_case_insensitive(self, arg):
        """
        Toggle case-insensitive search (/I flag).
        Default: True

        Example: case_insensitive true
        Example: case_insensitive false
        """
        if self.taskstarted:
            arg = arg.strip().lower()
            if not arg:
                print(self.cl.green("[?] Case-insensitive search: {}".format(self.case_insensitive)))
                return
            if arg in ('true', '1', 'yes', 'on'):
                self.case_insensitive = True
                print(self.cl.green("[*] Case-insensitive search enabled (/I flag will be included)"))
            elif arg in ('false', '0', 'no', 'off'):
                self.case_insensitive = False
                print(self.cl.green("[*] Case-insensitive search disabled (/I flag will be omitted)"))
            else:
                print(self.cl.red("[!] Invalid value '{}'. Use true or false.".format(arg)))
        else:
            print(self.cl.red("[!] <ERROR> Start a new Findstr interaction first with 'new'."))


    def do_assigned(self, arg):
        """
        Show the currently assigned findstr settings
        """
        flags = self._build_flags()
        command = self._build_findstr_command()
        print(self.cl.green("[?] Currently Assigned Findstr Settings"))
        print("[>] Search String    : '{}'".format(self.search_string))
        print("[>] Search Path      : '{}'".format(self.search_path))
        print("[>] Recursive        : {} {}".format(self.recursive, "(/S)" if self.recursive else ""))
        print("[>] Case-Insensitive : {} {}".format(self.case_insensitive, "(/I)" if self.case_insensitive else ""))
        print("[>] Flags            : {}".format(flags if flags else "(none)"))
        print("[>] Command          : {}".format(command))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """
        if self.taskstarted:
            if not self.search_string:
                print(self.cl.red("[!] <ERROR> You must set a search string before completing."))
                print(self.cl.red("[-] Use 'search_string <term>' to set the search string."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for next interaction
        self.search_string = ""
        self.search_path = "C:\\Windows\\Logs"
        self.recursive = True
        self.case_insensitive = True


    ######################################################################
    # Findstr AutoIT Block Definition
    #######################################################################


    def _build_flags(self):
        """
        Builds the findstr flag string based on current settings.
        Returns a string like '/S /I' or '' depending on enabled flags.
        """
        flags = []
        if self.recursive:
            flags.append("/S")
        if self.case_insensitive:
            flags.append("/I")
        return " ".join(flags)


    def _build_findstr_command(self):
        """
        Builds the complete findstr command string.
        findstr [/S] [/I] "<search_string>" "<path>"
        """
        flags = self._build_flags()
        if flags:
            return 'findstr {} "{}" "{}"'.format(flags, self.search_string, self.search_path)
        else:
            return 'findstr "{}" "{}"'.format(self.search_string, self.search_path)


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """
        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Findstr_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """
        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.findstr_typing_block() +
            self.close_commandshell()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        This function sets the various object attributes in the same way
        that the interactive mode does.

        JSON keys:
            search_string      : string to search for (required)
            path               : directory or file to search (default: C:\\Windows\\Logs)
            recursive          : boolean, /S flag for subdirectory search (default: true)
            case_insensitive   : boolean, /I flag for case-insensitive search (default: true)
        """
        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.search_string = kwargs.get("search_string", "").strip()
        self.search_path = kwargs.get("path", "C:\\Windows\\Logs").strip()
        self.recursive = bool(kwargs.get("recursive", True))
        self.case_insensitive = bool(kwargs.get("case_insensitive", True))

        print(f"[*] Setting search_string attribute : '{self.search_string}'")
        print(f"[*] Setting search_path attribute   : '{self.search_path}'")
        print(f"[*] Setting recursive attribute     : {self.recursive}")
        print(f"[*] Setting case_insensitive attribute : {self.case_insensitive}")

        if not self.search_string:
            print(self.cl.red("[!] Warning: search_string is empty — findstr will match all lines"))

        # once attributes are set, push the task onto the stack
        self.create_autoIT_block()


    # --------------------------------------------------->
    # Create Open Block

    def autoit_function_open(self):
        """
        Initial Entrypoint Definition for AutoIT function
        """
        function_declaration = """
        ; < ----------------------------------- >
        ; <      Findstr Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Findstr_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R for findstr execution
        """
        _open_commandshell = """

        Func Findstr_{}()

            ; Creates a CMD shell for findstr interaction

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
    # Findstr Command Output

    def findstr_typing_block(self):
        """
        Generates the AutoIT Send() calls for the findstr command.
        Builds: findstr [/S] [/I] "<search_string>" "<path>"
        """
        flags = self._build_flags()

        # Build the command with _escape_send applied to user-supplied values
        if flags:
            command = 'findstr {} "{}" "{}"'.format(
                flags,
                self._escape_send(self.search_string),
                self._escape_send(self.search_path)
            )
        else:
            command = 'findstr "{}" "{}"'.format(
                self._escape_send(self.search_string),
                self._escape_send(self.search_path)
            )

        typing_text = '\n'
        typing_text += 'Send("' + command + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_commandshell(self):
        """
        Closes the Findstr function declaration
        """
        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
