#!/usr/bin/env python3

"""
The Core Sheepl Program
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"
__version__ = "2.3"


import sys
import json
import random
import signal
import os
import argparse

# Sheepl Class Imports
from utils.tasks import Tasks
from utils.colours import ColourText
from utils.console import ConsoleContext
from utils.console import SheeplConsole
from profiles.profile import Profile
from template.template import CreateTemplate



def banner(version):
    banner = """

███████╗██╗  ██╗███████╗███████╗██████╗ ██╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔══██╗██║
███████╗███████║█████╗  █████╗  ██████╔╝██║
╚════██║██╔══██║██╔══╝  ██╔══╝  ██╔═══╝ ██║
███████║██║  ██║███████╗███████╗██║     ███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝

version : %s
author  : @lorentzenman

------------------------------------------------
    """ %version

    print(banner)


def signal_handler(sig, frame):
    """
    Catches Control + C
    """
    print("[!] You pressed Ctrl+C")
    print("[!] Exiting Sheepl")
    print("[<] ------------------------------------------ [>]")
    print("""
               /\___
    @@@@@@@@@@@  O  \\
 @@@@@@@@@@@@@@@____/--[ later ]
 @@@@@@@@@@@@@@@
    ||      ||
    ~~      ~~
---------------------------------------------
        """)
    sys.exit(0)


#######################################################################
#  Commandline Arguments
#######################################################################


def parse_arguments():
    # Below are the core arguments
    parser = argparse.ArgumentParser(description="Creating realistic user behaviour for tradecraft emulation.")
    main_parser = parser.add_argument_group('Main Program', 'Core Program Settings')
    main_parser.add_argument("--interactive", action="store_true", default=False, help="Launches an interactive console making it easier to create complex sequences")
    main_parser.add_argument("--no_loop", action="store_true", default=False, help="Run tasks once without looping; default behaviour loops continuously")
    main_parser.add_argument("--no_colour", action="store_false", help="Colours the output in the terminal <boolean> : defaults to True", default=True)
    main_parser.add_argument("--no_tray", action="store_true", help="Removes compiled script tray icon", default=False)
    main_parser.add_argument("--list", action="store_true", default=False, help="List available tasks and exit")

    # Profiles Options
    profile_group = parser.add_argument_group('Profiles', 'Creates Sheepl files from JSON format files')
    profile_group.add_argument("--profile", type=argparse.FileType('r', encoding='UTF-8'), help="Specifies a profile and will import commands based on the JSON file")

    # counts the supplied number of arguments and prints help if they are missing
    if len(sys.argv)==1:
        #parser.print_help()
        print("[≤≥] Creating realistic user behaviour for tradecraft emulation.")
        print("[>:] Either specify a profile file path for input or use interactive mode")
        print("[>:] Example 'python3 sheepl.py --interactive' mode")
        print("[oo] See 'python3 sheepl.py -h' for full list of switches")

        # OCD line break
        print()
        sys.exit(1)
    args = parser.parse_args()

    return args


def main():
    banner(__version__)
    # hr = "------------------------------------"
    # counter below needs to be added as part of the Sheepl Object
    # this should get automatically incremented either based on the
    # length of the task list or a counter tracker
    # Main Parser Setup
    args = parse_arguments()

    # assign colour output
    colour_output = args.no_colour
    print("[!] Colour output is set to : {}".format(str(colour_output).upper()))
    cl = ColourText(colour_output)
    tasks = Tasks()

    if args.list:
        print(cl.green("[!] Available tasks:"))
        for task in tasks.locate_available_tasks().values():
            print("[*] {}".format(task))
        print()
        sys.exit(0)

    if args.interactive:
        context = ConsoleContext()
        con = SheeplConsole(context, cl, tasks, loop=not args.no_loop)
        con.cmdloop()

    if args.profile:
        print("[!] Create a sheepl from the profile file : {}".format(cl.green(args.profile.name)))
        Profile(cl, args.profile.name, tasks)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
