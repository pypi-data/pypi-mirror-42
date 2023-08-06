# pyepgnotify
Reads EPG data from VDR, checks against a list of desired program titles, subtitles, or descriptions, and sends found programs via mail or it to stdout.

# Usage
```
usage: pyegnotify [-h] [--config file] [--no-cache] [--stdout]
                 [--cache-file file] [--epg-dst-file file]

Parses EPG data from VDR, checks against search config and sends mail

optional arguments:
  -h, --help           show this help message and exit
  --config file        Config file
  --no-cache           If given, caching is disabled (suitable for debugging)
  --stdout             Additionally print result to stdout
  --cache-file file    Optionally, cache file location, default
                       epgnotfiy.cache.yaml in home directory is used
  --epg-dst-file file  Store received EPG data to a file
```
