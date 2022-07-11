import requests,os,sys

def usage():
    print("Usage: python3 mirror.py <ip:port> <directory>")

HOST = sys.argv[1]
try:
    DIR = sys.argv[2]
except:
    DIR = "./"

f = open("sitemap.txt","r")
sitemap = f.readlines()
f.close()

def determine_doctype(url) -> str:
    """Returns 'file' or 'directory' depending on what kind the url points to. Can also return common errors"""
    r = requests.head(url)
    if 299 < r.status_code <= 399:
        return "directory"
    elif 199 < r.status_code <= 299:
        return "file"
    elif 399 < r.status_code <= 499:
        if r.status_code == 404:
            return "not found"
        return "bad request"
    elif 499 < r.status_code <= 599:
        return "server error"

def sanitize_sitemap(sitemap: list):
    if sitemap[0].rstrip().removesuffix("\n") == ".":
        sitemap.pop(0)
    for l in range(len(sitemap)):
        sitemap[l] = sitemap[l].rstrip()
        sitemap[l].removesuffix("\n")
        sitemap[l].removeprefix("./")
        sitemap[l] = sitemap[l][2:]
print(sitemap)
sanitize_sitemap(sitemap)
print(sitemap)
for endpoint in sitemap:
    url = f"http://{HOST}/{endpoint}"
    print(f"[*] Sending request: {url}")
    r = requests.get(url)
    doc = determine_doctype(url)
    if doc == "directory":
        print(f"[{r.status_code}] Creating dir {endpoint}")
        os.system(f"mkdir {DIR}{endpoint}")
    elif doc == "file":
        print(f"[{r.status_code}] Writing file {endpoint}")
        os.system(f"touch {DIR}{endpoint}")
        f = open(f"{DIR}{endpoint}","w")
        f.write(r.text)
        f.close()
    else:
        print(f"[{r.status_code}] Potential error with endpoint {endpoint}")
