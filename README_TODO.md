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

## Robust-convicter thread mitigating an overflow of max_queued_events:

It uses a dedicated thread to consume kernel events as quickly as possible.

When the kernel reports an overflow, robust should assume that all the files have will need to be re-crawled as though it had just started watching the dir.
This means that if an overflow does occur, you won't miss a legitimate new file notification, but files may be already queued in a thread. This should be mitigated as files are moved as soon as the thread becomes available, so if there are duplicate threads, the first thread will own the file and the second thread will error out. 
