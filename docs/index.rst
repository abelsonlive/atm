.. particle documentation master file, created by
   sphinx-quickstart on Wed Dec 25 21:19:20 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**atm**: Get/Cache
========


**atm** is a simple wrapper for ``requests.get()`` that intelligently fetches data from the web and caches it locally or on Amazon S3. It's best used for web scraping projects in which you want to avoid repeatedly requesting the source content.

Installation
----------

Install **atm** via ``pip``::

  $ pip install atm

Tests
-------
Test package with ``nosetests``::

  $ nosetests tests

Usage
-------
Set up a local cache::

  from atm import ATM

  teller = ATM('cache')
  r = teller.get_cache('http://www.google.com/')

  print teller.statement()

Set up a cache on Amazon S3:

**Note**: The bucket must already exist and and you must have ``AWS_ACCESS_KEY_ID`` and  ``AWS_ACCESS_KEY_SECRET`` set as environmental variables.

Do this as follows::
  
  $ export AWS_ACCESS_KEY_ID="myaccesskeyid"
  $ export AWS_ACCESS_KEY_ID="myaccesskeysecret"

Now you're all set to cache results on S3::

  from atm import ATM

  teller = ATM('s3://my-bucket/path/to/cache/')
  r = teller.get_cache('http://www.google.com/')

  print teller.statement()

Set the file format as json (default = "txt")::

  from atm import ATM

  teller = ATM('cache', format="json")
  r = teller.get_cache('https://www.healthcare.gov/what-is-the-health-insurance-marketplace.json')

  print teller.statement()

Set an interval (in seconds) at which to update the cache.  This option should be used when regularly polling static urls which have dynamic content::

  from atm import ATM
  import time

  teller = ATM('cache', interval=10)

  r = teller.get_cache('http://www.google.com/')
  r = teller.get_cache('http://www.google.com/')

  time.sleep(10)

  r = teller.get_cache('http://www.google.com/')

  print teller.statement()

Response Format
---------------
``ATM.get_cache()`` returns an object with the following attributes:

  * ``r.content``: The content returned from the url or the cache.
  * ``r.url``: The url of the content requested.
  * ``r.filepath``: The filepath of cache'd content.
  * ``r.cache_dir``: The directory of the cache'd content.
  * ``r.bucket_name``: The bucket name of this cache if the cache is located on S3.
  * ``r.is_s3``: A boolean indicating whether the cache is located on S3.
  * ``r.status_code``: The status code from ``reqeusts.get()`` if the content was not retrieved from the cache.
  * ``r.source``: The source of the content, either ``url`` or ``cache``.
  * ``r.timestamp``: The bucketed timestamp of the request if an ``interval`` is specified when intializing ``ATM``.

Convenience Methods
-------------------
**atm** also comes with some convenience methods for working with cache'd content.

``ATM.transaction(url, timestamp=None)`` returns the filepath in the cache for a url. If `ATM` has been initialized with a set `interval`, you can use the `timestamp` arg to look up the file in the cache associated with that timestamp.

``ATM.withdraw(filepath)`` returns the contents of a file in the cache, given it's filepath.

``ATM.liquidate()`` returns a generator of the contents located in the cache.

``ATM.statement()`` returns a list of filepaths in the cache.

``ATM.default()`` deletes all files from the cache.