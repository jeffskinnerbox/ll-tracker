#!/usr/bin/python3

'''-----------------------------------------------------------------------------
DESCRIPTION
    This module parses and decodes the payload delivered by the Link Labs
    GPS Tracker and places it in a Python dictionary object with the
    following form:

    { 'PayL': '10174D9BEBD1C13F1B0021FFE5', 'Msg Cnt': 4, 'Msg Type': 'GPS',
      'Lat': 39.0962155, 'Lon': -77.5864549, 'Alt': 33, 'Batt': 4.23,
      'Reserved': 'N/A' }

REFERENCE MATERIALS
    * https://stackoverflow.com/questions/6727875/hex-string-to-signed-int-in-python-3-2           # noqa
    * https://www.binaryhexconverter.com/hex-to-binary-converter
    * http://www.binaryconvert.com/convert_signed_int.html

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''

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

# mapping of hex characters to binary repensetation in ascii
hex2bin_map = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100',
               '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001',
               'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110',
               'F': '1111', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101',
               'e': '1110', 'f': '1111'}


def HextoBin(hexstring):
    '''Convert a hex encoded ascii string to a binary encoded ascii string.
    '''
    binarystring = ''.join(hex2bin_map[i] for i in hexstring)
    return binarystring


def BintoInt(binarystring):
    '''Convert binary encoded ascii string to integer data.
    '''
    return int(binarystring, 2)


def HextoInt(hexstring):
    '''Convert a hex encoded ascii string to integer data.
    '''
    return BintoInt(HextoBin(hexstring))


def HextoDec(hexstring):
    '''Convert a hex encoded ascii string to signed decimal data. This assumes
    that source is the proper length, and the sign bit is the first bit in the
    first byte of the correct length.
    For example: HextoDec('F') = -1 and HextoDec('0F') = 15
    '''
    if not isinstance(hexstring, str):
        raise ValueError('string type required')
    if len(hexstring) == 0:
        raise ValueError('string is empty')

    sign_bit_mask = 1 << (len(hexstring) * 4 - 1)
    other_bits_mask = sign_bit_mask - 1
    value = int(hexstring, 16)

    return -(value & sign_bit_mask) | (value & other_bits_mask)


def LatitudeChecker(lat):
    '''Check to validate latitude is in the proper range.
    '''
    if not -90 <= lat <= 90:
        return False, 'Error: Latitude value is not in range of +/-90.'

    return True, 'OK'


def LongitudeChecker(long):
    '''Check to validate longitude is in the proper range.
    '''
    if not -180 <= long <= 180:
        return False, 'Error: Longitude value is not in range of +/-180.'

    return True, 'OK'


def PayloadChecker(payload):
    '''Check the integrity of the payload for processing
    '''
    # check the character length of the payload
    if len(payload) != 14 and len(payload) != 26:
        return False, 'Error: Payload length is not equal to 14 or 26 characters long.'            # noqa

    # make sure only hexidcimal numbers are used
    chars = set('1234567890abcdefABCDEF')
    if not set(payload).issubset(chars):
        return False, 'Error: Payload has non-hex characters.'

    # check that you have a valid message type
    # last 2 bits of the hex formated single byte string gives you the message type                # noqa
    x = HextoBin(payload[0:2])
    if x[6:] != '00' and x[6:] != '01':
        return False, 'Error: Payload doesn\'t have the right message type.'

    # check the rolling message counter, range 0-63 (inclusive)
    x = HextoBin(payload[0:2])
    x = BintoInt(x[:6])
    if x < 0 or x > 63:
        return False, 'Error: Payload message count is out of range.'

    return True, 'OK'


def GPSPayloadParser(payload):
    '''Take a single GPS payload and parse it into its discrete components
    but still hex encoded.  These components, when decoded, will become
    the message count, message type, latitude, longitude, altitude,
    battery voltage, and a reserved string returned as a dictionary object.
    '''
    payloadparsed = {'PayL': payload, 'Byte_0': payload[0:2],
                     'Byte_1-4': payload[2:10], 'Byte_5-8': payload[10:18],
                     'Byte_9-10': payload[18:22], 'Byte_11-12': payload[22:]}

    return payloadparsed


def RegMessDecoder(payload):
    '''Take a single Registration type payload and parse it into a
    dictionary object with message count, message type, hardware ID,
    software version major, software version minor, software version tag,
    and battery voltage.
    '''
    # parse the payload into its elements
    payloadbinary = HextoBin(payload)

    # this is the orginal payload string encoded and unparsed
    payloaddecoded = {'PayL': payload}

    # first 6 bits of the first byte gives you the message count
    x = payloadbinary[:6]
    payloaddecoded.update({'Msg Cnt': BintoInt(x)})

    # last 2 bits of the first byte gives you the message type
    if payloadbinary[6:8] == '01':
        x = 'Reg'
    else:
        mess = 'Error: Wrong message type.  Should be \'Registration\''
        return False, mess, None
    payloaddecoded.update({'Msg Type': x})

    # bits 8 to 12 give hardware id
    x = payloadbinary[8:12]
    payloaddecoded.update({'Hardware ID': BintoInt(x)})

    # bits 12 to 20 give you software version major index
    x = payloadbinary[12:20]
    payloaddecoded.update({'Software Major': BintoInt(x)})

    # bits 20 to 28 give you software version minor index
    x = payloadbinary[20:28]
    payloaddecoded.update({'Software Minor': BintoInt(x)})

    # bits 20 to 44 give you software version tag index
    x = payloadbinary[28:44]
    payloaddecoded.update({'Software Tag': BintoInt(x)})

    # bits 44 to 54 give you battery voltage
    # This is a ADC reading for the battery voltage.  Convert the ADC reading
    # to unsigned integer use this formula: ( 13.1 * ADC ) / (3.1 * 1023)
    # maximum value will be  4.23V
    x = payloadbinary[44:54]
    x = BintoInt(x) * 13.1 / (3.1 * 1023)
    payloaddecoded.update({'Batt': round(x, 2)})

    # bits 54 to 56 give reserved field
    x = payloadbinary[54:56]
    payloaddecoded.update({'Reserved': 'N/A'})

    return True, 'OK', payloaddecoded


def GPSMessDecoder(payload):
    '''Take a single GPS type payload and parse it into a dictionary object
    with message count, message type, latitude, longitude, altitude,
    and battery voltage.
    '''
    # parse the payload into its elements
    payloadparsed = GPSPayloadParser(payload)

    # this is the original payload string encoded and unparsed
    payloaddecoded = {'PayL': payloadparsed['PayL']}

    # first 6 bits of the hex formated single byte string gives you the message count              # noqa
    x = HextoBin(payloadparsed['Byte_0'])
    x = x[:6]
    payloaddecoded.update({'Msg Cnt': BintoInt(x)})

    # last 2 bits of the hex formatted single byte string gives you the message type               # noqa
    x = HextoBin(payloadparsed['Byte_0'])
    if x[6:] == '00':
        x = 'GPS'
    else:
        return False, 'Error: Wrong message type.  Should be \'GPS\'', None
    payloaddecoded.update({'Msg Type': x})

    # from the hex formatted 4 byte string, convert it to a signed decimal
    # For Lat/Long, convert from hex to decimal and multiply by 1.0e-7.
    x = HextoDec(payloadparsed['Byte_1-4']) * 1.0E-7
    x = round(x, 7)
    rtn, mess = LatitudeChecker(x)
    if not rtn:
        return rtn, mess, payloaddecoded
    payloaddecoded.update({'Lat': x})

    # from the hex formatted 4 byte string, convert it to a signed decimal
    # For Lat/Long, convert from hex to decimal and multiply by 1.0e-7.
    x = HextoDec(payloadparsed['Byte_5-8']) * 1.0E-7
    x = round(x, 7)
    rtn, mess = LongitudeChecker(x)
    if not rtn:
        return rtn, mess, payloaddecoded
    payloaddecoded.update({'Lon': x})

    # from the hex formatted 2 byte string, convert it to a signed decimal
    payloaddecoded.update({'Alt': HextoDec(payloadparsed['Byte_9-10'])})

    # The first 10 bits of this hex formatted 2 byte string is a ADC reading
    # for the battery voltage.  Convert the ADC reading to unsigned integer
    # use this formula: ( 13.1 * ADC ) / (3.1 * 1023)
    # maximum value will be  4.23V
    x = HextoBin(payloadparsed['Byte_11-12'])
    x = x[:10]
    x = BintoInt(x) * 13.1 / (3.1 * 1023)
    payloaddecoded.update({'Batt': round(x, 2)})

    # the last 6 bits of this hex formatted 2 byte string isn't currently used
    x = HextoBin(payloadparsed['Byte_11-12'])
    x = x[10:]
    payloaddecoded.update({'Reserved': 'N/A'})

    return True, 'OK', payloaddecoded


def PayloadDecoder(payload):
    # check the integrity of the payload for processing
    rtn, mess = PayloadChecker(payload)
    if not rtn:
        return rtn, mess, None

    # last 2 bits of the hex formated single byte string gives you the message type                # noqa
    x = HextoBin(payload[0:2])
    if x[6:] == '00':
        rtn, mess, value = GPSMessDecoder(payload)
        return rtn, mess, value
    elif x[6:] == '01':
        rtn, mess, value = RegMessDecoder(payload)
        return rtn, mess, value
    else:
        return False, 'Error: Unknown message type.', None


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
# import pytest


# test cases for HextoBin, HextoInt, and BintoInt
CASE1 = [{'hex': '10', 'bin': '00010000', 'int': 16}]
CASE1.append({'hex': '4F5', 'bin': '010011110101', 'int': 1269})
CASE1.append({'hex': 'A37F', 'bin': '1010001101111111', 'int': 41855})
CASE1.append({'hex': 'c3a4c3b6c3bc',
              'bin': '110000111010010011000011101101101100001110111100',
              'int': 215112425587644})
CASE1.append({'hex': '3249CD52F37FF57D',
              'bin': '0011001001001001110011010101001011110011011111111111010101111101',           # noqa
              'int': 3623653131352536445})

# test cases for GPSPayloadParser and PayloadDecoder
CASE2 = [{'pl': '10174D9BEBD1C13F1B0021FFE5',
          'plp': {'PayL': '10174D9BEBD1C13F1B0021FFE5', 'Byte_0': '10',
                  'Byte_1-4': '174D9BEB', 'Byte_5-8': 'D1C13F1B',
                  'Byte_9-10': '0021', 'Byte_11-12': 'FFE5'},
          'pld': {'PayL': '10174D9BEBD1C13F1B0021FFE5', 'Msg Cnt': 4,
                  'Msg Type': 'GPS', 'Lat': 39.0962155,
                  'Lon': -77.5864549, 'Alt': 33, 'Batt': 4.23,
                  'Reserved': 'N/A'}}]
CASE2.append({'pl': '04174D918ED1C13B40007AFFE5',
              'plp': {'PayL': '04174D918ED1C13B40007AFFE5', 'Byte_0': '04',
                      'Byte_1-4': '174D918E', 'Byte_5-8': 'D1C13B40',
                      'Byte_9-10': '007A', 'Byte_11-12': 'FFE5'},
              'pld': {'PayL': '04174D918ED1C13B40007AFFE5', 'Msg Cnt': 1,
                      'Msg Type': 'GPS', 'Lat': 39.0959502, 'Lon': -77.5865536,
                      'Alt': 122, 'Batt': 4.23, 'Reserved': 'N/A'}})
CASE2.append({'pl': '14FFFFFFFFFFFFFFFFFFFF0025',
              'plp': {'PayL': '14FFFFFFFFFFFFFFFFFFFF0025', 'Byte_0': '14',
                      'Byte_1-4': 'FFFFFFFF', 'Byte_5-8': 'FFFFFFFF',
                      'Byte_9-10': 'FFFF', 'Byte_11-12': '0025'},
              'pld': {'PayL': '14FFFFFFFFFFFFFFFFFFFF0025', 'Msg Cnt': 5,
                      'Msg Type': 'GPS', 'Lat': -1e-07, 'Lon': -1e-07,
                      'Alt': -1, 'Batt': 0.0, 'Reserved': 'N/A'}})

# test cases for PayloadDecoder
CASE5 = [{'pl': '01101000001EC8',
          'pld': {"PayL": "01101000001EC8", "Msg Cnt": 0, "Msg Type": "Reg",
                  "Hardware ID": 1, "Software Major": 1, "Software Minor": 0,
                  "Software Tag": 1, "Batt": 3.91, "Reserved": "N/A"}}]
CASE5.append({'pl': '01101000001DB8',
              'pld': {"PayL": "01101000001DB8", "Msg Cnt": 0, "Msg Type": "Reg",
                      "Hardware ID": 1, "Software Major": 1, "Software Minor": 0,                  # noqa
                      "Software Tag": 1, "Batt": 3.63, "Reserved": "N/A"}})

# test cases for PayloadChecker
CASE3 = [{'challenge': '04174D8F17D1C139000067E9A5', 'response': True}]
CASE3.append({'challenge': '04174D8F17D1C13900z067E9A5', 'response': False})
CASE3.append({'challenge': '30174D8AECD1C13B18006FE5A5D', 'response': False})
CASE3.append({'challenge': '30174D8AECD1C13B18006FE5A', 'response': False})
CASE3.append({'challenge': '01101000001FFC', 'response': True})
CASE3.append({'challenge': '011010000001FFC', 'response': False})
CASE3.append({'challenge': '0110100001FFC', 'response': False})
CASE3.append({'challenge': '1234567890ABCD', 'response': False})
CASE3.append({'challenge': '', 'response': False})

# test cases for LatitudeChecker and LongitudeChecker
CASE4 =[{'lat': -3.45, 'lat-response': True, 'long': -3.45, 'long-response': True}]                # noqa
CASE4.append({'lat': 5.45, 'lat-response': True, 'long': 5.45, 'long-response': True})             # noqa
CASE4.append({'lat': 90, 'lat-response': True, 'long': 180, 'long-response': True})                # noqa
CASE4.append({'lat': -90, 'lat-response': True, 'long': -180, 'long-response': True})              # noqa
CASE4.append({'lat': 90.1, 'lat-response': False, 'long': 180.1, 'long-response': False})          # noqa
CASE4.append({'lat': -90.1, 'lat-response': False, 'long': -180.1, 'long-response': False})        # noqa


# execute all the unit tests below
def test_unit():
    test_HextoBin()
    test_BintoInt()
    test_HextoInt()
    test_LatLong()
    test_PayloadChecker()
    test_GPSPayloadParser()
    test_PayloadDecoder()


def test_PayloadChecker():
    for i in range(len(CASE3)):
        value, _ = PayloadChecker(CASE3[i]['challenge'])
        assert value == CASE3[i]['response']


def test_LatLong():
    for i in range(len(CASE4)):
        value, _ = LatitudeChecker(CASE4[i]['lat'])
        assert value == CASE4[i]['lat-response']
        value, _ = LongitudeChecker(CASE4[i]['long'])
        assert value == CASE4[i]['long-response']


def test_HextoBin():
    for i in range(len(CASE1)):
        value = HextoBin(CASE1[i]['hex'])
        assert value == CASE1[i]['bin']


def test_BintoInt():
    for i in range(len(CASE1)):
        value = BintoInt(CASE1[i]['bin'])
        assert value == CASE1[i]['int']


def test_HextoInt():
    for i in range(len(CASE1)):
        value = HextoInt(CASE1[i]['hex'])
        assert value == CASE1[i]['int']


def test_GPSPayloadParser():
    for i in range(len(CASE2)):
        value = GPSPayloadParser(CASE2[i]['pl'])
        assert value == CASE2[i]['plp']


def test_PayloadDecoder():
    for i in range(len(CASE2)):
        rtn, mess, value = PayloadDecoder(CASE2[i]['pl'])
        assert value == CASE2[i]['pld']

    for i in range(len(CASE5)):
        rtn, mess, value = PayloadDecoder(CASE5[i]['pl'])
        assert value == CASE5[i]['pld']


'''-----------------------------------------------------------------------------

DESCRIPTION
    This script decodes the payload delivered by the Link Labs GPS Tracker.

USAGE
    python3 tkrdecoder.py [--format table | json ] payload [ payload ... ]

REFERENCE MATERIALS
    * https://pymotw.com/3/argparse/

CREATED BY
    Jeff Irland (jeffrey.irland@verizon.com) in May 2018
-----------------------------------------------------------------------------'''
if __name__ == '__main__':
    # import the necessary packages
    import json
    import argparse

    # perform unit testing
    test_unit()

    # default delimiter for csv format
    DELIMITER = ','

    def LineArgumentParser():
        '''Construct the commandline argument parser, add the rules for the
        arguments, and then parse the arguments (found in sys.argv).
        '''
        # output format options
        list1 = ['table', 'json', 'csv']
        list2 = ['gps', 'reg', 'all']

        ap = argparse.ArgumentParser(
            prog=__prog__,
            formatter_class=argparse.RawTextHelpFormatter,
            description='This module parses and decodes the payload delivered by the Link Labs GPS Tracker\n'  # noqa
            + 'and places it in a JSON object with the following form:'
            + '\n\n'
            + '    { \'PayL\': \'10174D9BEBD1C13F1B0021FFE5\', \'Msg Cnt\': 4, \'Msg Type\': \'GPS\',\n'       # noqa
            + '      \'Lat\': 39.0962155, \'Lon\': -77.5864549, \'Alt\': 33, \'Batt\': 4.23,\n'                # noqa
            + '      \'Reserved\': \'N/A\' }',                                                                 # noqa
            epilog='Design details provided by the Link Labs team (www.link-labs.com).')                       # noqa

        ap.add_argument('-f', '--format',
                        required=False,
                        choices=list1,
                        default='json',
                        help='format of the output with allowed values of \'' +
                        '\', \''.join(list1) + '\'.',
                        metavar='')

        ap.add_argument('-m', '--message',
                        required=False,
                        choices=list2,
                        default='gps',
                        help='message types inthe output with allowed values of \'' +                  # noqa
                        '\', \''.join(list2) + '\'.',
                        metavar='')

        ap.add_argument('payload',
                        nargs='+',
                        help='payload(s) from the Link Labs Cat-M1 GPS Tracker')

        ap.add_argument('-d', '--delimiter',
                        required=False,
                        default=DELIMITER,
                        help='delimiter used in the csv format.')

        ap.add_argument('--version', action='version',
                        version='%(prog)s 0.3')

        return vars(ap.parse_args())

    def PrintHeader():
        print('\t\t' + '\t\tMessage' + '\tMessage' + '\t' + '\t' +
              '\t' + '\t\t\t  Battery' + '\t')
        print('Payload' + '\t\t\t\t Count' + '\t Type' + '\tLatitude' +
              '\tLongitude' + '\tAltitude' + '  Voltage' + '\tReserved')

    def PrintTable(parsedpayload):
        print(parsedpayload['PayL'], '\t   ', parsedpayload['Msg Cnt'], '\t  ',
              parsedpayload['Msg Type'], '\t', parsedpayload['Lat'], '\t',
              parsedpayload['Lon'], '\t  ', parsedpayload['Alt'], '\t   ',
              parsedpayload['Batt'], '\t\t  ', parsedpayload['Reserved'], sep='')                  # noqa

    def PrintCSV(parsedpayload):
        print(parsedpayload['PayL'], parsedpayload['Msg Cnt'],
              parsedpayload['Msg Type'], parsedpayload['Lat'],
              parsedpayload['Lon'], parsedpayload['Alt'],
              parsedpayload['Batt'], parsedpayload['Reserved'], sep=args['delimiter'])             # noqa

    # parse the commandline arguments
    args = LineArgumentParser()

    # if doing a table output, print the table headers
    if args['format'] == 'table':
        PrintHeader()

    # decode payloads from the commandline
    for pl in args['payload']:
        rtn, mess, decoded_payload = PayloadDecoder(pl)    # returns dictionary
        if not rtn:
            print(mess + '  Payload = ' + pl, file=sys.stderr)
            exit(1)

        # print a formated output of the payload strings
        if args['format'] == 'table':
            PrintTable(decoded_payload)                    # print table format
        elif args['format'] == 'csv':
            PrintCSV(decoded_payload)                      # print csv format
        else:
            print(json.dumps(decoded_payload))             # print json format
