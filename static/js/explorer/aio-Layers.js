/*jslint bitwise: true, browser: true, evil:true, devel: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals IMAGEOVERLAYROOT,dataTimeRanges, L, H, TIM, TimeRange, utc */


// AIzaSyCpNU_zklhsfdODQXAMyGQwS53kEHoBEGM

/*
min/max index = 0/30
Add layer as JSON
Add timeRange if canDate
Add as Overlay to base
*/

var Crs, Scripts = {}, Layers = {crs: {}, base: [], over: []}, timeRanges = {};

// updated 2018-07
timeRanges['arc-sentinel']  = new TimeRange("2018-03-01", utc().delta('hours', -48).toIso(3));

// updated 2018-07
timeRanges['arc-gibs']      = new TimeRange("2000-03-01", utc().delta('hours', -4).toIso(3));
timeRanges['ant-gibs']      = new TimeRange("2000-03-01", utc().delta('hours', -4).toIso(3));
timeRanges['ter-gibs']      = new TimeRange("2000-03-01", utc().delta('hours', -4).toIso(3));

// give full range, but change default
['arc-gibs', 'ant-gibs', 'ter-gibs'].forEach(function(token){
  var latest = utc(timeRanges[token].latest()).delta("hours", -8).toIso(3);
  timeRanges[token].latest = function(){return latest;};
});

timeRanges['sit-cryosat']   = new TimeRange()
  .push("2011-01", "2013-03");

timeRanges['test-m']        = new TimeRange("2013-08", "2013-10");
timeRanges['test-d']        = new TimeRange("2013-10-28", "2013-11-02");
timeRanges['test-h']        = new TimeRange("2013-11-02-00", "2013-11-04-00");

if (!dataTimeRanges){

  // ftp://ftp-projects.zmaw.de/seaice/AMSR2/3.125km/
  timeRanges['sic-amsr2']     = new TimeRange()
    .push("2013-03-01", utc().delta('days', -1).toIso(3));

  timeRanges['sit-smos']      = new TimeRange()
    .push("2011-01-01", "2011-01-10")
    .push("2012-10-15", "2012-10-31")
    .push("2013-02-01", "2013-04-15")
    .push("2013-10-13", "2013-10-19");

  timeRanges['gfs-forecast']  = new TimeRange()
    .push("2013-12-01-00", utc().delta('days', 4).toIso(3) + "-18");       


} else {

  // timeRanges['sic-amsr2']     = new TimeRange();
  // timeRanges['sit-smos']      = new TimeRange();
  // timeRanges['gfs-forecast']  = new TimeRange();
  // timeRanges['sit-piomas']    = new TimeRange();
  // timeRanges['sst-avhrr']     = new TimeRange();

  (function(){
    var name;
    for (name in dataTimeRanges) {

      // console.log(name);

      if (dataTimeRanges.hasOwnProperty(name) && name !== "stamp") {
        if (timeRanges[name] === undefined){
          timeRanges[name] = new TimeRange();
        }
        dataTimeRanges[name].forEach(function(r){
          timeRanges[name].push(r[0], r[1]);
        });
      }

    }
  })();

}


Crs = {
  
  '3413'  : function (zoomInfo, key) {
              return new L.Proj.CRS.TMS('EPSG:3413',
                '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
                [-4194304, -4194304, 4194304, 4194304],
                {resolutions: 
                  [131072, 65536, 32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1],
                  // 0       1     2      3     4      5    6       7    8    9    10  11  12
                  zoomInfo: zoomInfo,
                  key: key,
                  epsg: "3413",
                  domain: "NH"
                }
              );},


  '3995'  : function (zoomInfo, key) {
              return new L.Proj.CRS('EPSG:3995',
                // '+proj=stere +lat_0=90 +lat_ts=71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
                '+proj=stere +lat_0=90 +lat_ts=71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs',
                [-4194304, 4194304, 4194304, -4194304],
                {resolutions: 
                  [131072, 65536, 32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1],
                  // 0       1     2      3     4      5    6       7    8    9
                  zoomInfo: zoomInfo,
                  key: key,
                  epsg: "3995",
                  domain: "NH"
                }
              );},


  '3031'  : function (zoomInfo, key) {
              return new L.Proj.CRS.TMS('EPSG:3031',
                '+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
                [-4194304, -4194304, 4194304, 4194304],
                {resolutions: 
                  [131072, 65536, 32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16 ,8, 4, 2, 1],
                  // 0       1     2      3     4      5    6       7    8    9
                  zoomInfo: zoomInfo,
                  key: key,
                  epsg: "3031",
                  domain: "SH"
                }
              );},

  '4326'  : function (zoomInfo, key) {
              return new L.Proj.CRS.TMS('EPSG:4326',
                '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
                [-180, -90, 180, 90],
                {resolutions: 
                  [
                    360/(512 + 128), 
                    360/(512 + 128)/2,
                    360/(512 + 128)/4,
                    360/(512 + 128)/8,
                    360/(512 + 128)/16,
                    360/(512 + 128)/32,
                    360/(512 + 128)/64,
                    360/(512 + 128)/128,
                    360/(512 + 128)/256
                  ],
                  zoomInfo: zoomInfo,
                  key: key,
                  epsg: "3413",
                  domain: "PL"
                }
              );
            },

  '3857'  : function(zoomInfo, key){
              return L.extend(L.CRS.EPSG3857, {options: {
                zoomInfo: zoomInfo, 
                key: key, 
                epsg: "3413",
                domain: "PL"
              }});
            }
};

Layers = {
  
  base : [


////////////// G O O G L E  ///////////////////////////////////////////////////

    {'goo-sat' :    { enabled: true, index: 1, type: "base", order: 100,
        name: "Google Satellite",
        icon: "/images/explorer/maps/goo-sat-icon.png",
        comment: "Google's high resolution satellite map.",
        epsg: "3857",
        tms: false,
        latlngzoom: [34, 13, 1],
        zoom: {diff: 0, min: 0, max: 18},
        getTL: function(key){ return new L.Google('SATELLITE', {attribution: '', key: key});}
      }
    },

    // {'goo-rod' :    { enabled: false, index: 2, type: "base", order: 110,
    //     name: "Google Roadmap",
    //     icon: "/images/explorer/maps/goo-rod-icon.png",
    //     comment: "Nearly all streets of the planet.",
    //     epsg: "3857",
    //     tms: false,
    //     latlngzoom: [34, 13, 1],
    //     zoom: {diff: 0, min: 0, max: 18},
    //     getTL: function(key){ return new L.Google('ROADMAP', {attribution: '', key: key});}
    //   }
    // },


////////////// M A S K  ///////////////////////////////////////////////////////

    {'arc-data' :    { enabled: true, index: 0, type: "base",  order: 10,
        epsg: "3413",
        name: "Arctic - Data",
        icon: "/images/explorer/maps/arc-mask-icon.png",
        comment: "Land mask with multiple overlays: forecast, concentration, thickness, pemafrost, etc.",
        latlngzoom: [90, 0, 3],
        zoom: {min: 3, max: 6, off: 0, diff: 0},
        zoomAlt : {min: 4, max: 6, off: 1, diff: 0},
        overlays: ['gfs-forecast', 'sic-amsr2', "sit-smos", 'sit-cryosat', 'sst-avhrr', 'sit-piomas', 'gfs-simulation', 'labels-cities', 'labels-features', 'labels-economy'],
        getTL: function(key, zoom, fnDate){ 
          return new L.Proj.TileLayer.TMS('/images/explorer/layers/arc-mask/arc-mask-{z}-{y}-{x}.png', 
            Crs['3413'](zoom, key), {
              transpic: "/images/explorer/trans.512.png",
              noBlack: true,
              tms: false,
              minZoom: 0,
              maxZoom: zoom.max - zoom.min,
              attribution: '',
              tileSize: 512,
              noWrap: true,
              continuousWorld: true,
              key: key
        });}

      }

    },


////////////// M O S A   ///////////////////////////////////////////////////////

    // {'arc-false-test' :    { enabled: false, index: 13, type: "base",  order: 0,
    //     epsg: "3413",
    //     name: "Arctic - False Test",
    //     icon: "/images/explorer/maps/arc-721-icon.png",
    //     comment: "Layer with false colors, saturation of the blue band indicates 'ice wetness",
    //     timeRange: timeRanges['arc-gibs'],
    //     latlngzoom: [90, 0, 5],
    //     zoom: {min:3, max: 9, off: 0, diff: 0},
    //     overlays: ['sic-amsr2', 'labels-cities', 'labels-features'],
    //     getTL: function(key, zoom, fnDate){ 
    //       // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Terra_CorrectedReflectance_Bands721/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
    //       return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'terra/{s}.{d}.{z}.{y}.{x}', 
    //         Crs['3413'](zoom, key), {
    //           subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
    //           noBlack: true, tms: false, // keep this shit
    //           transpic: "/images/explorer/trans.512.png",
    //           minZoom: 0, maxZoom: zoom.max - zoom.min,
    //           attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
    //           tileSize: 512, noWrap: true, continuousWorld: true,
    //           key: key,
    //           zoomOffset: -1
    // });}}},


    // {'arc-mosa' :    { enabled: false, index: 13, type: "base",  order: 9,
    //     epsg: "3413",
    //     name: "Arctic - Mosa",
    //     icon: "/images/explorer/maps/arc-mask-icon.png",
    //     comment: "2 Levels 367 Example",
    //     latlngzoom: [90, 0, 3],
    //     zoom: {min:4, max: 9, off: 0, diff: 0},
    //     overlays: ['labels-features'],
    //     getTL: function(key, zoom, fnDate){ 
    //       return new L.Proj.TileLayer.TMS('/images/explorer/layers/arc-mosa/arc-mosa-{z}-{y}-{x}.png', 
    //         Crs['3413'](zoom, key), {
    //           transpic: "/images/explorer/trans.512.png",
    //           noBlack: true,
    //           tms: false,
    //           minZoom: 0,
    //           maxZoom: zoom.max - zoom.min,
    //           attribution: '',
    //           tileSize: 512,
    //           noWrap: true,
    //           continuousWorld: true,
    //           key: key
    // });}}},


// ////////////// T E S T  ///////////////////////////////////////////////////////

  //     {'arc-test' :    { enabled: true, index: 9, type: "base",  order: 9,
  //         epsg: "3413",
  //         name: "Arctic - Test",
  //         icon: "/images/explorer/maps/arc-mask-icon.png",
  //         comment: "Data layer with multiple overlays: buoys, temperature, forecasts, etc.",
  //         latlngzoom: [90, 0, 3],
  //         // zoom: {diff: 4, min: 0, max: 3, off: 1},
  //         zoom: {min: 4, max: 6, off: 1, diff: 0},
  //         overlays: ['labels-features'],
  //         getTL: function(key, zoom, fnDate){ 
  //           return new L.Proj.TileLayer.TMS('layers/arc-mask/arc-mask-{z}-{y}-{x}.png', 
  //             Crs['3413'](zoom, key), {
  //               transpic: "/images/explorer/trans.512.png",
  //               noBlack: true,
  //               tms: false,
  //               minZoom: 0,
  //               // maxZoom: 3,
  //               // minZoom: zoom.min - zoom.diff,
  //               maxZoom: zoom.max - zoom.min,
  //               attribution: '',
  //               tileSize: 512,
  //               noWrap: true,
  //               continuousWorld: true,
  //               key: key
  //         });}

  //       }

  //     },


////////////// A R C T I C   D A I L Y   //////////////////////////////////////

    {'arc-ter' :    { enabled: true, index: 3, type: "base",  order: 20,
        epsg: "3413",
        name: "Arctic - True Color",
        icon: "/images/explorer/maps/arc-341-icon.png",
        comment: "This is how it looks from space with a naked eye. In winter the black spot marks the Arctic night",
        timeRange: timeRanges['arc-gibs'],
        latlngzoom: [90, 0, 3],
        zoom: {min:3, max: 9, off: 0, diff: 0},
        overlays: ['sic-amsr2', 'labels-cities', 'labels-features', 'gfs-forecast'],
        getTL: function(key, zoom, fnDate){ 
          // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Terra_CorrectedReflectance_TrueColor/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
          return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'terra-341/{s}.{d}.{z}.{y}.{x}', 
            Crs['3413'](zoom, key), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
              noBlack: true, tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: 0, maxZoom: zoom.max - zoom.min,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
              tileSize: 512, noWrap: true, continuousWorld: true,
              key: key,
              zoomOffset: -1
    });}}},

    {'arc-367' :    { enabled: true, index: 4, type: "base",  order: 30,
        epsg: "3413",
        name: "Arctic - Infrared",
        icon: "/images/explorer/maps/arc-367-icon.png",
        comment: "Layer including infrared band, allows to distuinguish clouds and ice.",
        timeRange: timeRanges['arc-gibs'],
        latlngzoom: [90, 0, 3],
        zoom: {min:3, max: 9, off: 0, diff: 0},
        overlays: ['sic-amsr2', 'labels-cities', 'labels-features'],
        getTL: function(key, zoom, fnDate){ 
          // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Terra_CorrectedReflectance_Bands367/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
          return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'terra-367/{s}.{d}.{z}.{y}.{x}', 
            Crs['3413'](zoom, key), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
              noBlack: true, tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: 0, maxZoom: zoom.max - zoom.min,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
              tileSize: 512, noWrap: true, continuousWorld: true,
              key: key,
              zoomOffset: -1
    });}}},

    {'arc-721' :    { enabled: true, index: 5, type: "base",  order: 40,
        epsg: "3413",
        name: "Arctic - False Color",
        icon: "/images/explorer/maps/arc-721-icon.png",
        comment: "Layer with false colors, saturation of the blue band indicates 'ice wetness",
        timeRange: timeRanges['arc-gibs'],
        latlngzoom: [90, 0, 3],
        zoom: {min:3, max: 9, off: 0, diff: 0},
        overlays: ['sic-amsr2', 'labels-cities', 'labels-features'],
        getTL: function(key, zoom, fnDate){ 
          // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Terra_CorrectedReflectance_Bands721/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
          return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'terra-721/{s}.{d}.{z}.{y}.{x}', 
            Crs['3413'](zoom, key), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
              noBlack: true, tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: 0, maxZoom: zoom.max - zoom.min,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
              tileSize: 512, noWrap: true, continuousWorld: true,
              key: key,
              zoomOffset: -1
    });}}},


    {'arc-aqa' :    { enabled: true, index: 6, type: "base",  order: 50,
        epsg: "3413",
        name: "Arctic - True Color (Aqua)",
        icon: "/images/explorer/maps/arc-341-icon.png",
        comment: "Similar to Terra, but with a different time of overpass",
        timeRange: timeRanges['arc-gibs'],
        latlngzoom: [90, 0, 3],
        zoom: {min:3, max: 9, off: 0, diff: 0},
        overlays: ['sic-amsr2', 'labels-cities', 'labels-features', 'gfs-forecast'],
        getTL: function(key, zoom, fnDate){ 
          // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Aqua_CorrectedReflectance_TrueColor/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
          return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'aqua-341/{s}.{d}.{z}.{y}.{x}', 
            Crs['3413'](zoom, key), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
              noBlack: true, tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: 0, maxZoom: zoom.max - zoom.min,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
              tileSize: 512, noWrap: true, continuousWorld: true,
              key: key
    });}}},


//////////////  T E R R A   D A I L Y   //////////////////////////////////////

    {'ter-341' :    { enabled: true, index:  7, type: "base",  order: 60,
        name: "Terra - True Color",
        icon: "/images/explorer/maps/ter-341-icon.png",
        comment: "The earth as seen from the MODIS instrument at a 700km orbit. Updates within 3 hours after overpass.",
        epsg: "4326",
        timeRange: timeRanges['ter-gibs'],
        latlngzoom: [10, 0, 1],
        zoom: {min:0, max: 8, off: 0, diff: 0},
        getTL: function(key, zoom, fnDate){ 
          return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-geo/MODIS_Terra_CorrectedReflectance_TrueColor/default/{d}/EPSG4326_250m/{z}/{y}/{x}.jpg', 
            Crs['4326'](zoom), {
              noBlack: false, // TODO: adjust with offset here
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate,
              tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: zoom.min,
              maxZoom: zoom.max,
              tileSize: 512,
              noWrap: true,
              continuousWorld: true,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">NASA-Earthdata</a>',
              key: key
    });}}},

    {'ter-721' :    { enabled: true, index:  8, type: "base",  order: 70,
        name: "Terra - False Color",
        icon: "/images/explorer/maps/ter-721-icon.png",
        comment: "MODIS false color images, with bands 712 mapped onto a RGB spectrum",
        epsg: "4326",
        timeRange: timeRanges['ter-gibs'],
        latlngzoom: [10, 0, 1],
        zoom: {min:0, max: 8, off: 0, diff: 0},
        getTL: function(key, zoom, fnDate){ 
          return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-geo/MODIS_Terra_CorrectedReflectance_Bands721/default/{d}/EPSG4326_250m/{z}/{y}/{x}.jpg', 
            Crs['4326'](zoom), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate,
              transpic: "/images/explorer/trans.512.png",
              noBlack: false, tms: false, // keep this shit
              minZoom: zoom.min, maxZoom: zoom.max,
              tileSize: 512, noWrap: true, continuousWorld: true,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">NASA-Earthdata</a>',
              key: key
    });}}},


//////////////  A N T A R C T I C    //////////////////////////////////////

    {'ant-ter' :    { enabled: true, index: 9, type: "base",  order: 80,
        epsg: "3031",
        name: "Antarctic - True Color",
        icon: "/images/explorer/maps/ant-ter-icon.png",
        comment: "This is how it looks from space with a naked eye. In winter the black spot marks the Antarctic night",
        timeRange: timeRanges['ant-gibs'],
        latlngzoom: [-90, 0, 3],
        zoom: {min:3, max: 9, off: 0, diff: 0},
        overlays: ['labels-antarctic'],
        getTL: function(key, zoom, fnDate){ 
          // return new L.Proj.TileLayer.TMS('http://{s}.vis.earthdata.nasa.gov/wmts-arctic/MODIS_Terra_CorrectedReflectance_TrueColor/default/{d}/EPSG3413_250m/{z}/{y}/{x}.jpg', 
          return new L.Proj.TileLayer.TMS(IMAGEOVERLAYROOT + 'ant-terra/{s}.{d}.{z}.{y}.{x}', 
            Crs['3031'](zoom, key), {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'], d: fnDate, 
              noBlack: true, tms: false, // keep this shit
              transpic: "/images/explorer/trans.512.png",
              minZoom: 0, maxZoom: zoom.max - zoom.min,
              attribution: '<a href="https://wiki.earthdata.nasa.gov/display/GIBS/">Earthdata</a>',
              tileSize: 512, noWrap: true, continuousWorld: true,
              key: key,
              zoomOffset: -1
    });}}},


//////////////   O P E N S T R E E T M A P   //////////////////////////////////

    {'bwm-mapnik' :  { enabled: true, index: 10, type: "base",  order: 120,
        name: "Openstreet Map (b/w)",
        icon: "/images/explorer/maps/bwm-mapnik-icon.png",
        comment: "Beautiful black/white Openstreet Map, good for a low bandwidth connection.",
        epsg: "3857",
        crs: L.CRS.EPSG3857,
        latlngzoom: [0, 0, 1],
        zoom: {diff: 0, min: 0, max: 18},
        overlays: ['owm-temps', 'owm-press'],
        getTL: function(key, zoom){ return new L.TileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png', {
          key: key,
          minZoom: 0, maxZoom: 18,
          attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
    });}}},

    {'owm-temps' :    { enabled: true, index: 11, type: "map-overlay", order: 200,
        name: "Temperature",
        icon: "/images/explorer/maps/owm-temps-icon.png",
        comment: "worldwide, by OpenWeatherMap",
        epsg: "3857",
        zoom: {diff: 0, min: 0, max: 18},
        getTL: function(key, zoom){ return new L.TileLayer('http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png', {
          key: key,
          subdomains: '1234',
          maxZoom: 18, opacity: 0.4, 
          attribution: 'IMap data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
    });}}},


    {'owm-press' :    { enabled: true, index: 12, type: "map-overlay", order: 210,
        name: "Sea Level Pressure",
        icon: "/images/explorer/maps/owm-press-icon.png",
        comment: "worldwide, by OpenWeatherMap",
        epsg: "3857",
        zoom: {diff: 0, min: 0, max: 18},
        getTL: function(key, zoom){ return new L.TileLayer('http://{s}.tile.openweathermap.org/map/pressure_cntr/{z}/{x}/{y}.png', {
          key: key,
          subdomains: '1234',
          maxZoom: 18, opacity: 0.4, 
          attribution: 'IMap data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
    });}}},



////////////// O V E R L A Y S ////////////////////////////////////////////////


    {'arctic-coat' :    { enabled: true, index: 15, type: "map-overlay",  order: 300,
        name: "Arctic - Coastlines",
        icon: "/images/explorer/maps/sic-amsr2-icon.png",
        comment: "",
        epsg: "3413",
        crs: Crs['3413'],
        getTL: function(){ 
          return new L.Proj.TileLayer.TMS('https://map1c.vis.earthdata.nasa.gov/wmts-arctic/wmts.cgi?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=arctic_coastlines_3413&STYLE=&TILEMATRIXSET=EPSG3413_250m&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&FORMAT=image%2Fpng', 
            Crs['3413'], {
              subdomains: ['map1', 'map1a', 'map1b', 'map1c'],
              transpic: "/images/explorer/trans.512.png",
              tms: false,
              minZoom: 0,
              maxZoom: 5,
              attribution: '',
              tileSize: 512,
              noWrap: true,
              continuousWorld: true
    });}}},

    // {'ndc-perma' :    { enabled: true, index: 2, type: "wms-overlay",  order: 310,
      //     epsg: "3413",
      //     name: "Permafrost",
      //     icon: "/images/explorer/maps/arc-mask-icon.png",
      //     comment: "Permafrost and ground ice conditions",
      //     latlngzoom: [90, 0, 3],
      //     zoom: {min: 0, max: 3, off: 1, diff: 0},
      //     getTL: function(key, zoom){ 
      //       return new L.tileLayer.wms("http://nsidc.org/cgi-bin/atlas_north", {
      //           layers: "permafrost_extent",
      //           format: "image/png",
      //           transparent: true,
      //           version: "1.1.1",
      //           attribution: '<a href="http://www.nsidc.gov">NSIDC</a>',
      //           srs: "EPSG:3413",
      //           tileSize: 512,
      //           noWrap: true,
      //           continuousWorld: false,
      //           minZoom: zoom.min, maxZoom: zoom.max,
      //           key: key
      // });}}},


//// http://services.eocloud.sentinel-hub.com/v1/wms/11f6ec68-179b-43b8-8996-70305cee0942?service=WMS&request=GetMap&layers=CO&styles=&format=image/png&transparent=true&version=1.3.0&showlogo=false&width=1024&height=1024&pane=activeLayer&maxcc=100&time=2018-06-16/2018-06-16&crs=EPSG:3995&bbox=-3333134,-3333134,3333134,3333134
// http://services.eocloud.sentinel-hub.com/v1/wms/11f6ec68-179b-43b8-8996-70305cee0942?
// service=WMS&request=GetMap&
// layers=CO&styles=&format=image/png&transparent=true&
// version=1.3.0&showlogo=false&width=1024&height=1024&
// pane=activeLayer&maxcc=100&time=2018-06-16/2018-06-16&crs=EPSG:3995&bbox=-3333134,-3333134,3333134,3333134

// http://services.eocloud.sentinel-hub.com/v1/wms/11f6ec68-179b-43b8-8996-70305cee0942?
// SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.1&
// LAYERS=O3&STYLES=&FORMAT=image%2Fjpg&TRANSPARENT=true&HEIGHT=512&WIDTH=512&
// SRS=EPSG%3A3995&NOWRAP=true&CONTINUOUSWORLD=false&KEY=arc-sentinel&
// TIME=2018-06-16%2F2018-06-16&SHOWLOGO=false&CRS=EPSG%3A3995&
//BBOX=-3333135.000001276,-63775729.000000015,63775729.00000001,3333135.000001275

// https://www.sentinel-hub.com/develop/documentation/api/custom-url-parameters

    {'arc-sentinel' :    { enabled: true, index: 2, type: "base",  order: 15,
        epsg: "3995",
        name: "Sentinel 2 - Arctic",
        icon: "/images/explorer/maps/arc-sentinel2.png",
        comment: "NRT true color swaths from ESA's Sentinel Satellite",
        latlngzoom: [90, 0, 3],
        zoom: {min: 0, max: 12, off: 0, diff: 0},
        overlays: ['labels-cities', 'labels-features'],
        timeRange: timeRanges['arc-sentinel'],        
        getTL: function(key, zoom){ 
          return new L.tileLayer.sentinel("http://services.eocloud.sentinel-hub.com/v1/wms/{s}", {
              subdomains: [
                'ff6d8302-2479-4a5a-9406-255d87cab12f', 
                'b4144647-aedd-421f-8bfa-e93803bed520',
                '3edfd6dc-9de1-4e93-ae14-f49d8e73b0af',
                'de23c422-a74b-49ef-952f-335714aca15a'
              ],
              transpic: "/images/explorer/trans.512.png",
              layers: "1_TRUE_COLOR",
              format: "image/png",
              transparent: true,
              version: "1.3.1",
              attribution: '<a href="https://www.sentinel-hub.com/">Sentinel-Hub</a>',
              srs: "EPSG:3995",
              tileSize: 512,
              noWrap: true,
              continuousWorld: false,
              minZoom: zoom.min, 
              maxZoom: zoom.max - zoom.min

    });}}},

    {'arc-sentinel_3' :    { enabled: true, index: 13, type: "base",  order: 16,
        epsg: "3995",
        name: "Sentinel 2 - Arctic (3 days)",
        icon: "/images/explorer/maps/arc-sentinel2.png",
        comment: "Composite of last 3 days swaths from ESA's Sentinel Satellite",
        latlngzoom: [90, 0, 3],
        zoom: {min: 0, max: 12, off: 0, diff: 0},
        overlays: ['labels-cities', 'labels-features'],
        timeRange: timeRanges['arc-sentinel'],
        getTL: function(key, zoom){ 
          return new L.tileLayer.sentinel("http://services.eocloud.sentinel-hub.com/v1/wms/{s}", {
              buildDate: function (day) {
                return "&TIME=" + utc(day).delta("days", -3).toIso() + "/" + day;
              },
              subdomains: [
                '814e7a7a-d0b4-4355-a327-2e490cf268a2'
              ],
              transpic: "/images/explorer/trans.512.png",
              layers: "1_TRUE_COLOR",
              format: "image/png",
              transparent: true,
              version: "1.3.1",
              attribution: '<a href="https://www.sentinel-hub.com/">Sentinel-Hub</a>',
              srs: "EPSG:3995", 
              tileSize: 512,
              noWrap: true,
              continuousWorld: false,
              minZoom: zoom.min, 
              maxZoom: zoom.max - zoom.min

    });}}},


    {'gfs-simulation' :    { enabled: DEBUG, index: 21, type: "sim-overlay",  order: 310,
        name: "Weather Simulation",
        icon: "/images/explorer/maps/gfs-simulation.png",
        comment: "Surface conditions (2m temp, 10m wind)",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.6,
        urlPattern: IMAGEOVERLAYROOT + "gfs/%Y/gfs-%Y-%m-%d-%H.png",
        timeRange: timeRanges['gfs-simulation'],        
        attribution: "<a href='http://nomads.ncep.noaa.gov/txt_descriptions/GFS_high_resolution_doc.shtml'>NCEP/GFS</a>",
        colorbar: "/images/explorer/cbar-gfs.png"

    }},



////////////// I M A G E   O V E R L A Y S ////////////////////////////////////

    {'gfs-forecast' :    { enabled: true, index: 16, type: "image-overlay",  order: 400,
        name: "GFS Forecast",
        icon: "/images/explorer/maps/gfs-temps-icon.png",
        comment: "Surface conditions (2m temp, 10m wind (>10m/s), SLP)",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.6,
        urlPattern: IMAGEOVERLAYROOT + "gfs/%Y/gfs-%Y-%m-%d-%H.png",
        timeRange: timeRanges['gfs-forecast'],        
        attribution: "<a href='http://nomads.ncep.noaa.gov/txt_descriptions/GFS_high_resolution_doc.shtml'>NCEP/GFS</a>",
        colorbar: "/images/explorer/cbar-gfs.png"

    }},

    {'sst-avhrr' :    { enabled: true, index: 22, type: "image-overlay",  order: 410,
        name: "Sea Surface Temp.",
        icon: "/images/explorer/maps/sit-smos-icon.png",
        comment: "Daily Sea Surface Temperature (AVHRR)",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.9,
        urlPattern: IMAGEOVERLAYROOT + "sst/%Y/sst-%Y-%m-%d.png",
        timeRange: timeRanges['sst-avhrr'],
        attribution: '', //<a href="http://icdc.zmaw.de/l3c_smos_sit.html">University of Hamburg</a>',
        colorbar: "" ///images/explorer/cbar-smos.png"
      }},

    {'sic-amsr2' :    { enabled: true, index: 17, type: "image-overlay",  order: 420,
        name: "Sea Ice Concentration",
        icon: "/images/explorer/maps/sic-amsr2-icon.png",
        comment: "Daily high resolution maps from the AMSR2 instrument",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.9,
        urlPattern: IMAGEOVERLAYROOT + "amsr2/%Y/amsr2-%Y-%m-%d.png",
        timeRange: timeRanges['sic-amsr2'],
        attribution: '<a href="ftp://ftp-projects.zmaw.de/seaice/AMSR2/README.txt">University of Hamburg</a>'
    }},

    {'sit-cryosat' :    { enabled: true, index: 18, type: "image-overlay",  order: 430,
        name: "CryoSat Thickness",
        icon: "/images/explorer/maps/sit-smos-icon.png",
        comment: "Monthly (winter) thickness from the ESA's CryoSat 2 satellite",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.9,
        urlPattern: IMAGEOVERLAYROOT + "cryosat/%Y/cryosat-%Y-%m.png",
        timeRange: timeRanges['sit-cryosat'],
        attribution: '<a href="http://www.awi.de/en/home/">AWI</a>',
        colorbar: "/images/explorer/cbar-cryo.png"
    }},

    {'sit-smos' :    { enabled: true, index: 19, type: "image-overlay",  order: 440,
        name: "SMOS Thickness",
        icon: "/images/explorer/maps/sit-smos-icon.png",
        comment: "Daily (winter) sea ice thickness (m) from the ESA's SMOS satellite",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.9,
        urlPattern: IMAGEOVERLAYROOT + "smos/%Y/smos2-%Y-%m-%d.png",
        timeRange: timeRanges['sit-smos'],
        attribution: '<a href="http://icdc.zmaw.de/l3c_smos_sit.html">University of Hamburg</a>',
        colorbar: "/images/explorer/cbar-smos.png"
      }},

    {'sit-piomas' :    { enabled: true, index: 20, type: "image-overlay",  order: 450,
        name: "PIOMAS Thickness",
        icon: "/images/explorer/maps/sit-smos-icon.png",
        comment: "Monthly thickness from the PSC's sea ice model",
        epsg: "3413",
        bounds: [[38.8, 180], [38.8, 0]],
        opacity: 0.9,
        urlPattern: IMAGEOVERLAYROOT + "piomas/%Y/piomas-%Y-%m.png",
        timeRange: timeRanges['sit-piomas'],
        attribution: '<a href="http://psc.apl.washington.edu/wordpress/research/projects/projections-of-an-ice-diminished-arctic-ocean/data-piomas/">PSC</a>',
        colorbar: "/images/explorer/cbar-cryo.png"
    }},



    ////////////// L A B E L   O V E R L A Y S ////////////////////////////////

    {'labels-cities':      { enabled: true, index: 25, type: "marker-overlay",   order: 500,
        name: "Cities &amp; Places",
        icon: "/images/explorer/maps/sic-amsr2-icon.png",
        comment: "A few significant human settlements",
        style: 'aio-label-marker-red',
        data: {
          // http://www.gpsvisualizer.com/geocode
          // 'Toronto':              {coords: [43.6485596,  -79.3853226], style: "-bold"},
          'Paris':                {coords: [48.8569298,    2.3412001], lvl: 2, style: "-bold"},
          'London':               {coords: [51.506321,    -0.12714  ], lvl: 0, style: "-bold"},
          'Berlin':               {coords: [52.5160713,   13.3769798], lvl: 0, style: "-bold"},
          'Copenhagen':           {coords: [55.6756783,   12.5676003], lvl: 2, style: "-bold"},
          'Oslo':                 {coords: [59.912281,    10.74998  ], lvl: 0, style: "-bold"},
          'Stockholm':            {coords: [59.3323288,   18.0629292], lvl: 1, style: "-bold"},
          'Helsinki':             {coords: [60.1711617,   24.9326496], lvl: 0, style: "-bold"},
          'Moscow':               {coords: [55.751709,    37.6180229], lvl: 0, style: "-bold"},
          'Nuuk':                 {coords: [64.1812057,  -51.72995  ], lvl: 0, style: "-bold"},
          'Reykjavik':            {coords: [64.1474075,  -21.9339905], lvl: 0, style: "-bold"},
          'Warsaw':               {coords: [52.2287483,   21.0062504], lvl: 2, style: "-bold"},
          "Ulan Bator":           {coords: [47.9221001,  106.9169693], lvl: 3, style: "-bold"},
          "Minsk":                {coords: [53.8832016,   27.5042992], lvl: 4, style: "-bold"},
          'Alert':                {coords: [82.5137   ,  -62.3320   ], lvl: 1, style: ''},
          'Ambarchik':            {coords: [69.6138229,  162.2874603], lvl: 4, style: ''},
          'Anadyr’':              {coords: [64.735672,   177.5073853], lvl: 3, style: ''},
          'Anchorage':            {coords: [61.2175484, -149.8583832], lvl: 0, style: ''},
          'Arkhangel’sk':         {coords: [64.5377426,   40.5155792], lvl: 2, style: ''},
          'Barcelona':            {coords: [41.3855782,    2.16874  ], lvl: 3, style: ''},
          'Barrow':               {coords: [71.2888184, -156.7923737], lvl: 1, style: ''},
          'Bordeaux':             {coords: [44.8366318,   -0.58105  ], lvl: 4, style: ''},
          'Chicago':              {coords: [41.8841515,  -87.6324081], lvl: 3, style: ''},
          'Churchill':            {coords: [58.7691193,  -94.1679535], lvl: 3, style: ''},
          'Cologne':              {coords: [50.9416695,    6.9551601], lvl: 3, style: ''},
          'Edmonton':             {coords: [53.5462418, -113.4903717], lvl: 3, style: ''},
          'Fairbanks':            {coords: [64.8450775, -147.7220612], lvl: 4, style: ''},
          'Glasgow':              {coords: [55.857811,    -4.2425299], lvl: 4, style: ''},
          'Hammerfest':           {coords: [70.6623917,   23.6835308], lvl: 4, style: ''},
          'Inuvik':               {coords: [68.3610535, -133.7349243], lvl: 3, style: ''},
          'Iqaluit':              {coords: [63.753582,   -68.502802 ], lvl: 2, style: ''},
          'Irkutsk':              {coords: [52.3082504,  104.2391434], lvl: 2, style: ''},
          'Juneau':               {coords: [58.2997398, -134.4067841], lvl: 2, style: ''},
          'Kangerlussuaq':        {coords: [67.0086111,  -50.6891667], lvl: 4, style: ''},
          'Kodiak':               {coords: [57.79629,   -152.41455  ], lvl: 4, style: ''},
          'Labrador City':        {coords: [52.9500313,  -66.9145126], lvl: 3, style: ''},
          'Longyearbyen':         {coords: [78.2185898,   15.6487484], lvl: 4, style: ''},
          'Minneapolis':          {coords: [44.9790306,  -93.2649307], lvl: 3, style: ''},
          'Murmansk':             {coords: [68.9727936,   33.0868492], lvl: 1, style: ''},
          'Nome':                 {coords: [64.4994736, -165.4057922], lvl: 3, style: ''},
          'Noril\'sk':            {coords: [69.3473434,   88.2070236], lvl: 3, style: ''},
          'Okhotsk':              {coords: [59.3628998,  143.2270813], lvl: 4, style: ''},
          'Resolute':             {coords: [74.683333,   -94.9      ], lvl: 1, style: ''},
          'Surgut':               {coords: [61.2549515,   73.4354019], lvl: 3, style: ''},
          'Tiksi':                {coords: [71.6362381,  128.8588562], lvl: 0, style: ''},
          'Upermavik':            {coords: [72.7913589,  -56.1552811], lvl: 3, style: ''},
          'Vorkuta':              {coords: [67.5015869,   64.0609665], lvl: 3, style: ''},
          'Winnipeg':             {coords: [49.8995285,  -97.1411133], lvl: 3, style: ''},
          'Yakutsk':              {coords: [62.0330429,  129.7196808], lvl: 3, style: ''},
          'Yellowknife':          {coords: [62.4544792, -114.3709488], lvl: 3, style: ''},
          'Ürümqi':               {coords: [43.7878685,   87.5862732], lvl: 3, style: ''}
    }}},

    {'labels-features':      { enabled: true, index: 26, type: "marker-overlay",  order: 510,
        name: "Geographic Features",
        icon: "/images/explorer/maps/sic-amsr2-icon.png",
        comment: "Seas, Glaciers, Islands, etc.",
        style: 'aio-label-marker',
        data: {
          // http://www.gpsvisualizer.com/geocode
          // http://www.satelliteviews.net/country.htm
          'Petermann Glacier':    {coords: [80.75,       -60.75     ], lvl: 0, style: "-magenta"},
          'Wrangel':              {coords: [71.1999969, -179.4799957], lvl: 4, style: "-green"},
          'Jan Mayen':            {coords: [70.9710007,   -8.4879999], lvl: 3, style: "-green"},
          'Greenland Sea':        {coords: [75,          -10        ], lvl: 3, style: "-blue"},
          'Hudson Bay':           {coords: [59.9821968,  -85.762825 ], lvl: 3, style: "-blue"},
          'Lincoln Sea':          {coords: [83.6,        -55        ], lvl: 3, style: "-blue"},
          'Kara Sea':             {coords: [75.4245911,   80.4504166], lvl: 3, style: "-blue"},
          'Barents Sea':          {coords: [75,           40        ], lvl: 3, style: "-blue"},
          'Baffin Bay':           {coords: [73,          -67        ], lvl: 3, style: "-blue"},
          'Bering Sea':           {coords: [59.4500008, -177.6900024], lvl: 3, style: "-blue"},
          'Beaufort Sea':         {coords: [70.526108,  -141.498886 ], lvl: 3, style: "-blue"},
          'Chukchi Sea':          {coords: [69.37269,   -170.39854  ], lvl: 3, style: "-blue"},
          'Davis Strait':         {coords: [60.85101,    -63.39802  ], lvl: 3, style: "-blue"},
          'North Pole':           {coords: [90        ,    0        ], lvl: 3, style: "-orange"},
          'Lake Superior':        {coords: [47.5271988,  -87.7548981], lvl: 4, style: "-blue"},
          'Laptev Sea':           {coords: [75.06545,    126.90263  ], lvl: 3, style: "-blue"},
          'Magnetic Pole':        {coords: [86.395,      193.710    ], lvl: 2, style: "-orange"},  //193.710 86.395
          'Arctic Ocean':         {coords: [85.0   ,    -180.0      ], lvl: 0, style: "-blue"} ,
          'Jakobshavn Glacier':   {coords: [69.1666   , -49.833     ], lvl: 3, style: "-magenta"}, // N69.166667-W49.833333/Jakobshavn Glacier
          'Helheim Glacier':      {coords: [66.35     , -38.2       ], lvl: 0, style: "-magenta"}, // N69.166667-W49.833333/Jakobshavn Glacier
          'Zachariae Isstrom':    {coords: [78.916667 , -21.166667  ], lvl: 3, style: "-magenta"}  // Zachariae Isstrom: Lat: 78.916667 / Long: -21.166667

    }}},

    {'labels-economy':      { enabled: true, index: 27, type: "marker-overlay",  order: 520,
        name: "Resource Extraction",
        icon: "/images/explorer/maps/sic-amsr2-icon.png",
        comment: "EEZs, Oil rigs, mining projects, pipelines, harbours, airports, etc",
        style: 'aio-label-marker',
        data: {
          // http://www.gpsvisualizer.com/geocode
          'Isua Project':         {coords: [  65.188881,  -49.7586695 ], lvl: 3, style: "-black", link: ""},
          'Prirazlomnaya':        {coords: [  69.251944,   57.342778  ], lvl: 3, style: "-black", link: ""}
    }}},

    {'labels-marker':      { enabled: true, index: 28, type: "marker-overlay",  order: 530,
        name: "Wikimarker",
        icon: "",
        comment: "",
        style: 'aio-label-marker',
        data: {
          // http://www.gpsvisualizer.com/geocode
          'Isua Project':         {coords: [  65.188881,  -49.7586695 ], lvl: 3, style: "-black", link: ""},
          'Prirazlomnaya':        {coords: [  69.251944,   57.342778  ], lvl: 3, style: "-black", link: ""}
    }}},

    {'labels-antarctic':      { enabled: true, index: 29, type: "marker-overlay",  order: 540,
        name: "Place Names",
        icon: "",
        comment: "",
        style: 'aio-label-marker',
        data: {
          'Weddell Sea':                {coords: [-73,        -45],       lvl: 3, style: "-blue"},
          'Ross Sea':                   {coords: [-75,       -175],       lvl: 3, style: "-blue"},
          'Davis Sea':                  {coords: [-66,         93.5],     lvl: 3, style: "-blue"},
          'Bellingshausen Sea':         {coords: [-71,        -85.00],    lvl: 3, style: "-blue"},
          'Amundsen Sea':               {coords: [-72.5,     -111.91667], lvl: 3, style: "-blue"},
          'Byrd Station':               {coords: [-80.01667, -119.53333], lvl: 3, style: "-red"},
          'Georg von Neumayer Station': {coords: [-70.61667,   -8.36],    lvl: 3, style: "-red"},
          'McMurdo Station':            {coords: [-77.85,     166.66667], lvl: 3, style: "-red"},
          'Vostok Station':             {coords: [-78.46442,  106.83733], lvl: 3, style: "-red"},
          'Eilers Peak':                {coords: [-80.06667,  159.46667], lvl: 3, style: "-green"},
          'Aurora Peak':                {coords: [-67.38333,  144.2],     lvl: 3, style: "-green"},
          'Pine Island Glacier':        {coords: [-75.00,    -101.00],    lvl: 3, style: "-magenta"},
          'South Pole':                 {coords: [-90      ,    0      ], lvl: 3, style: "-orange"}
    }}},

    {'labels-antarctic-icebergs':      { enabled: false, index: 29, type: "marker-overlay",  order: 550,
        name: "Large Icebergs",
        icon: "",
        comment: "",
        style: 'aio-label-marker',
        data: {
          'Weddell Sea':                {coords: [-73,        -45],       lvl: 3, style: "-blue"}
    }}}


  ],



  ////////////// S U P P O R T   F U N C T I O N S  ///////////////////////////


  all : function (key, type) {

    var i, obj, lay, accu = [];

    type = type || "base";

    for (i in Layers[type]) {
      if (Layers[type].hasOwnProperty(i)) {
        key = H.firstAttr(Layers[type][i]);
        lay = Layers[type][i][key];
        if (lay.enabled) {
          lay.key = key;
          accu.push(lay);
        }
      }
    }
    return accu;

  },

  filter : function (fn, sorted) {
    var layers;
    if (typeof sorted === "undefined"){sorted = true;}
    layers = Layers.all().filter(fn);
    if (sorted) {
      return layers.sort(function (a, b){ return a.order - b.order;});
    } else {return layers;}
  },

  byKey : function (key, type) {

    var i, j, obj;

    type = type || "base";

    for (i in Layers[type]) {
      if (Layers[type].hasOwnProperty(i)) {
        for (j in Layers[type][i]) {
          if (Layers[type][i].hasOwnProperty(j)) {
            if (j === key) {
              obj = Layers[type][i][j];
              obj.key = key;
              return obj;
            }
          }
        }
      }
    }

  },

  // byEpsg : function (epsgs, type) {

  //   var i, obj, lay, key, accu = [];

  //   type = type || "base";

  //   for (i in Layers[type]) {
  //     if (Layers[type].hasOwnProperty(i)) {
  //       key = H.firstAttr(Layers[type][i]);
  //       lay = Layers[type][i][key];
  //       if (epsgs.indexOf(lay.epsg) >= 0 && lay.enabled) {
  //         lay.key = key;
  //         accu.push(lay);
  //       }
  //     }
  //   }
  //   return accu;
  // },

  byIndex : function (index, type) {

    var i, lay, key;

    type = type || "base";

    for (i in Layers[type]) {
      if (Layers[type].hasOwnProperty(i)) {
        key = H.firstAttr(Layers[type][i]);
        lay = Layers[type][i][key];
        if (lay.index === index) {
          lay.key = key;
          return lay;
        }
      }
    }
  },

  // byIndexes : function (indexes, type) {

  //   var accu = [];

  //   indexes.forEach(function(idx){
  //     var item = Layers.byIndex(idx, type);
  //     if (item) {
  //       accu.push(item);
  //     }
  //   });

  //   return accu;

  // },

  // keysByEpsg : function (epsg, type) {

  //   var i, obj, lay, key, accu = [];

  //   type = type || "base";

  //   for (i in Layers[type]) {
  //     key = H.firstAttr(Layers[type][i]);
  //     lay = Layers[type][i][key];
  //     if (lay.epsg === epsg && lay.enabled) {
  //       accu.push(key);
  //     }
  //   }
  //   return accu;
  // },

  code2layers: function(code){

    var i, layers = [];

    code = H.Base62.toNumber(code);

    function bit (i, test) {return (i & (1 << test));}

    for (i = 0; i < 32; i++){
      if (bit(code, i)){layers.push(i);}
    }

    return layers.sort(function(a, b){return a-b;});

  },
  layers2code: function(layers){

    var out = 0;

    if (!layers.length) {return null;}

    layers.forEach(function(l){
      out += 1 << l;
    });

    return H.Base62.fromNumber(out);

  },
  deb: function(){
    Layers.all()
      .sort(function(a, b){return a.index - b.index;})
      .forEach(function(l){
        var key = ("                 " + l.key);
        var cod = Layers.layers2code([l.index]);
        console.log(
          key.substr(key.length-18), 
          "\t", l.index, 
          "\t", cod, 
          "\t", l.order, 
          // "\t", l.type, l.name
          "\t", JSON.stringify(l.zoom)
        );
    });
  }

};


// Debug
(function () {

  var l, n, layers = [];

  for (l in Layers.base) {
    for (n in Layers.base[l]) {
      layers.push(n);
    }
  }

  // TIM.step("Layers", layers.join(", "));
  TIM.step("LOADED", "Layers: " + layers.length);

}());




