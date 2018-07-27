

import logging

from google.appengine.api import memcache
from google.appengine.api import urlfetch


class WebCache(object):

  data = None
  error = ""
  cached = True
  headers = {}
  length = 0

  def __init__ (self, url, timeout=3600):
    try :
      self.data = memcache.get(url)
      if self.data is None:
        self.cached = False
        request = urlfetch.fetch(url, method=urlfetch.GET, deadline=10, allow_truncated=False)
        self.headers = request.headers
        if request.status_code == 200 :
          self.data = request.content
          self.length = len(request.content)
          memcache.add(url, self.data, timeout)
        else :
          self.error = "status_code: %d" % request.status_code

    except Exception, e :
      logging.warn("WebCache.error: %s | %s" % (url, str(e)))
      self.error = str(e)

  def get(self):
    return self