
# #######################################################################
#
#  Task : Ldifde Interaction
#
# #######################################################################


"""
 Creates the autoIT stub code to be passed into the master compile

 Simulates legitimate Active Directory administrator use of ldifde.exe
 for exporting or importing AD objects (users, groups) for auditing
 or bulk migration operations.

"""

# SERVER-ONLY: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)
# LOLBAS: ldifde.exe — Legitimate use: AD object export for auditing and bulk import operations

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import cmd
import random
import textwrap


# Sheepl Class Imports
from utils.base.base_cmd_class import BaseCMD


class Ldifde(BaseCMD):
    """
    Inherits from BaseCMD
        This parent class contains:
        : do_back               > return to main menu
        : do_discard            > discard current task
        : do_complete           > completes the task and resets trackers
        : check_task_started    > checks to see task status

    # SERVER-ONLY: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)
    # LOLBAS: ldifde.exe — Legitimate use: AD object export for auditing and bulk import operations
    """

    def __init__(self, csh, cl):

        # Calling super to inherit from the BaseCMD Class __init__
        super(Ldifde, self).__init__(csh, cl)

        # Override the defined task name
        self.taskname = 'Ldifde'

        # current Sheepl Object
        self.csh = csh
        # current colour object
        self.cl = cl

        # Overrides Base Class Prompt Setup
        if csh.creating_subtasks:
            self.baseprompt = cl.yellow('[>] Creating subtask\n{} > ldifde >: '.format(csh.name.lower()))
        else:
            self.baseprompt = cl.yellow('{} > ldifde >: '.format(csh.name.lower()))

        self.prompt = self.baseprompt

        self.indent_space = '    '

        # ----------------------------------- >
        #      Task Specific Variables
        # ----------------------------------- >

        # SERVER-ONLY: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)
        self.action = 'export'
        self.server = ''
        self.base_dn = 'DC=domain,DC=local'
        self.ldif_file = 'C:\\ldap_export.ldf'
        self.ldap_filter = '(objectClass=user)'

        # ----------------------------------- >

        self.introduction = """
        ----------------------------------
        [!] Ldifde Interaction.
        Type help or ? to list commands.
        NOTE: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)
        1: Start a new block using 'new'
        2: Set action using 'action' (export or import, default: export)
        3: Set DC hostname using 'server'
        4: Set LDAP base DN using 'base_dn'
        5: Set output/input file using 'file'
        6: Set LDAP filter using 'filter' (export only)
        7: Complete the interaction using 'complete'
        """

        # ----------------------------------- >
        # now call the loop if we are in interactive mode by checking
        # if we are parsing JSON

        if not self.csh.json_parsing:
            # call the intro and then start the loop
            print(textwrap.dedent(self.introduction))
            self.cmdloop()


    #######################################################################
    #  Ldifde Console Commands
    #######################################################################


    def do_new(self, arg):
        """
        This command creates a new Ldifde interaction
        """
        if self.check_task_started():
            self.prompt = self.cl.blue("[*] Current Task : 'Ldifde_{}'".format(str(self.csh.counter.current())) + "\n" + self.baseprompt)


    def do_action(self, arg):
        """
        Set the ldifde action mode: export or import.
        Default: export
        Example: action export
                 action import
        """
        if self.taskstarted:
            if arg.lower() in ('export', 'import'):
                self.action = arg.lower()
                print(self.cl.green("[*] Action set to: {}".format(self.action)))
            else:
                print(self.cl.red("[!] <ERROR> Action must be 'export' or 'import'."))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ldifde Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_server(self, arg):
        """
        Set the DC hostname to connect to.
        Default: uses current domain (no -s flag)
        Example: server dc01.domain.local
        """
        if self.taskstarted:
            if arg:
                self.server = arg
                print(self.cl.green("[*] Server set to: {}".format(self.server)))
            else:
                print(self.cl.green("[*] No server specified — will use current domain default"))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ldifde Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_base_dn(self, arg):
        """
        Set the LDAP base DN for the export.
        Default: DC=domain,DC=local
        Example: base_dn DC=corp,DC=example,DC=com
        """
        if self.taskstarted:
            if arg:
                self.base_dn = arg
                print(self.cl.green("[*] Base DN set to: {}".format(self.base_dn)))
            else:
                print(self.cl.green("[*] Using default base DN: {}".format(self.base_dn)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ldifde Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_file(self, arg):
        """
        Set the LDIF output (export) or input (import) file path.
        Default: C:\\ldap_export.ldf
        Example: file C:\\temp\\ad_users.ldf
        """
        if self.taskstarted:
            if arg:
                self.ldif_file = arg
                print(self.cl.green("[*] LDIF file set to: {}".format(self.ldif_file)))
            else:
                print(self.cl.green("[*] Using default LDIF file: {}".format(self.ldif_file)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ldifde Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_filter(self, arg):
        """
        Set the LDAP filter used during export.
        Default: (objectClass=user)
        Example: filter (objectClass=group)
                 filter (&(objectClass=user)(department=Finance))
        """
        if self.taskstarted:
            if arg:
                self.ldap_filter = arg
                print(self.cl.green("[*] LDAP filter set to: {}".format(self.ldap_filter)))
            else:
                print(self.cl.green("[*] Using default LDAP filter: {}".format(self.ldap_filter)))
        else:
            print(self.cl.red("[!] <ERROR> You need to start a new Ldifde Interaction."))
            print(self.cl.red("[!] <ERROR> Start this with 'new' from the menu."))


    def do_assigned(self, arg):
        """
        Show the current Ldifde task settings
        """
        print(self.cl.green("[?] Currently Assigned Ldifde Settings"))
        print("[>] Action      : {}".format(self.action))
        print("[>] Server      : {}".format(self.server if self.server else "(current domain default)"))
        print("[>] Base DN     : {}".format(self.base_dn))
        print("[>] LDIF file   : {}".format(self.ldif_file))
        print("[>] LDAP filter : {}".format(self.ldap_filter))


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

        # reset task-specific variables for next interaction
        self.action = 'export'
        self.server = ''
        self.base_dn = 'DC=domain,DC=local'
        self.ldif_file = 'C:\\ldap_export.ldf'
        self.ldap_filter = '(objectClass=user)'


    ######################################################################
    # Ldifde AutoIT Block Definition
    #######################################################################


    def create_autoIT_block(self):
        """
        Creates the AutoIT Script Block
        csh.add_tasks takes two positional arguments
            commandname_{counter}, and task
        """

        current_counter = str(self.csh.counter.current())
        self.csh.add_task('Ldifde_' + current_counter, self.create_autoit_function())


    def create_autoit_function(self):
        """
        Grabs all the output from the respective functions and builds the AutoIT output
        """

        autoIT_script = (
            self.autoit_function_open() +
            self.open_commandshell() +
            self.text_typing_block() +
            self.close_ldifde()
        )

        return autoIT_script


    def parse_json_profile(self, **kwargs):
        """
        Takes kwargs in and builds out task variables when using JSON profiles.
        Reads action, server, base_dn, file, and filter from kwargs.
        """

        print("[%] Setting attributes from JSON Profile")
        print(f"[-] The following keys are needed for this task : {[x for x in list(kwargs.keys())[1:]]}")

        self.action = kwargs.get("action", 'export')
        print(f"[*] Setting the action attribute : {self.action}")

        self.server = kwargs.get("server", '')
        print(f"[*] Setting the server attribute : {self.server}")

        self.base_dn = kwargs.get("base_dn", 'DC=domain,DC=local')
        print(f"[*] Setting the base_dn attribute : {self.base_dn}")

        self.ldif_file = kwargs.get("file", 'C:\\ldap_export.ldf')
        print(f"[*] Setting the ldif_file attribute : {self.ldif_file}")

        self.ldap_filter = kwargs.get("filter", '(objectClass=user)')
        print(f"[*] Setting the ldap_filter attribute : {self.ldap_filter}")

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
        ; <      Ldifde Interaction
        ; < ----------------------------------- >
        ; < SERVER-ONLY: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)

        """
        if not self.csh.creating_subtasks:
            function_declaration += "Ldifde_{}()".format(self.csh.counter.current())

        return textwrap.dedent(function_declaration)


    # --------------------------------------------------->
    # Define AutoIT Function

    def open_commandshell(self):
        """
        Opens a CMD window via Win+R for ldifde commands
        """

        _open_commandshell = """

        Func Ldifde_{}()

            ; Creates an Ldifde Interaction via CMD
            ; SERVER-ONLY: ldifde.exe requires Active Directory (DC or RSAT AD tools installed)

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

    def _build_ldifde_command(self):
        """
        Constructs the ldifde command string based on current settings.

        Export: ldifde -f <file> -s <server> -d "<base_dn>" -r "<filter>"
        Import: ldifde -i -f <file> -s <server>
        """
        escaped_file = self._escape_send(self.ldif_file)

        if self.action == 'import':
            cmd_parts = ['ldifde -i -f {}'.format(escaped_file)]
            if self.server:
                cmd_parts.append('-s {}'.format(self._escape_send(self.server)))
        else:
            # export (default)
            escaped_base_dn = self._escape_send(self.base_dn)
            escaped_filter = self._escape_send(self.ldap_filter)
            cmd_parts = ['ldifde -f {}'.format(escaped_file)]
            if self.server:
                cmd_parts.append('-s {}'.format(self._escape_send(self.server)))
            cmd_parts.append('-d "{}"'.format(escaped_base_dn))
            cmd_parts.append('-r "{}"'.format(escaped_filter))

        return ' '.join(cmd_parts)

    def text_typing_block(self):
        """
        Builds the ldifde command sequence and sends it to the CMD window.
        """
        typing_text = '\n'

        ldifde_cmd = self._build_ldifde_command()
        typing_text += 'Send("{}{}")\n'.format(ldifde_cmd, '{ENTER}')
        typing_text += 'sleep({})\n'.format(random.randint(2000, 20000))

        typing_text += "Send('exit{ENTER}')\n"
        typing_text += "; Reset Focus\n"
        typing_text += 'SendKeepActive("")'

        return textwrap.indent(typing_text, self.indent_space)


    # --------------------------------------------------->
    # Close AutoIT Function

    def close_ldifde(self):
        """
        Closes the Ldifde function declaration
        """

        end_func = """

        EndFunc

        """

        return textwrap.dedent(end_func)
