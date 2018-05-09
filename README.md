# Warning
These are very early version of the
the commandline tools `tkrdecoder.py` and `tkrgetpl.py`.
Also, you will need Link Labs credentials to [Conductor](https://conductor.link-labs.com/).

# tkrdecoder.py
Two types of payloads are produced by the tracker: GPS message and Registration message.

```bash
$ ./tkrdecoder.py --help
usage: tkrdecoder [-h] [-f] [--version] payload [payload ...]

This module parses and decodes the payload delivered by the Link Labs GPS Tracker
and places it in a JSON object with the following form:

    { 'PayL': '10174D9BEBD1C13F1B0021FFE5', 'Msg Cnt': 4, 'Msg Type': 'GPS',
      'Lat': 39.0962155, 'Lon': -77.5864549, 'Alt': 33, 'Batt': 4.23,
      'Reserved': 'N/A' }

positional arguments:
  payload         payload(s) from the Link Labs Cat-M1 GPS Tracker

optional arguments:
  -h, --help      show this help message and exit
  -f , --format   format of the output with allowed values of 'table', 'json'.
  --version       show program's version number and exit

Design details provided by the Link Labs team (www.link-labs.com).
```

## Usage Examples
```bash
$ ./tkrdecoder.py -f table 74174D8902D1C1359D0063DFA5 04174D918ED1C13B40007AFFE5 10174D9BEBD1C13F1B0021FFE5
			            	Message	Message						              Battery
Payload		        		 Count	 Type	Latitude	Longitude	Altitude  Voltage	Reserved
74174D8902D1C1359D0063DFA5	   29	  GPS	39.0957314	-77.5866979	  99	   3.69		  N/A
04174D918ED1C13B40007AFFE5	   1	  GPS	39.0959502	-77.5865536	  122	   4.23		  N/A
10174D9BEBD1C13F1B0021FFE5	   4	  GPS	39.0962155	-77.5864549	  33	   4.23		  N/A
```

```bash
$ ./tkrdecoder.py 74174D8902D1C1359D0063DFA5 04174D918ED1C13B40007AFFE5 10174D9BEBD1C13F1B0021FFE5
{"PayL": "74174D8902D1C1359D0063DFA5", "Msg Cnt": 29, "Msg Type": "GPS", "Lat": 39.0957314, "Lon": -77.5866979, "Alt": 99, "Batt": 3.69, "Reserved": "N/A"}
{"PayL": "04174D918ED1C13B40007AFFE5", "Msg Cnt": 1, "Msg Type": "GPS", "Lat": 39.0959502, "Lon": -77.5865536, "Alt": 122, "Batt": 4.23, "Reserved": "N/A"}
{"PayL": "10174D9BEBD1C13F1B0021FFE5", "Msg Cnt": 4, "Msg Type": "GPS", "Lat": 39.0962155, "Lon": -77.5864549, "Alt": 33, "Batt": 4.23, "Reserved": "N/A"}
```

```bash
$ ./tkrdecoder.py 74174D8902D1C1359D0063DFA5 04174D918ED1C13B40007AFFE5 10174D9BEBD1C13F1B0021FFE5 | jq -C
{
  "PayL": "74174D8902D1C1359D0063DFA5",
  "Msg Cnt": 29,
  "Msg Type": "GPS",
  "Lat": 39.0957314,
  "Lon": -77.5866979,
  "Alt": 99,
  "Batt": 3.69,
  "Reserved": "N/A"
}
{
  "PayL": "04174D918ED1C13B40007AFFE5",
  "Msg Cnt": 1,
  "Msg Type": "GPS",
  "Lat": 39.0959502,
  "Lon": -77.5865536,
  "Alt": 122,
  "Batt": 4.23,
  "Reserved": "N/A"
}
{
  "PayL": "10174D9BEBD1C13F1B0021FFE5",
  "Msg Cnt": 4,
  "Msg Type": "GPS",
  "Lat": 39.0962155,
  "Lon": -77.5864549,
  "Alt": 33,
  "Batt": 4.23,
  "Reserved": "N/A"
}
```

```bash
$ cat example.data
04174D8B40D1C13BBD0078FFE5
30174E6EBCD1C07F950021E5A5
2C174D514FD1C0BA230021E5A5
28174CF0CFD1C0C6B50021E5A5
24174CDD61D1C106E20021E5A5
20174CF87ED1C0C0E20021E6A5
1C174D50AFD1C0D5090021E725
18174D8E2AD1C10C42009AE6A5
0C174DC555D1C2247E0021E8A5
0C174DC555D1C2247E0021E8A5
04174D924DD1C155330021E925
98174D9532D1C139330073FFE5
94174D8B6FD1C13608006BDDA5
90174D8E2AD1C136B7006EDDA5
8C174D8D07D1C1355C006ADDA5
88174D89B6D1C136650077DDA5
7C174D8C96D1C136AA0064DFA5
78174D8CE7D1C136D80063DFA5
74174D8902D1C1359D0063DFA5
```

```bash
$ ./tkrdecoder.py $(cat example.data)
{"PayL": "04174D8B40D1C13BBD0078FFE5", "Msg Cnt": 1, "Msg Type": "GPS", "Lat": 39.0957888, "Lon": -77.5865411, "Alt": 120, "Batt": 4.23, "Reserved": "N/A"}
{"PayL": "30174E6EBCD1C07F950021E5A5", "Msg Cnt": 12, "Msg Type": "GPS", "Lat": 39.1016124, "Lon": -77.5913579, "Alt": 33, "Batt": 3.79, "Reserved": "N/A"}
{"PayL": "2C174D514FD1C0BA230021E5A5", "Msg Cnt": 11, "Msg Type": "GPS", "Lat": 39.0943055, "Lon": -77.5898589, "Alt": 33, "Batt": 3.79, "Reserved": "N/A"}
{"PayL": "28174CF0CFD1C0C6B50021E5A5", "Msg Cnt": 10, "Msg Type": "GPS", "Lat": 39.0918351, "Lon": -77.5895371, "Alt": 33, "Batt": 3.79, "Reserved": "N/A"}
{"PayL": "24174CDD61D1C106E20021E5A5", "Msg Cnt": 9, "Msg Type": "GPS", "Lat": 39.0913377, "Lon": -77.5878942, "Alt": 33, "Batt": 3.79, "Reserved": "N/A"}
{"PayL": "20174CF87ED1C0C0E20021E6A5", "Msg Cnt": 8, "Msg Type": "GPS", "Lat": 39.0920318, "Lon": -77.5896862, "Alt": 33, "Batt": 3.81, "Reserved": "N/A"}
{"PayL": "1C174D50AFD1C0D5090021E725", "Msg Cnt": 7, "Msg Type": "GPS", "Lat": 39.0942895, "Lon": -77.5891703, "Alt": 33, "Batt": 3.82, "Reserved": "N/A"}
{"PayL": "18174D8E2AD1C10C42009AE6A5", "Msg Cnt": 6, "Msg Type": "GPS", "Lat": 39.0958634, "Lon": -77.5877566, "Alt": 154, "Batt": 3.81, "Reserved": "N/A"}
{"PayL": "0C174DC555D1C2247E0021E8A5", "Msg Cnt": 3, "Msg Type": "GPS", "Lat": 39.0972757, "Lon": -77.5805826, "Alt": 33, "Batt": 3.84, "Reserved": "N/A"}
{"PayL": "0C174DC555D1C2247E0021E8A5", "Msg Cnt": 3, "Msg Type": "GPS", "Lat": 39.0972757, "Lon": -77.5805826, "Alt": 33, "Batt": 3.84, "Reserved": "N/A"}
{"PayL": "04174D924DD1C155330021E925", "Msg Cnt": 1, "Msg Type": "GPS", "Lat": 39.0959693, "Lon": -77.5858893, "Alt": 33, "Batt": 3.85, "Reserved": "N/A"}
{"PayL": "98174D9532D1C139330073FFE5", "Msg Cnt": 38, "Msg Type": "GPS", "Lat": 39.0960434, "Lon": -77.5866061, "Alt": 115, "Batt": 4.23, "Reserved": "N/A"}
{"PayL": "94174D8B6FD1C13608006BDDA5", "Msg Cnt": 37, "Msg Type": "GPS", "Lat": 39.0957935, "Lon": -77.5866872, "Alt": 107, "Batt": 3.66, "Reserved": "N/A"}
{"PayL": "90174D8E2AD1C136B7006EDDA5", "Msg Cnt": 36, "Msg Type": "GPS", "Lat": 39.0958634, "Lon": -77.5866697, "Alt": 110, "Batt": 3.66, "Reserved": "N/A"}
{"PayL": "8C174D8D07D1C1355C006ADDA5", "Msg Cnt": 35, "Msg Type": "GPS", "Lat": 39.0958343, "Lon": -77.5867044, "Alt": 106, "Batt": 3.66, "Reserved": "N/A"}
{"PayL": "88174D89B6D1C136650077DDA5", "Msg Cnt": 34, "Msg Type": "GPS", "Lat": 39.0957494, "Lon": -77.5866779, "Alt": 119, "Batt": 3.66, "Reserved": "N/A"}
{"PayL": "7C174D8C96D1C136AA0064DFA5", "Msg Cnt": 31, "Msg Type": "GPS", "Lat": 39.095823, "Lon": -77.586671, "Alt": 100, "Batt": 3.69, "Reserved": "N/A"}
{"PayL": "78174D8CE7D1C136D80063DFA5", "Msg Cnt": 30, "Msg Type": "GPS", "Lat": 39.0958311, "Lon": -77.5866664, "Alt": 99, "Batt": 3.69, "Reserved": "N/A"}
{"PayL": "74174D8902D1C1359D0063DFA5", "Msg Cnt": 29, "Msg Type": "GPS", "Lat": 39.0957314, "Lon": -77.5866979, "Alt": 99, "Batt": 3.69, "Reserved": "N/A"}
```

# tkrgetpl.py
Two types of payloads are produced by the tracker: GPS message and Registration message.

```bash
$ ./tkrgetpl.py --help
usage: tkrgetpl [-h] [-f] [-s START] [-S STOP] [-c CREDENTIALS] [--version]

This script queries for the Link Labs GPS Tracker data. This information is
stored on the Link Labs Conductor platform.

optional arguments:
  -h, --help            show this help message and exit
  -f , --format         format of the output with allowed values of
                        'unformatted', 'table', 'json'.
  -s START, --start START
                        start time for messages (default is 3 days prior to
                        now)
  -S STOP, --stop STOP  stop time for messages (default time is now)
  -c CREDENTIALS, --credentials CREDENTIALS
                        file where credentials are stored.
  --version             show program's version number and exit

Design details provided by the Link Labs team (www.link-labs.com).
```

## Credentials File
The `tkrgetpl.py` needs login/password to pull the payload data from Conductor.
The tool looks for these credentials within
`/home/jeff/src/ll-tracker` by default.
You can modify where to find the credentials via the command line option `--credentials` (aka `-c`).
The credential file `.credentials.json` takes the following form:

```json
{
    "device": {
        "model": "LL-LTE-M-VZN-GPS1",
        "serial-no": "563803918285313",
        "imei": "538292916738193",
        "iccid": "78246937469363869101"
    },
    "conductor": {
        "url": "https://conductor.link-labs.com/",
        "login": "my@email.com",
        "password": "first-password",
        "node-id": "0-0-0005732-4bc63f71e",
        "app-name": "Application",
        "app-token": "c34ef6cac38e4468cb30",
        "network-token": "3eb582f1"
        },
    "airfinder": {
        "url": "https://app.airfinder.com/customerwideadmin",
        "login": "my-other@email.com",
        "password": "second-password",
        "tag": "$303$0-0-000e453-1be56eb2f",
        "app-token": "c42z8e7372ca8362cd10"
    }
}
```

## Usage Examples
```bash
$ ./tkrgetpl.py -s 2018-04-01T00:00:00 -S 2018-05-08T00:00:00 -f json
data['resultCount'] = 108
data['moreRecordsExist'] = False
data['nextPageId'] = None
{"time": "2018-05-07T16:48:52.213", "PayL": "10174D8D96D1C133800087DAA5"}
{"time": "2018-05-07T16:42:30.798", "PayL": "0C174D8C87D1C13349008FDAA5"}
{"time": "2018-05-07T16:40:57.592", "PayL": "01101000001DB8"}
{"time": "2018-05-07T15:41:57.481", "PayL": "30174D8CA2D1C135730080E1A5"}
{"time": "2018-05-07T15:21:57.571", "PayL": "1C174D90FAD1C13203005AE3A5"}
{"time": "2018-05-07T15:10:38.031", "PayL": "10174D8CBFD1C13C6B0070E425"}
{"time": "2018-05-07T14:59:54.232", "PayL": "04174D8C13D1C13754007FE4A5"}
{"time": "2018-05-07T14:59:04.043", "PayL": "01101000001E50"}
{"time": "2018-05-07T14:50:48.584", "PayL": "20174D9041D1C13DB80076E5A5"}
{"time": "2018-05-07T14:37:21.983", "PayL": "10174D8E00D1C136290085E8A5"}
{"time": "2018-05-07T14:21:57.080", "PayL": "04174D8DF2D1C138FD0087E8A5"}
{"time": "2018-05-07T14:20:50.931", "PayL": "01101000001E78"}
{"time": "2018-05-07T14:09:46.920", "PayL": "01101000001FFC"}
{"time": "2018-05-07T14:09:17.145", "PayL": "04174DA11BD1C11D4B0021FFE5"}
{"time": "2018-05-07T14:08:21.571", "PayL": "01101000001FFC"}
{"time": "2018-05-03T17:36:29.556", "PayL": "01101000001E98"}
{"time": "2018-05-01T21:54:46.290", "PayL": "04174D8B40D1C13BBD0078FFE5"}
{"time": "2018-05-01T21:52:52.275", "PayL": "01101000001FFC"}
{"time": "2018-05-01T21:44:35.003", "PayL": "30174E6EBCD1C07F950021E5A5"}
  .
  .
  .
  .
```

# tkrstatus.py
Two types of payloads are produced by the tracker: GPS message and Registration message.
This command both queries Conductor for data and decodes the returned payload.

```bash
$ ./tkrstatus.py --help
usage: tkrstatus [-h] [-f] [-s START] [-S STOP] [-c CREDENTIALS] [--version]

This script queries for the Link Labs GPS Tracker data. This information is
stored on the Link Labs Conductor platform.

optional arguments:
  -h, --help            show this help message and exit
  -f , --format         format of the output with allowed values of
                        'unformatted', 'table', 'json'.
  -s START, --start START
                        start time for messages (default is 3 days prior to
                        now)
  -S STOP, --stop STOP  stop time for messages (default time is now)
  -c CREDENTIALS, --credentials CREDENTIALS
                        file where credentials are stored.
  --version             show program's version number and exit

Design details provided by the Link Labs team (www.link-labs.com).
```

## Usage Examples
```bash
$ ./tkrstatus.py -f json | grep GPS | jq -C '.'
{
  "Time": "2018-05-08T21:48:21.513",
  "PayL": "38174D900DD1C135D90072D0A5",
  "Msg Cnt": 14,
  "Msg Type": "GPS",
  "Lat": 39.0959117,
  "Lon": -77.5866919,
  "Alt": 114,
  "Batt": 3.45,
  "Reserved": "N/A"
}
{
  "Time": "2018-05-08T21:33:42.317",
  "PayL": "2C174D8C16D1C1368C0074D125",
  "Msg Cnt": 11,
  "Msg Type": "GPS",
  "Lat": 39.0958102,
  "Lon": -77.586674,
  "Alt": 116,
  "Batt": 3.45,
  "Reserved": "N/A"
}
{
  "Time": "2018-05-08T21:25:26.540",
  "PayL": "24174D929BD1C132110057D1A5",
  "Msg Cnt": 9,
  "Msg Type": "GPS",
  "Lat": 39.0959771,
  "Lon": -77.5867887,
  "Alt": 87,
  "Batt": 3.46,
  "Reserved": "N/A"
}
  .
  .
  .
  .
```
