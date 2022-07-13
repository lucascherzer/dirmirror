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

The generated sitemap.txt file contains every file in the directory to mirror. It tells the script what to download.
The script parses this file and then first sends an HTTP HEAD request to find out what kind of document (primarily directory listing or file) each entry represents. That works because directory listings (at least in the python3 builtin webserver) give a respose code of 301, whereas files give a status of 200.

Once the script has figured out which entries are files and which are directory listings, it then simply downloads all files and creates directories where it has to.

## Verifying correct download

To verify that all files have been downloaded correctly, run `find . -type f -exec md5sum {} + | LC_ALL=C sort | md5sum` on both machines, if the hashes match, everything should be fine.

This does not only verify the correct hierarchy, but also the integrity of the files.
**NOTE:** The given command does not account for empty directories.

## TODO

- fix bash oneliner to verify download
- improve cli (color, uniform interface,...)
- maybe: add threading