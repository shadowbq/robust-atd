#!/usr/bin/env python

import sys
import getpass

import ratd.utils as utils

import ratd.cliargs
from ratd.cliargs import CliArgs

import ratd.lib
from ratd.lib import SampleSubmit

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# ***************************************************************************************************************************************************
# Script returns the following values:
#    -1 ---> Error connecting to the ATD Server
#    -2 ---> Error uploading file to the ATD Server
#    -3 ---> Analysis failed
#    -4 ---> Error getting report
#    -5 ---> Error Obtaining vmprofilelist
#     0 to 5 ---> Severity level (confident of the sample to be malware
# **************************************************************************************************************************************************


if __name__ == '__main__':
    # Get the list of parameters passed from command line
    options = CliArgs('sample')

    if options.password is None:
        options.password = getpass.getpass()

    if options.verbosity:
        utils.copyleftnotice()

    sample = SampleSubmit(options)
    severity = sample.rtnv
    md5 = sample.rtv_md5

    sys.exit(severity)
