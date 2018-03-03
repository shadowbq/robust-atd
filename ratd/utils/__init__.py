import errno
import os
import sys

def copyleftnotice():
    print '# Author - Shadowbq 2015 - www.github.com/shadowbq/robust-atd'
    print '# MIT LICENSE'
    print '# '
    print '# This is not a supported or official application of McAfee.'
    print '# This work is based off of published documentation for integrating'
    print '# with the ATD REST API.'


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

class Mkdirs:

    '''Class defining the mkdir_p algorithm folder'''
    def __init__(self, options):
        self.options = options
        self.path = options.directory
        try:
            if self.options.dirtydir:
                self.mkdir_p(self.options.dirtydir)
        except AttributeError:
            pass

        try:
            if self.options.cleandir:
                self.mkdir_p(self.options.cleandir)
        except AttributeError:
            pass

        try:
            if self.options.errordir:
                self.mkdir_p(self.options.errordir)
        except AttributeError:
            pass

        try:
            if self.options.reportdir:
                self.mkdir_p(self.options.reportdir)
        except AttributeError:
            pass

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
            if self.options.verbosity:
                print ('mkdir_p %s' % path)
                sys.stdout.flush()
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
