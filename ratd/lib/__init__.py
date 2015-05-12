
from __future__ import print_function
import sys, traceback, time
import argparse
import getpass
import pprint as pp
import os

from watchdog.observers import Observer
import watchdog.events

import urllib3


import ratd
import ratd.api
from ratd.api import atd
import ratd.utils as utils
import ratd.cliargs
from ratd.cliargs import cliargs


EXIT_SUCCESS = 0
EXIT_FAILURE = 1

class ScanFolder:
    'Class defining a scan folder'

    def __init__(self, options):

        self.options = options
        self.path = options.directory

        # self.event_handler = watchdog.events.PatternMatchingEventHandler(patterns=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf"],
        #                            ignore_patterns=[],
        #                            ignore_directories=True)

        self.event_handler = watchdog.events.FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()

    def on_created(self, event):
        self.options.file_to_upload = event.src_path
        if self.options.verbosity:
            print("New File identified", event.src_path)
        SampleSubmit(self.options)
        if self.options.verbosity:
            print("Completed ScanFolder()")

    def stop(self):
        self.observer.stop()
        self.observer.join()

class ExistingFolder:
    'Submit Existing files in directory'

    def __init__(self, options):
        # Run the above function and store its results in a variable.
        self.options = options
        self.path = options.directory

        full_file_paths = self.get_filepaths(self.path)

        for file_name in full_file_paths:
            self.options.file_to_upload = file_name
            SampleSubmit(self.options)

    def get_filepaths(self, directory):

        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        return file_paths


class SampleSubmit:
    'Class defining a file submission'

    def __init__(self, options):
        self.rtnv = EXIT_FAILURE

        # Create the ATD object and connect to it
        myatd = atd(options.atd_ip, options.skipssl)
        error_control, data = myatd.connect(options.user, options.password)

        if error_control == 0:
            print (data)
            sys.exit(-1)

        if options.verbosity > 1:
            print ('Connection successful...\n')
            print ('Session Value:     ',myatd.session)
            print ('User ID:           ',myatd.userId)
            print ('ATD ver:           ',myatd.matdver)

        # Get the heartbeat value of the ATD Box
        error_control, data = myatd.heartbeat()

        if options.verbosity > 1:
            if error_control == 0:
                print ('ATD Box heartbeat: Error Obtaining value')
            else:
                print ('ATD Box heartbeat: ',data)

        # Upload file to ATD Server
        error_control, data = myatd.upload_file(options.file_to_upload, options.analyzer_profile)

        if error_control == 0:
            print (data)
            myatd.disconnect()
            sys.exit(-2)
        else:
            if options.verbosity > 2:
                print (data)

        jobId  = data['jobId']
        taskId = data['taskId']

        if options.verbosity:
            print ('\nFile %s uploaded\n'%data['file'])
            print ('jobId:    ',data['jobId'])
            print ('taskId:   ',data['taskId'])
            print ('md5:      ',data['md5'])
            print ('size:     ',data['size'])
            print ('mimeType: ',data['mimeType'])
            print ('')

        # Check status before requesting the report
        stepwait = 5
        while True:
            error_control, data = myatd.check_status(taskId)
            if error_control == 4 or error_control == 3:
                if options.verbosity:
                    print ('{0} - Waiting for {1} seconds'.format(data, stepwait))
                    sys.stdout.flush()
                else:
                    if options.quiet is not True:
                      print ('.', end="")
                      sys.stdout.flush()
            elif error_control == -1:
                print (data)
                myatd.disconnect()
                sys.exit(-3)
            else:  # Analysis done
                if options.verbosity:
                    print ('\nAnalysis done')
                else:
                    if options.quiet is not True:
                      print ('.', end="")
                      sys.stdout.flush()
                break
            time.sleep(stepwait)
            if stepwait < 30:
                stepwait = stepwait + 5

        # Getting Report information
        if options.verbosity:
            print ('\nGetting report information...')

        while True:
            error_control, data = myatd.get_report(jobId)

            if error_control == 0:
                print ('\n',data)
                myatd.disconnect()
                sys.exit(-4)

            if error_control == 3:
                print ('\n',data)
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
                    print ('\n**BOMB parser**')
                    print (data)
                    myatd.disconnect()
                    sys.exit(-4)
                else:
                    if options.verbosity:
                        print ('\nFinal results...')
                        print (' Severity:    %s'%severity)
                        print (' Description: %s'%desc)
                        if options.verbosity > 1:
                            print (data)
                    break
            # error_control = 2
            if options.verbosity:
                print (' %s - Waiting for 30 seconds...'%data)
                sys.stdout.flush()
            time.sleep(30)

        myatd.disconnect()
        print ('')
        self.rtnv = int(severity)
        return

    def rtnv(self):
        return self.rtnv

class FetchProfiles():
    'Class defining fetching the Analyzer Profiles from ATD'

    def __init__(self, options):
        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE

        myatd = atd(options.atd_ip, options.skipssl)
        error_control, data = myatd.connect(options.user, options.password)

        if error_control == 0:
            print (data)
            sys.exit(-1)

        if options.verbosity > 1:
            print ('Connection successful...\n')
            print ('Session Value:     ',myatd.session)
            print ('User ID:           ',myatd.userId)
            print ('ATD ver:           ',myatd.matdver)

        # Get the heartbeat value of the ATD Box
        error_control, data = myatd.heartbeat()

        if options.verbosity > 1:
            if error_control == 0:
                print ('ATD Box heartbeat: Error Obtaining value')
            else:
                print ('ATD Box heartbeat: ',data)

        # Get the vmprofilelist
        if options.listprofiles:
            error_control, data = myatd.get_vmprofiles()
            if error_control == 0:
                print ('ATD Box profiles: Error Obtaining value')
                myatd.disconnect()
                sys.exit(-5)
            else:
                print ('ATD profiles: ',len(data))
                for profile in data:
                    print ('Profile id: ', profile['vmProfileid'])
                    print ('Name: ', profile['name'])
                    print ('OS:', profile['selectedOSName'])
                    print ('Run all down selects?: {0}'.format(['Off','On'][profile['recusiveAnalysis']]))
                    print ('******************')
                myatd.disconnect()
                self.rtnv = EXIT_SUCCESS
                return

    def rtnv(self):
        return self.rtnv
