import subprocess
import shlex
import os
import sys

from util.consts import *
from util.logging import *
from util.emulator import check_emulator

"""Parameters means:
-no-reboot : close the emulator on reboot
"""
EMULATOR_OPT_START = "-avd %s -verbose -show-kernel -no-snapshot-save -gpu on -netspeed full -netdelay none -selinux disabled " \
                     "-qemu -no-reboot "

# Output filtering
EMULATOR_START_LINE = "emulator: Starting QEMU main loop"
KERNEL_START_LINE = "[    0.000000] Linux version"
ERROR_LINE = "ERROR"
MAPPING_SYS_PART_LINE = "emulator: Mapping 'system' partition image to"
LOG_START_LINE = "logd.auditd: start"

INI_TEMPLATE = """avd.ini.encoding=UTF-8
path=%s
path.rel=%s
target=android-23
"""
OUTFILE = "%s.log" %BASIC_NAME
HTTP_PROXY_START = "http://"

def get_ini_file_name(arch):
    return "%s.ini" % get_emulator_name(arch)

def get_out_file_name(arch):
    return "%s.log" % get_emulator_name(arch)


def run_emulator(args, emulator_type):
    # Choose correct emulator
    if emulator_type == "local":
        emulator_cmd = EMULATOR_LOCAL_TOOLS_DIR+EMULATOR_CMD
    else:
        emulator_cmd = EMULATOR_CMD

    # Create parameters
    startParam = EMULATOR_OPT_START
    if args.proxy:
        print_info("Using proxy " + args.proxy)
        if not args.proxy.startswith(HTTP_PROXY_START):
            args.proxy = HTTP_PROXY_START + args.proxy
        startParam += " -http-proxy " + args.proxy

    print_info("Redirecting output to " + get_out_file_name(args.arch))
    with open(get_out_file_name(args.arch), 'w') as outfile:
        runCommand = emulator_cmd + " " + startParam % get_emulator_name(args.arch)
        print_debug("Starting emulator with:\n" + runCommand)
        p = subprocess.Popen(shlex.split(runCommand), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=dict(os.environ, ANDROID_AVD_HOME=os.getcwd()))
        try:
            while True:
                output = p.stdout.readline()
                if output == '' and p.poll() is not None:
                    print_info("Nathan closed. Byebye")
                    break
                check_emulator_output(output, args.arch)
                if output:
                    outfile.write(output)
                    if args.verbose:
                        if "warning" in output.lower():
                            print_debug(output.strip())
                        elif "error" in output.lower():
                            print_error(output.strip())
                        else:
                            print_info(output.strip())

                rc = p.poll()
        except KeyboardInterrupt:
            print_info("Nathan closed with Ctrl-c. Byebye")
        except Exception, e:
            print_error("Nathan closed with error: " + e.message)

    # Delete run_info file
    try:
        os.remove(get_full_nathan_path(RUNINFO_FILE_NAME, args.arch))
    except:
        pass
        #out, err = p.communicate()
        #print err

def check_emulator_output(line, arch):
    if line.startswith(EMULATOR_START_LINE):
        print_info("Nathan emulator boot in progress...")
    elif line.startswith(KERNEL_START_LINE):
        print_info("Running Kernel: " +line.split("0] ")[1].strip())
    elif line.startswith(MAPPING_SYS_PART_LINE):
        mapPath = line.replace(MAPPING_SYS_PART_LINE,"").strip();
        print_info("Mapped system partition to:" + mapPath)
        store_run_info(mapPath, arch)
    #elif line.find(LOG_START_LINE) != -1:
    #    print_info("ADB Logging system started.")
    elif line.find(ERROR_LINE) != -1:
        #print_error(line.strip())
        pass

def run_command(cmd, shell=False):
    if isinstance(cmd, basestring):
        cmd = shlex.split(cmd)
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = p.communicate()
        e = None
        success = True
    except OSError as e:
        out = None
        err = None
        success = False

    return ({"success":success, "out":out, "err":err, "exception":e})

def is_emulator_available():
    result = run_command([EMULATOR_CMD, EMULATOR_OPT_VER])
    if result["success"]:
        emulatorVersion = result["out"].split("\n")[0]
        print "Using %s" %emulatorVersion
        return True
    else:
        exception = result["exception"]
        if exception.errno == os.errno.ENOENT:
            print "Android emulator is not available"
            print "Check emulator in\n" + os.getenv("PATH")


        else:
            print "Error: " + exception
        return False

def is_ini_file_valid(arch):
    if not os.path.exists(get_ini_file_name(arch)):
        return False

    # Check file line for line
    line_to_check = completed_ini_template(arch).split()
    counter = 0
    with open(get_ini_file_name(arch)) as read_file:
        for line in read_file:
            if line.strip() != line_to_check[counter] :
                return False
            else:
                counter += 1
    return True

def completed_ini_template(arch):
    emulator_dir = get_emulator_name(arch)
    return INI_TEMPLATE %( os.getcwd()+"/"+emulator_dir, emulator_dir)

def create_ini_file(arch):
    print_info("Creating %s file..." %get_ini_file_name(arch))
    curDir = os.getcwd()
    emulator_dir = get_emulator_name(arch)
    resultOK = True
    with open(get_ini_file_name(arch), "w") as inifile:
        try:
            inifile.write(INI_TEMPLATE %( curDir+"/"+emulator_dir, emulator_dir))
        except Exception as e:
            print "Creating file error:" + enumerate
            resultOK = False
        finally:
            inifile.close()
    return resultOK

def get_current_version(arch):
    try:
        current_file = open(get_full_nathan_path(CURRENT_FILE_NAME,arch), "r")
        return current_file.readline().split(".json")[0]
    except:
        return None

def store_run_info(info,arch):
    with open(get_full_nathan_path(RUNINFO_FILE_NAME, arch),"w") as run_info_file:
        run_info_file.write(info)
        run_info_file.close()


def run_start(args):
    print_info("Selected architecture: " + args.arch)
    current_rom_version = get_current_version(args.arch)
    if current_rom_version == None:
        print_error("Emulator ROM files not available! Please initialize Nathan with ./nathan.py init.")
        sys.exit(1)
    else:
        print_info("Nathan ROM version: " + current_rom_version)

    emulator_type = check_emulator()
    if emulator_type == None:
        print_error("Emulator not available! Please retry ./nathan.py init.")
        sys.exit(1)
    # Check ini file
    if not is_ini_file_valid(args.arch):
        if not create_ini_file(args.arch):
            sys.exit(1)

    run_emulator(args, emulator_type)