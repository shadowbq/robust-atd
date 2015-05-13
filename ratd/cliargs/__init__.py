import argparse
import ConfigParser
import os.path
import ratd

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
            'ip': '(i)p or hostname address of ATD\n\t\t(default: %(default)s) ',
            'sample': '(s)ample or file to be analyzed\n\t\t(default: %(default)s)',
            'skipssl': 'do (n)ot verify the SSL certificate for the communications\n\t\t(default: %(default)s)',
            'analyzer': '(a)nalyzer profile id to be used during analysis\n\t\t(default: %(default)s)',
            'profiles': '(l)ist analyzer profiles available\n\t\t(default: %(default)s)',
            'directory': '(d)irectory to watch for events\n\t\t(default: %(default)s)',
            'existing': '(e)xisting files in directory will be submitted\n\t\t(default: %(default)s)',
            'quiet': '(q)uiet all output\n\t\t(default: %(default)s)',
            'verbosity': 'increase output (v)erbosity\n\t\t(default: %(default)s)'
            }
        self.description = 'Robust Intel Security ATD Python CLI tool'
        self.epilog = ''
        self.dot_robust = self.dot_robust_helper()

        self.parser = argparse.ArgumentParser(epilog=self.epilog, description=self.description, formatter_class=argparse.RawTextHelpFormatter)

        if tool == 'profile':
            self.auth_args()
            profile_group = self.parser.add_argument_group('Profile parameters')
            profile_group.add_argument('-l', required=True, action='store_true', dest='listprofiles', help=self.arg_dict['profiles'])

        elif tool == 'sample':
            self.auth_args()
            self.sample_args()

        elif tool == 'watch':
            self.auth_args()

            watch_group = self.parser.add_argument_group('Watch parameters')
            watch_group.add_argument('-a', required=True, action='store', dest='analyzer_profile', help=self.arg_dict['analyzer'])
            watch_group.add_argument('-d', required=True, action='store', dest='directory', help=self.arg_dict['directory'])
            watch_group.add_argument('-e', required=False, action='store_true', dest='existing', help=self.arg_dict['existing'])
            # SUPPRESSION flag for hidden submission
            watch_group.add_argument('--sample', dest='file_to_upload', help=argparse.SUPPRESS)
        else:
            raise CliArgError(tool)

        self.common_args()
        if explicit is None:
            self.parser.parse_args(namespace=self)
        else:
            self.parser.parse_args(args=explicit, namespace=self)    

    def dot_robust_helper(self):
        config = ConfigParser.ConfigParser({'user': False, 'password': False, 'host': False, 'skipssl': False})
        fname = os.path.expanduser("~/.robust")
        if os.path.isfile(fname):
            config.read(fname)
            dot_robust_dict = {
            'user': config.get("auth", "user"),
            'password': config.get("auth", "password"),
            'host': config.get("auth", "host"),
            'skipssl': config.get("auth", "skipssl")
            }
        else:
            dot_robust_dict = {'user': False, 'password': False, 'host': False, 'skipssl': False}
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
            auth_group.add_argument('-p', required=False, action='store', default=self.dot_robust['password'], dest='password', help=self.arg_dict['password'], metavar='PASSWORD')
        else:
            auth_group.add_argument('-p', required=False, action='store', dest='password', help=self.arg_dict['password'], metavar='PASSWORD')

        if self.dot_robust['host']:
            auth_group.add_argument('-i', required=False, action='store', default=self.dot_robust['host'], dest='atd_ip', help=self.arg_dict['ip'], metavar='ATD IP')
        else:
            auth_group.add_argument('-i', required=True, action='store', dest='atd_ip', help=self.arg_dict['ip'], metavar='ATD IP')

        if self.dot_robust['skipssl']:
            auth_group.add_argument('-n', required=False, action='store_true', default=True, dest='skipssl', help=self.arg_dict['skipssl'])
        else:
            auth_group.add_argument('-n', required=False, action='store_true', dest='skipssl', help=self.arg_dict['skipssl'])

    def sample_args(self):

        sample_group = self.parser.add_argument_group('Sample parameters')
        sample_group.add_argument('-s', required=True, action='store', dest='file_to_upload', help=self.arg_dict['sample'])
        sample_group.add_argument('-a', required=True, action='store', dest='analyzer_profile', help=self.arg_dict['analyzer'])
