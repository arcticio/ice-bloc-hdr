
import logging
from google.appengine.api import users

class Navigation(object):
  def __init__(self):
    pass
  def get(self):

    navLinks = [
      { "name": "Home",             "url": "/",                                         "title": "Home of arctic.io",      "submenu": [
        {"name": "Blog",            "url": "/", "submenu": self.getBlogLinks(),         "title":"Latest Articles" },
        {"name": "Zooms",           "url": "/tag/Zoom", "submenu": self.getZoomLinks(), "title":"Collection of Deepzoom Images"},
        # {"name": "Radio Features",  "url": "/radio-interviews-and-features",            "title":"Arctic Audio Archive"}
      ]}]
      
    if True :  navLinks.append(
      { "name": "Explorer",         "url": "/explorer/",                                "title": "Satellite (true color/infrared)",
        "submenu": self.getSatLinks()}
    )

    if users.is_current_user_admin() : navLinks.append(
      { "name": "Weather",           "url": "/climate-weather-forecast/",               "title": "Weather North of 60 Degree Latitude", "submenu": [
        {"name": "GFS 2.5 degree",    "url": "/models/gfs25/",                          "title": "NH Forecast",             "submenu": [
          {"name": "Global Forecast", "url": "/models/gfs25/",                          "title": "Temp2m, "},
        ]},
        {"name": "PIOMAS",            "url": "/models/piomas/",                         "title": "Sea Ice Thickness"},
      ]}
    )
    else :  navLinks.append( 
      { "name": "Weather",           "url": "/climate-weather-forecast/",               "title": "Weather North of 60 Degree Latitude", "submenu": [
        {"name": "NH Forecast - 6 days", "url": "/explorer/H33//4-N90-E0/",             "title": "Surface Conditions (MSLP, Wind 10m, Temperature 2m)"},
      ]}
    )


    if True :  navLinks.append(
      { "name": "Sea Ice",          "url": "/sea-ice-charts/",                          "title": "Sea Ice Data &amp; Charts" ,
        "submenu": self.getIceLinks()}
    )
    if False :  navLinks.append(
      { "name": "News",             "url": "http://news.arctic.io/",                    "title": "Daily News Feed"}
    )
    if True :  navLinks.append(
      { "name": "Contact",          "url": "/contact/",       "rel": "author",           "title": "Contact arctic.io" }
    )
      
    if users.is_current_user_admin() : navLinks.append(
      { "name": "Admin",         "url": "/frame/?url=https://appengine.google.com",                  "title": "App Engine",  "submenu": [
        { "name": "Clicky",      "url": "/frame/?url=http://getclicky.com/stats/?site_id=66436098",  "title": "Clicky"},
        { "name": "Analytics",   "url": "/frame/?url=https://www.google.com/analytics/web/#report/visitors-overview/a22811255w44820339p44942976/",  "title": "Clicky"},
        { "name": "Bloc Logs",   "url": "/frame/?url=https://appengine.google.com/logs?app_id=ice-bloc&severity_level_override=0&severity_level=3&tz=Europe%2FBerlin&filter_type=regex&date_type=now",  "title": "Error Logs (bloc)"},
        { "name": "Map Logs",    "url": "/frame/?url=https://appengine.google.com/logs?app_id=ice-map&severity_level_override=0&severity_level=3&tz=Europe%2FBerlin&filter_type=regex&date_type=now",  "title": "Error Logs (bloc)"},
        { "name": "Admin",       "url": "/frame/?url=/admin/"},
        { "name": "Interactive", "url": "/frame/?url=/admin/interactive"},
        { "name": "New Post",    "url": "/frame/?url=/post/new"},
        { "name": "XHTML",       "url": "http://validator.w3.org/check?uri=www.arctic.io"},
        ]}
      )


    return navLinks
  
  def getZoomLinks(self):
    return [
      { "name": "Circumpolar Map",      "url": "/zoom/XpKT/0.506339;0.532550;1.012468/Arctic-Map",          "title": "Detailed Map of the Arctic Circle" },
      { "name": "Bathymetry",           "url": "/zoom/yDzd/0.5;0.5;1/Bathymetry",                           "title": "Bathymetric Map of the Arctic Ocean" },
      { "name": "CGC HEALY (50 days)",  "url": "/zoom/n0nJ/0.5172314;0.1962748;1.5925805/cgc-healy",        "title": "1 icebreaker, 50 days, 1200 webcam pics, 519 megapixels"},
      { "name": "Arctic (2012-07-25)",  "url": "/zoom/t9O6d/0.4660414;0.5210002;1.6140440/Arctic-11-07-02", "title": "Full zoomable Arctic Mosaic"},
      { "name": "Arctic (2011-07-02)",  "url": "/zoom/Q658/0.4660414;0.5210002;1.6140440/Arctic-11-07-02",  "title": "Full zoomable Arctic Mosaic"},
      { "name": "Arctic (2011-09-03)",  "url": "/zoom/VLI1/0.5074147;0.4929371;0.6728306/Arctic-11-09-03",  "title": "Full zoomable Arctic Mosaic" },
      { "name": "Sea Ice, low concentrated",  "url": "/zoom/wAZa/0.4;0.6;1.4/sea-ice-low-concentrated",     "title": "" },
    ]

  def getIceLinks(self):
    return [
      { "name": "Latest Images &amp; Charts", "url": "/sea-ice-charts/",                                              "title": "Temperatures, Oberservations, Analyis, Weather" },
      { "name": "Maps",                       "url": "/2013/11/new-map-interface",                                     "title": "Rendered Information", "submenu": [
        {"name": "AMSR2 - Sea Ice Concentration", "url": "/explorer/Y65//4-N90-E0/",  "title": "" },
        {"name": "SMOS - Sea Ice Thickness",      "url": "/explorer/2COH//4-N90-E0/", "title": "" },
        {"name": "CryoSat - Sea Ice Thickness",   "url": "/explorer/16C9//4-N90-E0/", "title": "" },
      ] },
      { "name": "Experiments",              "url": "/", "title": "Some pixel hurt", "submenu": [
        { "name": "Split Zooms",            "url": "/split-zoom/",                                                  "title": "Day by Day Changes in the Arctic" },
        { "name": "Clear Sky Zooms",        "url": "/clear-sky-zoom/",                                              "title": "8 Day Cloud Free Mosaics" },
        { "name": "Plotter",                "url": "/sea-ice-plotter/?zoom=204.000,8.000,525.000,18.000&data=area", "title": "Daily Sea Ice Area plotted" },
        # { "name": "Archive",                "url": "/sea-ice-weather-archive/",                                     "title": "" },
        # { "name": "Earth 3D/GFS",           "url": "/models/gfs25/",                                                "title": "2.5 degree Analysis and Forcast" },
        # { "name": "Weather &amp; Forecast", "url": "/climate-weather-forecast/",                                    "title": "Weather &amp; Climate Information" },
      ]},
    ]

  def getSatLinks(self):

    return [
      {"name": "Daily Arctic",                    "url": "/explorer/8//4-N90-E0/North%20Pole",                "title": "NASA's Artic Mosaic", "submenu": [
        # {"name": "<strong>Ice Drift + SST</strong>",     "url": "/explorer/1544///ice-drift-sst",     "title": "" },
        {"name": "Barents Sea",             "url": "/explorer/8//6-N74-E36/Barents%20Sea",              "title": "" },
        {"name": "Beaufort Sea",            "url": "/explorer/8//6-N73-W146/Beaufort%20Sea"},
        {"name": "Fram Strait",             "url": "/explorer/8//6-N80-E2/Fram%20Strait"},
        {"name": "Jakobshavn Glacier",      "url": "/explorer/8//8-N69.14-W50.07/Jakobshavn%20Glacier"},
        {"name": "Kara Sea",                "url": "/explorer/8//6-N74-E66/Kara%20Sea"},
        {"name": "Laptev Sea",              "url": "/explorer/8//6-N75-E122/Laptev%20Sea"},
        {"name": "Nares Strait",            "url": "/explorer/8//8-N81.4-W66.1/Nares%20Strait"},
        {"name": "Northwest Passage",       "url": "/explorer/8//6-N76-W102/Northwest%20Passage"},
        {"name": "Petermann Glacier",       "url": "/explorer/8//8-N80.7-W60/Petermann%20Glacier"},
      ]},
      {"name": "Daily Earth",                     "url": "/explorer/24//1-N40.71-E0.69/", "title": "Daily Satellite Images", "submenu": [
        {"name": "Asia",                    "url": "/explorer/24//1-N47-E92/", "submenu": [
          { "name": "Bangladesh",           "url": "/explorer/24//5-N24-E90/Bangladesh" },
          { "name": "Japan",                "url": "/explorer/24//3-N38.17-E140/Japan" },
          { "name": "China",                "url": "/explorer/24//3-N33-E103/China" },
          { "name": "Persian Gulf",         "url": "/explorer/24//5-N27-E51/Persian%20Gulf" },
          { "name": "Sri Lanka",            "url": "/explorer/24//3-N7.54102-E80.70117/Sri%20Lanka" },
        ]},
        {"name": "Africa",                  "url": "/explorer/24//1-N5-E24/", "submenu": [
          { "name": "Lake Victoria",        "url": "/explorer/24//6-S1-E33/Lake%20Victoria" },
          { "name": "Mozambique Channel",   "url": "/explorer/24//4-S18-E42/Mozambique%20Channel" },
          { "name": "Strait of Gibraltar",  "url": "/explorer/24//5-N36-W6/Strait%20of%20Gibraltar" },
        ]},
        {"name": "Australia",               "url": "/explorer/24//3-S22-E132/", "submenu": [
          { "name": "Bass Strait",          "url": "/explorer/24//5-S39-E146/Bass%20Strait" },
          { "name": "Great Barrier Reef",   "url": "/explorer/24//4-S16-E145.85/Great-Barrier%20Reef" },
          { "name": "New Sealand",          "url": "/explorer/24//4-S42.89063-E172.93359/New%20Sealand" },
        ]},
        {"name": "Europe",                  "url": "/explorer/24//2-N53-E18/", "submenu": [
          { "name": "Mediterranean Sea",    "url": "/explorer/24//3-N40-E15/" },
          { "name": "United Kingdom, Ireland", "url": "/explorer/24//3-N55-W5/" },
          { "name": "Germany, Cologne",     "url": "/explorer/24//9-N51-E7/Cologne" },
        ]},
        {"name": "North America",           "url": "/explorer/24//2-N49-W105/", "submenu": [
          { "name": "North West Passage",   "url": "/explorer/24//4-N71-W104.5/North%20West%20Passage" },
          { "name": "Golf of California",   "url": "/explorer/24//5-N28-W112/Golf%20of%20California" },
          { "name": "Golf of Mexico",       "url": "/explorer/24//4-N24-W88/Golf%20of%20Mexico" },
        ]},
        {"name": "South America",           "url": "/explorer/24//2-S12-W60/", "submenu": [
          { "name": "Amazon Rainforest",    "url": "/explorer/24//3-S2-W59/Amazon%20Rainforest" },
          { "name": "Atacama Desert",       "url": "/explorer/24//5-S20-W70/Atacama%20Desert" },
        ]},
      ]},
      {"name": "Daily Antarctic", "url": "/explorer/aKemW//4-S90-W0/Antarctic" },
    ]

  def getBlogLinks(self):

    from models.blog import Article
    links = []
    articles = Article.all().filter("article_type = ", "blog entry").order("-published").fetch(7)
    for entry in articles :
      links.append({"url": "/" + entry.permalink, "name": entry.title })
    return links


  def getNewsLinks(self):

    import os
    import simplejson
    from google.appengine.api import urlfetch
    from google.appengine.api import memcache

    deb   = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
    if deb :
      url = "http://ice-cron.appspot.com/data/news/menu/"
      url = "http://192.168.2.110:8081/data/news/menu/?days=7&news=6"
      url = "http://localhost:8081/data/news/menu/?days=7&news=6"
      url = "http://ice-cron.appspot.com/data/news/menu/?days=7&news=6"
    else :
      url = "http://ice-cron.appspot.com/data/news/menu/?days=7&news=6"

    try :
      data = memcache.get(url)
      if data is None:
        data = simplejson.loads(urlfetch.fetch(url, deadline=10, allow_truncated=False).content)
        memcache.add(url, data, 60 * 60)
      return data

    except Exception, e :
      logging.warn("getNewsLinks : " + str(e) + " | " + url)
      return []
