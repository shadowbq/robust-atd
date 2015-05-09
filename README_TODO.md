Robust ATD CLI tools
================

## General Flags

Add output flags
```
-o <OUTPUT_FILE>
-t <type|[JSON/XML/TXT]>
```

## robust-watchdog

Create a tool that watches directory for changes and submits the files to ATD.

Add Directory Watch tool
https://pypi.python.org/pypi/watchdog

Example CLI
```
$> robust-watchdog -D <daemon> -p <PID> -d <directoryToMonitor> -O <OUTPUT_DIR> -t <type|[JSON/XML/TXT]>
```


## robust-reporter

Create a tool that ingests JSON file reports and creates an HTML|JSON file with a summary of the outputs

- Base64 Encode a IntelSecurity Logo.

Example CLI
```
$> robust-reporter -d <directory with JSON> -o <OUTPUT_FILE> -t <type|[HTML/JSON/XML/TXT]>
```

## robust-trust

Create a Python style 'Expect' script that can edit the blacklist or whitelist

it can read from `.robust`

```ini
[zebra]
username=
password=
port=
host=
```

Example CLI
```
$> robust-trust (-W|-B) (--query|--add|--drop) -H(--hash) md5
```
