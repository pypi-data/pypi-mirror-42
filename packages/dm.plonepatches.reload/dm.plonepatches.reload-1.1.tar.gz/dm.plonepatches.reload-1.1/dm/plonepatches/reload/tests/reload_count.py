"""Auxiliary module to count reloading."""
count = -1

def get_count():
  global count
  count += 1
  return count
