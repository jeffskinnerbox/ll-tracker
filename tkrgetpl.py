#!/usr/bin/python3

'''-----------------------------------------------------------------------------
DESCRIPTION
    This script pulls from Link Labs Conductor platform payload information
    for the Link Labs GPS Tracker

USAGE
    tkrgetpl.py [ -c credentials ] [ -s start-time ] [ -f final-time ]

REFERENCE MATERIALS
    * https://pymotw.com/3/argparse/
    * https://www.link-labs.com/documentation/conductor-data-platform-user-guide#Client-Edge       # noqa
    * https://www.youtube.com/watch?v=eirjjyP2qcQ
    * https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285  # noqa

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''

import re
import json
import requests

# authorship information
__prog__ = 'mongoin'
__version__ = '0.1'
__status__ = 'Development'
__author__ = 'Jeff Irland'
__maintainer__ = 'Jeff Irland'
__email__ = 'jeffskinnerbox@yahoo.com'
__credits__ = ''
__copyright__ = 'Copyright 2018'
__license__ = 'GNU General Public License'
__python__ = 'Version 3.6.3'


# regular expression for ISO8601 format validation
# (only for combined date & time in UTC ISO 8601 time format standard)
regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'    # noqa
match_iso8601 = re.compile(regex).match


def ReadCredentials(filename):
    '''Read in the credentials for Link Labs Conductor platform and
    place them in a dictionary object
    '''
    if filename:
        with open(filename, 'r') as json_data:
            cred = json.load(json_data)
    else:
        return False, 'Error: Credentials file doesn\'t exist.', None

    return True, 'OK', cred


def QueryConductor(cred, start, stop):
    '''Query Conductor for data.'''
    r = requests.get(cred['conductor']['clientedgebase'] +
                     '/data/uplinkPayload/node/' +
                     cred['conductor']['node-address'] +
                     '/events/' + stop + '/' + start,
                     auth=(cred['conductor']['login'],
                           cred['conductor']['password']))
    if r.status_code == 200:
        return True, 'OK', r
    else:
        return False, 'Error: Conductor query not successful.', r


def CheckTime(time):
    '''Validate that the string conforms to the combined date & time
    in UTC ISO 8601 time format standard.
    '''
    try:
        if match_iso8601(time) is not None:
            return True, 'OK'
    except:
        pass

    return False, 'Error: Time string doesn\'t conform to ISO 8601 format.'


'''-----------------------------------------------------------------------------
DESCRIPTION
    This module provides unit test routines for the Link Labs GPS Tracker
    parsing & decoding module.

REFERENCE MATERIALS
    pytest framework - https://docs.pytest.org/

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''
# import the necessary packages


# test cases for CheckTime (week number and ordinal date not supported)
CASE1 = [{'challenge': '2017-01-01', 'response': False}]
CASE1.append({'challenge': '2028-11-23T', 'response': False})
CASE1.append({'challenge': '2018-05-01T00:00:00', 'response': True})
CASE1.append({'challenge': '2018-05-01:00:00:00', 'response': False})
CASE1.append({'challenge': '2008-08-30T01:45:36.123Z', 'response': True})
CASE1.append({'challenge': '2016-12-13T21:20:37.593194+00:00', 'response': True})                  # noqa
CASE1.append({'challenge': '2018-05-06T12:53:22+00:00', 'response': True})
CASE1.append({'challenge': '2018-05-06T12:53:22Z', 'response': True})
CASE1.append({'challenge': '20180506T125322Z', 'response': False})
CASE1.append({'challenge': '2018-W18', 'response': False})
CASE1.append({'challenge': '2018-W18-7', 'response': False})
CASE1.append({'challenge': '2018-126', 'response': False})


# execute all the unit tests below
def test_unit(credpath):
    _, _, cred = test_ReadCredentials(credpath)
    test_QueryConductor(cred)
    test_CheckTime()


def test_CheckTime():
    for i in range(len(CASE1)):
        value, _ = CheckTime(CASE1[i]['challenge'])
        assert value == CASE1[i]['response']


def test_ReadCredentials(path_to_file):
    rtn, mess, value = ReadCredentials(path_to_file)
    assert rtn == True                                                                             # noqa
    assert mess == 'OK'
    assert value['device']['serial-no'] == '357353080088893'
    return rtn, mess, value


def test_QueryConductor(cred):
    tdelta = datetime.timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=0,
                                microseconds=0, milliseconds=0)
    stop = datetime.datetime.now()
    start = stop - tdelta
    rtn, mess, value = QueryConductor(cred, start.isoformat(), stop.isoformat())
    assert rtn == True                                                                             # noqa
    assert mess == 'OK'
    assert value.status_code == 200
    assert value.encoding == 'UTF-8'
    assert value.encoding == 'UTF-8'
    assert value.headers['content-type'] == 'application/json;charset=UTF-8'


'''-----------------------------------------------------------------------------
DESCRIPTION
    This script decodes the payload delivered by the Link Labs GPS Tracker.

USAGE
    python3 tkrdecoder.py [--format table | json ] payload [ payload ... ]

REFERENCE MATERIALS
    * https://pymotw.com/3/argparse/
    * https://stackoverflow.com/questions/41129921/validate-an-iso-8601-datetime-string-in-python  # noqa

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''
if __name__ == '__main__':
    # import the necessary packages
    import argparse
    import datetime

    # default path to where the credentials are stored
    CREDPATH = '/home/jeff/src/ll-tracker/.credentials.json'

    # default delimiter for csv format
    DELIMITER = ','

    # perform unit testing
    test_unit(CREDPATH)

    def CheckArgument(args):
        if args['stop'] < args['start']:
            return False, 'Error: Start-time is after stop-time.'

        if args['start'] > datetime.datetime.now().isoformat():
            return False, 'Error: Start-time is set a time in the future.'

        rtn, mess = CheckTime(args['stop'])
        if not rtn:
            return rtn, mess

        rtn, mess = CheckTime(args['start'])
        if not rtn:
            return rtn, mess

        return True, 'OK'

    def LineArgumentParser():
        '''Construct the commandline argument parser, add the rules for the
        arguments, and then parse the arguments (found in sys.argv).
        '''
        # default start and stop time for conductor query
        tdelta = datetime.timedelta(weeks=0, days=3, hours=0, minutes=0, seconds=0,                 # noqa
                                    microseconds=0, milliseconds=0)
        stop_time = datetime.datetime.now()
        start_time = stop_time - tdelta

        # output format options
        list = ['unformatted', 'table', 'json', 'csv']

        ap = argparse.ArgumentParser(
            prog=__prog__,
            description='This script queries for the Link Labs GPS Tracker data. \
            This information is stored on the Link Labs Conductor platform.',
            epilog='Design details provided by the Link Labs team (www.link-labs.com).')           # noqa

        ap.add_argument('-f', '--format',
                        required=False,
                        choices=list,
                        default='unformatted',
                        help='format of the output with allowed values of \'' +
                        '\', \''.join(list) + '\'.',
                        metavar='')

        ap.add_argument('-s', '--start',
                        required=False,
                        default=start_time.isoformat(),
                        help='start time for messages (default is 3 days prior to now)')           # noqa

        ap.add_argument('-S', '--stop',
                        required=False,
                        default=stop_time.isoformat(),
                        help='stop time for messages (default time is now)')

        ap.add_argument('-d', '--delimiter',
                        required=False,
                        default=DELIMITER,
                        help='delimiter used in the csv format.')

        ap.add_argument('-c', '--credentials',
                        required=False,
                        default=CREDPATH,
                        help='file where credentials are stored.')

        ap.add_argument('--version', action='version',
                        version='%(prog)s 0.3')

        # check the arguments passed for validity
        args = vars(ap.parse_args())
        rtn, mess = CheckArgument(args)
        if not rtn:
            print(mess, file=sys.stderr)
            exit(1)

        return args

    # parse the commandline arguments
    args = LineArgumentParser()

    # read the file containing your credentials for Conductor
    rtn, mess, cred = ReadCredentials(args['credentials'])
    if not rtn:
        print(mess, file=sys.stderr)
        exit(1)

    # query conductor for data
    rtn, mess, r = QueryConductor(cred, args['start'], args['stop'])
    if not rtn:
        print(mess + '  HTTP status codes = ' + str(r.status_code))
        print(r.text, file=sys.stderr)
        exit(1)

    # format the recieved json text as a python list object
    data = json.loads(r.text)

    # for debugging ... remove later
    print("data['resultCount'] =", data['resultCount'])
    print("data['moreRecordsExist'] =", data['moreRecordsExist'])
    print("data['nextPageId'] =", data['nextPageId'])

    # format the information sent by conductior
    if args['format'] == 'unformatted':
        # output all the data sent from conductor, unformated (it's in json)
        print(r.text)
    elif args['format'] == 'json':
        # output select data and format as json objects
        for i in range(data['resultCount']):
            print(json.dumps({'time': data['results'][i]['value']['startReceiveTime'],             # noqa
                              'PayL': data['results'][i]['value']['pld']}))
    elif args['format'] == 'csv':
        # output select data and format as comma separated values (csv)
        for i in range(data['resultCount']):
            print(data['results'][i]['value']['startReceiveTime']
                  + args['delimiter'] + data['results'][i]['value']['pld'])
    elif args['format'] == 'table':
        # output select data and format it in a table
        for i in range(data['resultCount']):
            print(data['results'][i]['value']['startReceiveTime'], '\t',
                  data['results'][i]['value']['pld'])
    else:
        print('Error: Unsupported format requested.', file=sys.stderr)
        exit(1)

