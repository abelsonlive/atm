atm
====

`atm` is a simple wrapper for `requests.get()` that intelligently fetches data from the web and caches it locally or on s3. It's best used for web scraping projects where you want to avoid repeatedly requesting the source content.

Install
=======
```
pip install atm
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
Set up a cache on s3:
```python
from atm import ATM

# note, bucket must exist, 
# and you must have `AWS_ACCESS_KEY_ID` and 
# `AWS_ACCESS_KEY_SECRET` set as environmental variables.
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