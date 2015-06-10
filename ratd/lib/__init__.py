from __future__ import print_function
import sys
import time
import os
import json
import tempfile

from watchdog.observers import Observer
import watchdog.events

import ratd.api
from ratd.api import Atd

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class CommonATD():

    def connection_check(self):
        if self.error_control == 0:
            print (self.data)
            sys.exit(-1)

        if self.options.verbosity > 1:
            print ('Connection successful...\n')
            print ('Session Value:     ', self.myatd.session)
            print ('User ID:           ', self.myatd.userId)
            print ('ATD ver:           ', self.myatd.matdver)

    def heartbeat(self):
        if self.options.verbosity > 1:
            if self.error_control == 0:
                print ('ATD Box heartbeat: Error Obtaining value')
            else:
                print ('ATD Box heartbeat: ', self.data)

    def report_errors(self):
        if self.error_control == 0:
            print ('\n', self.data)
            self.myatd.disconnect()
            sys.exit(-4)

        if self.error_control == 3:
            if self.options.quiet is not True:
                print ('({0}:{1}) = {2}: \"{3}\"'.format('-', self.options.md5, '-', self.data))
            self.myatd.disconnect()
            sys.exit(0)


    def report_rtype(self):
        error_control, itype, self.data = self.myatd.get_report_md5(self.options.md5, self.options.rType)
        self.report_errors()

        if itype == 'json':
                self.data = json.dumps(self.data)

        with open(self.options.filename, 'w') as f:
            f.write(self.data)
        f.closed

    def report_stdout(self):
        while True:
            error_control, itype, self.data = self.myatd.get_report_md5(self.options.md5)
            self.report_errors()

            if error_control == 1:
                try:
                    self.severity = self.data['Summary']['Verdict']['Severity']
                    if 'Description' in self.data['Summary']['Verdict']:
                        desc = self.data['Summary']['Verdict']['Description']
                    else:
                        desc = ""
                except:
                    print (sys.exc_info()[0])
                    print ('\n**BOMB parser**')
                    print (self.data)
                    self.myatd.disconnect()
                    sys.exit(-4)
                else:
                    if self.options.quiet is not True:
                        print ('({0}:{1}) = {2}: \"{3}\"'.format(self.data['Summary']['Subject']['Name'], self.data['Summary']['Subject']['md5'], self.data['Summary']['Verdict']['Severity'],desc))
                    if self.options.verbosity:
                        print ('\nFinal results...')
                        print (' Severity:    %s' %self.severity)
                        print (' Description: %s' %desc)
                        if self.options.verbosity > 1:
                            print (self.data)
                    break
            # error_control = 2
            if self.options.verbosity:
                print (' %s ...' %self.data)
                sys.stdout.flush()
            if self.options.quiet is not True:
                print ('({0}:{1}) = {2}: \"{3}\"'.format('-', self.options.md5, '-', '-'))
            sys.exit(-4)


    def rtnv(self):
        return self.rtnv

    def rtv_md5(self):
        return self.md5

class ScanFolder:
    'Class defining a scan folder'

    def __init__(self, options):

        self.options = options
        self.path = options.directory
        self.temp_dir = tempfile.mkdtemp()

        # self.event_handler = watchdog.events.PatternMatchingEventHandler(patterns=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf"],
        #                            ignore_patterns=[],
        #                            ignore_directories=True)

        self.event_handler = watchdog.events.FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()

    def on_created(self, event):

        if self.options.verbosity:
            print("New File identified", event.src_path)

        tmp_target =''
        if self.options.dirtydir:
            tmp_target = self.temp_dir+"/"+os.path.basename(event.src_path)
            if self.options.verbosity:
                print("moved to tmp: ", tmp_target)
            os.rename(event.src_path, tmp_target)
            self.options.file_to_upload = tmp_target
            filename = os.path.basename(tmp_target)
        else:
            self.options.file_to_upload = event.src_path
            filename = os.path.basename(event.src_path)


        sample = SampleSubmit(self.options)
        severity = sample.rtnv
        md5 = sample.rtv_md5

        if self.options.dirtydir:
            if severity > 4:
                target = self.options.dirtydir+filename
                if self.options.verbosity:
                    print('Move file {0}.. to dirty {1}'.format(filename, target))
                os.rename(tmp_target, target)
            elif severity > 0:
                target = self.options.cleandir+filename
                if self.options.verbosity:
                    print('Move file {0}.. to clean {1}'.format(filename, target))
                os.rename(tmp_target, target)
            else:
                target = self.options.errordir+filename
                if self.options.verbosity:
                    print('Move file {0}.. to ERROR {1}'.format(filename, target))
                os.rename(tmp_target, target)
        if self.options.reportdir:
            # find report by md5
            self.options.md5 = md5
            # Report ouput filename
            if 1 == 1:
                self.options.filename = self.options.reportdir + md5
            else:
                self.options.filename = self.options.reportdir + filename
            if self.options.verbosity:
                print('Downloading zip report for \'{0}\' into report: {1}'.format(event.src_path, self.options.filename))
                print ('rType:', self.options.rType)
            rb_rtnv = SearchReports(self.options)

        if self.options.verbosity:
            print("Completed ScanFolder()")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        os.rmdir(self.temp_dir)


class ExistingFolder:
    'Submit Existing files in directory'

    def __init__(self, options):
        # Run the above function and store its results in a variable.
        self.options = options
        self.path = options.directory

        full_file_paths = self.get_filepaths(self.path)

        for file_name in full_file_paths:
            self.options.file_to_upload = file_name
            rtnv, md5 = SampleSubmit(self.options)

    def get_filepaths(self, directory):

        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        return file_paths


class SampleSubmit(CommonATD):
    'Class defining a file submission'

    def __init__(self, options):
        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(options.atd_ip, options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()

        # Upload file to ATD Server
        error_control, self.data = self.myatd.upload_file(self.options.file_to_upload, self.options.analyzer_profile)

        if error_control == 0:
            print (self.data)
            myatd.disconnect()
            sys.exit(-2)
        else:
            if options.verbosity > 2:
                print (self.data)

        jobId = self.data['jobId']
        taskId = self.data['taskId']

        if self.options.verbosity:
            print ('\nFile %s uploaded\n' %self.data['file'])
            print ('jobId:    ', self.data['jobId'])
            print ('taskId:   ', self.data['taskId'])
            print ('md5:      ', self.data['md5'])
            print ('size:     ', self.data['size'])
            print ('mimeType: ', self.data['mimeType'])
            print ('')

        # Check status before requesting the report
        stepwait = 5
        while True:
            error_control, self.data = self.myatd.check_status(taskId)
            if error_control == 4 or error_control == 3:
                if self.options.verbosity:
                    print ('{0} - Waiting for {1} seconds'.format(self.data, stepwait))
                    sys.stdout.flush()
                else:
                    if self.options.quiet is not True:
                        print ('.', end="")
                        sys.stdout.flush()
            elif error_control == -1:
                print (self.data)
                self.myatd.disconnect()
                sys.exit(-3)
            else:  # Analysis done
                if self.options.verbosity:
                    print ('\nAnalysis done')
                else:
                    if self.options.quiet is not True:
                        print ('.', end="")
                        sys.stdout.flush()
                break
            time.sleep(stepwait)
            if stepwait < 30:
                stepwait = stepwait + 5

        # Getting Report information
        if self.options.verbosity:
            print ('\nGetting report information...')

        while True:
            error_control, self.data = self.myatd.get_report(jobId)

            if error_control == 0:
                print ('\n', self.data)
                self.myatd.disconnect()
                sys.exit(-4)

            if error_control == 3:
                print ('\n', self.data)
                self.myatd.disconnect()
                sys.exit(0)

            if error_control == 1:
                try:
                    self.severity = self.data['Summary']['Verdict']['Severity']
                    self.md5 = self.data['Summary']['Subject']['md5']
                    if 'Description' in self.data['Summary']['Verdict']:
                        desc = self.data['Summary']['Verdict']['Description']
                    else:
                        desc = ""
                except:
                    print ('\n**BOMB parser**')
                    print (self.data)
                    self.myatd.disconnect()
                    sys.exit(-4)
                else:
                    if self.options.quiet is not True:
                        print ('({0}:{1}) = {2}: \"{3}\"'.format(self.data['Summary']['Subject']['Name'], self.data['Summary']['Subject']['md5'], self.data['Summary']['Verdict']['Severity'],desc))
                    if self.options.verbosity:
                        print ('\nFinal results...')
                        print (' Severity:    %s' %self.severity)
                        print (' Description: %s' %desc)
                        if self.options.verbosity > 1:
                            print (self.data)
                    break
            # error_control = 2
            if self.options.verbosity:
                print (' %s - Waiting for 30 seconds...' %self.data)
                sys.stdout.flush()
            time.sleep(30)

        self.myatd.disconnect()
        if self.options.quiet is not True:
            print ('')
        self.rtnv = int(self.severity)
        self.rtv_md5 = self.md5
        return


class FetchProfiles(CommonATD):
    'Class defining fetching the Analyzer Profiles from ATD'

    def __init__(self, options):

        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(options.atd_ip, options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()

        # Get the vmprofilelist
        if self.options.listprofiles:
            self.error_control, self.data = self.myatd.get_vmprofiles()
            if self.error_control == 0:
                print ('ATD Box profiles: Error Obtaining value')
                self.myatd.disconnect()
                sys.exit(-5)
            else:
                print ('ATD profiles: ', len(self.data))
                for profile in self.data:
                    print ('Profile id: ', profile['vmProfileid'])
                    print ('Name: ', profile['name'])
                    print ('OS:', profile['selectedOSName'])
                    print ('Run all down selects?: {0}'.format(['Off', 'On'][profile['recusiveAnalysis']]))
                    print ('******************')
                self.myatd.disconnect()
                self.rtnv = EXIT_SUCCESS
                return


class SearchReports(CommonATD):
    'Class defining fetching the Analyzer Profiles from ATD'

    def __init__(self, options):
        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(self.options.atd_ip, self.options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()

        # Get the Basic JSON Report
        #if not self.options.quiet:
        self.report_stdout()

        # Get the iType Report
        if self.options.rType is not None:
            if self.options.filename is None:
                print('Filename (-f <filename>) not include when requesting report generation')
                sys.exit(-1)
            else:
                self.report_rtype()

        self.myatd.disconnect()
        self.rtnv = int(self.severity)
        return
