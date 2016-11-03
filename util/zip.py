import os
import zipfile
import sys

from util.consts import *
from util.logging import *

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

def decompress(file,data_dir):
    # Decompress file
    print_debug("Decompressing %s..." %file)
    try:
        with zipfile.ZipFile(file, 'r') as zipper:
            zipper.extractall(data_dir)
            zipper.close()
        print_debug("Done.")
    except Exception as e:
        print_error("Decompression error: "+ str(e))
        sys.exit()

def compress(from_file,to_file,simulation=False):
    print_debug("Compressing %s -> %s " %(from_file, to_file))
    if simulation:
        return True
    try:
        with zipfile.ZipFile(to_file, 'w') as zipper:
            zipper.write(from_file, arcname=os.path.basename(from_file), compress_type=compression)
            print_debug("Checking zip file...")
            res = zipper.testzip()
            if res != None:
                print_error("Error in creating zip file: " + res)
                return False
            else:
                zipper.close()
                print_debug("Zip file correctly created.")
                return True

    except IOError as err:
        print_error("Impossible to create zip. IOError: " + err.strerror)
    except OSError as oserr:
        print_error("Impossible to create zip. OSError: " + oserr.strerror)
    except Exception, e:
        print_error("Impossible to create zip: Generic exception")