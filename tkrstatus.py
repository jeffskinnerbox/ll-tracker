#!/usr/bin/python3

'''-----------------------------------------------------------------------------
DESCRIPTION
    This script pulls from Link Labs Conductor platform payload information
    for the Link Labs GPS Tracker

USAGE
    tkrstatus.py [ -c credentials ] [ -s start-time ] [ -f final-time ]

REFERENCE MATERIALS
    * https://pymotw.com/3/argparse/
    * https://www.link-labs.com/documentation/conductor-data-platform-user-guide#Client-Edge       # noqa
    * https://www.youtube.com/watch?v=eirjjyP2qcQ

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''
import json
import tkrgetpl
import tkrdecoder

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


if __name__ == '__main__':
    # import the necessary packages
    import argparse
    import datetime

    # path to where the credentials are stored
    CREDPATH = '/home/jeff/src/ll-tracker/.credentials.json'

    # default delimiter for csv format
    DELIMITER = ','

    def CheckArgument(args):
        if args['stop'] < args['start']:
            return False, 'Error: Start-time is after stop-time.'

        if args['start'] > datetime.datetime.now().isoformat():
            return False, 'Error: Start-time is set a time in the future.'

        rtn, mess = tkrgetpl.CheckTime(args['stop'])
        if not rtn:
            return rtn, mess

        rtn, mess = tkrgetpl.CheckTime(args['start'])
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
    rtn, mess, cred = tkrgetpl.ReadCredentials(args['credentials'])
    if not rtn:
        print(mess, file=sys.stderr)
        exit(1)

    # query conductor for data
    rtn, mess, r = tkrgetpl.QueryConductor(cred, args['start'], args['stop'])
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
            rtn, mess, decoded_payload = tkrdecoder.PayloadDecoder(data['results'][i]['value']['pld'])        # noqa
            data1 = {'Time': data['results'][i]['value']['startReceiveTime']}
            data1.update(decoded_payload)
            print(json.dumps(data1))
    elif args['format'] == 'table':
        # output select data and format it in a table
        for i in range(data['resultCount']):
            print(data['results'][i]['value']['startReceiveTime'], '\t',
                  data['results'][i]['value']['pld'])
    elif args['format'] == 'csv':
        # output select data and format it in a table
        for i in range(data['resultCount']):
            print(data['results'][i]['value']['startReceiveTime'] +
                  args['delimiter'] + data['results'][i]['value']['pld'])

    else:
        print('Error: Unsupported format requested.', file=sys.stderr)
        exit(1)
