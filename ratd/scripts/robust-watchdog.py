#!/usr/bin/env python
# Copyright (C) 2015 McAfee, Inc.  All Rights Reserved.

import sys, traceback, time
import getpass

import ratd.utils as utils

import ratd.cliargs
from ratd.cliargs import cliargs

import ratd.lib
from ratd.lib import ScanFolder


if __name__ == '__main__':
    # Get the list of parameters passed from command line

    options = cliargs('watch')

    if options.password is None:
        options.password = getpass.getpass()

    if options.verbosity:
        utils.copyleftnotice()

    job = ScanFolder(options)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        job.stop()
