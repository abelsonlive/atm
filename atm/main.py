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
    else:
      self.is_s3 = False
      self.cache_dir = cache_dir
      
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
      content = self.s3.download(filepath)
    else:
      content = load_local(filepath, self.format)

    # if it doesen't exist, fetch the url and cache it.
    if content is None:
      response = requests.get(url)

      if response.status_code != 200:
        raise ATM_Error('RESPONSE RETURNED WITH STATUS CODE %d' % response.status_code)

      else:
        # fetch
        if self.format =="json":
          content = response.json()

        elif self.format =="txt":
          content = response.content

        # cache
        if self.is_s3:
          self.s3.upload(filepath, content)
          
        else:
          store_local(filepath, content, self.format)

    return content

  def receipts(self):
    if self.is_s3:
      filenames = []
      for k in self.s3.bucket.list(self.s3.cache_dir):
        filename = re.sub(self.s3.cache_dir, '', k.key)[1:]
        filenames.append(filename)
      return filenames
    else:
      return os.listdir(self.cache_dir)

  def _url_to_filepath(self, url, interval_string):
    """ Make a url into a file name, using SHA1 hashes. """

    # use a sha1 hash to convert the url into a unique filepath
    hash_file = "%s.%s" % (sha1(url).hexdigest(), self.format)
    if interval_string:
      hash_file = "%s-%s" % (interval_string, hash_file)
    if self.is_s3:
      return hash_file
    else:
      return os.path.join(self.cache_dir, hash_file)

  def _gen_interval_string(self):
    now = int(datetime.now().strftime("%s"))
    if self.interval:
      return str(now - (now % int(self.interval)))
    else:
      return None




