import subprocess

def run_command(cmd, simulation=False):
    if simulation:
        return ({"success": True})

    if isinstance(cmd, basestring):
        cmd = cmd.split(" ")
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        e = None
        success = True
    except OSError as e:
        out = None
        err = None
        success = False

    if err:
        success = False
    return ({"success":success, "out":out, "err":err, "exception":e})
