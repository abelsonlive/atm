atm
====

`atm` is a simple wrapper for `requests.get()` that intelligently fetches data from the web and caches it locally or on Amazon S3. It's best used for web scraping projects where you want to avoid repeatedly requesting the source content. The inspiration for library came from a [tutorial](https://github.com/pudo/hhba-scraping) that [@pudo](http://www.twitter.com/pudo) gave at the [2013 Buenos Aires Hacks/Hackers Media Party](http://www.mediaparty.info/).

[Read the docs](http://atm.readthedocs.org/en/latest/).

Install
=======
```
$ pip install atm
```

Tests
=======
```
$ nosetests tests
```

Usage
=======
Set up a local cache:
```python
from atm import ATM

teller = ATM('cache')
content = teller.get_cache('http://www.google.com/')

print teller.receipts()
```
Set up a cache on Amazon S3:

**Note**: The bucket must already exist and and you must have `AWS_ACCESS_KEY_ID` and  `AWS_ACCESS_KEY_SECRET` set as environmental variables.

Do this as follows:
```
$ export AWS_ACCESS_KEY_ID="myaccesskeyid"
$ export AWS_ACCESS_KEY_ID="myaccesskeysecret"
```

Now you're all set to cache results on S3:
```python
from atm import ATM

teller = ATM('s3://my-bucket/path/to/cache/')
content = teller.get_cache('http://www.google.com/')

print teller.receipts()
```
Set the file format as json (default = "txt"):
```python
from atm import ATM

teller = ATM('cache', format="json")
content = teller.get_cache('https://www.healthcare.gov/what-is-the-health-insurance-marketplace.json')

print teller.receipts()
```
Set an interval (in seconds) at which to update the cache.  This option should be used when regularly polling static urls which have dynamic content. 
```python
from atm import ATM
import time

teller = ATM('cache', interval=10)

content = teller.get_cache('http://www.google.com/')
content = teller.get_cache('http://www.google.com/')

time.sleep(10)

content = teller.get_cache('http://www.google.com/')

print teller.receipts()
```