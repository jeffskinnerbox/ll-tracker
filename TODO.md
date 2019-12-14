# ToDo List
List of things that have yet to be accomplished:

1. **Make More Pythonic** - Proper use of `if __name__ == '__main__':`, use classes,
[magic methods](https://opensource.com/article/18/4/elegant-solutions-everyday-python-problems), etc.
1. **Support Muli-Page Output** - The query done by `rtkgetpl.py` could have multiple pages of data.
Need to implement functionality to support this.
1. **Text Table** - Replace your table creation method in `tkrdecoder.py`
Python's class to pretty-print tabular data in a terminal.
See [Texttable](https://pypi.org/project/texttable/),
[Simple formatted tables in python with Texttable module](https://oneau.wordpress.com/2010/05/30/simple-formatted-tables-in-python-with-texttable/), and
[Texttable Examples](https://programtalk.com/python-examples/texttable.Texttable/).
1. **Bring TextTable, JSON, and CSV all together** - The idea here is to support readable table, JSON, and CSV to support all types of usage.  Put all of this into a reusable object.
1. **JSON Encoding / Decoding** - Make proper use of JSON modules with Python.
Check out the following:
["JSON encoding and decoding with Python"](https://pythonspot.com/json-encoding-and-decoding-with-python/),
["How to use JSON with Python"](http://developer.rhino3d.com/guides/rhinopython/python-xml-json/),
and ["JSON.DUMP(S) & JSON.LOAD(S)"](http://www.bogotobogo.com/python/python-json-dumps-loads-file-read-write.php)
1. **Request to a RESTful API using Python** - Check out
["Requests: HTTP for Humans"](http://www.python-requests.org/en/master/)
1. **argparse --help** - Get the `--help` working properly and other such features.
[argparse — Command-Line Option and Argument Parsing](https://pymotw.com/3/argparse/)
1. More robust methodology needs to be implemented for testing:
See [pytest](https://docs.pytest.org/en/latest/),
[PYTHON TESTING 101: PYTEST](https://automationpanda.com/2017/03/14/python-testing-101-pytest/),
[Testing Python Applications with Pytest](https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest),
[PYTEST: CREATING AND USING FIXTURES FOR STREAMLINED TESTING](http://programeveryday.com/post/pytest-creating-and-using-fixtures-for-streamlined-testing/)
1. Consider including logging: [Python's Standard Logging Library](http://docs.python-guide.org/en/latest/writing/logging/), [Good logging practice in Python](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/), [Python logging best practices with JSON steroids](https://logmatic.io/blog/python-logging-with-json-steroids/)
1. **Geohasing and What3Words** - Make use of these encoding schemes to make it easier to work with the Lat / Lon data.
See [geohash.org](http://geohash.org/) and [What3Words](https://what3words.com/developers/)
1. **ThingsBoard** -Make use of ThingsBoard
1. **MapQuest** -Make use of MapQuest APIs
1. Make use of [How to work with dates and time with Python](https://opensource.com/article/17/5/understanding-datetime-python-primer)

# Done
These things have already been done:

1. **Use ISO Time Format** - Original implementation used Python's `datetime` object format for time input.
Change this to support the more familiar [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) time format.
1. **Include Parsing of Registration Message** - your currently only parsing GPS messages
1. **Combine tkrdecoder.py and tkrgetpl.py** Make these two program work together
in a single program (aka import tkrdecoder.py)
1. **Export to CSV File** - for the Bash script user, provide another format.

