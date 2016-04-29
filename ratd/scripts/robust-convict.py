#!/usr/bin/env python

import sys
import time
import getpass

import ratd.utils as utils

import ratd.cliargs
from ratd.cliargs import CliArgs

import ratd.lib

if __name__ == '__main__':
    # Get the list of parameters passed from command line

    options = CliArgs('convict')

    if options.password is None:
        options.password = getpass.getpass()
    try:
        print 'starting mkdirs'
        mkdirs = utils.Mkdirs(options)
        print 'running mkdirs'
    except:
        print 'Failed to create configured directories'
        sys.exit(1)

    job = ratd.lib.ScanFolder(options)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        job.stop()
        sys.exit(0)
