Robust ATD CLI tools
================

## Fix verbosity

should output like a test no flag, current verbose 1, debug verbose 2

<https://docs.python.org/2/howto/argparse.html#combining-positional-and-optional-arguments>

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
