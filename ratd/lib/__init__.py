from __future__ import print_function
import sys
import time
import os
import shutil
import json
import tempfile
import copy
import threading
import ratd.utils as utils

from collections import namedtuple

from watchdog.observers import Observer
import watchdog.events

import ratd.api
from ratd.api import Atd

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (T%(threadName)-2s) %(message)s',)


def worker(sema, pool, unsafe_options, src_path):

    '''Worker for Thread Pool'''
    # logging.debug('Waiting to join the pool')
    with sema:
        options = copy.copy(unsafe_options)
        name = threading.currentThread().getName()
        pool.make_active(name)

        if options.verbosity:
            print ("TPW{0} file => {1} opening".format(name, src_path))
        file_created = Handler(options, src_path)
        file_created.sort_file()

        pool.make_inactive(name)
        if options.verbosity:
            print ("TPW{0} file => {1} completed.".format(name, src_path))

class ActivePool(object):

    '''Semaphore pool allowing max active threads in a pool'''
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            # logging.debug('MA Running: %s', self.active)

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            # logging.debug('MI Running: %s', self.active)


class CommonATD():

    '''Common class for ATD sessions'''
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
                print ('({0}:{1}) = {2}: \"{3}\"'.format(
                    '-',
                    self.options.md5,
                    '-',
                    self.data
                ))
            self.myatd.disconnect()
            sys.exit(0)

    def report_rtype(self):
        error_control, itype, self.data = self.myatd.get_report_md5(
            self.options.md5,
            self.options.rType
        )
        self.report_errors()

        if itype == 'json':
                self.data = json.dumps(self.data)

        with open(self.options.filename, 'w') as f:
            f.write(self.data)
        f.closed

    def report_stdout(self):
        while True:
            error_control, itype, self.data = self.myatd.get_report_md5(self.options.md5)
            #DEBUG print (' %s ...' % self.data)
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
                        print ('({0}:{1}) = {2}: \"{3}\"'.format(
                            self.data['Summary']['Subject']['Name'],
                            self.data['Summary']['Subject']['md5'],
                            self.data['Summary']['Verdict']['Severity'],
                            desc
                        ))
                    if self.options.verbosity:
                        print ('\nFinal results...')
                        print (' Severity:    %s' % self.severity)
                        print (' Description: %s' % desc)
                        if self.options.verbosity > 1:
                            print (self.data)
                    break
            # error_control = 2
            if self.options.verbosity:
                print (' %s ...' % self.data)
                sys.stdout.flush()
            if self.options.quiet is not True:
                print ('({0}:{1}) = {2}: \"{3}\"'.format('-', self.options.md5, '-', '-'))
            sys.exit(-4)

    def rtnv(self):
        return self.rtnv

    def rtv_md5(self):
        return self.md5


class ScanFolder:

    '''Class defining a scan folder'''
    def __init__(self, options):

        self.options = options
        self.path = options.directory
        self.temp_dir = tempfile.mkdtemp()
        self.i = 0
        number_of_threads = int(self.options.maxthreads)
        self.pool = ActivePool()
        self.s = threading.Semaphore(number_of_threads)

        # self.event_handler = watchdog.events.PatternMatchingEventHandler(
        #   patterns=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf"],
        #   ignore_patterns=[],
        #   ignore_directories=True)

        if self.options.existing:
            if self.options.verbosity:
                print("Parsing Existing")
            full_file_paths = self.get_filepaths(self.path)
            self.i = 0
            for file_name in full_file_paths:
                if self.options.verbosity:
                    print("Existing file => {}".format(file_name))
                self.i = self.i + 1
                self.options.file_to_upload = file_name
                t = threading.Thread(
                    target=worker,
                    name=str(self.i),
                    args=(
                        self.s,
                        self.pool,
                        self.options,
                        self.options.file_to_upload
                    )
                )
                t.start()

        if self.options.follow:
            if self.options.verbosity:
                print("Starting Watchdog handlers")
            self.event_handler = watchdog.events.FileSystemEventHandler()
            # Thread handler
            self.event_handler.on_created = self.on_created
            self.observer = Observer()
            self.observer.schedule(self.event_handler, self.path, recursive=True)
            self.observer.start()

    def on_created(self, event):
        options = self.options
        src_path = copy.copy(event.src_path)
        if self.options.verbosity:
            print("New File Created Hook: {}".format(src_path))
        self.i = self.i + 1
        t = threading.Thread(
            target=worker,
            name=str(self.i),
            args=(self.s, self.pool, options, src_path)
        )
        t.start()

    def stop(self):
        try:
            self.observer.stop()
            self.observer.join()
        except:
            if self.options.verbosity:
                print('Watchdog not found or thread could not be joined.')
        os.rmdir(self.temp_dir)

    def get_filepaths(self, directory):

        file_paths = []

        for root, directories, files in os.walk(directory):
            files = [f for f in files if not f[0] == '.']
            directories[:] = [d for d in directories if not d[0] == '.']
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        return file_paths


class Handler:

    '''Class Handler needs to be Thread Safe!'''
    def __init__(self, options, src_path):
        #
        self.options = options
        self.src_path = src_path
        self.temp_dir = tempfile.mkdtemp()

    def sort_file(self):

        if self.options.verbosity:
            print("T{1}H - New File identified {0}".format(self.src_path,threading.currentThread().getName()))

        # Why are moving twice?
        # tmp_target = ''
        # try:
        #    if self.options.dirtydir:
        #        tmp_target = self.temp_dir+"/"+os.path.basename(self.src_path)
        #        if self.options.verbosity:
        #            print("moving to tmp: ", tmp_target)
        #        try:
        #            os.rename(self.src_path, tmp_target)
        #        except OSError:
        #            shutil.move(self.src_path, tmp_target)
        #        sample_fullpath = tmp_target
        #        self.options.file_to_upload = sample_fullpath
        #        filename = os.path.basename(tmp_target)
        #except AttributeError:

        self.options.file_to_upload = self.src_path
        filename = os.path.basename(self.src_path)
        sample_fullpath = self.options.file_to_upload

        if self.options.verbosity:
            print ("T{1}H file => {0}, id(options) {2}".format(
                self.options.file_to_upload,
                threading.currentThread().getName(),
                id(self.options)
            ))
        sample = SampleSubmit(self.options)
        severity = sample.rtnv
        md5 = sample.rtv_md5

        #Severity = 5 Known malicious
        #..
        #Severity = 1 Known Trusted
        #Severity = 0 means unverified (no of engines provided any score within maximum execution time)
        #Severity = -1 means GTI Clean
        #Severity = -2 means failed (either sample execution got terminated or platform is not supported)
        #Severity = -6 means incomplete (sample analysis is not completed)

        try:
            if self.options.dirtydir:
                if severity >= int(self.options.severity):
                    sorted_fullpath = self.options.dirtydir+filename
                    if self.options.verbosity:
                        print('Move file {0}.. to dirty {1}'.format(filename, sorted_fullpath))
                    try:
                        os.rename(sample_fullpath, sorted_fullpath)
                    except OSError:
                        shutil.move(sample_fullpath, sorted_fullpath)
                elif severity > 0 or severity == -1:
                    sorted_fullpath = self.options.cleandir+filename
                    if self.options.verbosity:
                        print('Move file {0}.. to clean {1}'.format(filename, sorted_fullpath))
                    try:
                        os.rename(sample_fullpath, sorted_fullpath)
                    except OSError:
                        shutil.move(sample_fullpath, sorted_fullpath)
                else:
                    sorted_fullpath = self.options.errordir+filename
                    if self.options.verbosity:
                        print('Move file {0}.. to ERROR {1}'.format(filename, sorted_fullpath))
                    try:
                        os.rename(sample_fullpath, sorted_fullpath)
                    except OSError:
                        shutil.move(sample_fullpath, sorted_fullpath)

        except AttributeError:
            pass

        try:
            if self.options.rType:
                # find report by md5
                self.options.md5 = md5
                # Report ouput filename
                if 1 == 1:
                    self.options.filename = self.options.reportdir + md5 + "." + self.options.rType
                else:
                    self.options.filename = self.options.reportdir + filename
                if self.options.verbosity:
                    print('Downloading zip report for \'{0}\' into report: {1}'.format(
                        self.src_path,
                        self.options.filename
                    ))
                    print ('rType:', self.options.rType)
                rb_rtnv = SearchReports(self.options)
        except AttributeError:
            pass

        if self.options.verbosity:
            print("Thread completed".format(threading.currentThread().getName()))


class SampleSubmit(CommonATD):

    '''Class defining a file submission'''
    def __init__(self, options):
        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(options.ip, options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()
        self.connection_check()

        if self.options.verbosity:
            print ("T{1}SS file => {0}, id(options) {2}".format(
                self.options.file_to_upload,
                threading.currentThread().getName(),
                id(self.options)
            ))

        # Upload file to ATD Server
        self.error_control, self.data = self.myatd.upload_file(
            self.options.file_to_upload,
            self.options.analyzer_profile
        )
        self.connection_check()

        if self.options.verbosity > 2:
            print (self.data)

        job_id = self.data['jobId']
        task_id = self.data['taskId']

        if self.options.verbosity:
            print ('\nFile %s uploaded\n' % self.data['file'])
            print ('jobId:    ', self.data['jobId'])
            print ('taskId:   ', self.data['taskId'])
            print ('md5:      ', self.data['md5'])
            print ('size:     ', self.data['size'])
            print ('mimeType: ', self.data['mimeType'])
            print ('')

        # Check status before requesting the report
        stepwait = 5
        while True:
            error_control, self.data = self.myatd.check_status(task_id)
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
            error_control, self.data = self.myatd.get_report(job_id)

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
                        print ('({0}:{1}) = {2}: \"{3}\"'.format(
                            self.data['Summary']['Subject']['Name'],
                            self.data['Summary']['Subject']['md5'],
                            self.data['Summary']['Verdict']['Severity'],
                            desc)
                        )
                    if self.options.verbosity:
                        print ('\nFinal results...')
                        print (' Severity:    %s' % self.severity)
                        print (' Description: %s' % desc)
                        if self.options.verbosity > 1:
                            print (self.data)
                    break
            # error_control = 2
            if self.options.verbosity:
                print (' %s - Waiting for 30 seconds...' % self.data)
                sys.stdout.flush()
            time.sleep(30)

        self.myatd.disconnect()
        if self.options.quiet is not True:
            print ('')
        self.rtnv = int(self.severity)
        self.rtv_md5 = self.md5

        # >>> DEBUG
        # self.myatd.disconnect()
        # self.rtnv = int(0)
        # self.rtv_md5 = "HARDCODED"
        # <<< END DEBUG

        return

class ServerVersionCheck(CommonATD):

    '''Class defining fetching the Analyzer Profiles from ATD'''
    def __init__(self, options):

        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(options.ip, options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.options.verbosity = 3
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()

        self.myatd.disconnect()
        self.rtnv = EXIT_SUCCESS

class FetchProfiles(CommonATD):

    '''Class defining fetching the Analyzer Profiles from ATD'''
    def __init__(self, options):

        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(options.ip, options.skipssl)
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

    '''Class defining searching for a report via an MD5'''
    def __init__(self, options):
        # Create the ATD object and connect to it
        self.rtnv = EXIT_FAILURE
        self.options = options

        # Get an authenticated connection to ATD
        self.myatd = Atd(self.options.ip, self.options.skipssl)
        self.error_control, self.data = self.myatd.connect(self.options.user, self.options.password)
        self.connection_check()

        # Get the heartbeat value of the ATD Box
        self.error_control, self.data = self.myatd.heartbeat()
        self.heartbeat()

        # Get the Basic JSON Report
        # if not self.options.quiet:
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

class Reporter():
    '''Class defining a scan folder'''
    def __init__(self, options):

        self.engine_names = ["GTI File Reputation", "Gateway Anti-Malware", "Anti-Malware", "YARA", "CustomRules","Sandbox"]
        self.options = options
        if self.options.verbosity:
            print("Reporter Started for {}".format(self.options.reportdir))

        full_file_paths = self.get_filepaths(self.options.reportdir)
        if self.options.rPrint == 'csv':
            sys.stdout.write('Timestamp,md5,sha-1,sha-256,size,Type,File Name,Malware Name,')
            for engine_name in self.engine_names:
                sys.stdout.write(engine_name + "," + engine_name + " Severity," + engine_name + " Malware Name,")
            sys.stdout.write('Severity,Severity Value,Analysis Seconds\n')
        for file_name in full_file_paths:
            with open(file_name, 'r') as f:
                parsed_json = json.load(f)

            parsed_json['Summary']['Selectors'] = self.pad_engine_values(parsed_json['Summary']['Selectors'])
            if self.options.rPrint == 'txt':
                self.printer_txt(parsed_json)

            elif self.options.rPrint == 'csv':
                self.printer_csv(parsed_json)

            else:
                self.printer_txt(parsed_json)

    def printer_txt(self, parsed_json):
        sys.stdout.write(parsed_json['Summary']['Subject']['md5'] + " ")
        sys.stdout.write("(" + self.malware_name(parsed_json['Summary']['Selectors'])+ ") : ")
        sys.stdout.write(self.map_severity(parsed_json['Summary']['Verdict']['Severity']))
        sys.stdout.write(" - ")
        sys.stdout.write(parsed_json['Summary']['Data']['analysis_seconds'] + "sec")
        print ("")

    def printer_csv(self, parsed_json):
        sys.stdout.write(parsed_json['Summary']['Subject']['Timestamp'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['md5'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['sha-1'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['sha-256'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['size'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['Type'] + ",")
        sys.stdout.write(parsed_json['Summary']['Subject']['Name'] + ",")
        sys.stdout.write(self.malware_name(parsed_json['Summary']['Selectors']) + ",")

        order_dict = {value_of_engine: idx for idx, value_of_engine in enumerate(self.engine_names)};
        parsed_json['Summary']['Selectors'].sort(key=lambda d: order_dict[d['Engine']])
        for engine in parsed_json['Summary']['Selectors']:
            sys.stdout.write(engine['Engine'] + ",")
            sys.stdout.write(engine['Severity'] + ",")
            sys.stdout.write(engine['MalwareName'] + ",")

        sys.stdout.write(self.map_severity(parsed_json['Summary']['Verdict']['Severity']) + "," + parsed_json['Summary']['Verdict']['Severity'] + "," )
        sys.stdout.write(parsed_json['Summary']['Data']['analysis_seconds'] + " sec")
        print ("")

    def malware_name(self, selectors_tuple):
        name = "---"
        for engine in selectors_tuple:
            #selectors_tuple.iteritems()
            #print engine["MalwareName"]
            if engine["MalwareName"] != "---":
                if engine["MalwareName"] == "Malware.Dynamic" and name == "---":
                    name = engine["MalwareName"]
                elif engine["MalwareName"] != "Malware.Dynamic":
                    name = engine["MalwareName"]
        return name

    def pad_engine_values(self, selectors_tuple):

        for engine in self.engine_names:
            found = False
            for ran_engine in selectors_tuple:
                if engine == ran_engine["Engine"]:
                    found = True
            if not found:
                empty_engine = {}
                empty_engine["Engine"] = engine
                empty_engine["Severity"] = '0'
                empty_engine["MalwareName"] = '---'
                selectors_tuple.append(empty_engine)
        return selectors_tuple


    def map_severity(self, severity):
        try:
            sev_map = {"-1": "White listed", "0": "No malicious activity detected (None)", \
            "1": "Slightly suspicious (Low)", "2": "Somewhat/probably is suspicious(Low-Medium)", \
            "3": "Malicious (Medium)", "4": "Malicious(High)", \
            "5": "Malicious (Very High)"}
            rtv = sev_map[severity]
        except:
            rtv = "Unknown Severity Value: ({})".format(severity)
        return rtv

    def get_filepaths(self, directory):

        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                if filename.endswith('json'):
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

        return file_paths
