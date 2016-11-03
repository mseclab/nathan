import os
import re
import zipfile
import zlib
import sys

from urllib2 import urlopen

from util.consts import *
from util.logging import *
from util.zip import *
from util.emulator import *
from util.files import *
from util.net import *
import commands.snapshot


def download_files(args,nathan_conf, download_proxy = None):
    if args.download_url:
        download_url = args.download_url
    else:
        download_url = DEFAULT_DOWNLOAD_URL
    print_info("Downloading files from %s " % download_url)

    for nathan_file in nathan_conf["files"]:
        file = nathan_file["file"]
        print_debug("Checking file: " + file)
        fullFile = get_full_path("%s/%s" % (EMULATOR_DIR,file))
        if os.path.exists(fullFile):
            if get_sha1(fullFile) != nathan_file["sha1"]:
                print_error("Signature file incorrect. Retrying download...")
            elif args.force_download:
                print_info("Forcing download...")
            else:
                print_error("%s already exists. Skip." % fullFile)
                #sys.exit()
                continue

        download_file("%s/%s" %(download_url,file), fullFile, download_proxy)
        print_debug("Check signature...")
        sha1_file = get_sha1(fullFile)
        if sha1_file != nathan_file["sha1"]:
            print_error("%s File corrupted!" %file)
            sys.exit()
        else:
            print "Signature correct. Decompressing file..."
            decompress(get_full_nathan_path(file,args.arch),EMULATOR_DIR)


def reset_nathan():
    print_info("Resetting Nathan emulator...")
    print_error("Are you sure? (y/n)")
    answer = raw_input()
    if answer.isalpha() and answer.upper() == "Y":
        files_to_remove = []
        for file in EMULATOR_RUN_FILE:
            files_to_remove.append("%s/%s" % (EMULATOR_DIR,file))
        for file in os.listdir(EMULATOR_DIR):
            if file.endswith(".zip") or file.endswith(".json"):
                files_to_remove.append("%s/%s" % (EMULATOR_DIR, file))
        for file in files_to_remove:
            if os.path.exists(file):
                print_debug("Removing %s..." % file)
                os.remove(file)

def check_dirs():
    if not os.path.exists(EMULATOR_DIR):
        os.makedirs(EMULATOR_DIR)

def store_current(current,arch):
    with open(get_full_nathan_path(CURRENT_FILE_NAME, arch), "w") as current_file:
        current_file.write(current)


def run_init(args):
    print_info("Starting Nathan Emulator init...")
    check_dirs()
    if args.reset:
        reset_nathan()
    else:
        emulator_type = check_emulator(with_download=True)
        try:
            # Download latest Info
            if args.download_proxy:
                print_info("Using proxy: " + args.download_proxy)
            print_info("Downloading lastest configuration...")
            current_conf_info =  download_file(get_full_download_url(CURRENT_FILE_NAME), download_proxy=args.download_proxy)
            print_info("Current version available: %s" %current_conf_info )
            store_current(current_conf_info, args.arch)
            current_conf_json = get_current_file_json(current_conf_info,args.arch)
            nathan_conf =  json.loads(download_file(get_full_download_url(current_conf_json),
                                                                      download_proxy=args.download_proxy))
            print_info ("Nathan Version:\nID = %s\nCreation Date = %s" %(nathan_conf["build_id"],nathan_conf["date"]))
            write_to_json(get_full_nathan_path(current_conf_json, args.arch),nathan_conf)
            download_files(args,nathan_conf, args.download_proxy)
        except KeyboardInterrupt:
            print_info("Nathan init stopped. Byebye")
        except Exception, e:
            print_error("Nathan init closed with error: " + e.message)

