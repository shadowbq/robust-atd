#!/usr/bin/env python
# Copyright (C) 2015 McAfee, Inc.  All Rights Reserved.

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
# The following example of the use of the atd class is quite basic, it just connects to the atd server, uploads a file and return a value from 1-5
# indicating the potential of the file of being malware. This value can be used in third party tools where the integration with the ATD box must
# be done via API.
# ***************************************************************************************************************************************************
# In order to integrate the script with third party tools, the script returns the following values:
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

    rtnv = SampleSubmit(options)
    sys.exit(rtnv.exit())
