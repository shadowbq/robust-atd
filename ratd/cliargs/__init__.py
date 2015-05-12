import argparse
import ConfigParser
import os.path
import ratd

class cliargs():

    def __init__(self, tool):
        self.arg_dict = {
            'user':'(u)sername for the API of the ATD\n\t\t(default: %(default)s)',
            'password':'(p)assword for username\n\t\t(default: %(default)s) ',
            'ip':'(i)p or hostname address of ATD\n\t\t(default: %(default)s) ',
            'sample':'(s)ample or file to be analyzed\n\t\t(default: %(default)s)',
            'skipssl':'do (n)ot verify the SSL certificate for the communications\n\t\t(default: %(default)s)',
            'analyzer':'(a)nalyzer profile id to be used during analysis\n\t\t(default: %(default)s)',
            'profiles':'(l)ist analyzer profiles available\n\t\t(default: %(default)s)',
            'verbosity':'increase output verbosity\n\t\t(default: %(default)s)'
            }
        self.description = 'Robust Intel Security ATD Python CLI tool'
        self.epilog      = 'Examples:\n\trobust-profiles.py -u admin -p admin -i 192.168.0.202 -l'
        self.dot_robust = self.dot_robust_helper()

        self.parser = argparse.ArgumentParser(epilog=self.epilog, description=self.description, formatter_class=argparse.RawTextHelpFormatter)

        if tool == 'profile':
            self.auth_args()
            profile_group = self.parser.add_argument_group('Profile parameters')
            profile_group.add_argument('-l', required=True, action='store_true', dest='listprofiles', help=self.arg_dict['profiles'])

        if tool == 'sample':
            self.auth_args()
            self.sample_args()

        self.parser.add_argument('--version', action='version', version=ratd.__version__)
        self.parser.add_argument('-v', "--verbosity", action="count", help=self.arg_dict['verbosity'])

        self.parser.parse_args(namespace=self)

    def dot_robust_helper(self):
        config = ConfigParser.ConfigParser({'user': False, 'password': False, 'host': False, 'skipssl': False})
        fname = os.path.expanduser("~/.robust")
        if os.path.isfile(fname):
            config.read(fname)
            dot_robust_dict = {
            'user' : config.get("auth", "user"),
            'password' : config.get("auth", "password"),
            'host' : config.get("auth", "host"),
            'skipssl' : config.get("auth", "skipssl")
            }
        else:
            dot_robust_dict = {'user': False, 'password': False, 'host': False, 'skipssl': False}
        return dot_robust_dict

    def auth_args(self):

        auth_group = self.parser.add_argument_group('Authentication parameters')

        if self.dot_robust['user']:
            auth_group.add_argument('-u', required=False, action='store', default=self.dot_robust['user'], dest='user', help=self.arg_dict['user'], metavar='USER')
        else:
            auth_group.add_argument('-u', required=True, action='store', dest='user', help=self.arg_dict['user'], metavar='USER')

        if self.dot_robust['password']:
            auth_group.add_argument('-p', required=False, action='store', default=self.dot_robust['password'], dest='password', help=self.arg_dict['password'], metavar='PASSWORD')
        else:
            auth_group.add_argument('-p', required=True, action='store', dest='password', help=self.arg_dict['password'], metavar='PASSWORD')

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
