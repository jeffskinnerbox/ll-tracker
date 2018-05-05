#!/usr/bin/python3

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
    * https://www.youtube.com/watch?v=eirjjyP2qcQ

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

    CREDPATH = '/home/jeff/src/ll-tracker/.credentials.json'

    with open(CREDPATH) as json_data:
        cred = json.load(json_data)

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
    import datetime

    cred = GetCredentials()

    account = conductor.ConductorAccount(cred['conductor']['login'],
                                         cred['conductor']['password'])
    node = account.get_module(cred['conductor']['node-address'])
    print("account =", account)
    print("node =", node)

    # start_time and stop_time are Python 'datetime.datetime' objects
    tdelta = datetime.timedelta(weeks=0, days=1, hours=0, minutes=0, seconds=0,
                                microseconds=0, milliseconds=0)
    stop_time = datetime.datetime.now()
    start_time = stop_time - tdelta
    # start_time = datetime.datetime.now()
    # stop_time = start_time - tdelta
    print("tdelta =", tdelta)
    print("stop_time =", stop_time)
    print("start_time =", start_time)

    # list of all messages received from that node in the last 5000 minutes
    # messages = node.get_recent_messages(mins_back=24*60)
    # print("messages =", messages)

    # pull a list of all uplink messages from a particular node
    # in the time interval between start_time and stop_time
    # messages = node.get_messages_time_range(start_time, stop_time)
    # print("messages =", messages)

    # alternatively
    # where start_time and stop_time are Python 'datetime.datetime' objects
    # messages = node.get_messages_time_range(start_time, stop_time)

    application = account.get_application_token(cred['conductor']['app-token'])
    print('application token =', cred['conductor']['app-token'])
    messages = application.get_messages_time_range(start_time, stop_time)
    print("messages =", messages)

    # parsed = json.loads(messages)
    # print(json.dumps(parsed, indent=4, sort_keys=True))
