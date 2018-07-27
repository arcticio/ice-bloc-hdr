

import os
import logging
import webapp2

import aio

import config ## DEBUG

from datetime import datetime, timedelta

from google.appengine.api import memcache
from google.appengine.api import urlfetch

from utils.clock import Clock

KEEPMONTH = 60*60*24*30 ## 30 days
KEEPDAY   = 60*60*24    ##  1 day
KEEPHOUR  = 60*60       ##  1 hour
KEEPNOT   = 0           ##  redirect

class Cache(webapp2.RequestHandler) :


  def fetch(self, url, timeout) :

    try :

      data = memcache.get(url)

      if data is None:
        request = urlfetch.fetch(url, method=urlfetch.GET, deadline=40, allow_truncated=False)

        if request.status_code == 200 :
          pack = {
            "bytes":  request.content,
            "length": len(request.content),
            "mime":   request.headers['Content-Type'],
            "method": "nocache"
          }
          if len(request.content) < 1000000 :
            memcache.add(url, pack, timeout)
          
          return pack

        else :
          return {"error": "status_code: %d" % request.status_code, "method": "nocache"}

      else :
        data["method"] = "cache"
        return data

    except Exception, e :
      logging.error("Cache.error: %s | %s" % (url, str(e)))
      return {"error": str(e), "method": "nocache"}


  def serve(self, pack, keep) :

    expires_date = datetime.utcnow() + timedelta(seconds=(keep or KEEPHOUR))

    self.response.headers.update({
      'Expires'        : expires_date.strftime("%d %b %Y %H:%M:%S GMT"),
      'cache-control'  : "public, max-age=%d" % (keep or KEEPHOUR),
      'Pragma'         : "Public",
      'Content-Type'   : pack["mime"],
      'Content-Length' : pack["length"],
    })

    self.response.out.write(pack["bytes"])


  def get(self):

    if 'Referer' in self.request.headers.keys() :
      theReferer = self.request.headers['Referer']
    elif 'HTTP_REFERER' in os.environ :
      theReferer = os.environ['HTTP_REFERER']
    else :
      theReferer = "no Referer found"

    path = self.request.path
    url = self.request.path[7:]

    if url.startswith("http/") :
      url = "http://" + url[5:]

    elif url.startswith("https/") :
      url = "https://" + url[6:]

    else :
      aio.debug("error.path: %s", path)


    # aio.debug("url: %s ref: %s", url, theReferer)

    pack = self.fetch(url, 3600)

    if not pack.has_key("error") : 
      self.serve(pack, 3600)

    else :
      self.error(404)
      return self.logExit(url, theReferer, pack)
    
  def logExit(self, url, referer, pack) :
    logging.info("""
      rurl: %s 
      path: %s 
      refr: %s 
      cached: %s, error: %s """ % (url, self.request.path, referer, pack["method"], pack["error"]))


app = webapp2.WSGIApplication([('/cache/.*', Cache)])
