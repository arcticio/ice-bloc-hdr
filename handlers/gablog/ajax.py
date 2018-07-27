"""
ajax.py

Created by Torsten Becker on 2011-04-15.
"""
__author__ = "Torsten Becker"

import logging
import os
import simplejson
import traceback
import time
from datetime import datetime, timedelta

from google.appengine.runtime import DeadlineExceededError

from google.appengine.api import memcache
from google.appengine.api import urlfetch

from handlers import restful
import view

from utils.clock import Clock

##
##
###############  A J A X    H A N D L E R   #########################

class AjaxHandler(restful.Controller):

  def get(self, params=""):

    params = filter(None, params.split("/"))

    if len(params) == 0 :
      logging.warn("AJAX: NO MODULE GIVEN")
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write("MODULE?")
      return

    module = params[0]

#
#
##########################

    if module == "nomad" :

      url = self.request.url

      ## first delete old stuff from memcache
      if self.request.get('deletecache', "") == "true" :
        memcache.delete(url)

      if self.request.get('usecache') == "true" : 
        data = memcache.get(url)
        if data :
          json = simplejson.loads(data)
          json['_meta']['cache'] = True
          self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
          self.response.out.write(simplejson.dumps(json, sort_keys=True, indent=2))
          logging.info("AJAX.nomad.cached: " + url)
          return

      from utils.nomads import Nomads, sets as dataSetParams, datasets as svrSetParams

      tim0 = datetime.now(); tim1=-1; tim2=-1; tim3=-1; tim4=-1;
      debb = True if self.request.get('deb',  False) == "True" else False

      def debDuration() : 
        def s(t1, t2) : 
          try :    return (t2 - t1).seconds
          except : return 999        
        params = (s(tim0, tim1), s(tim1, tim2), s(tim2, tim3), s(tim3, tim4))
        return "last:%s; urls:%s; fetch:%s; parse:%s" % params

      json = {
        '_meta': {
          'referer': self.request.environ['HTTP_REFERER'] if 'HTTP_REFERER' in self.request.environ else None,
          'request': url,
          'duration': "",  
          'ip': os.environ['REMOTE_ADDR'],
          'error': "",
          'errortrace': "",
          'cache': False,
        }, 
        'data': {
          '_stats': None,
          'home': "",
          'assets': "",
          'model': "",
          'credit': "",
          "timestamp": None,
          'datasets': {},
          'projection': {
            "type": "spherical", 
            "center": None, 
            "resolution": None, 
            "lats": None,
            "lons": None,
          },
        }
      }

      try :

        if self.request.get('qry') == "latest" : 

          svr, sets, lons, lats, rng = "gfs_2p5", "tmp2m", "0:143", "1:71", "-2:7"

          svr  = self.request.get('svr',  svr)
          sets = self.request.get('sets', sets)  ## ",wind10m,icecsfc,pressfc")
          lons = self.request.get('lons', lons)  ##   0.00000000000E to 357.50000000000E (144 points, avg. res. 2.5) 
          lats = self.request.get('lats', lats)  ## -90.00000000000N to  90.00000000000N  (73 points, avg. res. 2.5) 
          rng  = self.request.get('rng',  rng)   ##  (33 points, avg. res. 0.5 days) we get DAYS !!!

        else :

          svr  = self.request.get('svr',   "gfs_2p5")
          sets = self.request.get('sets',  "tmp2m,icecsfc") ## ",wind10m,icecsfc,pressfc")
          lons = self.request.get('lons',  "0:143")   ##   0.00000000000E to 357.50000000000E (144 points, avg. res. 2.5) 
          lats = self.request.get('lats',  "54:71")   ## -90.00000000000N to  90.00000000000N  (73 points, avg. res. 2.5) 
          rng  = self.request.get('rng',  "-2:7")     ##  (33 points, avg. res. 0.5 days) we get DAYS !!!

        ## init with params
        nomad = Nomads(svr, sets, lats, lons, rng)
        
        ## a = 1/0  ## DEBUG

        if sets == "coltest" :
          last, urlLast, runUrls = "", "", []
          json['data'] = nomad.getTestData()
          tim4 = datetime.now()

        else :
          last, urlLast = nomad.getLatest()
          tim1 = datetime.now()

          runUrls = nomad.getRunUrls()
          tim2 = datetime.now()

          results = nomad.fetchData(runUrls)      ## comment to debug urls
          tim3 = datetime.now()

          # json['data'] = nomad.parseData(results) ## comment to debug urls
          parsedData = nomad.parseData(results) ## comment to debug urls
          tim4 = datetime.now()
          

        if parsedData['error'] :

          ## complete meta
          json['_meta']['error'] = parsedData['error']

        else :

          ## complete meta
          json['_meta']['last'] = last

          ## complete model
          json['data']['model']   = svrSetParams[svr]["label"]
          json['data']['credit']  = svrSetParams[svr]["credit"]

          ## complete stats
          json['data']['_stats'] = parsedData['_stats']
          json['data']["_stats"]["sets"] = len(sets.split(","))

          ## complete projection
          json['data']['projection']['resolution'] = svrSetParams[svr]["reso"]
          json['data']['projection']['lats'] = parsedData['coords']['lats']
          json['data']['projection']['lons'] = parsedData['coords']['lons']
          
          ## complete datasets
          for set in sets.split(",") :
            
            logging.info("SET: " + set)

            json['data']['datasets'][set] = dataSetParams[set].copy()
            json['data']['datasets'][set]["scale"] = {
              "x": svrSetParams[svr]["scales"]["x"],
              "y": svrSetParams[svr]["scales"]["y"],
              "z": dataSetParams[set]["zscale"],
            }
            del json['data']['datasets'][set]["ign"]
            del json['data']['datasets'][set]["zscale"]
          
          ## complete timesets
          json['data']['timestamp'] = parsedData['timestamp']
          json['data']['timesets']  = parsedData['timesets']


        ## finalize
        if debb : json['_meta']['urls']    = runUrls
        if debb : json['_meta']['urlLast'] = urlLast
        if debb : json['_meta']['agent']   = os.environ['HTTP_USER_AGENT']

        ## finalize
        if self.request.get('usecache') == "true" : 
          memcache.add(self.request.url, simplejson.dumps(json), 3600)
      
      except DeadlineExceededError:
        logging.error("DeadlineExceededError: " + debDuration() + ", " + url) 
        json["_meta"]["error"] = "DeadlineExceededError"
        json['data']["_stats"]["sets"] = len(sets.split(","))

      except Exception, e:
        logging.error("Exception: " + debDuration()  + ", " + url + ", " + str(e) )
        json["_meta"]["error"] = str(e)
        json["_meta"]["errortrace"] = traceback.format_exc()

      finally :
        logging.info("Duration: " + debDuration() + ", " + url)
        json['_meta']['duration']  = debDuration()
        self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
        self.response.out.write(simplejson.dumps(json, sort_keys=True, indent=2))

      return  

#
#
##########################

    if module == "geocode" :
      latlng = self.request.get('latlng')
      json   = {"error": "", "errortrace": "", "address": "", "results": [], "latlng": ""}
      try :
        home = "http://maps.googleapis.com/maps/api/geocode/json"
        url  = home + "?latlng=" + latlng + "&sensor=false"
        answer = urlfetch.fetch(url, method=urlfetch.GET, deadline=30, allow_truncated=False).content
        answer = simplejson.loads(answer)
        json["latlng"] = latlng
        latlng = latlng.split(",")
        json["formatted"] = "%s N, %s E" % (latlng[0], latlng[1])

        for item in answer["results"] :
          if item.has_key("formatted_address") :
            json["results"].append(item["formatted_address"])

        num = len(json["results"])
        if num > 1 :
          json["address"] = json["results"][num -2]
        elif num == 1 :
          json["address"] = json["results"][0] + ", " + json["formatted"]
        else :
          json["address"] = json["formatted"]
      except Exception, e :
        json["error"] = str(e)
        json["errortrace"] = traceback.format_exc()
      finally :
        self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
        self.response.out.write(simplejson.dumps(json, sort_keys=True, indent=2))
      return

#
#
##########################

    if module == "proxy" :
      try :
        ## http://localhost:8080/ajax/proxy/?url=http://arctic.atmos.uiuc.edu/cryosphere/timeseries.anom.1979-2008
        ## urllib.unquote()
        url = self.request.get('url')
        if url[:1] == "/" : url = "http://www.arctic.io" + url
        data = memcache.get(url)
        if data is None:
          data = urlfetch.fetch(url, method=urlfetch.GET, deadline=30, allow_truncated=False).content
          memcache.add(url, data, 3600)
          logging.info("AJAX.proxy.fresh: " + url)
        else :
          logging.info("AJAX.proxy.cache: " + url)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(data)
      except Exception, e :
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(str(e))
        self.response.out.write(traceback.format_exc())
      return
#
#
##########################
#
#   get column of area data from this year

    if module == "latestarea" :
      try :
        cached = True
        url = "http://arctic.atmos.uiuc.edu/cryosphere/timeseries.anom.1979-2008"
        data = memcache.get(url)
        if data is None or self.request.get('nocache', ""):        
          cached = False
          data = urlfetch.fetch(url, method=urlfetch.GET, deadline=30, allow_truncated=False).content
          memcache.add(url, data, 3600)

        lines = data.split("\n")

        if cached : 
          logging.info("AJAX.latestarea.cached: " + str(len(lines)))
        else :
          logging.info("AJAX.latestarea.fresh: "  + str(len(lines)))

        lastYear = ""
        first = None
        doy = 0
        area = {}

        for line in lines:

          items = line.split("  ")
          year = items[0].split(".")[0].strip()
          if year == "" : continue
          iYear = int(year)

          if year != lastYear :
            lastYear = year
            first = datetime(iYear, 1, 1)
            doy = 2 if year == "1979" else 1
            area[year] = {'days': [], 'area': []}

          day = time.strftime("%Y-%m-%d", (first + timedelta(days=doy-1)).timetuple())
          value = str(int(items[2].strip().replace(".", ""))/10)
          area[year]['days'].append(day)
          area[year]['area'].append(value)
          doy += 1

        year = str(datetime.now().year)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("\n".join(str(a) for a in area[year]['area'])  )      

      except Exception, e :
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(str(e))
        self.response.out.write(traceback.format_exc())
      return

#
#
##########################

    ## /ajax/sea-ice-drift/48

    if module == "sea-ice-drift" :

      self.response.headers['Content-Type'] = 'text/plain'

      try :
        json = memcache.get("sea-ice-drift")
        if json is None:
          from utils.icedrift import IceDrift
          Drift = IceDrift()
          Drift.processPoints()
          Drift.processData()
          json = simplejson.dumps(Drift.export, sort_keys=True, indent=2)
          memcache.add("sea-ice-drift", json, 4 * 3600)

        self.response.out.write(json)
      except Exception, e :
        self.response.out.write(simplejson.dumps({"error" : str(e)}))

      return


#
#
##########################

    if module == "sea-ice-archive-list" :

      from seaiceArchive import Archive

      datum = params[1]
      archive = Archive(datum)

      template_data  = {
        'yir': Clock.year,
        'ipu': self.request.remote_addr,
        'deb': os.environ.get('SERVER_SOFTWARE', '').startswith('Development'),
        'archive': ["huhu", "haha"],
        'module_name': None,
        "handler_name": module
      }
      view.ViewPage(cache_time=3600).render(self, template_data)
      return


#
#
##########################

    logging.warn("AJAX: NO MODULE FOUND")
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("MODULE?: " + module)
    return



