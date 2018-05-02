#!/usr/bin/python2

'''--------------------------------------------------------------------------'''
'''
DESCRIPTION
    This script pulls from Link Labs Conductor platform payload information
    for the Link Labs GPS Tracker

USAGE
    python2 tkrgetpl.py         format table | json ] payload [ payload ... ]

REFERENCE MATERIALS
    * https://pymotw.com/3/argparse/
    * https://www.link-labs.com/documentation/software-downloads-conductor-downloads               # noqa

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
'''


import argparse
import conductor

'''
account = conductor.ConductorAccount('jeff.irland@verizon.net', '1@#Zippitydo2')
node = account.get_module('$303$0-0-0001450-2bf65e93d')

# list of all messages received from that node in the last 5000 minutes
messages = node.get_recent_messages(mins_back=60)
# messages = node.get_recent_messages(10)

# alternatively
# where start_time and stop_time are Python 'datetime.datetime' objects
# messages = node.get_messages_time_range(start_time, stop_time)
print(messages)

# parsed = json.loads(messages)
# print(json.dumps(parsed, indent=4, sort_keys=True))
'''


def GetCredentials():

    import json

    CREDPATH = '/home/jeff/src/link-labs-gps-tracker/.credentials.json'

    with open(CREDPATH) as json_data:
        cred = json.load(json_data)

    print("cred =", cred)
    print("cred['device'] =", cred['device'])
    print("cred['device']['imei'] =", cred['device']['imei'])

    return cred


def LineArgumentParser():
    '''Construct the commandline argument parser, add the rules for the
    arguments, and then parse the arguments (found in sys.argv).
    '''
    list = ['table', 'json']        # output format options

    ap = argparse.ArgumentParser(
        prog='tkrgetpl',
        description='This script parses the payload delivered by the \
        Link Labs GPS Tracker.',
        epilog='See XXX for additional information.')

    ap.add_argument('-f', '--format',
                    required=False,
                    choices=list,
                    default='table',
                    help='format of the output with allowed values of \'' +
                    '\', \''.join(list) + '\'.',
                    metavar='')

    ap.add_argument('payload',
                    nargs='+',
                    help='payload(s) from the Link Labs Cat-M1 GPS Tracker')

    ap.add_argument('--version', action='version',
                    version='%(prog)s 0.1')

    return vars(ap.parse_args())


if __name__ == '__main__':
    cred = GetCredentials()

    account = conductor.ConductorAccount(cred['conductor']['login'],
                                         cred['conductor']['password'])
    node = account.get_module(cred['node-address'])

    # list of all messages received from that node in the last 5000 minutes
    messages = node.get_recent_messages(mins_back=60)
    # messages = node.get_recent_messages(10)

    # alternatively
    # where start_time and stop_time are Python 'datetime.datetime' objects
    # messages = node.get_messages_time_range(start_time, stop_time)
    print(messages)

    # parsed = json.loads(messages)
    # print(json.dumps(parsed, indent=4, sort_keys=True))
