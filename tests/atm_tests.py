import unittest
from hashlib import sha1
import time
import shutil
import requests
import time

from atm import ATM 
from atm.s3 import is_s3_uri, parse_s3_uri

url = 'http://www.google.com'
url2 = 'http://www.nytimes.com'
local_cache_dir = 'cache-atm-tests-12345678910'
s3_cache_dir = 's3://atm-test-bucket/cache/'
s3_file = 'http://atm-test-bucket.s3.amazonaws.com/fixtures/foo.txt'
s3_bucket = "atm-test-bucket"
s3_path = "cache/"

class ATMTests(unittest.TestCase):


  def test_s3_get(self):
    teller = ATM(s3_cache_dir)

    s3_content = teller.get_cache(s3_file).content
    requests_content = requests.get(s3_file).content

    assert s3_content == requests_content

  def test_is_s3_uri(self):
    assert is_s3_uri(s3_cache_dir)

  def test_parse_s3_uri(self):
    bucket, path = parse_s3_uri(s3_cache_dir)
    assert bucket == s3_bucket and path == s3_path

  def test__url_to_filepath(self):

    filepath1 = local_cache_dir + '/' + sha1(url).hexdigest() + '.txt'
    teller = ATM(local_cache_dir)
    filepath2 = teller._url_to_filepath(url, interval_string=None)

    # remove cache directory
    shutil.rmtree(local_cache_dir)

    # test
    assert filepath1 == filepath2

  def test_local_liquidate(self):
    teller = ATM(local_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)

    files = [f for f in teller.liquidate()]

    # remove cache directory
    shutil.rmtree(local_cache_dir)

    assert len(files) == 2

  def test_local_statement(self):
    teller = ATM(local_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)

    # statement
    statement = teller.statement()

    # remove cache directory
    shutil.rmtree(local_cache_dir)

    assert len(statement) == 2 

  def test_local_default(self):
    teller = ATM(local_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)

    statement1 = teller.statement()

    # now delete
    teller.default()

    # statement again
    statement2 = teller.statement()

    # remove cache directory
    shutil.rmtree(local_cache_dir)

    assert len(statement1) == 2 and len(statement2) == 0

  def test_local_interval(self):
    teller = ATM(local_cache_dir, interval=10)

    r = teller.get_cache(url)
    r = teller.get_cache(url)

    time.sleep(10)

    r = teller.get_cache(url)

    statement = teller.statement()
    
    # remove cache directory
    shutil.rmtree(local_cache_dir)

    # test
    assert len(statement)==2

  def test_s3_liquidate(self):
    teller = ATM(s3_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)
    
    assets = [f for f in teller.liquidate()]

    # remove files
    teller.default()

    assert len(assets) == 2

  def test_s3_statement(self):
    teller = ATM(s3_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)

    # get statement
    statement = teller.statement()

    # remove files
    teller.default()

    assert len(statement) == 2 

  def test_s3_default(self):
    teller = ATM(s3_cache_dir)
    r = teller.get_cache(url)
    r = teller.get_cache(url2)

    statement1 = teller.statement()

    # now delete
    teller.default()

    # statement again
    statement2 = teller.statement()

    # remove files
    teller.default()

    assert len(statement1) == 2 and len(statement2) == 0

  def test_s3_interval(self):
    teller = ATM(s3_cache_dir, interval=10)
    
    # remove cache directory
    teller.default()

    r = teller.get_cache(url)
    r = teller.get_cache(url)

    time.sleep(10)

    r = teller.get_cache(url)

    statement = teller.statement()

    # remove cache directory
    teller.default()

    # test
    assert len(statement)==2

  def test_source(self):
    teller = ATM(s3_cache_dir, interval=10)

    r = teller.get_cache(url)
    source1 = r.source
    r = teller.get_cache(url)
    source2 = r.source

    teller.default()

    assert source1=="url" and source2=="cache"





