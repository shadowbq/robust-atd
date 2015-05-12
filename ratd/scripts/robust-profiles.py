#!/usr/bin/env python
# Copyright (C) 2015 McAfee, Inc.  All Rights Reserved.

import sys, traceback, time
import argparse
import getpass
import pprint as pp
import urllib3

import ratd
import ratd.api
from ratd.api import atd
import ratd.utils as utils
import ratd.cliargs
from ratd.cliargs import cliargs

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


def main():
    # Get the list of parameters passed from command line

    options = cliargs('profile')

    if options.password is None:
        options.password = getpass.getpass()

    if options.verbosity:
        utils.copyleftnotice()

    # Create the ATD object and connect to it
    myatd = atd(options.atd_ip, options.skipssl)
    error_control, data = myatd.connect(options.user, options.password)

    if error_control == 0:
        print data
        sys.exit(-1)

    if options.verbosity:
        print 'Connection successful...\n'
        print 'Session Value:     ',myatd.session
        print 'User ID:           ',myatd.userId
        print 'ATD ver:           ',myatd.matdver

    # Get the heartbeat value of the ATD Box
    error_control, data = myatd.heartbeat()

    if options.verbosity:
        if error_control == 0:
            print 'ATD Box heartbeat: Error Obtaining value'
        else:
            print 'ATD Box heartbeat: ',data

    # Get the vmprofilelist
    if options.listprofiles:
        error_control, data = myatd.get_vmprofiles()
        if error_control == 0:
            print 'ATD Box profiles: Error Obtaining value'
            myatd.disconnect()
            sys.exit(-5)
        else:
            print 'ATD profiles: ',len(data)
            for profile in data:
                print 'Profile id: ', profile['vmProfileid']
                print 'Name: ', profile['name']
                print 'OS:', profile['selectedOSName']
                print 'Run all down selects?: {0}'.format(['Off','On'][profile['recusiveAnalysis']])
                print '******************'
            myatd.disconnect()
            sys.exit(EXIT_SUCCESS)

if __name__ == '__main__':
    main()
