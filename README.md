# Kenshi Mod Tools

These are still "work in progress" and mostly prototype, yet already working, features. 

# Usage

```
kenshi-mod-tools % python extract.py --help
usage: extract.py [-h] [--output OUTPUT] [--pretty] FILE [FILE ...]

Extracts Kenshi game data and dump it in processable format.

positional arguments:
  FILE             list of files to be processed and merged (order matters)

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  output file name (default: output.json)
  --pretty         prettify JSON output
```

```
kenshi-mod-tools % python merge.py --help
usage: merge.py [-h] [--output OUTPUT] [--version VERSION] [--author AUTHOR]
                FILE [FILE ...]

Merge Kenshi mods into one data file.

positional arguments:
  FILE               list of files to be merged (order matters)

optional arguments:
  -h, --help         show this help message and exit
  --output OUTPUT    output file name (default: output.mod)
  --version VERSION  output mod version (default: 1)
  --author AUTHOR    output mod author (default: "Merged")
```

```
kenshi-mod-tools % python diff.py --help
usage: diff.py [-h] FILE_A FILE_B

Display difference between two mods or mod versions.

positional arguments:
  FILE_A      First file path
  FILE_B      Second file path

optional arguments:
  -h, --help  show this help message and exit
```

# Thanks

Special thanks to [Weaver](https://steamcommunity.com/id/weaverthree) (Steam user) for details about [Kenshi data file format](https://steamcommunity.com/sharedfiles/filedetails/?id=797652627)
