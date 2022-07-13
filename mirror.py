import requests,os,sys, argparse

def usage():
    print("Usage: python3 mirror.py <ip:port>")

def get_sitemap(url: str) -> list:
    r = requests.get(f"http://{HOST}/sitemap.txt")
    return r.text.splitlines()


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
        sitemap[l] = sitemap[l][2:] # For some reason, the line above does not remove the prefix, so here we are


parser = argparse.ArgumentParser(description="Mirror directories via an HTTP server",prefix_chars="--")
parser.add_argument("Host", metavar="host",type=str, nargs=1, help="The host you want to connect to", required=True)
parser.add_argument("Port", metavar="port", type=str, nargs=1, help="The port on the remote host", required=True)
args = parser.parse_args()

HOST = f"{args.host[0]}:{args.port[0]}"
SITEMAP = get_sitemap(HOST)
sanitize_sitemap(SITEMAP)

for endpoint in SITEMAP:
    url = f"http://{HOST}/{endpoint}"
    print(f"[*] Sending request: {url}")
    r = requests.get(url)
    doc = determine_doctype(url)
    if doc == "directory":
        print(f"[{r.status_code}] Creating dir {endpoint}")
        os.system(f"mkdir ./{endpoint}")
    elif doc == "file":
        print(f"[{r.status_code}] Writing file {endpoint}")
        os.system(f"touch ./{endpoint}")
        f = open(f"./{endpoint}","w")
        f.write(r.text)
        f.close()
    else:
        print(f"[{r.status_code}] Potential error with endpoint {endpoint}")
print("Run the following command on both machines to ensure integrity of the files:\n\tfind . -type f -exec md5sum {} + | LC_ALL=C sort | md5sum")