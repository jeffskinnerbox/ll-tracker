# Warning
Very early version of the tool.
Only `tkrdecoder.py` is working right now.

# Usage Examples
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

# Credentials File
the credential file `.credentials.json` takes the following form:

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

# Testing Tools
* [PYTHON TESTING 101: PYTEST](https://automationpanda.com/2017/03/14/python-testing-101-pytest/)
* [pytest](https://docs.pytest.org/en/latest/)
