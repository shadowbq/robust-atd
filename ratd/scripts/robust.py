#!/usr/bin/env python
# Copyright (C) 2015 McAfee, Inc.  All Rights Reserved.

import sys, traceback, time
import argparse
import getpass
import pprint as pp

import ratd
import ratd.api
from ratd.api import atd

import ratd.utils as utils

import urllib3


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

    options = utils.robustargs()

    if options.verbose:
        options = utils.copyleftnotice()

    # Create the ATD object and connect to it
    myatd = atd(options.atd_ip, options.skipssl)
    error_control, data = myatd.connect(options.user, options.password)

    if error_control == 0:
        print data
        sys.exit(-1)

    if options.verbose:
        print 'Connection successful...\n'
        print 'Session Value:     ',myatd.session
        print 'User ID:           ',myatd.userId
        print 'ATD ver:           ',myatd.matdver

    # Get the heartbeat value of the ATD Box
    error_control, data = myatd.heartbeat()

    if options.verbose:
        if error_control == 0:
            print 'ATD Box heartbeat: Error Obtaining value'
        else:
            print 'ATD Box heartbeat: ',data

    # Upload file to ATD Server
    error_control, data = myatd.upload_file(options.file_to_upload, options.analyzer_profile)

    if error_control == 0:
        print data
        myatd.disconnect()
        sys.exit(-2)
    else:
        print data

    jobId  = data['jobId']
    taskId = data['taskId']

    print '\nFile %s uploaded\n'%data['file']
    print 'jobId:    ',data['jobId']
    print 'taskId:   ',data['taskId']
    print 'md5:      ',data['md5']
    print 'size:     ',data['size']
    print 'mimeType: ',data['mimeType']
    print ''

    # Check status before requesting the report
    stepwait = 5
    while True:
        error_control, data = myatd.check_status(taskId)
        if error_control == 4 or error_control == 3:
            print '{0} - Waiting for {1} seconds'.format(data, stepwait)
        elif error_control == -1:
            print data
            myatd.disconnect()
            sys.exit(-3)
        else:  # Analysis done
            print '\nAnalysis done'
            break
        time.sleep(stepwait)
        if stepwait < 30:
            stepwait = stepwait + 5

    # Getting Report information
    print '\nGetting report information...'

    while True:
        error_control, data = myatd.get_report(jobId)

        if error_control == 0:
            print '\n',data
            myatd.disconnect()
            sys.exit(-4)

        if error_control == 3:
            print '\n',data
            myatd.disconnect()
            sys.exit(0)

        if error_control == 1:
            try:
                severity = data['Summary']['Verdict']['Severity']
                if 'Description' in data['Summary']['Verdict']:
                    desc = data['Summary']['Verdict']['Description']
                else:
                    desc = ""
            except:
                print '\n**BOMB PARSER**'
                print data
                myatd.disconnect()
                sys.exit(-4)
            else:
                print '\nFinal results...'
                print ' Severity:    %s'%severity
                print ' Description: %s'%desc
                break
        # error_control = 2
        print ' %s - Waiting for 30 seconds...'%data
        time.sleep(30)

    myatd.disconnect()
    sys.exit(severity)

if __name__ == '__main__':
    main()
