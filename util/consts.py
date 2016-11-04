BASIC_NAME = "nathan"

EMULATOR_CMD = "emulator"
EMULATOR_OPT_VER = "-version"
EMULATOR_DIR = "nathan_x86"
EMULATOR_DEVEL_DIR = "nathan_x86_devel"
EMULATOR_MIN_MAJOR_VER = 25
EMULATOR_SDK_DIR = "sdk/"
EMULATOR_LOCAL_TOOLS_DIR = "./sdk/tools/"
EMULATOR_LOCAL_PTOOLS_DIR = "./sdk/platform-tools/"

ADB_CMD = "adb"
ADB_MIN_MAJOR_VER = 1
ADB_MIN_MINOR_VER = 0
ADB_MIN_PATCH_VER = 36

RELEASE_DIR = "release"

NATHAN_LOGO ="""  _   _       _   _
 | \ | |     | | | |
 |  \| | __ _| |_| |__   __ _ _ __
 | . ` |/ _` | __| '_ \ / _` | '_ \\
 | |\  | (_| | |_| | | | (_| | | | |
 |_| \_|\__,_|\__|_| |_|\__,_|_| |_|
"""

APP_NAME = "Nathan Emulator - Mobile Security Lab 2016\n"
APP_VERSION = "1.0.0"
APP_DESC = "%sVersion %s\nAuthor: Roberto Gassira' - r.gassira@mseclab.com\nDistributed under MIT license.\n" %(APP_NAME, APP_VERSION)

SYS_FILE_NAME = "system.img"
USERIMAGE_FILE_NAME = "userdata-qemu.img"
USERIMAGE_FILE_NAME_TEMPLATE = "userdata-qemu-%s-%s.img.zip"
CURRENT_FILE_NAME = "current"
RUNINFO_FILE_NAME = ".run_info"

EMULATOR_RUN_FILE = ["current", "cache.img", "userdata-qemu.img", "emulator-user.ini", "hardware-qemu.ini"]

#DEFAULT_DOWNLOAD_URL = "http://127.0.0.1:8000"
DEFAULT_DOWNLOAD_URL = "http://repo.mseclab.com/nathan"


def get_full_download_url(path):
    return "%s/%s" % (DEFAULT_DOWNLOAD_URL, path)

def get_full_nathan_path(path,arch):
    return "%s/%s" % (get_emulator_name(arch), path)

def get_emulator_name(arch):
    return "%s_%s" %(BASIC_NAME, arch)

def get_emulator_devel_name(arch):
    return "%s_%s_devel" %(BASIC_NAME, arch)

def get_current_file_json(current_file, arch):
    return "%s_%s.json" % (current_file, arch)