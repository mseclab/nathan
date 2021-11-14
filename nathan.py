#! /usr/bin/env python/learn git
import os
import argparse

from util.consts import *
from util.logging import *

from commands.restore import run_restore
from commands.snapshot import run_snapshot
from commands.start import run_start
from commands.init import run_init
from commands.freeze import run_freeze
from commands.push import run_push


def error_msg(msg):
    print msg
    os.exit(1)

if __name__ == "__main__":
    print_info(NATHAN_LOGO)
    print_info(APP_DESC)
    parser = argparse.ArgumentParser()
    parser_commands = parser.add_subparsers(title='Command to run', dest="command")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show emulator/kernel logs")
    parser.add_argument("-a", "--arch", help="Select architecture (arm/x86) - Default = x86", default="x86")

    parser_init = parser_commands.add_parser("init", help="Download and init Nathan emulator")
    parser_init.add_argument("-dp", "--download-proxy", help="Proxy address for downloading Nathan emulator", required=False)
    parser_init.add_argument("-du", "--download-url", help="Alternative URL to download files",
                                required=False)
    parser_init.add_argument("-fd", "--force-download", help="Force Download and overwrite local files",
                                action="store_true", required=False)
    parser_init.add_argument("--reset", help="Reset Nathan emulator (DANGEROUS)", action="store_true", required=False)

    parser_start = parser_commands.add_parser("start", help= "Start Nathan emulator")
    parser_start.add_argument("-p", "--proxy", help="Set Proxy for communication", type=str)

    parser_snapshot = parser_commands.add_parser("snapshot", help="Create userdata image snapshot")
    parser_snapshot.add_argument("-sl", "--snapshot-label", help="Label of userdata image to restore", required=False)
    parser_snapshot.add_argument("-nc", "--no-compression", help="Disable snapshot compression", action="store_true")

    parser_restore = parser_commands.add_parser("restore", help="Restore userdata image snapshot")
    parser_restore.add_argument("-rl", "--restore-label", help="Label of userdata image to restore")
    parser_restore.add_argument("-ll", "--list-label", action="store_true", help="List only the userdata image snapshots available")
    parser_restore.add_argument("-sb", "--skip-backup", action="store_true", help="Skip backup of the current userdata image")

    parser_freeze = parser_commands.add_parser("freeze", help="Freeze temporary system image")
    parser_freeze.add_argument("-y", "--yes", help="Freeze without asking for confirmation", action="store_true", default=False)

    parser_push = parser_commands.add_parser("push", help="Push files to Nathan emulator ")
    parser_push.add_argument("-f", "--from_dir", help="Source directory", required=True)
    parser_push.add_argument("-p", "--prefix", help="Add prefix to files")
    parser_push.add_argument("-s", "--simulation", help="Simulate push files", action="store_true", default=False)


    args = parser.parse_args()

    if args.command == "restore":
        run_restore(args)
    elif args.command == "snapshot":
        run_snapshot(args)
    elif args.command == "start":
        run_start(args)
    elif args.command == "init":
        run_init(args)
    elif args.command == "freeze":
        run_freeze(args)
    elif args.command == "push":
        run_push(args)
    else:
        pass
