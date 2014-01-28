#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

def store_local(local_path, content, format):
  """ Save a local copy of the file. """
  # Save to disk.
  with open(local_path, 'wb') as f:

    if format == 'json':
      f.write(json.dumps(content))

    elif format=="txt":
      return f.write(content)


def load_local(local_path, format):
  """ Read a local copy of a url. """

  if not os.path.exists(local_path):
    return None

  with open(local_path, 'rb') as f:
    if format=='json':
      try:
        content = json.load(f)
      except ValueError:
        raise ValueError("JSON file is corrupted!")
      else:
        return content

    elif format=="txt":
      return f.read()
