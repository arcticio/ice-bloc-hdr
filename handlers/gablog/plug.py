"""
plug.py

Created by Torsten Becker on 2011-04-15.
"""
__author__ = "Torsten Becker"

import aio

import time
import os
import simplejson
import logging
import urlparse
import cgi
import urllib
import copy

from datetime import datetime, timedelta

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import config
from handlers import restful
import view
import unicodedata

from configs.configSeaice import SeaiceData
from configs.configWeather import WeatherData
from configs.seaiceArchive import Archive
from utils.clock import Clock

def parseArgs(args, argname, default=None):
  try:
    return args[argname][0]
  except:
    return default

def getReferer(req):
  hkeys = req.headers.keys()
  if 'Referer' in hkeys:
    return req.headers['Referer']
  else :
    if 'HTTP_REFERER' in os.environ :
      return os.environ['HTTP_REFERER']  
  return ""

def asciify(item):
  buffer = ""
  for letter in item :
    try:
      buffer += unicodedata.normalize('NFKD', letter.decode('utf-8', 'replace')).encode('ascii', 'ignore')
    except:
      buffer += "_"
  return buffer


##
##
###############  W I K P E D I A    H A N D L E R   #########################

class WikipediaHandler(restful.Controller):

  def get(self):

    def parseFloat(str):
      out = ""
      for l in str :
        if l.isdigit() or l == "." or l == "-" :
          out += l
      return float(out)

    referer = getReferer(self.request)
    if  referer :
      aio.info("WikipediaHandler.REF: %s " % referer)


    lat = parseFloat(self.request.get('lat', 0))
    lon = parseFloat(self.request.get('lon', 0))
    tit = self.request.get('title', "")

    day = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%d")
    cod = 'IAKKG' if lat > 70 else 'IAKMC'
    lvl = 6  if lat > 70 else 8

    ## http://www.arctic.io/wikipedia/?lon=9.993333&lat=53.550556&title=Hamburg
    ## http://localhost:8093/wikipedia/?lon=9.993333&lat=53.550556&title=Hamburg
    ## http://localhost:8093/wikipedia/?lon=9.993333&lat=80.550556&title=North

    if lat >= 0: lat = "N" + str(abs(lat))
    if lat  < 0: lat = "S" + str(abs(lat))
    if lon >= 0: lon = "E" + str(abs(lon))
    if lon  < 0: lon = "W" + str(abs(lon))

    tit = urllib.quote(tit.encode('utf8'))

    url = "/explorer/%s/%s/%s-%s-%s/%s" % (cod, day, lvl, lat, lon, tit)

    aio.info("WikipediaHandler.from: " + asciify(self.request.url))
    aio.info("WikipediaHandler.to: "   + asciify(url))

    self.redirect(url)

    return

##
##
###############  E X P L O R E R    H A N D L E R   #########################

class ExplorerHandler(restful.Controller):

  def get(self, layers="8", datum=None, position="4-N89-E0", toponym=""):

    if view.render_if_cached(self):
      return

    title = config.APP['title'] + " - Daily Satellite Images + Observations"
    if toponym  : title += ": " + urllib.unquote(toponym)
    if position : title += ", " + position
    title = title.replace("\"", "'")

    template_data  = {
      'yir': Clock().year,
      'ipu': self.request.remote_addr,
      'deb': config.DEBUG,
      'title': title,
      'description': "Interactive Satelite Maps of Earth and Arctic",
    }

    view.ViewPage(cache_time=3600).render(self, template_data)


##
##
###############  S E A I C E    H A N D L E R   ####################################

class SeaiceHandler(restful.Controller):

  def get(self):

    if view.render_if_cached(self) :
      return

    newData = []
    oldData = SeaiceData[:]
    host    = "http://127.0.0.10:8080/pics/?"
    host    = "http://omega.ice-pics.appspot.com/pics/?"
    host    = "http://ice-pics.appspot.com/pics/?"

    for gallery in oldData:
      if gallery["active"] :
        gal = copy.deepcopy(gallery)
        if not "anchor" in gal :
          for pic in gal["items"]:

            if "url" in pic :
              rot     = 0  if not pic.has_key("rot")       else int(pic["rot"])  ## 4 hours
              keep    = 14400  if not pic.has_key("keep")  else int(pic["keep"])  ## 4 hours
              width   = 140    if not pic.has_key("width") else pic["width"]
              params = "rot=%s&crop=%s&width=%s&keep=%s&" % (rot, pic['crop'], width, keep)
              pic["icon"] = host + params + urllib.urlencode({ 'url': pic["url"] })
              if type(pic['date']).__name__ == "function" :
                pic['date'] = pic['date']()

        newData.append(gal)
    
    templateData = {
      'gallerydata': newData, ##SeaiceData,
      'galleryjson': simplejson.dumps(newData),
      'title': config.APP['title'] + " - Daily Sea Ice Charts, Graphs and Forecasts"
      }
    view.ViewPage(cache_time=3600).render(self, templateData)


##
##
###############  Z O O M   H A N D L E R   ####################################
## http://www.google.com/fusiontables/DataSource?dsrcid=914580&pli=1
## https://www.google.com/fusiontables/api/query?sql=SELECT%20*%20FROM%20914580%20

class ZoomHandler(restful.Controller):

  def get(self, params=""):

    if view.render_if_cached(self):
      return

    aio.debug("plug.ZoomHandler params: %s", params)

    if len(params) == 0 :
      self.redirect("/maps/circumpolar")
      return

    else :
      params = params.split("/")
      dzi = params[0]
      if len(params) > 1 : pos = urllib.unquote(params[1])



    template_data  = {
      'title':          config.APP['title'] + ' - Zoom: ' + params[0].title(),
      'dzi':            params[0],
    }

    view.ViewPage(cache_time=3600).render(self, template_data)