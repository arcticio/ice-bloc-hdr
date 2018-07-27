
from utils.clock import Clock
m = Clock().formatISO

## http://saf.met.no/p/ice/nh/conc/tums/
## http://topaz.nersc.no/Knut/IceForecast/FramStrait/

archive = {
  "ns-G02135-ca": {
    "start":  "1979-01-01", "end": "9999-99-99", "active": True,
    "title":  "Sea Ice Index (Concentration Anomalies)",
    "credit": "NSIDC",
    "home" :  "http://nsidc.org/data/g02135.html",
    "root":   "ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/",
    "flex"  :  lambda d: "%s/N_%s_anom.png" % ( m(d,"%b"), m(d,"%Y%m") ),
  },
  "ns-G02135-e": {
    "start":  "1979-01-01", "end": "9999-99-99", "active": True,
    "title":  "Sea Ice Index (Extent)",
    "credit": "NSIDC",
    "home" :  "http://nsidc.org/data/g02135.html",
    "root":   "ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/",
    "flex"  :  lambda d: "%s/N_%s_extn.png" % ( m(d,"%b"), m(d,"%Y%m") ),
  },
  "ns-G02135-c": {
    "start":  "1979-01-01", "end": "9999-99-99", "active": True,
    "title":  "Sea Ice Index (Concentration)",
    "credit": "NSIDC",
    "home" :  "http://nsidc.org/data/g02135.html",
    "root":   "ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/",
    "flex"  :  lambda d: "%s/N_%s_conc.png" % ( m(d,"%b"), m(d,"%Y%m") ),
  },
  "nl-terra-tc": {
    "start":  "2009-03-18", "end": "9999-99-99", "active": True,
    "title":  "Daily Arctic Mosaic (MODIS-Terra)",
    "credit": "NASA Lance",
    "home" :  "http://lance.nasa.gov/imagery/rapid-response/",
    "root" :  "http://lance-modis.eosdis.nasa.gov/imagery/subsets/?mosaic=Arctic.",
    "flex" :  lambda d: "%s.terra.4km.jpg" % ( m(d,"%Y%j") )
  },
  "wz-gfs-850": {
    "start":  "1999-01-01", "end": "9999-99-99", "active": True,
    "title":  "MRF/AVN Model 00z, 850hPa Temperature",
    "credit": "WetterZentrale.de",
    "home" :  "http://www.wetterzentrale.de",
    "root" :  "http://www.wetterzentrale.de/archive",
    "flex" :  lambda d: "/%s/avn/Rhavn002%s.png" % ( m(d,"%Y"), m(d,"%Y%m%d") )
  },
  "msfa-ascat": {
    "start":  "2010-01-01", "end": "9999-99-99", "active": True,
    "title":  "Advanced Scatterometer (ASCAT)",
    "credit": "Ocean Surface Winds Team",
    "home" :  "http://manati.orbit.nesdis.noaa.gov/",
    "root" :  "http://manati.orbit.nesdis.noaa.gov/ascat_images/ice_image/msfa-NHe-a-",
    "flex" :  lambda d: "%s.sir.gif" % ( m(d,"%Y%j") )
  },
  "knmi-pano-o500": {
    "start":  "1981-01-01", "end": "9999-99-99", "active": True,
    "title":  "500mb Height (observed)",
    "credit": "KNMI Climate Explorer (NCEP/NCAR)",
    "home" :  "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "root":   "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "flex"  : lambda d: "%s/z500_ncepncar_f_%s%s.png" % ( m(d,"%Y"), (m(d,"%b")).lower(), m(d,"%Y") ),
  },
  "knmi-pano-pa": {
    "start":  "1981-01-01", "end": "9999-99-99", "active": True,
    "title":  "Sea-Level Pressure Anomaly",
    "credit": "KNMI Climate Explorer (NCEP/CPC)",
    "home" :  "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "root":   "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "flex"  : lambda d: "%s/slp_ncepncar_%s%s.png" % ( m(d,"%Y"), (m(d,"%b")).lower(), m(d,"%Y") ),
  },
  "knmi-pano-ta": {
    "start":  "1981-01-01", "end": "9999-99-99", "active": True,
    "title":  "Temperatur (2m) Anomaly",
    "credit": "KNMI Climate Explorer (NCEP/CPC)",
    "home" :  "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "root":   "http://www.knmi.nl/klimatologie/monthly_overview_world_weather/",
    "flex"  : lambda d: "%s/t2m_ghcncams_%s%s.png" % ( m(d,"%Y"), (m(d,"%b")).lower(), m(d,"%Y") ),
  },
  "XXXXXXX": {
    "start":  "2010-01-01", "end": "9999-99-99", "active": False,
    "title":  "",
    "credit": "",
    "home" :  "",
    "root":   "",
    "flex"  : lambda d: "%s" % ( m(d,"%Y") ),
  },


}




class Archive(object):
  def __init__(self, datum=""):
    self.items = []
    if datum :
      for item in archive :
        entry = archive[item]
        if entry['active'] == True :
          if entry['start'] <= datum and entry['end'] >= datum :
            entry['url'] = entry['root'] + entry['flex'](datum)
            entry['sig'] = item
            self.items.append(entry)

  def get(self):
    return self.items
