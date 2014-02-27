from datetime import datetime

def convert_to_epoch(dt):
  diff = (dt - datetime(1970, 1, 1))
  seconds = int(diff.total_seconds())
  return seconds