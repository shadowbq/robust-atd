import argparse
import ConfigParser
import os.path
import ratd
import ratd.utils as utils


def check_md5(value):
    if len(value) != 32:
        raise argparse.ArgumentTypeError("%s is an invalid md5 hash value" % value)
    return value


def slash_dir(value):
    if value[len(value)-1] != "/":
        raise argparse.ArgumentTypeError("%s should end in a slash" % value)
    value = os.path.expanduser(value)
    return value


class CliArgError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CliArgs():

    def __init__(self, tool, explicit=None):
        self.arg_dict = {
            'user': '(u)sername for the API of the ATD\n\t\t(default: %(default)s)',
            'password': '(p)assword for username\n\t\t(default: %(default)s) ',
            'password_secured': '(p)assword for username\n\t\t(default: ****<.robust>*****) ',
            'ip': '(i)p or hostname address of ATD\n\t\t(default: %(default)s) ',
            'sample': '(s)ample or file to be analyzed\n\t\t(default: %(default)s)',
            'skipssl': 'do (n)ot verify the SSL certificate for the communications\n\t\t(default: %(default)s)',
            'analyzer': '(a)nalyzer profile id to be used during analysis\n\t\t(default: %(default)s)',
            'profiles': '(l)ist analyzer profiles available\n\t\t(default: %(default)s)',
            'directory': '(d)irectory to watch for events\n\t\t(default: %(default)s)',
            'existing': '(e)xisting files in directory will be submitted\n\t\t(default: %(default)s)',
            'rType': '(t)ype of report requested\n\t\t(default: %(default)s)',
            'rPrint': '(o)utput type for reporter \n\t\t(default: %(default)s)',
            'follow': '(f)ollow and watch the directory for new files to submit\n\t\t(default: %(default)s)',
            'filename': '(w)rite report to filename for saving the requested report\n\t\t(default: %(default)s)',
            'md5': '(m)d5 32bit hash of the sample to search\n\t\t(default: %(default)s)',
            'cleandir': '(c) move clean files to this directory\n\t\t(default: %(default)s)',
            'dirtydir': '(x) move processed dirty files to this directory\n\t\t(default: %(default)s)',
            'reportdir': '(r) reports are processed or stored using this directory\n\t\t(default: %(default)s)',
            'errordir': '(z) move error or skip files to this directory \n\t\t(default: %(default)s)',
            'severity': '(y) treat sample as dirty with this severity [0-5] or higher\n\t\t(default: %(default)s)',
            'maxthreads': '(j) max number of threads\n\t\t(default: %(default)s)',
            'quiet': '(q)uiet all output\n\t\t(default: %(default)s)',
            'verbosity': 'increase output (v)erbosity\n\t\t(default: %(default)s)'
        }
        self.description = 'Robust McAfee ATD Python CLI tool'
        self.epilog = ''
        self.dot_robust = self.dot_robust_helper()

        self.parser = argparse.ArgumentParser(epilog=self.epilog, description=self.description, formatter_class=argparse.RawTextHelpFormatter)

        if tool == 'authOnly':
            self.auth_args()

        elif tool == 'profile':
            self.auth_args()
            profile_group = self.parser.add_argument_group('Profile parameters')
            profile_group.add_argument('-l', required=True, action='store_true', dest='listprofiles', help=self.arg_dict['profiles'])

        elif tool == 'sample':
            self.auth_args()
            self.sample_args()

        elif tool == 'search':
            self.auth_args()
            self.search_args()
            self.output_args()

        elif tool == 'reporter':
            reporter_group = self.parser.add_argument_group('Reporter parameters')
            reporter_group.add_argument('-o', required=False, action='store', dest='rPrint', default='txt', choices=['txt', 'csv'], help=self.arg_dict['rPrint'])
            if 'reportdir' in self.dot_robust:
                reporter_group.add_argument('-r', required=False, action='store', type=slash_dir, default=self.dot_robust['reportdir'], dest='reportdir', help=self.arg_dict['reportdir'])
            else:
                reporter_group.add_argument('-r', required=True, action='store', type=slash_dir, dest='reportdir', help=self.arg_dict['reportdir'])

        elif tool == 'watch' or tool == 'convict':
            self.auth_args()

            watch_group = self.parser.add_argument_group('Watch parameters')

            if tool == 'watch':
                watch_group.add_argument('-f', required=False, action='store_true', default=True, dest='follow', help=self.arg_dict['follow'])
            else:
                watch_group.add_argument('-f', required=False, action='store_true', dest='follow', help=self.arg_dict['follow'])

            watch_group.add_argument('-a', required=True, action='store', dest='analyzer_profile', help=self.arg_dict['analyzer'])
            watch_group.add_argument('-d', required=True, action='store', dest='directory', help=self.arg_dict['directory'])
            watch_group.add_argument('-e', required=False, action='store_true', dest='existing', help=self.arg_dict['existing'])
            # SUPPRESSION flag for hidden submission
            watch_group.add_argument('--sample', dest='file_to_upload', help=argparse.SUPPRESS)

            if tool == 'convict':
                convict_group = self.parser.add_argument_group('Convict parameters')
                if 'severity' in self.dot_robust:
                    convict_group.add_argument('-y', required=False, action='store', default=self.dot_robust['severity'], dest='severity', help=self.arg_dict['severity'])
                else:
                    convict_group.add_argument('-y', required=False, action='store', dest='severity', help=self.arg_dict['severity'])

                if 'cleandir' in self.dot_robust:
                    convict_group.add_argument('-c', required=False, action='store', type=slash_dir, default=self.dot_robust['cleandir'], dest='cleandir', help=self.arg_dict['cleandir'])
                else:
                    convict_group.add_argument('-c', required=True, action='store', type=slash_dir, dest='cleandir', help=self.arg_dict['cleandir'])

                if 'dirtydir' in self.dot_robust:
                    convict_group.add_argument('-x', required=False, action='store', type=slash_dir, default=self.dot_robust['dirtydir'], dest='dirtydir', help=self.arg_dict['dirtydir'])
                else:
                    convict_group.add_argument('-x', required=True, action='store', type=slash_dir, dest='dirtydir', help=self.arg_dict['dirtydir'])

                if 'reportdir' in self.dot_robust:
                    convict_group.add_argument('-r', required=False, action='store', type=slash_dir, default=self.dot_robust['reportdir'], dest='reportdir', help=self.arg_dict['reportdir'])
                else:
                    convict_group.add_argument('-r', required=True, action='store', type=slash_dir, dest='reportdir', help=self.arg_dict['reportdir'])

                if 'errordir' in self.dot_robust:
                    convict_group.add_argument('-z', required=False, action='store', type=slash_dir, default=self.dot_robust['errordir'], dest='errordir', help=self.arg_dict['errordir'])
                else:
                    convict_group.add_argument('-z', required=True, action='store', type=slash_dir, dest='errordir', help=self.arg_dict['errordir'])

                convict_group.add_argument('-t', required=False, action='store', dest='rType', choices=['html', 'txt', 'xml', 'zip', 'json', 'ioc', 'stix', 'pdf', 'sample'], help=self.arg_dict['rType'])

            if 'maxthreads' in self.dot_robust:
                watch_group.add_argument('-j', required=False, action='store', default=self.dot_robust['maxthreads'], dest='maxthreads', help=self.arg_dict['maxthreads'])
            else:
                watch_group.add_argument('-j', required=False, action='store', dest='maxthreads', help=self.arg_dict['maxthreads'])

        else:
            raise CliArgError(tool)

        self.common_args()
        if explicit is None:
            self.parser.parse_args(namespace=self)
        else:
            self.parser.parse_args(args=explicit, namespace=self)

    def config_section_map(self, config, section, defaults):
        dict1 = {}
        options = config.options(section)

        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                try:
                    dict1[option] = defaults[option]
                except:
                    print("exception on %s!" % option)
                    dict1[option] = None

        for k,v in defaults.iteritems():
            if not k in dict1:
                dict1[k] = v

        return dict1

    def dot_robust_helper(self):
        config = ConfigParser.ConfigParser({})
        fname = os.path.expanduser("~/.robust")

        auth_defaults = {'user': False, 'password': False}
        connection_defaults = {'ip': False, 'skipssl': False, 'maxthreads': 1}
        storage_defaults = {'severity': 3, 'cleandir': '~/robust/clean/', 'dirtydir': '~/robust/malware/', 'reportdir': '~/robust/reports/', 'errordir': '~/robust/errors/'}

        if os.path.isfile(fname):
            config.read(fname)
            if config.has_section("auth"):
                auth = self.config_section_map(config, "auth", auth_defaults)
                dot_robust_auth = {
                    'user': auth["user"],
                    'password':  auth["password"]
                }
            else:
                dot_robust_auth = auth_defaults

            if config.has_section("connection"):
                connection = self.config_section_map(config, "connection", connection_defaults)
                dot_robust_connection = {
                    'ip': connection["ip"],
                    'skipssl': connection["skipssl"],
                    'maxthreads': connection["maxthreads"]
                }
            else:
                dot_robust_connection = connection_defaults

            if config.has_section("storage"):
                storage = self.config_section_map(config, "storage", storage_defaults)
                dot_robust_storage = {
                    'severity': storage["severity"],
                    'cleandir': storage["cleandir"],
                    'dirtydir': storage["dirtydir"],
                    'reportdir': storage["reportdir"],
                    'errordir': storage["errordir"]
                }
            else:
                dot_robust_storage = storage_defaults

            dot_robust_dict = utils.merge_dicts(dot_robust_auth, dot_robust_connection, dot_robust_storage)
        else:
            dot_robust_dict = utils.merge_dicts(auth_defaults, connection_defaults, storage_defaults)
        return dot_robust_dict

    def common_args(self):
        self.parser.add_argument('--version', action='version', version=ratd.__version__)

        exclusive = self.parser.add_mutually_exclusive_group()
        exclusive.add_argument('-v', "--verbosity", action="count", help=self.arg_dict['verbosity'])
        exclusive.add_argument('-q', "--quiet", required=False, action='store_true', dest='quiet', help=self.arg_dict['quiet'])

    def auth_args(self):

        auth_group = self.parser.add_argument_group('Authentication parameters')

        if self.dot_robust['user']:
            auth_group.add_argument('-u', required=False, action='store', default=self.dot_robust['user'], dest='user', help=self.arg_dict['user'], metavar='USER')
        else:
            auth_group.add_argument('-u', required=True, action='store', dest='user', help=self.arg_dict['user'], metavar='USER')

        if self.dot_robust['password']:
            auth_group.add_argument('-p', required=False, action='store', default=self.dot_robust['password'], dest='password', help=self.arg_dict['password_secured'], metavar='PASSWORD')
        else:
            auth_group.add_argument('-p', required=False, action='store', dest='password', help=self.arg_dict['password'], metavar='PASSWORD')

        if self.dot_robust['ip']:
            auth_group.add_argument('-i', required=False, action='store', default=self.dot_robust['ip'], dest='ip', help=self.arg_dict['ip'], metavar='ATD IP')
        else:
            auth_group.add_argument('-i', required=True, action='store', dest='ip', help=self.arg_dict['ip'], metavar='ATD IP')

        if self.dot_robust['skipssl']:
            auth_group.add_argument('-n', required=False, action='store_true', default=self.dot_robust['skipssl'], dest='skipssl', help=self.arg_dict['skipssl'])
        else:
            auth_group.add_argument('-n', required=False, action='store_true', dest='skipssl', help=self.arg_dict['skipssl'])

    def sample_args(self):

        sample_group = self.parser.add_argument_group('Sample parameters')
        sample_group.add_argument('-s', required=True, action='store', dest='file_to_upload', help=self.arg_dict['sample'])
        sample_group.add_argument('-a', required=True, action='store', dest='analyzer_profile', help=self.arg_dict['analyzer'])

    def search_args(self):

        search_group = self.parser.add_argument_group('Search parameters')
        search_group.add_argument('-m', required=True, type=check_md5, action='store', dest='md5', help=self.arg_dict['md5'])

    def output_args(self):

        output_group = self.parser.add_argument_group('Reporting parameters')
        output_group.add_argument('-t', required=False, action='store', dest='rType', choices=['html', 'txt', 'xml', 'zip', 'json', 'ioc', 'stix', 'pdf', 'sample'], help=self.arg_dict['rType'])
        output_group.add_argument('-w', required=False, action='store', dest='filename', help=self.arg_dict['filename'])
