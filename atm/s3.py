#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import boto
import boto.s3
from boto.s3.key import Key
import sys
import json
from urlparse import urlparse, urljoin

def is_s3_uri(uri):
  """Return True if *uri* can be parsed into an S3 URI, False otherwise."""
  try:
    parse_s3_uri(uri)
    return True
  except ValueError:
    return False

def parse_s3_uri(uri):
  """Parse an S3 URI into (bucket, key)

  >>> parse_s3_uri('s3://walrus/tmp/')
  ('walrus', 'tmp/')

  If ``uri`` is not an S3 URI, raise a ValueError
  """
  if not uri.endswith('/'):
    uri += '/'
    
  components = urlparse(uri)
  if (components.scheme not in ('s3', 's3n')
          or '/' not in components.path):
    raise ValueError('Invalid S3 URI: %s' % uri)

  return components.netloc, components.path[1:]

class S3(object):
  """ A class for connecting to a s3 bucket and uploading/downloading files"""
  def __init__(self, s3_uri):
      self.bucket_name, self.cache_dir = parse_s3_uri(s3_uri)
      self.bucket = self._connect_to_bucket(self.bucket_name)

  def _connect_to_bucket(self, bucket_name):
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    for i in conn.get_all_buckets():
      if bucket_name == i.name:
          return i

  def upload(self, filepath, data, format):
    k = Key(self.bucket)
    k.key = filepath
    if format == "txt":
      k.set_contents_from_string(data)
    elif format == "json":
      k.set_contents_from_string(json.dumps(data))

  def download(self, filepath, format):
    k = Key(self.bucket)
    k.key = filepath
    if k.exists():
      if format == "txt":
        return k.get_contents_as_string()
      elif format == "json":
        return json.loads(k.get_contents_as_string())
    else:
        return None

  def delete(self, filepath):
    k = Key(self.bucket)
    k.key = filepath
    self.bucket.delete_key(k)
