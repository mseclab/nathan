import os
import re
from util.logging import *
from util.consts import *
from util.running import run_command
from util.emulator import download_emulator_from_google

ADB_VERSION_LINE = "Android Debug Bridge version"
ADB_DEVICES_LINE = "List of devices attached"
ADB_CMD_DEVICES = "devices -l"

def is_adb_version_valid(adb_ver):
    if adb_ver != "" and adb_ver.find(ADB_VERSION_LINE)!= -1:
        full_version = adb_ver.split(ADB_VERSION_LINE)[1]
        if (int(full_version.split(".")[0]) >= ADB_MIN_MAJOR_VER) and (int(full_version.split(".")[2]) >= ADB_MIN_PATCH_VER):
            return True
        else:
            print_error("System ADB version is old. Please update.")
    return False


def is_local_adb_valid():
    print_info("Checking local adb version...")
    if os.path.isdir(EMULATOR_LOCAL_PTOOLS_DIR):
        result = run_command([EMULATOR_LOCAL_PTOOLS_DIR+ADB_CMD, EMULATOR_OPT_VER])
        if result["err"] and result["err"].find(ADB_VERSION_LINE)!= -1:
            print_info("OK: using local %s" % result["err"].split("\n")[0])
            return True
        else:
            print_error("KO: Local emulator error = %s." %result["err"])
    else:
        print_error("KO: Local folder not exists.")
    return False

def is_path_adb_valid():
    print_info("Checking system adb version...")
    result = run_command([ADB_CMD, EMULATOR_OPT_VER])
    if result["success"]:
        adbVersion = result["out"].split("\n")[0]
        if is_adb_version_valid(adbVersion):
            print_info("OK: %s" %adbVersion)
            return True
        else:
            print_error("KO: Emulator version %s obsolete." % adbVersion)
    else:
        exception = result["exception"]
        if result["err"]:
            print_error(result["err"])
            return False
        if exception == None:
            return False
        if exception.errno == os.errno.ENOENT:
            print_error("Android emulator is not available in PATH:\n" + os.getenv("PATH"))
        else:
            print "Error: " + exception
        return False


def check_adb(with_download=False):
    print_info("Checking adb...")
    if is_local_adb_valid():
        return "local"
    if is_path_adb_valid():
        return "path"
    if with_download:
        # Start download emulator
        print_info("A valid emulator/adb cannot be find. Downloading sdk from official site...")
        download_emulator_from_google()
        return "local"
    else:
        return None

def run_adb_command(adb_type, command):
    if adb_type == "local":
        adb_cmd = EMULATOR_LOCAL_PTOOLS_DIR+ADB_CMD
    elif adb_type == "path":
        adb_cmd = ADB_CMD
    else:
        print_error("ADB type error!")
        os.exit(1)
    return run_command(adb_cmd + " " + command)

def get_nathan_device_list(adb_type):
    ret = []
    devices_list_result = run_adb_command(adb_type,ADB_CMD_DEVICES)
    if devices_list_result["success"]:
        devices_list_raw = devices_list_result["out"]
        if devices_list_raw.find(ADB_DEVICES_LINE) != -1:
            devices_list = devices_list_raw.split("\n")[1:]
            for line in devices_list:
                if line != "" and line.find(BASIC_NAME) != -1:
                    values = re.split("\s+", line)
                    ret.append({"emulator":values[0], "device": values[-1]})
    return ret