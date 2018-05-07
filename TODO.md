# ToDo List
List of things that have yet to be accomplished:

1. **Include Parsing of Registration Message** - your currently only parsing GPS messages
1. **Make More Pythonic** - Proper use of `if __name__ == '__main__':`.
1. **Support Muli-Page Output** - The query done by `rtkgetpl.py` could have multiple pages of data.
Need to implement functionality to support this.
1. **Text Table** - Replace your table creation method in `tkrdecoder.py`
Python's class to pretty-print tabular data in a terminal.
See [Texttable](https://pypi.org/project/texttable/),
[Simple formatted tables in python with Texttable module](https://oneau.wordpress.com/2010/05/30/simple-formatted-tables-in-python-with-texttable/), and
[Texttable Examples](https://programtalk.com/python-examples/texttable.Texttable/).
1. **JSON Encoding / Decoding** - Make proper use of JSON modules with Python.
Check out the following:
["JSON encoding and decoding with Python"](https://pythonspot.com/json-encoding-and-decoding-with-python/),
["How to use JSON with Python"](http://developer.rhino3d.com/guides/rhinopython/python-xml-json/),
and ["JSON.DUMP(S) & JSON.LOAD(S)"](http://www.bogotobogo.com/python/python-json-dumps-loads-file-read-write.php)
1. **Request to a RESTful API using Python** - Check out
["Requests: HTTP for Humans"](http://www.python-requests.org/en/master/)
1. **argparse --help** - Get the `--help` working properly
1. More robust methodology needs to be implemented for testing:
See [PYTHON TESTING 101: PYTEST](https://automationpanda.com/2017/03/14/python-testing-101-pytest/)
and [pytest](https://docs.pytest.org/en/latest/)
1. Make use of ThingsBoard
1. Make use of MapQuest APIs

# Done
These things have already been done:

1. **Use ISO Time Format** - Original implementation used Python's `datetime` object format for time input.
Change this to support the more familiar [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) time format.
