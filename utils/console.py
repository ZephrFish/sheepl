"""
 This instances the main Sheepl console and provides the interactive
 console to assign tasks

"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"


import os
import cmd
import sys
import textwrap
from pathlib import Path

from utils.base.base_sheepl_class import Sheepl


# https://stackoverflow.com/questions/5822164/object-inheritance-and-nested-cmd

# the wrapper console
class MainConsole(cmd.Cmd):
    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.context = context
        # self.task_list = self.locate_available_tasks()
        # by creating a reference to this here, it
        # tiers down through inheritence to the others
        self.interactive = True


class ConsoleContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


#######################################################################
#   Console Class
#######################################################################

class SheeplConsole(MainConsole):
    """
    Creates a person object
    """

    def __init__(self, context, cl, tasks, loop=True):
        MainConsole.__init__(self, context)

        self.cl = cl
        self.tasks = tasks
        self.loop = "True" if loop else "False"
        self.interactive = True
        # boolean to track whether currently creating a Sheepl
        self.birth = False
        self.icon = False

        self.baseprompt = self.cl.yellow('>: ')
        self.prompt = self.baseprompt
        self.introduction = """
        Sheepl Interactive Console
        ----------------------------------------------
        [!] type 'help' or '?' for command list
        [>] Create a new Sheepl 'create <name>'
        """

        print(textwrap.dedent(self.introduction))



    #######################################################################
    #   Console Functions
    #######################################################################


    def do_create(self, name):
        """
        Create a Sheepl by giving them a name
        example: create <sheeplname>
        """

        if name:
            # first check to see if we are already creating a Sheepl
            if self.birth:
                print(self.cl.red("[!] <ERROR> Already creating a Sheepl named '{}'.".format(self.csh.name)))
                return

            # check to see if the file exists already from a previous Sheepl creation
            output_base = "output/"
            file_name = output_base + name.lower().replace(' ', '_') + '.au3'
            chk_file = Path(file_name)

            if chk_file.is_file():
                print(self.cl.red("[!] The Sheepl output file '{}' already exists".format(file_name)))
                self.replace_file = self.ask_yes_no_question("[?] Do you want to replace this? {}".format(self.cl.green("<yes> <no> : ")))
                if self.replace_file == True:
                    print("[-] Removing file : {}".format(self.cl.yellow(file_name)))
                    chk_file.unlink()
                    self.create_sheepl(name)
                else:
                    print("[*] Leaving file : {} ".format(file_name))
                    return None
            else:
                self.create_sheepl(name)

        else:
            print(self.cl.red("[!] <ERROR> You need to specify a name e.g. 'create <name>'"))


    def do_task(self, task):
        """
        Assign a task to the current Sheepl
        example: task PowerShell
        """
        if not self.birth:
            print(self.cl.red("[!] You need to create a Sheepl to assign tasks to first of all"))
            return

        if not task:
            print(self.cl.red("[!] <ERROR> You need to specify a task e.g. 'task <name>'"))
            print("[?] You can list available tasks using the command 'list'")
            return

        if task not in self.csh.task_list.values():
            print(self.cl.red("[!] <ERROR> Unknown task '{}'. Use 'list' to see available tasks.".format(task)))
            return

        print(self.cl.yellow("[>] You have selected : " + task))
        self.csh.generate_task(task)


    def do_list(self, arg):
        """
        List the available Tasks to assign to a Sheepl
        """
        # # OCD line break
        if self.birth:
            self.csh.list_tasks()
            # OCD line break
            print()
        else:
            print(self.cl.red("[!] Please create a Sheepl to see available tasks 'create <name>'"))


    def do_update(self, arg):
        """
        Updates the available task list
        """
        self.csh.update_available_tasks()


    def do_finished(self, arg):
        """
        Marks the current Sheepl as completed and calls
        the file write functon on the Sheepl Class.
        """
        if self.birth:
            print("[!] Writing the file {} :".format(self.cl.green(self.csh.file_name)))
            self.csh.write_file(self.csh.file_name)
            print("[!] Written the file {} :".format(self.cl.green(self.csh.file_name)))
        else:
            print(self.cl.red("[!] Not currently creating Sheepl - nothing to write"))
        self.prompt = self.cl.yellow(self.baseprompt)


    def do_loop(self, arg):
        """
        Specifies whether to loop or not <default is True>
        """
        if self.birth:
            # this could retrieve the current setting
            print("[*] Default Looping is set to : {}".format(self.csh.loop))
            loop_setting = self.ask_yes_no_question("[?] Do you want to loop tasks? {}".format(self.cl.green("<yes> <no> : ")))
            self.csh.loop = str(loop_setting)

        else:
            print(self.cl.red("[!] You need to create a Sheepl to assign tasks to first of all"))


    def do_icon(self, arg):
        """
        Specifies whether to display the tray icon or not.
        Defaults to 'False' and therefore is hidden
        """
        if self.birth:
            # this could retrieve the current setting
            print("[*] Tray Icon is set to : {}".format(self.csh.icon))
            icon_setting = self.ask_yes_no_question("[?] Do you want to show the icon in the system tray? {}".format(self.cl.green("<yes> <no> : ")))
            self.csh.icon = icon_setting

        else:
            print(self.cl.red("[!] You need to create a Sheepl to assign tasks to first of all"))
        # need to call an operating system check to command to issue


    def do_quit(self, arg):
        """
        Exits the program
        """
        print("------------------------------------------")
        print(r"""
                      /\___
            @@@@@@@@@@@  O \
        @@@@@@@@@@@@@@@____/--[ later ]
        @@@@@@@@@@@@@@@
            ||      ||
            ~~      ~~
        -----------------
            """)
        print("[!] >>>           {}           <<< [!]".format(self.cl.red("Exiting Sheepl")))
        print("[<] ------------------------------------------")
        sys.exit(0)


    ########################################
    # Normal methods
    ########################################


    def create_sheepl(self, name):
        """
        Questions to setup the initial Sheepl
        """

        print(self.cl.yellow("[%] Creating Sheepl called '{}'".format(name)))
        # check the input for spacing
        print("[?] How long would you like {} to take to complete tasks?".format(self.cl.green_ul(name)))
        # NEW: function to deal with time issue bug : requires 'm', 'h' or 'd'
        total_time = self.set_time()

        # Typing Speed
        print("[?] How fast can {} type? <default is 40ms between key>".format(self.cl.green_ul(name)))
        typing_speed = input("#> Enter the typing speed <40> : ")
        if len(typing_speed) == 0:
            typing_speed = 40
        print(self.cl.yellow("Typing speed is {} milliseconds".format(typing_speed)))

        # Prompt Setup
        self.prompt = self.cl.yellow('{} >: '.format(name.lower()))

        # Create the Sheepl Object - the 'self' has a 'csh' object
        # we are in interactive mode, so let's set that
        self.csh = Sheepl(name, total_time, typing_speed, self.loop, self.cl, self.interactive)

        # mark as born in both this console and Sheepl object
        self.birth = True
        self.csh.birth = self.birth


    def set_time(self):
        print("[!] Time values are minutes {}".format(self.cl.green_ul("(m), hours (h) or days (d)")))
        while 1:
            total_time = input("#> Enter the time (e.g. 45m or 6h or 2d) : ")
            if len(total_time) == 0:
                total_time = "10m"
                print("[!] Setting default total time to 10 minutes")
                return total_time
            if total_time.endswith(("m", "h", "d")):
                print("[!] Setting total time to {}".format(self.cl.green_ul(total_time)))
                return total_time
            print(self.cl.red("[!] Error : Time values end with (m), (h) or (d)"))


    def ask_yes_no_question(self, question):
        """
        Small helper function to take in a question and check the response
        is either yes or no
        """
        while 1:
            input_answer = input(question)
            if input_answer.lower() == "yes" or input_answer.lower() == "no":
                break

        if input_answer.lower() == "yes":
            return True
        else:
            return False


    def complete_task(self, text, line, begidx, endidx):
        """
        Tab complete for task list
        """
        if not hasattr(self, 'csh'):
            return []
        return [i for i in self.csh.task_list.values() if i.startswith(text)]
