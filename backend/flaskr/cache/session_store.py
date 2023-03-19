import time

import redis


class SessionStore:
  cache = None

  def __init__(self, host, port) -> None:
    self.cache = redis.Redis(host=host, port=port)

  def get_hit_count(self):
    retries = 5
    while True:
      try:
        return self.cache.incr('hits')
      except redis.exceptions.ConnectionError as exc:
        if retries == 0:
          raise exc
        retries -= 1
        time.sleep(0.5)
