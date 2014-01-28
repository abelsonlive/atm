import unittest
from hashlib import sha1
import time
import shutil
import requests

from atm import ATM 
from atm.s3 import is_s3_uri, parse_s3_uri


class ATMTests(unittest.TestCase):

  def test_interval(self):
    cache_dir = 'cache-atm-tests-12345678910'
    teller = ATM(cache_dir, interval=10)

    content = teller.get_cache('http://www.google.com/')
    content = teller.get_cache('http://www.google.com/')

    time.sleep(10)

    content = teller.get_cache('http://www.google.com/')

    files = teller.receipts()
    
    # remove cache directory
    shutil.rmtree(cache_dir)

    # test
    assert len(files)==2

  def test_s3(self):
    teller = ATM('s3://atm-test-bucket/cache/')

    s3_content = teller.get_cache('http://atm-test-bucket.s3.amazonaws.com/fixtures/foo.txt')
    requests_content = requests.get('http://atm-test-bucket.s3.amazonaws.com/fixtures/foo.txt').content

    assert s3_content == requests_content

  def test_is_s3_uri(self):
    assert is_s3_uri('s3://atm-test-bucket/cache/')

  def test_parse_s3_uri(self):
    bucket, path = parse_s3_uri('s3://atm-test-bucket/cache/')
    assert bucket == "atm-test-bucket" and path == "cache/"

  def test__url_to_filepath(self):
    url = 'http://www.google.com'
    cache_dir = 'cache-atm-tests-12345678910'

    filepath1 = cache_dir + '/' + sha1(url).hexdigest() + '.txt'

    teller = ATM(cache_dir)
    filepath2 = teller._url_to_filepath(url, interval_string=None)

    # remove cache directory
    shutil.rmtree(cache_dir)

    # test
    assert filepath1 == filepath2