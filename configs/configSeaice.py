
## used in seaice Handler

'''
  Docs: http://docs.python.org/library/time.html#time.strftime

print utc()                               2012-08-10
print utc(hours=-24)                      2012-08-09
print utc("%Y-%m-%d", hours=-48)          2012-08-08
print utc("%Y-%j", hours=-48)             2012-221
print utc("%Y-%m-%d %H:%M:%S", hours=-48)      

'''

from utils.clock import Clock

s = Clock().fromStamp
m = Clock().formatISO
utc = Clock().UTC  ## UTC(self, "%Y-%m-%d", hours=0, ) :

SeaiceData = [
  
## Top Gallery
  { 
    'id':     "NSDIC", 'isFixed': 1, 'info':   "NSIDC: Mean sea ice anomalies, 1953-2010", 'active': True,
    'items': [{
      'id'      : 'nsidcH1',
      }]
    },{
    'id':     "Cryosat", 'isFixed': 1, 'info':   "Sea Iee Thickness in the Arctic Ocean (Jan-Feb 2011)", 'active': True,
    'items': [{
      'id'      : 'cryosat1',
      }]
    },{
    'id':     "Sunlight", 'isFixed': 1, 'info':   "Current Sunlight Conditions", 'active': True,
    'items': [{
      'id'      : 'sunlight1',
      'title'   : "Fourmilab Day and Night",
      },{
      'id'      : 'sunlight2',
      'title'   : "Length of Days",
      }]


#### ANCHOR Satellites & Webcams
  },{  
      'anchor': "webcams-satellites", 'active': True, 
      'info': "Satellites & Webcams",

## NOAA Arctic Theme Page Web Cams    
  },{  
    'id':     "NPCams", 'active': True,
    'info':   "NOAA Arctic Theme Page Web Cams",
    'credit': "NOAA/PMEL",
    'url':    "http://psc.apl.washington.edu/northpole/",
    'description'  : "The web cams operate during the Summer warmth and daylight (April - October) and are redeployed each Spring",
    'items': [{
      'id'      : 'noaa1',
      'title'   : "North Pole Cam 1",
      'width'   : 218, 'height': 122, 'crop': '0,0,0,0', 'keep': 60 * 60,
      'url'     : "http://psc.apl.washington.edu/northpole/NPEO2015/2015cam1_1.jpg",
      'target'  : "http://psc.apl.washington.edu/northpole/NPEO2015/2015cam1_1.jpg",
      'date'    : lambda: utc("as of %Y-%m-%d %H:%M:%S UTC")
      },{
      'id'      : 'noaa2',
      'title'   : "North Pole Cam 2",
      'width'   : 218, 'height': 122, 'crop': '0,0,0,0', 'keep': 60 * 60,
      'url'     : "http://psc.apl.washington.edu/northpole/NPEO2015/2015cam2_1.jpg",
      'target'  : "http://psc.apl.washington.edu/northpole/NPEO2015/2015cam2_1.jpg",
      'date'    : lambda: utc("as of %Y-%m-%d %H:%M:%S UTC")
      }]

## O-BUOY Project
  },{  
    'id':     "obuoy", 'active': True,
    'info':   "Real-Time Telemetry Monitor",
    'credit': "O-BUOY Project",
    'url':    "http://obuoy.datatransport.org/monitor#overview/",
    'description'   : "Check out <a target='_blank' href='http://obuoy.datatransport.org/monitor#overview/gpstracks'>buoy positions</a>",
    'items': [{
      'id'      : 'obuoy1',
      'title'   : "Buoy #9",
      'width'   : 218, 'height': 164, 'crop': '0,0,0,0', 'keep': "1000", 
      'url'     : "http://obuoy.datatransport.org/data/obuoy/var/plots/buoy9/camera/webcam.jpg",
      'target'  : "http://obuoy.datatransport.org/data/obuoy/var/plots/buoy9/camera/webcam.jpg",
      'date'    : lambda: utc("as of %Y-%m-%d %H:%M:%S UTC")
      },{
      'id'      : 'obuoy2',
      'title'   : "Buoy #10",
      'width'   : 218, 'height': 164, 'crop': '0,0,0,0', 'keep': "1000", 
      'url'     : "http://obuoy.datatransport.org/data/obuoy/var/plots/buoy10/camera/webcam.jpg",
      'target'  : "http://obuoy.datatransport.org/data/obuoy/var/plots/buoy10/camera/webcam.jpg",
      'date'    : lambda: utc("as of %Y-%m-%d %H:%M:%S UTC")
      }]

## Daily Arctic & Global Mosaics
  },{  
    'id':     "lance", 'active': True,
    'info':   "Daily Arctic & Global Mosaics",
    'credit': "NASA Rapid Response System",
    'url':    "http://lance.nasa.gov/imagery/rapid-response/",
    'description'   : "The Rapid Response system provides a variety of imagery for certain products from the MODIS, AIRS, and OMI instruments. ",
    'items': [{
      'id'      : 'lance1',
      'title'   : "Arctic True Color",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://ice-map.appspot.com/tiles/?tile=" + s("year.doy-1") + ".04.001.001.arc.ter",
      'target'  : "http://lance-modis.eosdis.nasa.gov/imagery/subsets/?mosaic=Arctic." + s("yeardoy-1") + ".terra.4km.jpg",
      'date'    : lambda: utc(diff=-24)
      },{
      'id'      : 'lance2',
      'title'   : "Arctic Infrared",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://ice-map.appspot.com/tiles/?tile=" + s("year.doy-1") + ".04.001.001.arc.367",
      'target'  : "http://lance-modis.eosdis.nasa.gov/imagery/subsets/?mosaic=Arctic." + s("yeardoy-1") + ".terra.367.4km.jpg",
      'date'    : lambda: utc(diff=-24)
      },{
      'id'      : 'lance3',
      'title'   : "Hudson Bay",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://map2.vis.earthdata.nasa.gov/image-download?TIME=" + s("yeardoy-1") + "&extent=-96.70589389714425,46.939345931429514,-72.02620639714425,70.77528343142951&epsg=4326&layers=MODIS_Terra_CorrectedReflectance_TrueColor&opacities=1&worldfile=false&format=image/jpeg&width=140&height=140",
      'target'  : "http://map2.vis.earthdata.nasa.gov/image-download?TIME=" + s("yeardoy-1") + "&extent=-96.70589389714425,46.939345931429514,-72.02620639714425,70.77528343142951&epsg=4326&layers=MODIS_Terra_CorrectedReflectance_TrueColor&opacities=1&worldfile=false&format=image/jpeg&width=960&height=960",
      'date'    : lambda: utc(diff=-24)
      }]

## NOAA Aviation Weather Center
  },{  
    'id':     "noaaAv", 'active': True,
    'info':   "International Satellite Imagery (infrared, bw)",
    'credit': "NOAA Aviation Weather Center",
    'url':    "http://aviationweather.gov/obs/sat/intl/",
    'description'   : "International Satellite Imagery (infrared, bw)",
    'items': [{
      'id'      : 'noaaAv1',
      'title'   : 'ICAO Area H (Atlantic)',
      'width'   : 140, 'height': 113, 'crop': '0,0,0,0',
      'url'     : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-H_bw.jpg",
      'target'  : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-H_bw.jpg",
      'date'    : "latest"
      },{
      'id'      : 'noaaAv2',
      'title'   : 'ICAO Area I (Pacific)',
      'width'   : 140, 'height': 113, 'crop': '0,0,0,0',
      'url'     : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-I_bw.jpg",
      'target'  : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-I_bw.jpg",
      'date'    : "latest"
      },{
      'id'      : 'noaaAv3',
      'title'   : 'ICAO Area G (Asia)',
      'width'   : 140, 'height': 113, 'crop': '0,0,0,0',
      'url'     : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-G_bw.jpg",
      'target'  : "http://aviationweather.gov/data/obs/sat/intl/ir_ICAO-G_bw.jpg",
      'date'    : "latest"
      }]

## Advanced Scatterometer (ASCAT)
  },{  
    'id':     "Star", 'active': True,
    'info':   "Advanced Scatterometer (ASCAT)",
    'credit': "Center for Satellite Applications and Research (STAR)",
    'url':    "http://manati.orbit.nesdis.noaa.gov/datasets/ASCATData.php",
    'description'   : "The advanced scatterometer flies on board the meteorological operational EUMETSAT METOP satellite",
    'items': [{
      'id'      : 'Star1',
      'title'   : 'Today -1',
      'width'   : 140, 'height': 140, 'crop': '288,288,288,288',
      'url'     : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/msfa-NHe-a-"+ s("yeardoy-1") +".sir.gif" ,
      'target'  : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/msfa-NHe-a-"+ s("yeardoy-1") +".sir.gif" ,
      'date'    : lambda: utc(diff=-24)
      },{
      'id'      : 'Star2',
      'title'   : '2012',
      'width'   : 140, 'height': 140, 'crop': '288,288,288,288',
      'url'     : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/msfa-NHe-a-2013%s.sir.gif" % s("doy", -1),
      'target'  : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/msfa-NHe-a-2013%s.sir.gif" % s("doy", -1),
      'date'    : lambda: utc("2013-%m-%d", diff=-24),
      },{
      'id'      : 'Star3',
      'title'   : '2011',
      'width'   : 140, 'height': 140, 'crop': '288,288,288,288',
      'url'     : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/2012/msfa-NHe-a-2012%s.sir.gif" % s("doy", -1),
      'target'  : "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/2012/msfa-NHe-a-2012%s.sir.gif" % s("doy", -1),
      'date'    : lambda: utc("2012-%m-%d", diff=-24),
      }]
  
## Canada Infrared
  },{  
    'id':     "canir", 'active': False,
    'info':   "NOAA 18 - Infrared",
    'credit': "Environment Canada",
    'url':    "http://www.weatheroffice.gc.ca/satellite/index_e.html#hrpt",
    'description'   : "Infrared images from polar orbiting satellites",
    'items': [{
      'id'      : 'canir1',
      'title'   : 'Infrared',
      'width'   : 442, 'height': 342, 'crop': '0,0,0,0',
      'url'     : "http://www.weatheroffice.gc.ca/data/satellite/hrpt_dfo_ir_100.jpg",
      'target'  : "http://www.weatheroffice.gc.ca/data/satellite/hrpt_dfo_ir_100.jpg",
      'date'    : 'latest'
    }]

## Canada Infrared
  },{  
    'id':     "canir", 'active': True,
    'info':   "Arctic Infrared Composite",
    'credit': "Environment Canada",
    'url':    "http://www.weatheroffice.gc.ca/satellite/index_e.html#hrpt",
    'description'   : "Infrared images from polar orbiting satellites (1600x1300, ~2.2MB)",
    'items': [{
      'id'      : 'canir1',
      'title'   : 'Infrared',
      'width'   : 442, 'height': 360, 'crop': '0,0,0,0',
      'url'     : "http://noiv.pythonanywhere.com/latest/ftp/arwguest:guest@cisclient.cis.ec.gc.ca/HRPT-Resolute--ArcticComposite",
      'target'  : "http://noiv.pythonanywhere.com/latest/ftp/arwguest:guest@cisclient.cis.ec.gc.ca/HRPT-Resolute--ArcticComposite",
      'date'    : 'latest'
    }]

## IJIS RGB(36V,36H,18V)
  },{  
    'id':     "a2rgb", 'active': False,
    'info':   "AMSR2-RGB(36V,36H,18V)",
    'credit': "IJIS Sea Ice Monitor",
    'url':    "http://www.ijis.iarc.uaf.edu/cgi-bin/seaice-monitor.cgi?lang=e",
    'description'   : "False color image with BT and polarization mapped at rgb values. AMSR2 validation ongoing (1000x1000, ~1.8MB)",
    'items': [{
      'id'      : 'a2rgb1',
      'title'   : 'RGB(36V,36H,18V)',
      'width'   : 442, 'height': 432, 'crop': '120,100,120,160', 'rot':180, 
      'url'     : "http://www.ijis.iarc.uaf.edu/seaice/data/RGB/" + utc("%Y%m/AM2SI%Y%m%dRGB.jpg", diff=-24),
      'target'  : "http://www.ijis.iarc.uaf.edu/seaice/data/RGB/" + utc("%Y%m/AM2SI%Y%m%dRGB_high.png", diff=-24),
      'date'    : utc("%Y-%m-%d", diff=-24)
    }]

## Arctic Mosaic
  },{  
    'id':     "lam", 'active': True,
    'info':   "Arctic Mosaic, Terra, MODIS",
    'credit': "EOSDIS - NASA's Earth Observing Systen",
    'url':    "http://earthdata.nasa.gov/data/near-real-time-data/visualization/rapid-response",
    'description'   : "True colour daily Arctic mosaic from the Rapid Response Team. (1536x1536, ~1.1MB), also check the <a href='/explorer/'>interactive map</a>",
    'items': [{
      'id'      : 'lam1',
      'title'   : 'Arctic Mosaic',
      'width'   : 442, 'height': 442, 'crop': '0,0,0,0', 
      'url'     : "http://rapidfire.sci.gsfc.nasa.gov/imagery/subsets/?mosaic=Arctic." + utc("%Y%j.terra.4km.jpg", -36),
      'target'  : "http://rapidfire.sci.gsfc.nasa.gov/imagery/subsets/?mosaic=Arctic." + utc("%Y%j.terra.4km.jpg", -36),
      'date'    : utc("%Y-%m-%d", diff=-36)
    }]

#### ANCHOR Sea Ice Thickness
  },{  
    'anchor': "ice-thick", 'active': True, 
    'info': "Sea Ice Thickness",

## Cryosat
  },{  
    'id':     "cs", 'active': True,
    'info':   "CryoSat Operational Monitoring",
    'credit': "Centre for Polar Observation & Modelling",
    'url':    "http://www.cpom.ucl.ac.uk/csopr/seaice.html",
    'description'   : "CryoSat uses a synthetic aperture radar to sample a much smaller footprint than previous satellite radar altimeters.",
    'items': [{
      'id'      : 'cs1',
      'title'   : 'CS2 Thickness',
      'width'   : 442, 'height': 442, 'crop': '22,10,20,84',
      'url'     : "http://www.cpom.ucl.ac.uk/csopr/sidata/thk_28.png",
      'target'  : "http://www.cpom.ucl.ac.uk/csopr/sidata/thk_28_big.png",
      'date'    : 'recent 28 days'
      }]

## AMSR2
  },{  
    'id':     "athk", 'active': True,
    'info':   "Arctic Data Archive System",
    'credit': "Japan Aerospace Exploration Agency (JAXA)",
    'url':    "https://ads.nipr.ac.jp/vishop/vishop-monitor.html",
    'description'   : "This experimental product of sea ice thickness is calculated from AMSR-E and AMSR2 data by using a research algorithm developed by K. Tateyama (Kitami Institute of Technology).",
    'items': [{
      'id'      : 'athk1',
      'title'   : 'AMSR2 Thickness',
      'width'   : 442, 'height': 498, 'crop': '100,50,100,50', "rot": 180,
      'url'     : "https://ads.nipr.ac.jp/vishop/data/" + utc("%Y%m") + "/AM2SI" + utc("%Y%m%d", diff=-24) + "D_SIT_NP.png",
      'target'  : "https://ads.nipr.ac.jp/vishop/data/" + utc("%Y%m") + "/AM2SI" + utc("%Y%m%d", diff=-24) + "D_SIT_NP.png",
      'date'    : utc("%Y%m%d", diff=-24)
      }]


#### ANCHOR Sea Ice Extent & Area
  },{  
    'anchor': "snow-ice", 'active': True, 
    'info': "Ice & Snow",

## NSIDC Sea Ice Extent(15%)
  },{  
    'id':     "nsdic", 'active': True,
    'info':   "NSIDC Sea Ice Extent, Concentration",
    'credit': "NSIDC Sea Ice Index Web site",
    'url':    "http://nsidc.org/arcticseaicenews/",
    'description'   : "Scientific analysis on Arctic sea ice conditions. ",
    'items': [{
      'id'      : 'nsdic1',
      'title'   : "Extent 2014/15",
      'width'   : 140, 'height': 106, 'crop': '19,24,21,16',
      'url'     : "http://nsidc.org/data/seaice_index/images/daily_images/N_stddev_timeseries_webtmb.png",
      'target'  : "http://nsidc.org/data/seaice_index/images/daily_images/N_stddev_timeseries.png",
      'date'    : "latest"
      },{
      'id'      : 'nsdic2',
      'title'   : "Conc. 2015",
      'width'   : 140, 'height': 212, 'crop': '10,24,80,16',
      'url'     : "http://nsidc.org/data/seaice_index/images/daily_images/N_daily_concentration_dthumb.png",
      'target'  : "http://nsidc.org/data/seaice_index/images/daily_images/N_daily_concentration.png",
      'date'    : "latest"
      },{
      'id'      : 'nsdic3',
      'title'   : "Conc. 2012",
      'width'   : 140, 'height': 212, 'crop': '19,27,100,24',
      'url'     : "http://nsidc.org/data/seaice_index/images/daily_images/N_record_concentration.png",
      'target'  : "http://nsidc.org/data/seaice_index/images/daily_images/N_record_concentration.png",
      'date'    : '2012-%s' % s('doy', -1),
      }]

## Tschudi Ice Age
  },{  
    'id':     "tschu", 'active': True,
    'info':   "Sea Ice Age",
    'credit': "Fowler, Tschudi, Maslanik",
    'url':    "http://polarbear.colorado.edu/",
    'description'   : "Generated using a model using w/ ice motion vectors and ice extent and run at weekly steps. The ice is 'aged' one year the week after the date showing the minimum ice extent.",
    'items': [{
      'id'      : 'tschu1',
      'title'   : "Ice Age latest",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "iceagelatest",
      'target'  : "iceagelatest",
      'date'    : "latest"
      },{
      'id'      : 'tschu2',
      'title'   : "Ice Age 2014",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "iceageyear-1",
      'target'  : "iceageyear-1",
      'date'    : utc("2014 week %W", diff=7*24),
      },{
      'id'      : 'tschu3',
      'title'   : "Ice Age 2012",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "iceageyear-2",
      'target'  : "iceageyear-2",
      'date'    : utc("2012 week %W", diff=7*24),
      }]

## Bundesamt fuer Seeschifffahrt
  },{  
    'id':     "bsh", 'active': True,
    'info':   "Arctic Sea Ice Concentration versus Extent",
    'credit':  'Bundesamt fuer Seeschifffahrt und Hydrographie, Germany',
    'url':    "http://www.bsh.de/aktdat/mk/ICE/M54ICE_daily_e.html",
    'description'   : "Charts are based on NSIDC data <a target='_blank' href='http://www.bsh.de/aktdat/mk/ICE/Methods.html'>(methods)</a>",
    'items': [{
      'id'      : 'bsh1',
      'title'   : '2015 -2 days',
      'width'   : 140, 'height': 206,  'crop': '0,0,0,0',
      'url'     : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("%Y%m%d", diff=-48),
      'target'  : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("%Y%m%d", diff=-48),
      'date'    : utc(diff=-48),
      },{
      'id'      : 'bsh2',
      'title'   : '2014',
      'width'   : 140, 'height': 206, 'crop': '0,0,0,0',
      'url'     : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("2014%m%d", diff=-48),
      'target'  : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("2014%m%d", diff=-48),
      'date'    : utc("2013-%m-%d", diff=-48),
      },{
      'id'      : 'bsh3',
      'title'   : '2012',
      'width'   : 140, 'height': 206, 'crop': '0,0,0,0',
      'url'     : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("2012%m%d", diff=-48),
      'target'  : "http://www.bsh.de/aktdat/mk/ICE/daily/n%s.ic.gif" % utc("2012%m%d", diff=-48),
      'date'    : utc("2012-%m-%d", diff=-48),
      }]

## Jaxa
  },{  
    'id':     "Jaxa", 'active': False,
     ## 'url'     : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/201107/20110730/browse/PMtbPnAY110730V06saC.jpeg",
    'info':   "AMSR-E Brightness Temperature (ascending, vertical polarization)",
    'credit': "Japan Aerospace Exploration Agency",
    'url':    "http://www.jaxa.jp/index_e.html",
    'description'   : "Strange Description here",
    'items': [{
      'id'      : 'Jaxa1',
      'title'   : '6GHZ',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V06saC.jpeg",
      'target'  : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V06saF.jpeg",
      'date'    : s("yester/day")
      },{
      'id'      : 'Jaxa2',
      'title'   : '37GHZ',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V37saC.jpeg",
      'target'  : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V37saF.jpeg",
      'date'    : s("yester/day")
      },{
      'id'      : 'Jaxa3',
      'title'   : '89GHZ',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V89saC.jpeg",
      'target'  : "http://sharaku.eorc.jaxa.jp/AMSR/High_res/DATA/PM_fine_mesh/tb/polar_n/A/" + s("now/day/no/-1")[:6] + "/" + s("now/day/no/-1") + "/browse/PMtbPnAY" + s("now/day/no/-1")[2:] + "V89saF.jpeg",
      'date'    : s("yester/day")
      }]

## AMSR
  },{  
    'id':     "AMSR", 'active': False,
     ##    'url'     : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/2011.08.08/AMSR_E_L3_SeaIce12km_V13_20110807_brws.1.jpg",
    'info':   "Aqua AMSR-E Sea Ice Concentration",
    'credit': "NSIDC",
    'url':    "http://nsidc.org/data/ae_si12.html",
    'description'   : "Strange Description here",
    'items': [{
      'id'      : 'AMSR1',
      'title'   : '-2 days',
      'width'   : 140, 'height': 156, 'crop': '0,0,0,0',
      'url'     : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-24) , utc("%Y%m%d", diff=-48) ),
      'target'  : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-24) , utc("%Y%m%d", diff=-48) ),
      'date'    : utc(diff=-48)
      },{
      'id'      : 'AMSR2',
      'title'   : '-3 days',
      'width'   : 140, 'height': 156, 'crop': '0,0,0,0',
      'url'     : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-48) , utc("%Y%m%d", diff=-72) ),
      'target'  : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-48) , utc("%Y%m%d", diff=-72) ),
      'date'    : utc(diff=-72)
      },{
      'id'      : 'AMSR3',
      'title'   : '-4 days',
      'width'   : 140, 'height': 156, 'crop': '0,0,0,0',
      'url'     : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-72) , utc("%Y%m%d", diff=-96) ),
      'target'  : "http://n4eil01u.ecs.nasa.gov:22000/WebAccess/data/SAN/BRWS/Browse.001/%s/AMSR_E_L3_SeaIce12km_V13_%s_brws.1.jpg"  % ( utc("%Y.%m.%d", diff=-72) , utc("%Y%m%d", diff=-96) ),
      'date'    : utc(diff=-96)
      }]

## DTU-IOMASA / UNI Bremen
  },{  
    'id':     "ssmi", 'active': True,
    'info':   "Mappings of AMSR2 Sea Ice concentration",
    'credit': "DTU-IOMASA / UNI Bremen",
    'url':    "/",
    'description'   : "Mappings as produced by different institutes",
    'items': [{
      'id'      : 'ssmi1',
      'title'   : 'Kara Sea (iomasa)',
      'width'   : 140, 'height': 135, 'crop': '0,0,0,0',
      'url'     : "http://www.seaice.dk/iomasa/amsr/thin/today/AMSR2.Kara.%s.small.gif" % s("YYYYMMDD"),
      'target'  : "http://www.seaice.dk/iomasa/amsr/thin/today/AMSR2.Kara.%s.gif" % s("YYYYMMDD"),
      'date'    : "latest"
      },{
      'id'      : 'ssmi2',
      'title'   : 'Visual (Uni Bremen)',
      'width'   : 140, 'height': 206, 'crop': '30,44,32,76',
      'url'     : "http://iup.physik.uni-bremen.de:8084/amsr2/arctic_AMSR2_visual_small.jpg",
      'target'  : "http://iup.physik.uni-bremen.de:8084/amsr2/arctic_AMSR2_visual.png",
      'date'    : "latest"
      },{
      'id'      : 'ssmi3',
      'title'   : 'False Color (Uni Bremen)',
      'width'   : 140, 'height': 206, 'crop': '30,44,32,76',
      'url'     : "http://iup.physik.uni-bremen.de:8084/amsr2/arctic_AMSR2_nic_small.jpg",
      'target'  : "http://iup.physik.uni-bremen.de:8084/amsr2/arctic_AMSR2_nic.png",
      'date'    : "latest"
      }]

## AARI
  },{  
    'id':     "aari", 'active': True,
    'info':   "AARI: Ice Analysis from Satellite Images",
    'credit': "Arctic and Antarctic Research Institute",
    'url':    "http://www.aari.ru/odata/_d0015.php?lang=1",
    'description'   : "Ice charts are based on automatical generalization of regional ice charts which are compiled on a basis of analysis of satellite (visible, infra-red and radar) information and reporets from coastal stations and ships. (weekly updates)",
    'items': [{
      'id'      : 'aari1',
      'title'   : 'Ice Types',
      'width'   : 442, 'height': 310, 'crop': '38,48,50,34',
      'url'     : "http://www.aari.ru/resources/d0015/arctic/gif.en/2015/%s.GIF" % s("Last-Tue/YYYYMMDD"),
      'target'  : "http://www.aari.ru/resources/d0015/arctic/gif.en/2015/%s.GIF" % s("Last-Tue/YYYYMMDD"),
      'date'    : 'latest'
      }]

## Daily forecast 'ice coverage' from  MyOcean
  },{  
    'id':     "topaz4", 'active': True,
    'info':   "TOPAZ4: Forecast of Sea Ice Coverage",
    'credit': "MyOcean ARC MFC",
    'url':    "http://myocean.met.no/ARC-MFC/",
    'description'   : "The MyOcean ARC MFC delivers ocean forecast and analysis data produced by a coupled numerical ocean-ice model with data assimilation. ",
    'items': [{
      'id'      : 'topaz41',
      'title'   : 'Current',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+0_small.png",
      'target'  : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+0.png",
      'date'    : "latest"
      },{
      'id'      : 'topaz42',
      'title'   : '+1 day',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+1_small.png",
      'target'  : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+1.png",
      'date'    : "latest"
      },{
      'id'      : 'topaz43',
      'title'   : '+3 days',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+3_small.png",
      'target'  : "http://myocean.met.no/ARC-MFC/images/topaz4_myocean_arc_ice_T+3.png",
      'date'    : "latest"
      }]

## TOPAZ Ice Drift Forecast
  },{  
    'id':     "framTopaz", 'active': False,
    'info':   "TOPAZ Ice Drift Forecast - Fram Strait",
    'credit':  'Nansen Center',
    'url':    "http://topaz.nersc.no/Knut/IceForecast/FramStrait/",
    'description'   : "",
    'items': [{
      'id'      : 'fram1',
      'title'   : 'Conc/Velo',
      'width'   : 140, 'height': 140/4*3, 'crop': '0,0,0,0',
      'url'     : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_drift.lq.jpg"),
      'target'  : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_drift.jpg"),
      'date'    : s("now/day")
      },{
      'id'      : 'fram2',
      'title'   : 'Speed (m/s)',
      'width'   : 140, 'height': 140/4*3, 'crop': '0,0,0,0',
      'url'     : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_speed.jpg"),
      'target'  : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_speed.jpg"),
      'date'    : s("now/day")
      },{
      'id'      : 'fram3',
      'title'   : 'Thickness (m)',
      'width'   : 140, 'height': 140/4*3, 'crop': '0,0,0,0',
      'url'     : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_hice.jpg"),
      'target'  : "http://topaz.nersc.no/Knut/IceForecast/FramStrait/ice-forecast-" + m("", "%d-") + m("", "%b-") + m("", "%Y_hice.jpg"),
      'date'    : s("now/day")
      }]


#### ANCHOR Observations & Measurements
  },{  
      'anchor': "observation-measurements", 'active': True, 
      'info': "Observation & Measurements",

## Rutgers Snow Extent Climate
  },{  
    'id':     "rutDSC", 'active': True,
    'info':   "Rutgers: Snow Extent Climate Data Record",
    'credit': "Rutgers University Global Snow Lab ",
    'url':    "http://climate.rutgers.edu/snowcover/",
    'description'   : "Rutgers Snow Extent Climate Data Record",
    'items': [{
      'id'      : 'rutDSC1',
      'title'   : utc("%Y-%m-%d", diff=-24),
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("%Y%j", diff=-24) + ".png",
      'target'  : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("%Y%j", diff=-24) + ".png",
      'date'    : utc("%Y-%m-%d", diff=-24),
      },{
      'id'      : 'rutDSC2',
      'title'   : utc("2014-%m-%d", diff=-24),
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("2014%j", diff=-24) + ".png",
      'target'  : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("2014%j", diff=-24) + ".png",
      'date'    : utc("2014-%m-%d", diff=-24),
      },{
      'id'      : 'rutDSC3',
      'title'   : utc("2013-%m-%d", diff=-24),
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("2013%j", diff=-24) + ".png",
      'target'  : "http://climate.rutgers.edu/snowcover/png/daily_ims/" + utc("2013%j", diff=-24) + ".png",
      'date'    : utc("2013-%m-%d", diff=-24),
      }]

## Daily mean temperatures
  },{  
    'id':     "dmiDMT", 'active': True,
    'info':   "DMI: Daily mean temperatures",
    'credit': "Danish Meteorological Institute",
    'url':    "http://ocean.dmi.dk/arctic/meant80n.uk.php",
    'description'   : "For the Arctic area north of the 80th northern parallel, plotted with daily climate values calculated from the period 1958-2002.",
    'items': [{
      'id'      : 'dmiDMT1',
      'title'   : '2013',
      'width'   : 140, 'height': 94, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("%Y") + ".png",
      'target'  : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("%Y") + ".png",
      'date'    : utc("%Y")
      },{
      'id'      : 'dmiDMT2',
      'title'   : '2012',
      'width'   : 140, 'height': 94, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("2012") + ".png",
      'target'  : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("2012") + ".png",
      'date'    : "2012"
      },{
      'id'      : 'dmiDMT3',
      'title'   : '2007',
      'width'   : 140, 'height': 94, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("2007") + ".png",
      'target'  : "http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_" + utc("2007") + ".png",
      'date'    : "2007"
      }]

## UniCologne
  },{  
    'id':     "UniCologne", 'active': False,
    'info':   "Surface Observations, Sea Level Pressure, SST from Buoys/Ships",
    'credit': "University of Cologne",
    'url':    "http://www.meteo.uni-koeln.de/meteo.php?show=En_We_We",
    'description'   : "Temperatur, total cloud cover, wind, sig. weather. EURAD MM5 model Forecast 2mT hPa 24H",
    'items': [{
      'id'      : 'colNNWW',
      'title'   : "SFC Oberservations",
      'width'   : 140, 'height': 131, 'crop': '20,20,20,20',
      'url'     : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/synNNWWarctisicon.gif",
      'target'  : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/synNNWWarctis.gif",
      'date'    : "latest"
      },{
      'id'      : 'colSLP',
      'title'   : "2mT, SLP, Weather",
      'width'   : 140, 'height': 131, 'crop': '20,20,20,20',
      'url'     : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/arcisoTTPPWWicon.gif",
      'target'  : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/arcisoTTPPWW.gif",
      'date'    : "latest"
      },{
      'id'      : 'colSST',
      'title'   : 'Snow Depth, SST',
      'width'   : 140, 'height': 131, 'crop': '20,30,20,30',
      'url'     : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/snowarctisicon.gif",
      'target'  : "http://www.uni-koeln.de/math-nat-fak/geomet/meteo/winfos/snowarctis.gif",
      'date'    : "latest"
      }]

## Data from Weatherstations
  },{  
    'id':     "Stations01", 'active': True,
    'info':   "Data from Arctic Weatherstations",
    'credit': "wetterzentrale.de",
    'url':    "http://www.wetterzentrale.de/topkarten/fsbeobl.html",
    'description'   : "Temperature, Wind",
    'items': [{
      'id'      : 'wz-stations01',
      'title'   : "Temperature",
      'width'   : 140, 'height': 167, 'crop': '330,360,400,180',
      'url'     : "http://www.wetterzentrale.de/pics/Rarcmapt.gif",
      'target'  : "http://www.wetterzentrale.de/pics/Rarcmapt.gif",
      'date'    : "latest"
      },{
      'id'      : 'wz-stations02',
      'title'   : "Actual Weather",
      'width'   : 140, 'height': 167, 'crop': '230,270,200,170',
      'url'     : "http://www.wetterzentrale.de/pics/Rarcmapx.gif",
      'target'  : "http://www.wetterzentrale.de/pics/Rarcmapx.gif",
      'date'    : "latest"
      },{
      'id'      :'wz-stations03',
      'title'   : 'Wind',
      'width'   : 140, 'height': 167, 'crop': '230,270,200,170',
      'url'     : "http://www.wetterzentrale.de/pics/Rarcmapw.gif",
      'target'  : "http://www.wetterzentrale.de/pics/Rarcmapw.gif",
      'date'    : "latest"
      }]


#### ANCHOR Ocean Parameter
  },{  
      'anchor': "ocean-parameters", 'active': True, 
      'info': "Ocean Parameter",

## GLOBSST
  },{  
    'id':     "gsst", 'active': True,
    'info':   "MyOcean: Global Sea Surface Temperature",
    'credit': "MyOcean SST-TAC",
    'url':    "http://myocean.met.no/SST-TAC/",
    'description'   : "Analysed SST. Includes observations from AATSR, AVHRR SAFNAR, AVHRR NAVO_G, AMSRE (Metop-A)",
    'items': [{
      'id'      : 'gsst1',
      'title'   : 'Global SST',
      'width'   : 442, 'height': 219, 'crop': '43,66,43,88',
      'url'     : "http://ocean.dmi.dk/arctic/satellite/plots/satsst.gbl.d-30.png",
      'target'  : "http://ocean.dmi.dk/arctic/satellite/plots/satsst.gbl.d-30.png",
      'date'    : 'latest'
      }]

## MyOcean SST-TAC
  },{  
    'id':     "mySST", 'active': True,
    'info':   "Sea Surface Temperature, Northern Hemisphere",
    'credit': "MyOcean SST-TAC",
    'url':    "http://myocean.met.no/SST-TAC/analysis/index.html",
    'description'   : "Analysed SST. Includes observations from AATSR, AVHRR SAFNAR, AVHRR NAVO_G, AMSRE (Metop-A)",
    'items': [{
      'id'      : 'mySST1',
      'title'   : 'Temperature',
      'width'   : 140, 'height': 176, 'crop': '0,0,0,0',
      'url'     : "http://myocean.met.no/SST-TAC/oi_latest.asc_sm.png",
      'target'  : "http://myocean.met.no/SST-TAC/oi_latest.asc_sm.png",
      'date'    : "latest"
      },{
      'id'      : 'mySST2',
      'title'   : 'Anomaly',
      'width'   : 140, 'height': 176, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/satellite/plots/satanom.arc.d-00.png",
      'target'  : "http://ocean.dmi.dk/arctic/satellite/plots/satanom.arc.d-00.png",
      'date'    : "latest"
      },{
      'id'      : 'mySST3',
      'title'   : 'Increment',
      'width'   : 140, 'height': 176, 'crop': '0,0,0,0',
      'url'     : "http://myocean.met.no/SST-TAC/incr_latest.asc.png",
      'target'  : "http://myocean.met.no/SST-TAC/incr_latest.asc.png",
      'date'    : "latest"
      }]

## DMI: Temperature, Pressure, Sea Surface Temp
  },{  
    'id':     "dmiWEA", 'active': False,
    'info':   "DMI: SST Analysis",
    'credit': "Centre for Ocean and Ice in the Arctic Ocean",
    'url':    "http://ocean.dmi.dk/arctic/satellite/index.uk.php",
    'description'   : "Temperature, Pressure, Sea Surface Temperature",
    'items': [{
      'id'      : 'dmiWEA1',
      'title'   : 'Temperature',
      'width'   : 140, 'height': 194, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/weather/temp_latest.big.png",
      'target'  : "http://ocean.dmi.dk/arctic/weather/temp_latest.big.png",
      'date'    : "latest"
      },{
      'id'      : 'dmiWEA2',
      'title'   : 'Pressure',
      'width'   : 140, 'height': 194, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/weather/mslp_latest.big.png",
      'target'  : "http://ocean.dmi.dk/arctic/weather/mslp_latest.big.png",
      'date'    : "latest"
      },{
      'id'      : 'dmiWEA3',
      'title'   : 'SST',
      'width'   : 140, 'height': 167, 'crop': '0,0,0,0',
      'url'     : "http://ocean.dmi.dk/arctic/satellite/plots/satsst.arc.d-00.png",
      'target'  : "http://ocean.dmi.dk/arctic/satellite/plots/satsst.arc.d-00.png",
      'date'    : "latest"
      }]

## SST median and OSTIA anomalies (NCEP)
  },{  
    'id':     "ghrsst", 'active': False,
    'info':   "NCEP/OSTIA: SST median and anomalies",
    'credit': "Group for High Resolution Sea Surface Temperature",
    'url':    "https://www.ghrsst.org/",
    # 'action': 'test',
    'description'   : "The Group for High-Resolution Sea Surface Temperature provides a new generation of global high-resolution (<10km) SST products to the operational oceanographic, meteorological, climate and general scientific community.",
    'items': [{
      'id'      : 'ghrsst1',
      'title'   : 'Median',
      'width'   : 218, 'height': 218, 'crop': '9,371,264,5',
      'url'     : "https://www.ghrsst.org/files/pages/original/ensemble-sst-median.png",
      'target'  : "https://www.ghrsst.org/files/pages/original/ensemble-sst-median.png",
      'date'    : "latest"
      },{
      'id'      : 'ghrsst2',
      'title'   : 'Anomaly',
      'width'   : 218, 'height': 218, 'crop': '24,326,280,3',
      'url'     : "https://www.ghrsst.org/files/pages/original/ensemble-sst-anomaly.png",
      'target'  : "https://www.ghrsst.org/files/pages/original/ensemble-sst-anomaly.png",
      'date'    : "latest"
      }]

## met.no: Sea Surface Temp (Forecast)
  },{  
    'id':     "metno", 'active': False,
    'info':   "met.no: Sea Surface Temp (Forecast).",
    'credit': "Meteorologisk institutt",
    'url':    "http://met.no/",
    'description'   : "",
    'items': [{
      'id'      : 'metno1',
      'title'   : 'SST',
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://retro.met.no/images/image_000379_1332472818.png",
      'target'  : "http://retro.met.no/images/image_000379_1332472818.png",
      'date'    : "Today"
      },{
      'id'      : 'metno2',
      'title'   : "SST",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://retro.met.no/images/image_000383_1332472818.png",
      'target'  : "http://retro.met.no/images/image_000383_1332472818.png",
      'date'    : "+1 day"
      },{
      'id'      : 'metno3',
      'title'   : "SST",
      'width'   : 140, 'height': 140, 'crop': '0,0,0,0',
      'url'     : "http://retro.met.no/images/image_000391_1332472818.png",
      'target'  : "http://retro.met.no/images/image_000391_1332472818.png",
      'date'    : "+3 days"
      }]


#### ANCHOR Arctic Buoys
  },{  
      'anchor': "arctic-buoys", 'active': True, 
      'info': "Arctic Buoys",

## 60 Day Drift Track
  },{  
    'id':     "iabp", 'active': True,
    'info':   "IABP: 60 Day Drift Track",
    'credit': "International Arctic Buoy Programme",
    'url':    "http://iabp.apl.washington.edu/",
    'description'   : "The IABP maintains a network of drifting buoys in the Arctic Ocean to provide meteorological and oceanographic data for real-time operational requirements and research purposes",
    'items': [{
      'id'      : 'iabp1',
      'title'   : 'Arctic Ocean',
      'width'   : 218, 'height': 172,  'crop': '120,80,240,140',
      'url'     : "http://iabp.apl.washington.edu/DAILYMAPS/dailyiceconc_60daytrack.jpg",
      'target'  : "http://iabp.apl.washington.edu/DAILYMAPS/dailyiceconc_60daytrack.jpg",
      'date'    : "latest"
      },{
      'id'      : 'iabp2',
      'title'   : 'Nares Strait',
      'width'   : 218, 'height': 265, 'crop': '2,10,220,280',
      'url'     : "http://iabp.apl.washington.edu/DAILYMAPS/dailymap.nares.60day.jpg",
      'target'  : "http://iabp.apl.washington.edu/DAILYMAPS/dailymap.nares.60day.jpg",
      'date'    : "latest"
      }]

  # },{  #### ANCHOR Forecast & Analysis
  #     'anchor': "forecast-analysis", 'active': False, 
  #     'info': "Forecast & Analysis",
  # },{  ## 850 mb Temperature Anomaly
  #   'id':     "esrlncep", 'active': True,
  #   'info':   "NCEP/NMC: Ensemble Forecast, 850 mb Temperature Anomaly Probability (2 sigma)",
  #   'credit': "Earth System Research Laboratory",
  #   'url':    "http://www.esrl.noaa.gov/psd/map/images/ens/ens.html#nh",
  #   'description'   : "The ensemble mean 850 mb temp anomaly is calculated by subtracting a 1979-95 climatology from the forecast data at a particular forecast hour.",
  #   'items': [{
  #     'id'      : 'ncep1',
  #     'title'   : "Current",
  #     'width'   : 140, 'height': 167, 'crop': '100,140,100,140',
  #     'url'     : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f000_nhsm.gif",
  #     'target'  : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f000_nhsm.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'ncep2',
  #     'title'   : "+24 hours",
  #     'width'   : 140, 'height': 167, 'crop': '100,140,100,140',
  #     'url'     : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f024_nhsm.gif",
  #     'target'  : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f024_nhsm.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'ncep3',
  #     'title'   : '+72 hours',
  #     'width'   : 140, 'height': 167, 'crop': '100,140,100,140',
  #     'url'     : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f072_nhsm.gif",
  #     'target'  : "http://www.esrl.noaa.gov/psd/map/images/ens/t850std2_f072_nhsm.gif",
  #     'date'    : "latest"
  #     }]
  # },{  ## Meteociel.fr
  #   'id':     "ciel", 'active': True,
  #   'info':   "ECMWF, z500-PRMSL, (%s, 12h run)" % utc(diff=-36),
  #   'credit': "Meteociel.fr",
  #   'url':    "http://meteociel.fr/modeles/ecmwf.php",
  #   'description'   : "The  ECMWF operational medium- and extended-range forecasts and a state-of-the-art super-computing facility for scientific research. ",
  #   'action': 'test',
  #   'items': [{
  #     'id'      : 'ciel1',
  #     'title'   : 'Analysis',
  #     'width'   : 140, 'height': 174, 'crop': '220,180,220,180',
  #     'url'     : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-0.GIF" % utc("%Y%m%d", diff=-24),
  #     'target'  : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-0.GIF" % utc("%Y%m%d", diff=-24),
  #     'date'    : utc("%Y-%m-%d 00z anls", diff=-24)
  #     },{
  #     'id'      : 'ciel2',
  #     'title'   : '+5 day',
  #     'width'   : 140, 'height': 174, 'crop': '220,180,220,180',
  #     'url'     : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-120.GIF" % utc("%Y%m%d", diff=-24),
  #     'target'  : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-120.GIF" % utc("%Y%m%d", diff=-24),
  #     'date'    : utc("%Y-%m-%d 00z fcst", diff=96)
  #     },{
  #     'id'      : 'ciel3',
  #     'title'   : '+ 10 days',
  #     'width'   : 140, 'height': 174, 'crop': '220,180,220,180',
  #     'url'     : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-240.GIF" % utc("%Y%m%d", diff=-24),
  #     'target'  : "http://meteociel.fr/modeles/ecmwf/runs/%s12/ECH1-240.GIF" % utc("%Y%m%d", diff=-24),
  #     'date'    : utc("%Y-%m-%d 00z fcst", diff=216)
  #     }]
  # },{  ## wetterpool.de
  #   'id':     "pool", 'active': True,
  #   'info':   "GFS Analysis: Max Temp, Wind 10m, Snow + Ice",
  #   'credit': "wetterpool.de",
  #   'url':    "http://www.wetterpool.de/prognosekarten.php",
  #   'description'   : "GFS Model",
  #   'items': [{
  #     'id'      : 'pool1',
  #     'title'   : 'max. Temp.',
  #     'width'   : 140, 'height': 152, 'crop': '340,200,340,200',
  #     'url'     : "http://www.wetterpool.eu/png/NHem/current/tmax2m_%s00z.png" % utc("%Y%m%d"),
  #     'target'  : "http://www.wetterpool.eu/png/NHem/current/tmax2m_%s00z.png" % utc("%Y%m%d"),
  #     'date'    : lambda: utc("%Y-%m-%d 00z")
  #     },{
  #     'id'      : 'pool2',
  #     'title'   : 'Wind 10m',
  #     'width'   : 140, 'height': 152, 'crop': '340,200,340,200',
  #     'url'     : "http://www.wetterpool.eu/png/NHem/current/wind10m_%s00z.png" % utc("%Y%m%d"),
  #     'target'  : "http://www.wetterpool.eu/png/NHem/current/wind10m_%s00z.png" % utc("%Y%m%d"),
  #     'date'    : lambda: utc("%Y-%m-%d 00z")
  #     },{
  #     'id'      : 'pool3',
  #     'title'   : 'Snow + Sea Ice',
  #     'width'   : 140, 'height': 152, 'crop': '340,200,340,200',
  #     'url'     : "http://www.wetterpool.eu/png/NHem/current/ptyp_%s00z.png" % utc("%Y%m%d"),
  #     'target'  : "http://www.wetterpool.eu/png/NHem/current/ptyp_%s00z.png" % utc("%Y%m%d"),
  #     'date'    : lambda: utc("%Y-%m-%d 00z")
  #     }]
  # },{  ## GFS Model Forecast: 2m Temperature
  #   'id':     "gfs2m", 'active': True,
  #   'info':   "GFS Forecast: 2m Temperature",
  #   'credit': "wetterzentrale.de",
  #   'url':    "http://www.wetterzentrale.de/topkarten/fsavnnh.html",
  #   'description'   : "latest available images",
  #   'items': [{
  #     'id'      : 'gfs2m1',
  #     'title'   : 'Analysis',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn003.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn003.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'gfs2m2',
  #     'title'   : '+24 hours',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn243.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn243.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'gfs2m3',
  #     'title'   : '+72 hours',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn723.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn723.gif",
  #     'date'    : "latest"
  #     }]
  # },{  ## GFS Model Forecast, 850hPa Temperature
  #   'id':     "gfs850hPa", 'active': True,
  #   'info':   "GFS Forecast, 850hPa Temperature",
  #   'credit': "wetterzentrale.de",
  #   'url':    "http://www.wetterzentrale.de/topkarten/fsavnnh.html",
  #   'description'   : "latest available images",
  #   'items': [{
  #     'id'      : 'gfs850hPa1',
  #     'title'   : 'Analysis',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn002.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn002.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'gfs850hPa2',
  #     'title'   : '+24 hours',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn242.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn242.gif",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'gfs850hPa3',
  #     'title'   : '+72 hours',
  #     'width'   : 140, 'height': 172, 'crop': '220,160,260,160',
  #     'url'     : "http://www.wetterzentrale.de/pics/Rhavn722.gif",
  #     'target'  : "http://www.wetterzentrale.de/pics/Rhavn722.gif",
  #     'date'    : "latest"
  #     }]
  # },{  ## D. Kelly O\'Day
  #   'id':     "proc", 'active': False,
  #   'info':   "Comparisons based on JAXA and UIUC data",
  #   'credit':  'D. Kelly O\'Day - ProcessTrends.Com',
  #   'url':    "http://processtrends.com/RClimate.htm",
  #   'description'   : "Updates start in second half of year",
  #   'items': [{
  #     'id'      : 'proc1',
  #     'title'   : 'Jaxa Extent',
  #     'width'   : 140, 'height': 105, 'crop': '0,0,0,0',
  #     'url'     : "http://processtrends.com/images/RClimate_JAXA_Arctic_SIE_latest.png",
  #     'target'  : "http://processtrends.com/images/RClimate_JAXA_Arctic_SIE_latest.png",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'proc2',
  #     'title'   : 'SIE Daily Change 07/11',
  #     'width'   : 140, 'height': 94, 'crop': '0,0,0,0',
  #     'url'     : "http://processtrends.com/images/RClimate_JAXA_ASIE_derivative.png",
  #     'target'  : "http://processtrends.com/images/RClimate_JAXA_ASIE_derivative.png",
  #     'date'    : "latest"
  #     },{
  #     'id'      : 'proc3  ',
  #     'title'   : 'Area Anomaly',
  #     'width'   : 140, 'height': 206, 'crop': '0,0,0,0',
  #     'url'     : "http://processtrends.com/images/RClimate_UIUC_SIA_Anom_latest.png",
  #     'target'  : "http://processtrends.com/images/RClimate_UIUC_SIA_Anom_latest.png",
  #     'date'    : "latest"
  #     }]

}]
