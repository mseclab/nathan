import os
import running
import hashlib
import json

def get_full_path(path):
    return os.path.abspath(path)

def get_real_path(path):
    if os.path.isabs(path):
        ret_dir = path
    else:
        ret_dir = os.path.abspath(path)
    if not os.path.exists(ret_dir):
        raise Exception("%s not exist!" % ret_dir)
    return ret_dir

def check_file(path, data):
    with open (path) as file:
        print file

def check_missing_dir(path,simulation):
    sub_dir = path.split("/")
    final_path = path[0:-(len(sub_dir[-1]))]
    if not os.path.exists(final_path):
        running.run_command("mkdir -p " + final_path, simulation)

def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

def write_to_json(file, data):
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=4)

def get_sha1(file,simulation=False):
    if simulation:
        return "0000000000000000"
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
