import sys
import urllib2

from util.consts import *
from util.logging import *
from util.files import *
#from urllib2 import urlopen

CHUNK_SIZE = 16 * 1024
PROXY_SPLIT = "://"

def get_proxy_info(download_proxy):
    proxy_info = {}
    # Get protocol type
    if download_proxy.lower().startswith("https"):
        proxy_info["proto"] = "https"
    else:
        proxy_info["proto"] = "http"

    if download_proxy.find(PROXY_SPLIT) != -1:
        proxy_info["address"] = download_proxy.split(PROXY_SPLIT)[1]
    else:
        proxy_info["address"] = download_proxy
    return proxy_info

def download_file(url, filePath=None, download_proxy=None):
    print_info("GET %s..." % url)
    try:
        # Check for proxy
        if download_proxy:
            proxy_info = get_proxy_info(download_proxy)
            proxy = urllib2.ProxyHandler({proxy_info["proto"]: proxy_info["address"]})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
        req = urllib2.urlopen(url)
        meta = req.info()
        dataLen = meta.getheaders("Content-Length")[0]
        print_info("Size: %s" %humanbytes(dataLen))
        print "Status: 0%",
        file_size = int(dataLen)
        file_size_dl = 0
        status = 0
        min_status= 0
        fp = None
        buffer = None

        if filePath:
            fp = open(filePath, 'wb')
        else:
            buffer = ""
        for chunk in iter(lambda: req.read(CHUNK_SIZE), ''):
            if filePath:
                fp.write(chunk)
            else:
                buffer += chunk

            file_size_dl += len(chunk)
            current_status = int (file_size_dl * 100. / file_size)
            if current_status % 10 == 0:
                if status != current_status:
                    sys.stdout.write("%d%%" %current_status)
                    sys.stdout.flush()
                    status = current_status
            elif current_status % 1 == 0:
                if min_status!= current_status:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    min_status = current_status

        print_info("\nDownload file complete.")
        if not filePath:
            return  buffer


    except Exception, e:
        print_error("Impossible to download the file -> " + str(e))
        sys.exit()

