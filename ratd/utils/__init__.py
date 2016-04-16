def copyleftnotice():
    print '# Author - Shadowbq 2015 - www.github.com/shadowbq/robust-atd'
    print '# MIT LICENSE'
    print '# '
    print '# This is not a supported or official application of Intel Security.'
    print '# This work is based off of published documentation for integrating'
    print '# with the ATD REST API.'
    print '#'
    print '# A modified Fork of atdcli.py (Carlos Munoz - 2014) is included.'

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result    
