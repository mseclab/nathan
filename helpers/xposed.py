import os
import sys
from util import running
from util.logging import *
from util.files import *

import subprocess

FLASH_SCRIPT_PATH = "/META-INF/com/google/android/flash-script.sh"
XPOSED_TRAIL = "_xposed"
START_PARSING = "- Placing files"
STOP_PARSING = "if [ $IS64BIT ]; then"
INSTALL_AND_LINK = "install_and_link"
XPOSED_INSTALLER = "/system/app/XposedInstaller/XposedInstaller_3.0_alpha4.apk"

def run_command(cmd):
    if isinstance(cmd, basestring):
        cmd = cmd.split(" ")
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        e = None
        success = True
    except OSError as e:
        out = None
        err = None
        success = False

    return ({"success":success, "out":out, "err":err, "exception":e})

def parse_flash_script(xposed_path):
    startParsing = False
    full_path = xposed_path + FLASH_SCRIPT_PATH
    xposed_files = []
    print_debug("Parsing " + full_path)
    with open(full_path) as script:
        for line in script:
            line = line.strip()
            if not startParsing:
                if line.find(START_PARSING) != -1:
                    startParsing = True
            else:
                if line.find(STOP_PARSING) != -1:
                    break
                elif line == "":
                    continue
                else:
                    print line
                    lineInfo = line.split(" ")
                    cmd = lineInfo[0]
                    path = lineInfo[1]
                    if cmd == INSTALL_AND_LINK:
                        path = path+"_xposed"
                    if not os.path.exists(xposed_path + path):
                        print "File %s not exists!" % (xposed_path + path)
                    else:
                        xposed_files.append(path)
    # Add xposed installation file
    xposed_files.append(XPOSED_INSTALLER)
    return xposed_files

def copy_xposed_file(args, xposed_files):
    sys_dir = get_real_path(args.sys_dir)
    xpo_dir = get_real_path(args.xpo_dir)
    print_info("Copying %s ---> %s..." % (xpo_dir, sys_dir))
    for src_file in xposed_files:
        if src_file.find(XPOSED_TRAIL) != -1:
            dst_file = src_file.strip(XPOSED_TRAIL)
        else:
            dst_file = src_file
        # Check dir
        check_missing_dir(sys_dir+ dst_file, args.simulation)
        cmd = "cp %s %s" %(xpo_dir+src_file, sys_dir+ dst_file)
        ret = running.run_command(cmd, args.simulation)
        if not ret["success"]:
            print "Error in running command " + cmd
        else:
            print_debug(cmd)

def add_files(args):
    print_info("Adding xposed files")

    try:
        xpo_dir = get_real_path(args.xpo_dir)
    except Exception, e:
        print_error("Error: " + e.message)
        sys.exit()

    xposed_files = parse_flash_script(xpo_dir)
    copy_xposed_file(args, xposed_files)