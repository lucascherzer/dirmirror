# Mirror Script

This is a simple python script to mirror directories across different devices

## Installation
```sh
git clone https://gitlab.com/lucascherzer/directory-mirror.git
cd directory-mirror
pip3 install -r requirements.txt
```

## Usage

Get help: `python3 mirror.py -h`
On the first machine, in the directory you want to copy
```sh
find . > sitemap.txt
python3 -m http.server
```

On the machine you want to mirror the directory to:
```sh
python3 mirror.py <ip address or hostname> 8000
```
__NOTE__: This script assumes that the two machines are either on the same network, or that machine two can reach port 8000 (or any port for that matter) on machine one.

## How it works

The files are served by an HTTP server. This script simply utilizes HTTP status codes to determine whether a given page is a file or a directory listing.
Once the script has figured out which entries are files and which are directory listings, it then simply downloads all files and creates directories where it has to.
This tool depends on the existance of the `sitemap.txt` file being present on the server as this file contains information on the names of subdirectories and files. 

## Verifying correct download

To verify that all files have been downloaded correctly, run `tree | md5sum` on both machines in the mirrored directory, if the hashes match, everything should be fine.

This does not only verify the correct hierarchy, but also the integrity of the files.

## TODO

- maybe: add threading
