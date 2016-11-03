import os
import platform
import stat
from util.running import run_command
from util.consts import *
from util.logging import *
from util.net import *
from util.zip import decompress

ANDROID_EMULATOR_VERSION = "Android emulator version "
DOWNLOAD_SDK_BASE_URL = "https://dl.google.com/android/repository/"
DOWNLOAD_TOOLS_FILENAME = "tools_r25.1.7-%s.zip"
DOWNLOAD_PTOOLS_FILENAME = "platform-tools_r24.0.2-%s.zip"

def system_type():
    os_type = platform.system().lower()
    if os_type == "linux":
        return os_type
    elif os_type == "darwin":
        return "macosx"
    else:
        return ""

def is_emulator_running(arch):
    return os.path.exists(get_full_nathan_path(RUNINFO_FILE_NAME, arch))


def is_emulator_version_valid(emulator_ver):
    if emulator_ver != "" and emulator_ver.find(ANDROID_EMULATOR_VERSION)!= -1:
        full_version = emulator_ver.split(ANDROID_EMULATOR_VERSION)[1]
        if int(full_version.split(".")[0]) >= EMULATOR_MIN_MAJOR_VER:
            return True
    return False

def is_local_emulator_valid():
    print_info("Checking local emulator version...")
    if os.path.isdir(EMULATOR_LOCAL_TOOLS_DIR):
        result = run_command([EMULATOR_LOCAL_TOOLS_DIR+EMULATOR_CMD, EMULATOR_OPT_VER])
        if result["success"]:
            print_info("OK: using local %s" % result["out"].split("\n")[0])
            return True
        else:
            print_error("KO: Local emulator error = %s." %result["err"])
    else:
        print_error("KO: Local folder not exists.")
    return False


def is_path_emulator_valid():
    print_info("Checking system emulator version...")
    result = run_command([EMULATOR_CMD, EMULATOR_OPT_VER])
    if result["success"]:
        emulatorVersion = result["out"].split("\n")[0]
        if is_emulator_version_valid(emulatorVersion):
            print_info("OK: %s" %emulatorVersion)
            return True
        else:
            print_error("KO: Emulator version %s obsolete." % emulatorVersion)
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

def set_execute_permission(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.chmod(os.path.join(root, f), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

def download_emulator_file(tool_file):
    print_info("Downloading %s" % tool_file)
    download_file(DOWNLOAD_SDK_BASE_URL + tool_file, EMULATOR_SDK_DIR + tool_file)
    print_info("Decompress %s" % tool_file)
    decompress(EMULATOR_SDK_DIR + tool_file, EMULATOR_SDK_DIR)

def download_emulator_from_google():
    # Create sdk dir
    if not os.path.exists(EMULATOR_LOCAL_TOOLS_DIR):
        os.makedirs(EMULATOR_LOCAL_TOOLS_DIR)
    # Download files and set correct permissions - tools
    tool_file = DOWNLOAD_TOOLS_FILENAME % system_type()
    download_emulator_file(tool_file)
    set_execute_permission(EMULATOR_LOCAL_TOOLS_DIR)
    # Download files and set correct permissions - platform tools
    ptool_file = DOWNLOAD_PTOOLS_FILENAME % system_type()
    download_emulator_file(ptool_file)
    set_execute_permission(EMULATOR_LOCAL_PTOOLS_DIR)

def check_emulator(with_download=False):
    print_info("Checking emulator...")
    if is_local_emulator_valid():
        return "local"
    if is_path_emulator_valid():
        return "path"
    if with_download:
        # Start download emulator
        print_info("A valid emulator/adb cannot be find. Downloading sdk from official site...")
        download_emulator_from_google()
        return "local"
    else:
        return None