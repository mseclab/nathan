import os
import sys
from util import running
from util.logging import *
from util.files import *

SUPER_SU_UPDATE_BINARY="""
# 20+   /common/SuperSU.apk           /system/app/SuperSU/SuperSU.apk     0644    u:object_r:system_file:s0   gui
# 7+    /x86/su                       /system/xbin/su                     0755    u:object_r:system_file:s0   required
# 17+   /x86/daemonsu                 /system/xbin/daemonsu               0755    u:object_r:system_file:s0   required
# 19+   /x86/supolicy                 /system/xbin/supolicy               0755    u:object_r:system_file:s0   required
# 20+   /common/init.goldfish.sh      /system/etc/init.goldfish.sh        0755    u:object_r:system_file:s0   required

"""
class SupersuItem:
    def __init__(self, line):
        data = line.split()
        self.src = data[2]
        self.dst = data[3]
        self.chmod = data[4]

def parse_supersu_script():
    cmds = []
    for line in SUPER_SU_UPDATE_BINARY.split("\n"):
        if line:
            cmds.append(SupersuItem(line))
    return cmds

def copy_data(args, cmds):
    sys_dir = get_real_path(args.sys_dir)

    try:
        su_dir = get_real_path(args.su_dir)
    except Exception, e:
        print_error("Error: " + e.message)
        sys.exit()

    print_info("%s ---> %s" % (su_dir,sys_dir))
    for cmd in cmds:
        sub_dir = (sys_dir+cmd.dst).split("/")
        final_path = (sys_dir+cmd.dst)[0:-(len(sub_dir[-1]))]
        if not os.path.exists(final_path):
            running.run_command("mkdir -p " + final_path, args.simulation)

        copy_cmd = "cp -f %s %s" %(su_dir+cmd.src, sys_dir+cmd.dst)
        print_debug(copy_cmd)
        exit_status = running.run_command(copy_cmd, args.simulation)
        if not exit_status["success"]:
            print "Error copying %s" % sys_dir+cmd.dst
            return

        chmod_cmd = "chmod %s %s" %(cmd.chmod, sys_dir+cmd.dst)
        print_debug(chmod_cmd)
        exit_status =  running.run_command(chmod_cmd, args.simulation)
        if not exit_status["success"]:
            print "Error with chmod for %s" % sys_dir + cmd.dst
            return


def add_files(args):
    print_info("Adding files for SuperSU")
    cmds = parse_supersu_script()
    copy_data(args, cmds)