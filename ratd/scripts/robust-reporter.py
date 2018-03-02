#!/usr/bin/env python
# A tool designed to quickly summarize the downloaded *.json files in your ENV['reports'] directory.

import sys
import getpass

import ratd.utils as utils

import ratd.cliargs
from ratd.cliargs import CliArgs

import ratd.lib
from ratd.lib import Reporter

if __name__ == '__main__':
    # Get the list of parameters passed from command line

    options = CliArgs('reporter')

    if options.verbosity:
        utils.copyleftnotice()

    report = ratd.lib.Reporter(options)
    sys.exit(0)
