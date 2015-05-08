import argparse
import ConfigParser
import os.path
import ratd

def arghelp():
    return {
            'user':'(u)sername for the API of the ATD\n\t\t(default: %(default)s)',
            'password':'(p)assword for username\n\t\t(default: %(default)s) ',
            'ip':'(i)p or hostname address of ATD\n\t\t(default: %(default)s) ',
            'sample':'(s)ample or file to be analyzed\n\t\t(default: %(default)s)',
            'skipssl':'do (n)ot verify the SSL certificate for the communications\n\t\t(default: %(default)s)',
            'analyzer':'(a)nalyzer profile id to be used during analysis\n\t\t(default: %(default)s)',
            'profiles':'(l)ist analyzer profiles available\n\t\t(default: %(default)s)',
            'verbose':'increase output verbosity\n\t\t(default: %(default)s)'
            }

def copyleftnotice():
    print '# Author - Shadowbq 2015 - www.github.com/shadowbq/robust'
    print '# MIT LICENSE'


def dot_robust_helper():
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

def robustcommonargs(parser):

    dot_robust  = dot_robust_helper()
    arg_dict    = arghelp()

    auth_group = parser.add_argument_group('Authentication parameters')

    if dot_robust['user']:
        auth_group.add_argument('-u', required=False, action='store', default=dot_robust['user'], dest='user', help=arg_dict['user'], metavar='USER')
    else:
        auth_group.add_argument('-u', required=True, action='store', dest='user', help=arg_dict['user'], metavar='USER')

    if dot_robust['password']:
        auth_group.add_argument('-p', required=False, action='store', default=dot_robust['password'], dest='password', help=arg_dict['password'], metavar='PASSWORD')
    else:
        auth_group.add_argument('-p', required=True, action='store', dest='password', help=arg_dict['password'], metavar='PASSWORD')

    if dot_robust['host']:
        auth_group.add_argument('-i', required=False, action='store', default=dot_robust['host'], dest='atd_ip', help=arg_dict['ip'], metavar='ATD IP')
    else:
        auth_group.add_argument('-i', required=True, action='store', dest='atd_ip', help=arg_dict['ip'], metavar='ATD IP')

    if dot_robust['skipssl']:
        auth_group.add_argument('-n', required=False, action='store_true', default=True, dest='skipssl', help=arg_dict['skipssl'])
    else:
        auth_group.add_argument('-n', required=False, action='store_true', dest='skipssl', help=arg_dict['skipssl'])

    return auth_group

def robustargs():
    description = 'Robust Intel Security ATD Python CLI tool'
    epilog      = 'Examples:\n\trobust.py -u admin -p admin -i 192.168.0.202 -s /usr/local/bin/file_to_scan -a 1'

    arg_dict    = arghelp()

    parser = argparse.ArgumentParser(epilog=epilog, description=description, formatter_class=argparse.RawTextHelpFormatter)

    robustcommonargs(parser)

    sample_group = parser.add_argument_group('Sample parameters')
    sample_group.add_argument('-s', required=True, action='store', dest='file_to_upload', help=arg_dict['sample'])
    sample_group.add_argument('-a', required=True, action='store', dest='analyzer_profile', help=arg_dict['analyzer'])

    parser.add_argument('-v', "--verbose", action="store_true", help=arg_dict['verbose'])
    parser.add_argument('--version', action='version', version=ratd.__version__)

    return parser.parse_args()

def profileargs():

    description = 'Robust Intel Security ATD Python CLI tool'
    epilog      = 'Examples:\n\trobust-profiles.py -u admin -p admin -i 192.168.0.202 -l'

    arg_dict    = arghelp()

    parser = argparse.ArgumentParser(epilog=epilog, description=description, formatter_class=argparse.RawTextHelpFormatter)

    auth_group = parser.add_argument_group('Authentication parameters')

    robustcommonargs(parser)

    profile_group = parser.add_argument_group('Profile parameters')
    profile_group.add_argument('-l', required=True, action='store_true', dest='listprofiles', help=arg_dict['profiles'])

    parser.add_argument('-v', "--verbose", action="store_true", help=arg_dict['verbose'])
    parser.add_argument('--version', action='version', version=ratd.__version__)

    return parser.parse_args()
