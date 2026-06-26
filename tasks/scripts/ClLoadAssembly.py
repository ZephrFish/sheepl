
# LOLBAS: CL_LoadAssembly.ps1 — Legitimate use: loading .NET diagnostic assemblies via PowerShell diagnostic scripts
# #######################################################################
#
#  Task : CL_LoadAssembly Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates use of the Windows PowerShell diagnostic script CL_LoadAssembly.ps1
 located at C:\Windows\diagnostics\system\Audio\ to load a .NET assembly from
 a specified path via the LoadAssemblyFromPath function, then invoke a method
 from the loaded assembly.

 Takes a dll_path parameter specifying the managed DLL to load, and a
 class_method parameter specifying the [Class]::Method() to call after loading.
 the master script will already define the typing speed as part of the master declarations
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap

# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class ClLoadAssembly(BaseCMD):
    """
    # LOLBAS: CL_LoadAssembly.ps1 — Legitimate use: loading .NET diagnostic assemblies via PowerShell diagnostic scripts

    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(ClLoadAssembly, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'ClLoadAssembly'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > cl_loadassembly >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > cl_loadassembly >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        # Path to the managed DLL to load
        self.dll_path = None
        # [Class]::Method() to invoke after loading the assembly
        self.class_method = None

        self.indent_space = '    '

        self.introduction = """
        ----------------------------------
        [!] CL_LoadAssembly Interaction.
        Type help or ? to list commands.
        1: Start a new block using 'new'
        2: Set the managed DLL path using 'dll_path <path>'
        3: Set the class method to invoke using 'class_method <[Class]::Method()>'
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
    #  ClLoadAssembly Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new ClLoadAssembly interaction block
        """
        # Init tracking booleans
        # method from parent class BaseCMD
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'ClLoadAssembly_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_dll_path(self, dll_path):
        """
        Set the path to the managed .NET DLL to load via LoadAssemblyFromPath.
        Example: dll_path C:\\Users\\user\\tools\\diagnostic.dll
        """
        if dll_path:
            if self.taskstarted:
                self.dll_path = dll_path.strip()
                print(self.cl.green("[*] DLL path set to: {}".format(self.dll_path)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClLoadAssembly Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a DLL path."))


    def do_class_method(self, class_method):
        """
        Set the [Class]::Method() expression to invoke after loading the assembly.
        Example: class_method [DiagHelper]::RunCheck()
        """
        if class_method:
            if self.taskstarted:
                self.class_method = class_method.strip()
                print(self.cl.green("[*] Class method set to: {}".format(self.class_method)))
            else:
                print(self.cl.red("[!] <ERROR> You need to start a new ClLoadAssembly Interaction."))
                print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))
        else:
            print(self.cl.red("[!] <ERROR> Please provide a class method expression."))


    def do_assigned(self, arg):
        """
        Get the current assigned ClLoadAssembly configuration
        """
        print(self.cl.green("[?] Currently Assigned ClLoadAssembly Configuration"))
        print("[>] DLL Path     : {}".format(self.dll_path if self.dll_path else "(not set)"))
        print("[>] Class Method : {}".format(self.class_method if self.class_method else "(not set)"))


    def do_complete(self, arg):
        """
        This command calls the constructor on the AutoITBlock
        with all the specific arguments
        >> Check the AutoIT constructor requirements
        """

        if self.taskstarted:
            if not self.dll_path:
                print(self.cl.red("[!] <ERROR> dll_path is required. Set it with 'dll_path <path>'."))
                return
            self.create_autoIT_block()

        # now reset the tracking values and prompt
        self.complete_task()

        # reset task-specific state for the next interaction
        self.dll_path = None
        self.class_method = None


    ######################################################################
    # ClLoadAssembly AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('ClLoadAssembly_' + current_counter, self.create_autoit_function())


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
            dll_path     : str — path to the managed .NET DLL to load
        Optional JSON keys:
            class_method : str — [Class]::Method() expression to invoke after loading
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.dll_path = kwargs.get("dll_path", None)
        if self.dll_path:
            print(f"[*] Setting dll_path attribute : {self.dll_path}")
        else:
            print("[!] <ERROR> dll_path is required for ClLoadAssembly.")
            return

        self.class_method = kwargs.get("class_method", None)
        if self.class_method:
            print(f"[*] Setting class_method attribute : {self.class_method}")
        else:
            print("[*] No class_method provided — assembly will be loaded only")

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
        ; <      ClLoadAssembly Interaction
        ; < ----------------------------------- >

        """
        if not self.csh.creating_subtasks:
            fn += "ClLoadAssembly_{}()".format(self.csh.counter.current())

        return textwrap.dedent(fn)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD shell via Win+R run dialogue
        """

        _open_commandshell = """

        Func ClLoadAssembly_{}()

            ; Creates a ClLoadAssembly Interaction via CMD

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
        Builds the PowerShell command to type into the CMD window.
        Uses CL_LoadAssembly.ps1 from the Windows Audio diagnostics path
        to load a managed .NET assembly via LoadAssemblyFromPath, then
        optionally invokes a class method from the loaded assembly.
        """
        typing_text = '\n'

        # Build the powershell -ep bypass -command string
        ps_script_dir = 'C:\\Windows\\diagnostics\\system\\Audio'
        load_call = 'LoadAssemblyFromPath {}'.format(self.dll_path)

        if self.class_method:
            ps_command = (
                'powershell.exe -ep bypass -command "'
                'set-location -path {script_dir}; '
                'import-module .\\CL_LoadAssembly.ps1; '
                '{load}; '
                '{method}"'
            ).format(
                script_dir=ps_script_dir,
                load=load_call,
                method=self.class_method
            )
        else:
            ps_command = (
                'powershell.exe -ep bypass -command "'
                'set-location -path {script_dir}; '
                'import-module .\\CL_LoadAssembly.ps1; '
                '{load}"'
            ).format(
                script_dir=ps_script_dir,
                load=load_call
            )

        typing_text += 'Send("' + self._escape_send(ps_command) + '{ENTER}")\n'
        typing_text += 'sleep({})\n'.format(random.randint(2000, 5000))
        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_function(self):
        """
        Closes the ClLoadAssembly AutoIT function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
