import requests, re, os, threading, urllib, json, hashlib, shutil, sys

# This file downloads all the URLs mentioned in a provided file

if len(sys.argv) != 3:
    print("Usage: download.py <flounder URL list> <download file extension>")
    quit()

# File extension for this filetype
FILETYPE_EXT = sys.argv[2]
    
# Create output folder if it doesn't already exist
if not os.path.isdir(FILETYPE_EXT):
    os.mkdir(FILETYPE_EXT)
assert os.path.isdir(FILETYPE_EXT)

print_lock = threading.Lock()
remain = 0

def urlretrieve_with_basic_auth(url, filename=None, reporthook=None, data=None,
        username="", password=""):
    r = requests.get(url, allow_redirects=True, auth=requests.auth.HTTPBasicAuth('',''))
    if r.status_code == 200:
        with open(filename, "wb") as f:
            f.write(r.content)

def download_url(url):
    global remain, print_lock

    file_name = url.split(b'/')[-1].split(b'#')[0].split(b'?')[0]
    file_name = "%s.%s" % (hashlib.sha256(file_name).hexdigest(), FILETYPE_EXT)
    file_path = "%s/%s" % (FILETYPE_EXT, file_name)

    if not os.path.isfile(file_path):
        urlretrieve_with_basic_auth(url, file_path)

    # Write your filter here to prune files which do not match. In this example
    # we prune if they're not RTF files. This is required as filetype: in Bing
    # isn't perfect, especially with PHP pages with dynamic downloads based
    # on GET/POST data

    # Nuke the file if it doesn't start with {\rtf
    try:
        if not open(file_path, "rb").read(8).startswith(b'{\\rtf'):
            os.remove(file_path)
    except:
        pass

    remain -= 1
    with print_lock:
        print("%8d remain" % remain)

    return

def load_bing_cache():
    return open(sys.argv[1], "rb").read().split(b"738ced42e85db6ed9095b29dc94b9253")

def fetch_files():
    global remain

    da_urls = load_bing_cache()
    print("Bing cache loaded")

    #print len(set(da_urls))
    #for url in da_urls:
    #    print repr(url)

    remain = len(set(da_urls))
    for url in set(da_urls):
        threading.Timer(0.0, download_url, args=[url]).start()

fetch_files()

