import os
import re
import zipfile
import zlib

from util.consts import *
from util.logging import *

from util.files import get_full_path
import commands.snapshot

SNAP_INFO = "--->  Number: %d - Date: %s - Label: %s"
BACKUP_LABEL = "BACKUP"

class SnapInfo:
    def __init__(self, _id, _date, _label, _file):
        self.id = _id
        self.date = _date
        self.label = _label
        self.file = _file

    def __str__(self):
        return SNAP_INFO %(self.id, self.date, self.label)

def get_label_available():
    snap_available = []
    snap_counter = 1
    for file in os.listdir(get_full_path(EMULATOR_DIR)):
        m = re.search(r'userdata-qemu-(\w*)-(\w*)\.img\.zip', file)
        if m:
            filename = m.group()
            snapDate = m.group(1)
            label = m.group(2)
            snap_available.append(SnapInfo(snap_counter, snapDate, label, filename))
            snap_counter += 1

    return snap_available

def show_label_available():
    snap_available = get_label_available()
    if len(snap_available) > 0:
        print_info("Snapshots available:")
        for snap in snap_available:
            print snap
    else:
        print_info("No snapshots available.")
    print ""

def request_restore():
    show_label_available()
    label_available = get_label_available()
    print_info("Select the number")
    complete_selection = False
    while not complete_selection:
        number = raw_input("> ")
        if (number.isdigit()) and (int(number) < len(label_available)+1):
            complete_selection = True
        else:
            print_info("Incorrect selection. Retry")
    snap_selected = label_available[int(number) -1]
    print_info("Ara you sure to restore the snapshot with label %s ? (y/n)" %snap_selected.label)
    selection = raw_input("> ")
    if selection.lower() != "y":
        print_error("Snapshot restore aborted.")
        return
    restore_label(snap_selected.label)

def restore_label(label, skip_backup=False):
    print_info("Restoring label: " + label)
    snap_file = ""
    # Search file
    snap_available = get_label_available()
    for snap in snap_available:
        if snap.label == label:
            snap_file = "%s/%s" %(EMULATOR_DIR,snap.file)
            print_debug("Restoring file %s" %snap_file)
            break
    if snap_file == "":
        print_error("Label %s not available. Please check the label and retry ( use restore -ll for the list of label)" % label)
        return

    # Create Backup
    if not skip_backup:
        print_info("Creating backup of current userdata image...")
        commands.snapshot.create_snapshot(BACKUP_LABEL)

    # Decompress file
    with zipfile.ZipFile(snap_file, 'r') as zipper:
        zipper.extractall(EMULATOR_DIR)
        zipper.close()
    print_info("Restore of %s completed." % label)

def run_restore(args):
    if args.list_label:
        show_label_available()
    elif args.restore_label:
        restore_label(args.restore_label, args.skip_backup)
    else:
        request_restore()

