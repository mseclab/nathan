import time
import zipfile
import os
import commands.restore

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

from util.consts import *
from util.logging import *
from util.files import get_full_path

NO_LABEL = "NO_LABEL"

def get_current_time():
    return time.strftime("%Y%m%d_%H%M%S")

def correctLabel(new_label):
    labels_available = commands.restore.get_label_available()
    counter_label = 0
    quit_search = False
    final_label = new_label
    while not quit_search:
        quit_search = True
        for data in labels_available:
            if data.label == final_label:
                final_label = "%s_%s" % (new_label, counter_label)
                counter_label +=1
                quit_search = False
                break
    return final_label

def run_snapshot(args):
    snapFile = ""
    if args.snapshot_label:
        final_label = correctLabel(args.snapshot_label)
    else:
        final_label = correctLabel(NO_LABEL)

    create_snapshot(final_label, args.no_compression)

def create_snapshot(label, no_compression=False):
    global compression
    label = correctLabel(label)

    snapFile = USERIMAGE_FILE_NAME_TEMPLATE % (get_current_time(), label)

    print_info("Creating snapshot " + snapFile)
    snapFile = get_full_path("%s/%s" % (EMULATOR_DIR, snapFile))
    fileToZip = get_full_path("%s/%s" % (EMULATOR_DIR, USERIMAGE_FILE_NAME))

    if no_compression:
        print_info("Snapshot compression disabled.")
        compression = zipfile.ZIP_STORED

    try:
        with zipfile.ZipFile(snapFile, 'w') as zipper:
            print_debug("Zipping %s..." %fileToZip)
            zipper.write(fileToZip, arcname=os.path.basename(fileToZip),compress_type=compression)
            print_info("Checking zip file...")
            res = zipper.testzip()
            if res != None:
                print_error("Error in creating zip file: " + res)
            else:
                zipper.close()
                print_info("Snapshot correctly created.")
    except IOError as err:
        print_error("Impossible to create snapshot. IOError: " + err.strerror)
    except OSError as oserr:
        print_error("Impossible to create snapshot. OSError: " + oserr.strerror)
    except Exception, e:
        print_error("Impossible to create snapshot: Generic exception")