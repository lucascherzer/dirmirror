# Mirror Script

This is a simple python script to mirror directories across different devices

## Usage

Get help: `python3 mirror.py -h`
On the machine you want to mirror a directory from:
```sh
find . > sitemap.txt
python3 -m http.server
```

On the machine you want to mirror the directory to:
```sh
python3 mirror.py <ip address or hostname> 8000
```

## How it works

The files are served by an HTTP server. This script simply utilizes HTTP status codes to determine whether a given page is a file or a directory listing.
Once the script has figured out which entries are files and which are directory listings, it then simply downloads all files and creates directories where it has to.
This tool depends on the existance of the `sitemap.txt` file being present on the server as this file contains information on the names of subdirectories and files. 

## Verifying correct download

To verify that all files have been downloaded correctly, run `find . -type f -exec md5sum {} + | LC_ALL=C sort | md5sum` on both machines, if the hashes match, everything should be fine.

This does not only verify the correct hierarchy, but also the integrity of the files.
**NOTE:** The given command does not account for empty directories.

## Dependencies

- argparse
- termcolor
- alive_progress

All dependencies can be installed via `pip3`

## TODO

- fix bash oneliner to verify download
- maybe: add threading