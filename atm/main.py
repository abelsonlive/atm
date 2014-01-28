#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from urlparse import urljoin
import os, re
from hashlib import sha1
import json
from s3 import is_s3_uri, S3

from local import load_local, store_local
from datetime import datetime


class ATM_Response(object):
  """a return object for ATM.get_cache"""
  def __init__(self, content,  url, filepath, cache_dir, bucket_name, is_s3, status_code, source, timestamp):
    self.content = content
    self.url = url
    self.filepath = filepath
    self.cache_dir = cache_dir
    self.bucket_name =  bucket_name
    self.is_s3 = is_s3
    self.status_code = status_code
    self.source = source
    self.timestamp = timestamp

class ATM_Error(Exception):
  pass

class ATM(object):
  """
  A class for intelligently caching / retrieving data fetched from urls
  """
  def __init__(self, cache_dir, format="txt", interval = None):
    
    # determine s3 / local
    if is_s3_uri(cache_dir):
      self.is_s3 = True
      self.s3 = S3(cache_dir)
      self.cache_dir = self.s3.cache_dir
      self.bucket_name = self.s3.bucket_name

    else:
      self.is_s3 = False
      self.cache_dir = cache_dir
      self.bucket_name = None
      
      # If the cache directory does not exist, make one.
      if not os.path.isdir(self.cache_dir):
        os.makedirs(self.cache_dir)

    self.format = format.lower()
    self.interval = interval

  def get_cache(self, url):
    """ Wrap requests.get() """
    # create a filepath
    interval_string = self._gen_interval_string()
    filepath = self._url_to_filepath(url, interval_string)

    # get cached content
    if self.is_s3:
      content = self.s3.download(filepath, self.format)

    else:
      content = load_local(filepath, self.format)

    # if it doesen't exist, fetch the url and cache it.
    if content is None:
      response = requests.get(url)

      status_code = response.status_code
      
      if response.status_code != 200:
        content = None
         
      else:
        # fetch
        if self.format =="json":
          content = response.json()

        elif self.format =="txt":
          content = response.content

        # cache
        if self.is_s3:
          self.s3.upload(filepath, content, self.format)
          
        else:
          store_local(filepath, content, self.format)

    else:

      status_code = None

    return ATM_Response(
      content = content,
      url = url,
      filepath = filepath,
      cache_dir = self.cache_dir,
      bucket_name = self.bucket_name,
      is_s3 = self.is_s3,
      status_code = status_code,
      source = "cache" if status_code is None else "url",
      timestamp = int(interval_string) if interval_string else None
    ) 

  def liquidate(self):
    """ Retrieve all files from the cache. Returns a generator"""
    if self.is_s3:
      for filepath in self.statement():
        yield self.s3.download(filepath, self.format)
    else:
      for filepath in self.statement():
        yield load_local(filepath, self.format)

  def default(self):
    """ Delete all files from the cache"""
    if self.is_s3:
      for filepath in self.statement():
        self.s3.delete(filepath)
    else:
      for filepath in self.statement():
        os.remove(filepath)

  def statement(self):
    """ List all files in the cache """
    if self.is_s3:
        return [k.key for k in self.s3.bucket.list(self.cache_dir)]
    else:
      return [os.path.join(self.cache_dir, f) for f in os.listdir(self.cache_dir)]

  def _url_to_filepath(self, url, interval_string):
    """ Make a url into a file name, using SHA1 hashes. """

    # use a sha1 hash to convert the url into a unique filepath
    hash_file = "%s.%s" % (sha1(url).hexdigest(), self.format)
    if interval_string:
      hash_file = "%s-%s" % (interval_string, hash_file)

    return os.path.join(self.cache_dir, hash_file)

  def _gen_interval_string(self):
    """Generate a timestamp string that will be used to update the cache at a set interval"""
    now = int(datetime.now().strftime("%s"))
    if self.interval:
      return str(now - (now % int(self.interval)))
    else:
      return None




