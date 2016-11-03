import time
import zipfile
import os
import commands.restore
from util.consts import *
from util.logging import *
from util.files import *
from shutil import copy2

def get_run_info(arch):
    try:
        current_file = open(get_full_nathan_path(RUNINFO_FILE_NAME,arch), "r")
        return current_file.readline().strip()
    except:
        return None


def run_freeze(args):
    map_file_path = get_run_info(args.arch)
    if not map_file_path:
        print_error("SKIP:Map file not available!")
        return

    if not args.yes:
        print_info("Are you sure to freeze the current system image? (Y/N)")
        selection = raw_input("> ")
        if selection.lower() != "y":
            print_error("System image freeze aborted.")
            return
    print_info("Freezing system image from %s" %map_file_path)
    sys_file_path = get_full_path(get_full_nathan_path(SYS_FILE_NAME,args.arch))
    try:
        print_debug("Copying file from %s to %s " % (map_file_path, sys_file_path))
        copy2(map_file_path,sys_file_path)
    except Exception,e:
        print_error("Impossible to copy files. Error: " + e.message)
        return
    print_info("Freeze complete.")