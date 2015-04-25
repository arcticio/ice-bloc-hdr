import logging
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

utils_path = os.path.join(BASEDIR, "utils")
ext_utils_path = os.path.join(utils_path, "external")

# Enabling debugging prints extra messages about what's going on "under 
# the hood". Currently only enabled automatically when running on the 
# GAE development server.

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Development')
# DEBUG = False


def getUser():

  from google.appengine.api import users
  
  user = users.get_current_user()
  if not user :
    return {
      'ip': os.environ['REMOTE_ADDR'],
      'admin': users.is_current_user_admin()
      }
  else :
    from google.appengine.ext import db
    dbuser = db.GqlQuery("SELECT * FROM User WHERE mail = :1", user.email()).get()
    if not dbuser :
      return {
        'ip': os.environ['REMOTE_ADDR'],
        'mail': user.email(),
        'nick': user.nickname(),
        'admin': users.is_current_user_admin()
        }
    else :
      return dbuser.toDict()

#USER = getUser()

# This dict contains application-wide configuration values
APP = {
	"name": "arctic.io",
	"version": "0.3",
	"description": "Look, it's melting",
	"title": "arctic.io",
	"author": "Torsten Becker",

	# Your Twitter username, for the Twitter widget. Set to None if you
	# don't want to use the widget or if you don't have a Twitter
	# account.
	"twitter_username": "arctic.io",

	# The number of posts to load from Twitter
	"twitter_posts": 3,

	# The AppEngine mail API requires that this be the email 
	# address for a registered admin of the application. This will be 
	# the email address emails sent from this application appear to 
	# come from.
	"email": "tb@arctic.io",

	# This will be the MIME type and character set used
	"mimetype": "application/xml+xhtml",
	"charset": "UTF-8",

	"base_url": "http://www.arctic.io",

	# The jQuery version to use
	"jquery_version": "1.4.2",

	# Timeout for memcache in seconds.
	"memcache_timeout": 3600,

	# The directory containing HTML templates.
	"template_dir": "templates",

	# Must be the name of a directory under the template_dir directory.
	"theme": "arctic",

	# Your Google Analytics tracking code. Set to None if you don't have
	# one (or don't want to use one).
	"analytics": "UA-22811255-1",
  
	# The base domain for this app. For example, if you use
	# 'http://www.example.com' then the base domain would be 'example.com'.
	"base_domain": "arctic.io",

	# Your Google site verification code for Google Webmaster, if you 
	# are using this service.
	"google_webmaster_verify": None,

	# The legacy software to map URI's from. Adding support is a
	# two-step process: add the name here (either on its own or as part
	# of the list) and add required code to resolve_legacy_mapping in
	# handlers/gablog/blog.py
	#
	# This can either be a single supported value, or a list of
	# supported values. Currently supported legacy software packages
	# are:
	#	Drupal - URLs look like this: /node/3, /node/58/
	#	Serendipity - URLs look like this: /archives/54-something.html
	#	Blogger - URLs look like this:
	"legacy_software": None,

	# If this is set to False, legacy entries _not_ mapped through
	# legacy software in legacy_aliases.py will be served on their old
	# URIs.  If this is set to True, legacy URIs will be redirected to
	# their new permalink.
	"legacy_entry_redirect": True,
}

# This is the main configuration dict for things specific to the blog system
BLOG = {

  #truncater in blogs
  "truncater": "[MORE]", ## see /utils/templatefilters

	# RSS and Atom feeds are at these locations
	"rss_url": "/feeds/rss",
	"atom_url": "/feeds/atom",
	
	"pingback_url": "/pingback",
	
	# The CKEditor skin to use
	"ckeditor_skin": "kama",

	# Set to True if you want to have the post scanned for links to
	# other sites and pingbacks sent to those sites that support
	# pingbacks.
	# WARNING: Enabling this will substantially slow down the posting
	# process. Although this is the last thing to be done before
	# redirecting to the new permalink, it may appear that nothing is
	# happening. Please ensure that you wait for the redirect to occur
	# before navigating anywhere.
	"do_pingback": False,

	# Set to True if you want your feed to use the article excerpt
	# instead of the full article text.
	"feed_use_summary": False,

	# Number of days posts are open for commenting by default. If the 
	# selection on a post is set to "No" or "Yes", that will override
	# this setting.
	"comment_window": 14,	# 4 weeks

	# The number of blog posts to display on each page.
	"posts_per_page": 20,

	# The number of comments to display on each page of each post
	"comments_per_page": 40,

	# Check for a Gravatar for the email address each commenter 
	# provides?
	"use_gravatars": False,

	# Do you want to be emailed when new comments are posted?
	"send_comment_notification": True,
}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

if logger.isEnabledFor(logging.DEBUG):
	logging.debug("Starting %s %s with debug logging enabled", 
		APP['name'], APP['version'])
else:
	logging.info("Starting %s %s", APP['name'], APP['version'])


## Meta, Past, Future, Ad, Intro, News, Tags, Admin, Info

## 'info': "The Arctic is the symbol of Climate Change. See read and explore the consequences of the anthropocene",

SIDEBAR = {
  'default': {
    'info': "We are all living on the same Planet. Cruise speed is 30 kilometers per second around sun. All energy comes from there. <br /><br />Earth has no emergency exit and is getting hotter. Polar caps are melting and oceans are rising. Arctic will be ice free soon. Can we stop CO2 and terraforming early enough?",
    'col1': ('Admin', 'Info', 'Past'),
    'col2': ('Ad', 'Meta', 'Tags', 'Future', 'News')
  },
  'seaice': {
    'info': "The overall knowledge of the Arctic is little. Physical exploration may have started 325 BC, the satellite record goes back to 1979 and before there are few reports from ships. Latest model predict an ice free Arctic in a few years, caused by sea ice volume decline.",
    'col1': ('Admin', 'Info', 'Seaice'),
    'col2': ('Ad', 'Meta', 'Tags', 'Future', 'News')
  },
  'news': {
    'info': "The Internet connects everybody on this planet. Global communication is needed to get the message on the wire. The Arctic is melting, it is time to act.",
    'col1': ('Admin', 'Info', 'Seaice'),
    'col2': ('Ad', 'Meta', 'Tags', 'Future', 'News')
  }
}

BARDEF = SIDEBAR['default']
BARSEA = SIDEBAR['seaice']
BARNEW = SIDEBAR['news']

class ArcticIo(object):
  """ this is used in main.py
      this is used in view.py"""
  def __init__(self) :

    from handlers.gablog import blog, contact, cache_stats, post, page, timings, update, xmlrpc, plug, ajax

    self.config = [
[blog.RootHandler,                 '/*$',                           {'layout': BARDEF,   'hdl': '0',    'urlmenu': True,   'navMenu': True}],
# [xmlrpc.PingbackHandler,           BLOG['pingback_url'],            {'layout': None,     'hdl': '6'}],
# [update.CommentAddPingbackHandler, '/updates/comment-add-pingback', {'layout': None,     'hdl': '1',    'urlmenu': True}],
[cache_stats.CacheStatsHandler,    '/admin/cache_stats/?$',         {'layout': BARDEF,   'hdl': '10',   'navMenu': True}],
[timings.TimingHandler,            '/admin/timings/?$',             {'layout': BARDEF,   'hdl': '11',   'navMenu': True}],
[contact.ContactHandler,           '/contact/?$',                   {'layout': BARDEF,   'hdl': '14',   'navMenu': True, 'navSocial': ['G', 'T', 'F']}],
[post.NewPostHandler,              '/post/new/?$',                  {'layout': BARDEF,   'hdl': '2'}],
[post.EditPostHandler,             '/post/edit/([\d\w]+)/?$',       {'layout': BARDEF,   'hdl': '3',    'urlmenu': True}],
[blog.UnauthorizedHandler,         '/403.html',                     {'layout': BARDEF,   'hdl': '4'}],
[blog.NotFoundHandler,             '/404.html',                     {'layout': BARDEF,   'hdl': '5'}],
[blog.YearHandler,                 '/([12]\d\d\d)/?$',              {'layout': BARDEF,   'hdl': '7',    'urlmenu': True,   'navMenu': True}],
[blog.MonthHandler,                '/([12]\d\d\d)/(\d|[01]\d)/?$',  {'layout': BARDEF,   'hdl': '8',    'urlmenu': True,   'navMenu': True}],
[blog.BlogEntryHandler,    '/([12]\d\d\d)/(\d|[01]\d)/([-\w]+)/?$', {'layout': BARDEF,   'hdl': '9',    'disqus':  True,   'editor':  False, 'urlmenu': True, 'navMenu': True}],
[blog.SearchHandler,               '/search',                       {'layout': BARDEF,   'hdl': '12',   'urlmenu': True,   'navMenu': True}],
# [blog.CommentHandler,              '/comment/?([\w-]+)?',           {'layout': None,     'hdl': '13'}],
[blog.TagFeedHandler,              '/tag/(.*?)/feed/?$',            {'layout': BARDEF,   'hdl': '15'}],
[blog.TagHandler,                  '/tag/(.*?)/?$',                 {'layout': BARDEF,   'hdl': '16',   'urlmenu': True,   'navMenu': True}],
[blog.AtomHandler,                 BLOG['atom_url'] + '/?$',        {'layout': None,     'hdl': '17'}],
[blog.ArticlesHandler,             '/articles/',                    {'layout': BARDEF,   'hdl': '18',   'urlmenu': True,   'navMenu': True}],
[plug.NewsHandler,                 '/polar-news/(.*)',              {'layout': BARNEW,   'hdl': '19',   'urlmenu': True,   'navPerma': False, 'navMenu': True}],
[plug.PlotterHandler,              '/sea-ice-plotter/(.*)',         {'layout': BARDEF,   'hdl': '20',   'navMenu': True,   'navPerma': True}],
# [plug.SatelliteHandler,            '/observations/(.*)/(.*)/(.*)/(.*)',{'layout': None,  'hdl': '21',   'navMenu': True,   'navPerma': True}],
# [plug.SatelliteHandler,            '/observations/(.*)/(.*)/(.*)',     {'layout': None,  'hdl': '21',   'navMenu': True,   'navPerma': True}],
# [plug.SatelliteHandler,            '/observations/',                   {'layout': None,  'hdl': '21',   'navMenu': True,   'navPerma': True}],
[plug.ExplorerHandler,             '/explorer/(.*)/(.*)/(.*)/(.*)', {'layout': None,     'hdl': '21',   'navMenu': True,   'navPerma': True}],
[plug.ExplorerHandler,             '/explorer/(.*)/(.*)/(.*)',      {'layout': None,     'hdl': '21',   'navMenu': True,   'navPerma': True}],
[plug.ExplorerHandler,             '/explorer/',                    {'layout': None,     'hdl': '21',   'navMenu': True,   'navPerma': True}],
[plug.WikipediaHandler,            '/wikipedia/',                   {'layout': None,     'hdl': '21',   'navMenu': True,   'navPerma': True}],
[plug.SeaiceHandler,               '/sea-ice-charts/',              {'layout': BARSEA,   'hdl': '22',   'shadowbox': True, 'navMenu': True, 'indexes': True}],
[plug.WeatherHandler,              '/climate-weather-forecast/',    {'layout': BARSEA,   'hdl': '23',   'shadowbox': True, 'navMenu': True, 'gfsindizes': True}],
[plug.FrameHandler,                '/frame/(.*)/(.*)/',             {'layout': None,     'hdl': '25',   'navMenu': True}],
[plug.FrameHandler,                '/frame/(.*)',                   {'layout': None,     'hdl': '25',   'navMenu': True}],
[plug.ClearSkyHandler,             '/clear-sky-zoom/(.*)',          {'layout': None,     'hdl': '26',   'navPerma': True,  'navMenu': True}],
[plug.SplitZoomHandler,            '/split-zoom/(.*)',              {'layout': None,     'hdl': '26',   'navPerma': True,  'navMenu': True}],
[plug.DoubleZoomHandler,           '/double-zoom/(.*)',             {'layout': None,     'hdl': '26',   'navPerma': True,  'navMenu': True}],
[plug.ZoomHandler,                 '/zoom/(.*)',                    {'layout': None,     'hdl': '26',   'navPerma': True,  'navMenu': True}],
[plug.ModelsHandler,               '/models/',                      {'layout': None,     'hdl': '27',   'navPerma': False, 'navMenu': True}],
[plug.ModelsHandler,               '/models/(.*)/',                 {'layout': None,     'hdl': '27',   'navPerma': False, 'navMenu': True}],
[plug.ArchiveHandler,              '/sea-ice-weather-archive/(.*)', {'layout': BARDEF,   'hdl': '28',   'urlmenu':  True,  'archive': True, 'navMenu': True}],
[ajax.AjaxHandler,                 '/ajax/(.*)',                    {'layout': None,     'hdl': '29'}],
[blog.SitemapHandler,              '/sitemap.xml',                  {'layout': None,     'hdl': '30'}],
[page.PageHandler,                 '/(.*)',                         {'layout': BARDEF,   'hdl': '31',   'urlmenu': True,   'navMenu': True}],
    ]

    self.routes = []
    for entry in self.config :
      self.routes.append((entry[1], entry[0]))

  def getRoutes(self) :
    return self.routes

  def getParams(self, handler) :
    for entry in self.config :
      if isinstance(handler, entry[0]) :
        return entry[2]
    return {'handler': str(handler)}


  def getFutureLinks(self, handler):
    return [{
      "name":  "NOAA Administrative Order 202-735: ",
      "url":   "http://www.doi.gov/news/pressreleases/upload/Sec-Order-No-3305.pdf",
      "title": "Scientific Integrity Policy",
      },{
      "name":  "Ensuring Scientific Integrity within the Department of the Interior",
      "url":   "http://www.doi.gov/news/pressreleases/upload/Sec-Order-No-3305.pdf",
      "title": "DOI Order No. 3305",
      },{
      "name":  "Comparing the Arctic Offshore Oil and Gas Drilling Regulatory Regimes",
      "url":   "http://pubs.pembina.org/reports/comparing-offshore-regulations-executive-summary-final.pdf",
      "title": "of the Canadian Arctic, the U.S., the U.K, Greenland, and Norway",
      },{
      "name":  "The Future of Arctic Sea Ice",
      "url":   "https://docs.google.com/open?id=0B1xsbFlqmAA_Wi1zeEZkS3RRbWs",
      "title": "Maslowski, Kinney, Higgins, Roberts"
      },{
      "name":  "Evidence linking Arctic amplification to extreme weather in mid-latitudes",
      "url":   "https://docs.google.com/open?id=0B1xsbFlqmAA_dVVpTS0xdXRFcFE",
      "title": "J. A. Francis,  S. J. Vavrus"
      },{
      "name":  "The sea ice mass budget of the Arctic and its future change as simulated by coupled climate models",
      "url":   "https://docs.google.com/open?id=0B1xsbFlqmAA_VVlEZ290Y3o2RzA",
      "title": "Holland, Serreze, Stroeve"
      },{
      "name":  "Arctic Energy: Pathway to Conflict or Cooperation in the High North?",
      "url":   "http://www.ensec.org/index.php?option=com_content&amp;view=article&amp;id=310:arctic-energy-pathway-to-conflict-or-cooperation-in-the-high-north&amp;catid=116:content0411&amp;Itemid=375",
      "title": "IAGS Journal of Energy Security"
      },{
      "name":  "Thinking about the Arctic's Future: Scenarios for 2040",
      "url":   "http://www.crrc.unh.edu/workshops/arctic_spill_summit/arctic_scenarios_09_07.pdf",
      "title": "Lawson W. Brigha"
      },{
      "name":  "The Arctic's rapidly shrinking sea ice cover",
      "url":   "http://www.springerlink.com/content/c4m01048200k08w3/fulltext.pdf",
      "title": "NSIDC - Research Synthesis"
      }
    ]



  def getPastLinks(self, handler):
    return [{
      # "name"  : "Finger Close to Alarm Button",
      # "url"   : "/2012/10/finger-close-to-alarm-button",
      # "img"   : "http://dl.dropbox.com/u/354885/Arctic/aio/minis/finger-alarm.jpg",
      # "title" : "If you press the alarm button and nobody knows what to do, all you're doing is noise." 
      # },{
      "name"  : "Brinicles and the Origin of Life",
      "url"   : "/2013/4/brinicles-and-the-origin-of-life",
      "img"   : "/images/minis/brinicles.jpg",
      "title" : "Brinicles are the most bizarre phenomena below sea ice. They grow like stalactites, but much faster and in absent of other forces eventually" 
      },{
      "name"  : "Colors of a Melting Cryosphere",
      "url"   : "/2013/4/colors-of-a-melting-cryosphere",
      "img"   : "/images/minis/colors-cryosphere.jpg",
      "title" : "With 2010 a new era started, interestingly with no trend between years in winter and much higher losses" 
      },{
      "name"  : "PIOMAS Thickness 2012",
      "url"   : "/2013/1/sea-ice-volume-s1e3-monthly-piomas-thickness-maps-2012",
      "img"   : "/images/minis/piomas-2012.jpg",
      "title" : "PIOMAS shows significant reduction of the thickest ice" 
      },{
      "name"  : "My Problem with Sea Ice Extent",
      "url"   : "/2012/8/my-problem-with-sea-ice-extent",
      "img"   : "http://dl.dropbox.com/u/354885/Arctic/aio/minis/blog-problem-extent.png",
      "title" : "Imagine a single idealized ice floe: 1 kilometer long and 1 kilometer wide with a thickness of 2 meter drifting in the Arctic Ocean" 
      },{
      "name"  : "Yearly Sea Ice Volume Loss",
      "url"   : "/2012/7/yearly-sea-ice-volume-loss",
      "img"   : "http://dl.dropbox.com/u/354885/Arctic/aio/minis/blog-volume-loss.png",
      "title" : "The question: 'When will the Arctic be ice free?' can be posed differently as: 'When will we have 100% ice loss during the melting season?'. The interactive chart above" 
      },{
      "name"  : "North Pole painted by Mercator (published 1596)",
      "url"   : "/2012/4/north-pole-painted-by-mercator-published-1596",
      "img"   : "http://farm6.staticflickr.com/5344/6969553574_5163af5554_s.jpg",
      "title" : "Gerardus Mercator was born in 1512 and invented the famous Mercator projection showing the planet on a"
      },{
      "name"  : "24 Years with Montreal Protocol - Why there are two Ozone Holes?",
      "url"   : "/2011/10/24-years-with-montreal-protocol-why-there-are-two-ozone-holes",
      "img"   : "http://farm7.static.flickr.com/6105/6237947806_3a8d4b4151_s.jpg",
      "title" : "There is not much ozone in the atmosphere, all molecules at eye level would build a layer of a few millimeters"
      },{
      "name"  : "Sea Ice is not flat - Let's discuss Thickness",
      "url"   : "/2011/10/sea-ice-is-not-flat-lets-discuss-thickness",
      "img"   : "http://farm7.static.flickr.com/6159/6203339443_1d1a0d36bb_s.jpg",
      "title" : "Actually you may call it a red herring hiding the true nature of sea ice decline. It is time to put on 3D glasses and talk about volume and thickness"
      },{
      "name"  : "50 Days with CGC HEALY in the Ice",
      "url"   : "/2011/10/50-days-with-cgc-healy-in-the-ice",
      "img"   : "http://farm7.static.flickr.com/6151/6200677183_8ed36461c0_s.jpg",
      "title" : "Having a sailing webcam in the Arctic fascinated me from the first day I've found the link. Although it is only one image per hour"
      },{
      "name"  : "Silly Polar Questions",
      "url"   : "/2011/9/silly-polar-questions",
      "img"   : "http://dl.dropbox.com/u/354885/Arctic/aio/minis/eisbaer-icon.jpg",
      "title" : "Does this island go all the way down to the bottom of the sea?"
      },{
      "name"  : "Cairn Energy Oil Spill Plan for Greenland, Episode 1",
      "url"   : "/2011/9/cairn-energy-oil-spill-plan-for-greenland-episode-1",
      "img"   : "http://farm7.static.flickr.com/6191/6106412952_6b20f53b79_s.jpg",
      "title" : "On page one you are referred to page 13 in the event of an oil spill. On this page you learn you have to consult"
      },{
      "name"  : "New Sea Ice Drift Vector and SST Overlay",
      "url"   : "/2011/8/new-sea-ice-drift-vector-and-sst-overlay",
      "img"   : "http://farm7.static.flickr.com/6192/6095847353_2e14524c26_s.jpg",
      "title" : "Now close to the end of the season wind has most impact on sea ice extent and area. Depending on the average concentration"
      },{
      "name"  : "UNSC agrees on Possible Security Implications of Climate Change",
      "url"   : "/2011/7/unsc-agrees-on-possible-security-implications-of-climate-change",
      "img"   : "http://farm7.static.flickr.com/6024/5960562594_1b65604a35_s.jpg",
      "title" : "Exactly why Dr. Peter Wittig - the German permanent representative to the UN - mentions and simultaneously disclaims 'Green-Helmets'"
      },{
      "name"  : "Northern Sea Route open for Transit",
      "url"   : "/2011/7/northern-sea-route-open-for-transit",
      "img"   : "http://farm7.static.flickr.com/6004/5949706217_30f8e0b2a3_s.jpg",
      "title" : "According to nuclear.ru the Northern Passage has been successfully navigated first time this year. Two russian nuclear icebreakers"
      },{
      "name"  : "What has happened to Sea Ice last Winter?",
      "url"   : "/2011/7/what-happened-to-sea-ice-last-winter",
      "img"   : "http://farm7.static.flickr.com/6020/5922874436_2e4432d00a_s.jpg",
      "title" : "Since 10 days sea ice extent is falling of the cliff. Over the course of June it showed already little difference"
      },{
      "name"  : "No Drill - No Spill",
      "url"   : "/2011/6/no-drill-no-spill",
      "img"   : "http://farm6.static.flickr.com/5266/5874273734_d34b8010c7_s.jpg",
      "title" : "Any drilling well puts the Arctic at risk. In case of an oil spill there is not enough day light during winter, not enough ice-capable"
      },{
      "name"  : "'On the Ice' wins SIFF 2011 Prize for Best New American Film",
      "url"   : "/2011/6/on-the-ice-wins-siff-2011-prize-for-best-new-american-film",
      "img"   : "http://farm3.static.flickr.com/2723/5833337411_acc9ee5e80_s.jpg",
      "title" : "A story told with outstanding naturalistic performances with a confident, compelling narrative."
      },{
      "name"  : "Climate change is real, we are causing it, and it is happening right now.",
      "url"   : "/2011/6/climate-change-is-real-we-are-causing-it-and-it-is-happening-right-now",
      "img"   : "http://farm6.static.flickr.com/5040/5833686006_81c8e0df1b_s.jpg",
      "title" : "The overwhelming scientific evidence tells us that human greenhouse gas emissions are resulting"
      },{
      "name"  : "USGS - Estimates of Undiscovered Oil and Gas North of the Arctic Circle",
      "url"   : "/2011/6/usgs-estimates-of-undiscovered-oil-and-gas-north-of-the-arctic-circle",
      "img"   : "http://farm3.static.flickr.com/2469/5786285575_38db84be9b_s.jpg",
      "title" : "90 billion barrels of oil, 1,669 trillion ..."
      },{
      "name"  : "Oil Spill Sensitivity Atlas and Responds Plans",
      "url"   : "/2011/5/oil-spill-sensitivity-atlas-and-responds-plans",
      "img"   : "http://farm6.static.flickr.com/5109/5761749244_c65154b988_s.jpg",
      "title" : "Scottish-based Cairn Energy PLC claims it can safely explore for oil"
      },{
      "name"  : "Arctic Search and Rescue Agreement",
      "url"   : "/2011/5/arctic-search-and-rescue-agreement",
      "img"   : "http://farm3.static.flickr.com/2529/5750609577_de5054ccca_s.jpg",
      "title" : "The main emphasis of the Agreement is to develop swift and efficient measures when accidents"
      },{
      "name"  : "Video: Sea Ice Coverage from 1978 to 2008",
      "url"   : "/2011/5/video-sea-ice-coverage-from-1978-to-2008",
      "img"   : "http://farm3.static.flickr.com/2602/5743770776_151c5ccd55_s.jpg",
      "title" : " The pulses depict the annual expansion and contraction of the sea ice"
      },{
      "name"  : "Beaufort Sea getting Thinner and Thinner",
      "url"   : "/2011/5/arctic-oil-rush-continued",
      "img"   : "http://farm6.static.flickr.com/5109/5737266005_3691783a7c_s.jpg",
      "title" : "An average of 1.4 metres was measured, to compare"
      },{
      "name"  : "Arctic Oil Rush continued",
      "url"   : "/2011/5/arctic-oil-rush-continued",
      "img"   : "http://farm6.static.flickr.com/5106/5729958111_7e4e7bbdb2_s.jpg",
      "title" : "What appeared as an innocent 'talk-shop' may have pulled the trigger"
      },{
      "name"  : "Shell's New Drilling Plan",
      "url"   : "/2011/5/shells-new-drilling-plan",
      "img"   : "http://farm6.static.flickr.com/5143/5703358434_5c7871124d_s.jpg",
      "title" : "Shell Offshore Inc. submitted a revised Exploration Plan last week. The company plans"
      }
  ]
