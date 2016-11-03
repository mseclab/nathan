import json
import datetime
import os
import sys
import shutil
from util.consts import *
from util.logging import *
from util.zip import compress
from util.files import *
from util.running import *
from util.adb import *

ADB_CMD_REMOUNT="remount"
ADB_CMD_PUSH = "push"
ADB_CMD_MKDIR = "shell mkdir -p"

list_file = []

from_dir = ""
to_dir = ""

def slash_path(path):
    if not path.endswith(os.sep):
        path += os.sep
    return path

def scan_dir(dir,from_dir, to_dir, simulation=False):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if name.startswith("."):
            continue
        if os.path.isfile(path):
            full_path = path.replace(from_dir,"",1)
            #print_debug(full_path)
            full_from = from_dir + full_path
            full_to = to_dir[:-1]+full_path
            print_debug("%s -> %s" %(full_from,full_to))
            if not simulation:
                link_copy(full_from, full_to)
        else:
            scan_dir(path,from_dir, to_dir, simulation)

def link_copy(src, dst):
    # Check if dir exists or create
    dir_file = os.path.dirname(dst)
    if not os.path.exists(dir_file):
        os.makedirs(dir_file)
    # Copy file or link
    if os.path.islink(src):
        linkto = os.readlink(src)
        if not os.path.exists(src):
            os.symlink(linkto, dst)
    else:
        shutil.copy(src,dst)

def push_files(start_dir, dir, adb_type, prefix, simulation):
    for name in os.listdir(dir):
        if name.startswith("."):
            continue
        fullname = os.path.join(dir, name)
        if os.path.isfile(fullname):
            targetFile = fullname.replace(start_dir,"")
            dirTargetFile=  os.path.dirname(targetFile)
            # Create directory
            cmd = "%s %s%s" % (ADB_CMD_MKDIR, prefix, dirTargetFile)
            #print_debug("CMD: " + cmd)
            if not simulation:
                result = run_adb_command(adb_type, cmd)
                if not result["success"]:
                    print_error("Error creating directory:" + result["err"])
                    sys.exit()

            # Push file
            cmd = "%s %s %s%s"% (ADB_CMD_PUSH, fullname, prefix, targetFile)
            print_debug("CMD: " + cmd)
            if not simulation:
                result = run_adb_command(adb_type, cmd)
                if not result["success"]:
                    print_error("Error pushing file:" + result["err"])
                    sys.exit()
        else:
            push_files(start_dir, fullname,adb_type, prefix, simulation)

def exec_push(args, adb_type, simulation=True):
    from_dir = args.from_dir
    print_info("Remount System partition in read-write")
    result = run_adb_command(adb_type, ADB_CMD_REMOUNT)
    if not result["success"]:
        print_error("Error: " + result["err"])
        return
    #Push files
    if args.prefix:
        prefix = args.prefix
    else:
        prefix = ""

    print_info("Pushing files...")
    push_files(from_dir,from_dir,adb_type, prefix, args.simulation)
    #for name in os.listdir(from_dir):
    #    if os.path.isdir(os.path.join(from_dir, name)):
    #        print_info("Package: " + name)
    #        push_files(name, os.path.join(from_dir, name),False)


def run_push(args):
    global from_dir, to_dir

    if not args.from_dir:
        print_error("From dir parameters missing...")
        return

    # Check dirs
    from_dir = slash_path(args.from_dir)
    if not get_real_path(from_dir):
        print_error("Error: %s not exists!" % from_dir)
        return

    # Check adb
    adb_type = check_adb(False)
    if adb_type == None:
        print_error("ADB not available! Please retry ./nathan.py init.")
        sys.exit(1)

    dev_lists = get_nathan_device_list(adb_type)
    if len(dev_lists) == 0:
        print_error("Nathan emulators not available")
    elif len(dev_lists) > 1:
        print_error("To much Nathan emulator. Please keep only one.")
    else:
        print_info("Pushing file to %s on %s..." % (dev_lists[0]["device"],dev_lists[0]["emulator"]))
        exec_push(args, adb_type)

