/*jslint bitwise: true, browser: true, evil:true, devel: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, L, Layers, google, Crs, TIM, TimeRange, utc, H */

var MAPS = (function () {

  var self, isSplitScreen = false,

      dfLocation = "/explorer/8//3-N90-E0/", 

      wikiMarkers = [null, null],

      mapR = {map: null, div: null, list: {}, overs: {}, ctrls: {}, timeRange: new TimeRange()}, 
      mapL = {map: null, div: null, list: {}, overs: {}, ctrls: {}, timeRange: new TimeRange()}, 

      layout = {paddingTop: 52, borderCenter: 4},
      divMsgOverlay,
      geocoder = new google.maps.Geocoder(),
      debTitle = true,

      status = {
        lay1:     [], 
        lay2:     [],
        day1:     null,
        day2:     null,
        lat:      null,
        lng:      null,
        zoom:     null
      },
      ignore = {events: false};

      function getMapTL(map){return map._layers[H.firstAttr(map._layers)];}

  return {
    deb: function(){  

        var rTL = getMapTL(mapR.map),
            lTL = getMapTL(mapL.map),
            rZo = rTL.options.minZoom + "/" + rTL.options.maxZoom,
            lZo = lTL.options.minZoom + "/" + lTL.options.maxZoom,
            rZi = mapR.map.options.crs.options.zoomInfo.min + "/" + mapR.map.options.crs.options.zoomInfo.max + "/" + mapR.map.options.crs.options.zoomInfo.off,
            lZi = mapL.map.options.crs.options.zoomInfo.min + "/" + mapL.map.options.crs.options.zoomInfo.max + "/" + mapL.map.options.crs.options.zoomInfo.off,
            rLY = Layers.byIndex(status.lay1[0]),
            lLY = Layers.byIndex(status.lay2[0]),
            rYz = rLY.zoom.min + "/" + rLY.zoom.max,
            lYz = lLY.zoom.min + "/" + lLY.zoom.max;

      console.table([
        ["side",  "mZoom",             "cZoom", "lKey",   "tlZoom", "lyZoom"], 
        ["right",  mapR.map.getZoom(), rZi,     rTL.key,  rZo,      rYz],
        ["left",   mapL.map.getZoom(), lZi,     lTL.key,  lZo,      lYz]
      ]);
    },
    oversource: "",
    left:  mapL,
    right: mapR,
    status: status,
    ignore: ignore,
    layout: layout,
    markers: wikiMarkers,
    transpic: "/images/explorer/trans.512.png",
    notavail: "/images/explorer/notavail.512.png",
    isSplitScreen : function(){return isSplitScreen;},
    boot : function(){
      self = this;
      window.onload   = this.onload;
      window.onresize = this.updateSize;
      window.onhashchange = this.onhashchange;
      return this;
    },
    onhashchange : function(){console.log("Hash", location.hash);},
    onload :   function(){

      var path = location.pathname || dfLocation;

      TIM.step("LOADING", "Hash: " + path);

      mapR.div = $("#mapR");
      mapL.div = $("#mapL");

      self.parseLocation(path);
      self.updateSize();
      self.prepBaseList("right");
      self.prepBaseList("left");
      self.createMap("right");
      self.createMap("left");
      self.updateControls("right");
      self.updateControls("left");
      self.activateMap("right");
      self.activateMap("left");
      self.initOverlays();
      self.initMarker();
      self.updateAttribution();
      self.updateSplitScreen(isSplitScreen);
      self.updateTime();
      self.updatePerma();

      // hide at start

      // css tricks
      // $(mapR.ctrls.coords._container).css({visibility: "hidden"});
      // $(mapL.ctrls.coords._container).css({visibility: "hidden"});
      $(mapR.ctrls.loader._container).css({'box-shadow': "0 0", 'background': 'transparent'});
      $(mapL.ctrls.loader._container).css({'box-shadow': "0 0", 'background': 'transparent'});

      $(".leaflet-control-loading").parent().css({background:"#666"});
      $("form.leaflet-control-layers-list").css({margin:"4px 6px"});
      $("#mapContainer").css({background:"#740F0F"}); // splitscreen trenner
      $("#msgs-overlay").css({display:"none"});

      // $(".permaWait").css({
      $("#navPerma img").css({
        'background': 'transparent',
        'background-image': 'url()',
        'padding-left': '2px'
      });

      TIM.step("LOADED", "Maps");

    },
    updateSize : function(){

      var navHeight = $(".navbar").height(),
          trnHeight = $("#sec-maphead").height(),
          w = $(window).width(), 
          // t = navHeight + trnHeight, // layout.paddingTop,
          t = fullScreenApi.isFullScreen() ? trnHeight : navHeight + trnHeight,
          h = $(window).height() - t,
          b = layout.borderCenter/2;

      if (isSplitScreen){
        mapR.div.css({top: t + "px", height: h + "px", width: w/2 - b + "px", left: w/2 + b + "px"});
        mapL.div.css({top: t + "px", height: h + "px", width: w/2 - b + "px", left: 0});
      } else {
        mapR.div.css({top: t + "px", height: h + "px", width: w + "px", left: 0});
        mapL.div.css({top: t + "px", height: h + "px", width: 0, left: 0});
      }
      if (mapL.map){
        mapL.map.invalidateSize();
        mapR.map.invalidateSize();
      }

      // $("#msgs-overlay").css({top: t + "px", height: h + "px", width: w + "px", left: 0, zIndex: 10000000});

    },
    geocode: function(){

      var loc, cmpnts, types, 
          center = mapR.map.getCenter(), 
          latlng = new google.maps.LatLng(center.lat, center.lng);

      mapR.map.fire("dataloading");
      mapL.map.fire("dataloading");

      geocoder.geocode({latLng: latlng}, function(res, stats){

        var locs = [];

        mapR.map.fire("dataload");
        mapL.map.fire("dataload");

        if (stats === google.maps.GeocoderStatus.OK) {

          // console.log("res", res);

          res.reverse().forEach(function(r, idx){
            cmpnts = r.address_components.map(function(c){
              return c.short_name;
            });
            types = r.types.reduce(function(a, b){
              return a + ", " + b;
            }, "");
            // console.log(idx, r.formatted_address, cmpnts, types);
          });

          if  (res.length === 0){
            locs.push("uninhabited");

          } else {

            // remove postal code, routes
            // make sure to have country code (mexico) country, political
            // which is not always in [0]
            // remove stuff in brackets Colombia

            if (res[0].types[0] === "country"){
              locs.push(res[0].address_components[0].short_name);
              locs.push(res[0].address_components[0].long_name);
            }

            if (res.length === 2){
              locs.push(res[1].address_components[0].long_name);}

            else if (res.length === 3){
              locs.push(res[2].address_components[0].long_name);}

            else if (res.length > 3){
              // locs.push(res[2].address_components[0].long_name);
              locs.push(res[3].address_components[0].long_name);}
          }


          // console.log("locs", locs);

          $("#navLocation").text(locs.join(" "));

        } else if (stats === google.maps.GeocoderStatus.ZERO_RESULTS){
          // DEBUG && console.log("GEOCODE", google.maps.GeocoderStatus.ZERO_RESULTS);
          $("#navLocation").text("uninhabited");

        } else {
          // DEBUG && console.log("GEOCODE", google.maps.GeocoderStatus.ZERO_RESULTS);
          $("#navLocation").text("unidentified");
        }

        $("#navLocation").href = $("permaLink").href;

      });

    },
    parseLocation: function(pathname){

      var path = (pathname || location.pathname).split("/");

      function ged (i, value){
        return  (i >= path.length) ? value :
                (path[i] === "" )  ? value : path[i]; 
      }

      function layerRange(layers){
        var tr = new TimeRange();
        if (Layers.byIndex(layers[0]).timeRange && Layers.byIndex(layers[0]).type === "base") {
          return Layers.byIndex(layers[0]).timeRange;
        } else {
          layers.forEach(function(idx){
            var l = Layers.byIndex(idx);
            if(!!l.timeRange){
              tr.push(l.timeRange);
            }
          });
          return tr;
        }
      }

      var dfDate = utc().delta("days", -1).toIso(),
          dfLay  = dfLocation.split("/")[2],
          dfCrds = dfLocation.split("/")[4],
          code   = ged(2, dfLay).split("-"),
          date   = ged(3, "").split(";"),
          coords = ged(4, "").split("-"),
          place  = decodeURIComponent(ged(5, "")), 
          lat, lng, baseR, baseL, timeR, timeL;

      status.place = place || "";
      status.lay1  = Layers.code2layers(code[0]);

      if (code.length === 2){
        status.lay2 = Layers.code2layers(code[1]); // only base here // Why
        isSplitScreen = true;
      } else {
        status.lay2 = [status.lay1[0]];
      }

      baseR = Layers.byIndex(status.lay1[0]);
      baseL = Layers.byIndex(status.lay2[0]);

      if (!baseR || !baseL) {
        console.log("parseLocation: unknown indezes", status.lay1[0], status.lay2[0]);
      }

      timeR = layerRange(status.lay1);
      timeL = layerRange(status.lay2);

      if ((date.length === 0) || (date.length === 1 && date[0] === "")) {
        status.day1 = (timeR.length()) ? timeR.latest() : dfDate;
        status.day2 = (timeL.length()) ? timeL.latest() : dfDate;
      } else if (date.length === 1) {
        status.day1 = date[0];
        status.day2 = date[0];
      } if (date.length === 2) {
        status.day1 = date[0];
        status.day2 = date[1];
      }

      if (coords.length !== 3) {
        coords = baseR.latlngzoom;
        coords = [coords[2], coords[0], coords[1]]
      }

      //assuming no zoom cheats here
      status.zoom = ~~coords[0]; // - base.zoom.diff;
      status.zoom = H.bounds(status.zoom, baseR.zoom.min, baseR.zoom.max);
      if (isSplitScreen){
        status.zoom = H.bounds(status.zoom, baseL.zoom.min, baseL.zoom.max);
      }

      lat = coords[1]; lng = coords[2];
      status.lat = (lat[0] === "N") ?  parseFloat(lat.substr(1)) : 
                   (lat[0] === "S") ? -parseFloat(lat.substr(1)) : lat;

      status.lng = (lng[0] === "E") ?  parseFloat(lng.substr(1)) : 
                   (lng[0] === "W") ? -parseFloat(lng.substr(1)) : lng;


      TIM.step("STATUS", JSON.stringify(status).split('"').join(''));

    },

    updatePerma: function(){

      var perma = $("#navPerma a"),
          link = "/" + dfLocation.split("/")[1] + "/",
          title = "Permalink: " + location.host + link, 
          text = "//arctic.io/" + dfLocation.split("/")[1] + "/",
          code, codeL, codeR, datum = "", zoom, lat, lng, fragment,
          abs = Math.abs,
          rightCanDate, leftCanDate;

      rightCanDate = mapR.timeRange.ranges.length > 0;
      leftCanDate  = mapL.timeRange.ranges.length > 0;

      codeR = Layers.layers2code(status.lay1);
      codeL = Layers.layers2code(status.lay2);
      code  = codeR + (isSplitScreen ? "-" + codeL : "");

      datum = ( rightCanDate && !isSplitScreen)                ? status.day1 : 
              ( rightCanDate &&  leftCanDate && isSplitScreen) ? status.day1 + ";" + status.day2 :
              (!rightCanDate &&  leftCanDate && isSplitScreen) ? ";" + status.day2 : 
              ( rightCanDate && !leftCanDate && isSplitScreen) ? status.day1 : undefined;

      zoom  = status.zoom ;
      lat   = status.lat.toFixed(5);
      lng   = status.lng.toFixed(5);
      lat   = (lat < 0) ? "S" + abs(lat) : "N" + abs(lat);
      lng   = (lng < 0) ? "W" + abs(lng) : "E" + abs(lng);
      fragment = [code, datum, [zoom, lat, lng].join("-")].join("/");

      perma.text(text + fragment);
      perma.attr("href", link + fragment);
      perma.attr("title", title + fragment);

    },
    setMarker : function(map, lat, lng, feat){

      var mapX = (map === mapR.map) ? mapR : mapL,
          idx  = (map === mapR.map) ? 0 : 1;

      // console.log("setM", wikiMarkers, idx, lat, lng, feat);

      if (wikiMarkers[idx]) {
        mapX.map.removeLayer(wikiMarkers[idx]);
        wikiMarkers[idx] = null;
      }

      if (feat) {

        wikiMarkers[idx] = L.marker([lat, lng], {
            icon: new L.Label({className: 'aio-label-marker-wiki', html: feat || "name me"}),
            clickable: true
          }).addTo(mapX.map);        

        wikiMarkers[idx].on("click", function(){
            // console.log(wikiMarkers[idx]);
            // mapX.ctrls.coords.expand(wikiMarkers[idx]);
          });

        if (idx === 0){status.place = feat;}

        return wikiMarkers[idx];

      }

    },
    getCenter: function(map){

      var prj = map.options.crs.projection,
          sw  = map.getBounds()._southWest,
          ne  = map.getBounds()._northEast,
          psw = prj.project(sw),
          pne = prj.project(ne),
          x   = psw.x + (pne.x - psw.x)/2,
          y   = psw.y + (pne.y - psw.y)/2;
          
      return prj.unproject({x:x, y:y});

    },
    initMarker : function(){
      if (status.place) {
        self.setMarker(mapR.map, status.lat, status.lng, status.place);
        self.setMarker(mapL.map, status.lat, status.lng, status.place);
      }
    
    },
    updateAttribution : function(){

      // var rightAttr = "", leftAttr = "";

      // rightAttr = Layers.byIndex(status.lay1[0]).attribution;
      // leftAttr = Layers.byIndex(status.lay2[0]).attribution;

      // mapR.attribution._attributions = [];
      // mapL.attribution._attributions = [];
      // mapR.attribution.addAttribution(rightAttr);
      // mapL.attribution.addAttribution(leftAttr);

    },
    changeTime : function(cal, stamp){

      var mapX  = (cal.side === "right") ? mapR : mapL,
          dayX  = (cal.side === "right") ? "day1" : "day2",
          res   = mapX.timeRange.resolution(),
          base  = (cal.side === "right") ? 
            Layers.byIndex(status.lay1[0]) :
            Layers.byIndex(status.lay2[0]),
          token = (cal.side === "right") ? base.key : base.name;

      status[dayX] = stamp.toIso(res);
      if (!!base.timeRange){mapX.list[token].redraw();}
      H.each(mapX.overs, function(a, o){
        o.updateTime(stamp);
      });

      self.updateTime();
      self.updatePerma();

    },
    updateTime : function(){

      var rightCanDate, leftCanDate, res, iso;

      mapR.timeRange = new TimeRange();
      mapL.timeRange = new TimeRange();

      status.lay1.forEach(function(idx){
        var l = Layers.byIndex(idx);
        if(!!l.timeRange){
          rightCanDate = true;
          mapR.timeRange.push(l.timeRange);
        }
      });

      status.lay2.forEach(function(idx){
        var l = Layers.byIndex(idx);
        if(!!l.timeRange){
          leftCanDate = true;
          mapL.timeRange.push(l.timeRange);
        }
      });

      if (rightCanDate) {
        status.day1 = status.day1 || utc().toIso();
        res = mapR.timeRange.resolution();
        iso = (res < 4) ?  utc(status.day1).toIso(res) : utc(status.day1).format("%Y-%m-%d %Hh");
        mapR.ctrls.calendar.updateDisplay(iso);
        mapR.ctrls.calendar.updateRange(mapR.timeRange, utc(status.day1));
      }
      mapR.ctrls.calendar._container.style.visibility = rightCanDate ? "visible" : "hidden";

      if (leftCanDate) {
        status.day2 = status.day2 || utc().toIso();
        res = mapL.timeRange.resolution();
        iso = (res < 4) ?  utc(status.day2).toIso(res) : utc(status.day2).format("%Y-%m-%d %Hh");
        mapL.ctrls.calendar.updateDisplay(iso);
        mapL.ctrls.calendar.updateRange(mapL.timeRange, utc(status.day2));
      }
      mapL.ctrls.calendar._container.style.visibility = leftCanDate  ? "visible" : "hidden";

      mapR.timeRange.log();

      // console.log ("updateTime.out", status.lay1.map(function(idx){ return Layers.byIndex(idx).key;}));

    },        
    initOverlays: function(){ // only onload

      status.lay1.slice(1).forEach(function(idx){
        self.changeOverlay(mapR.map, Layers.byIndex(idx).key, true, true);
      });

      status.lay2.slice(1).forEach(function(idx){
        self.changeOverlay(mapL.map, Layers.byIndex(idx).key, true, true);
      });

    },
    toggleOverlay: function (layers, key){
      var idx = Layers.byKey(key).index, pos = layers.indexOf(idx);
      if (pos === -1) {layers.push(idx);} 
      else {layers.splice(pos, 1);}
    },
    changeOverlay : function(map, key, onoff, silent){
      
      // console.log("toggleOverlay", key, ">", onoff);

      var layer   = Layers.byKey(key),
          layers  = (map === mapR.map) ? status.lay1  : status.lay2,
          day     = (map === mapR.map) ? status.day1  : status.day2,
          overs   = (map === mapR.map) ? mapR.overs  : mapL.overs,
          ctrlLayers = (map === mapR.map) ? mapR.ctrls.layers : mapL.ctrls.layers;

      if (onoff) {
        switch (layer.type) {
          case "map-overlay"    :      
          case "wms-overlay"    : overs[key] = layer.getTL(layer.key, layer.zoom).addTo(map);   break;
          case 'image-overlay'  : overs[key] = new L.TimeOverlay(layer, utc(day)).addTo(map);   break;
          case 'sim-overlay'    : overs[key] = new L.SimOverlay(layer, utc(day)).addTo(map);    break;
          case "marker-overlay" : overs[key] = new L.MarkerOverlay(layer).addTo(map);           break;
          default:                throw new Error("Unknown Layer Type: " + key);
        }
      } else {
        map.removeLayer(overs[key]);
        delete overs[key];
      }

      if (map === mapR.map) {
        mapR.ctrls.layers._overlays[key] = onoff;
      }

      if (!silent){
        self.toggleOverlay(layers, key);
        self.updateTime();
        self.updateAttribution(); 
        self.updatePerma();
      }

      ctrlLayers.update();

    },
    changeBase : function(map, newKey, forceSilent){

      // TODO:  check allowed overlays if short switch
      //        make sure date is appropiate if short switch

      forceSilent = (typeof forceSilent === "undefined") ? false : true;

      var newCrsTL, othCrsTL, crsZoomMin, crsZoomMax, curZoom, othZoom,
          side      = (map === mapR.map) ? "right"     : "left",
          curMap    = (map === mapR.map) ? mapR.map    : mapL.map,
          othMap    = (map === mapR.map) ? mapL.map    : mapR.map,
          curList   = (map === mapR.map) ? mapR.list   : mapL.list,
          othList   = (map === mapR.map) ? mapL.list   : mapR.list,
          curLayers = (map === mapR.map) ? status.lay1 : status.lay2,
          othLayers = (map === mapR.map) ? status.lay2 : status.lay1,

          othLay    = Layers.byIndex(othLayers[0]),
          curLay    = Layers.byIndex(curLayers[0]),
          newLay    = Layers.byKey(newKey),

          newCrs    = Crs[newLay.epsg](newLay.zoom),
          curCrs    = Crs[curLay.epsg](curLay.zoom),

          curToken  = (map === mapR.map) ? curLay.key  : curLay.name,
          othToken  = (map === mapR.map) ? othLay.name : othLay.key,
          newToken  = (map === mapR.map) ? newLay.key  : newLay.name,

          llzoom    = newLay.latlngzoom,

          prevFade  = curMap.options.fadeAnimation,
          prevZoom  = curMap.options.zoomAnimation,

          fnDate = (map === mapR.map) ? 
              function(){return MAPS.status.day1;} : 
              function(){return MAPS.status.day2;};

      function getMaskCrsTLForMap(key, map){

        var layMask = Layers.byKey("arc-data"), 
            zoom   = (key === "arc-data") ? layMask.zoom : layMask.zoomAlt,
            fnDate = (map === mapR.map) ? 
              function(){return MAPS.status.day1;} : 
              function(){return MAPS.status.day2;};

        return [Crs["3413"](zoom), layMask.getTL("arc-data", zoom, fnDate)];
      }

      DEBUG && console.log("");  
      DEBUG && console.log("Stat0", curLay.key, ">", newKey, curLay.epsg, ">", newLay.epsg);

      if (curLay.key === newKey && !forceSilent) { 
        
        // console.log("Stat0a", forceSilent, curLay.key, "=", newKey, curLay.epsg, ">", newLay.epsg);
        return; 

      } else if (newLay.epsg === curLay.epsg || forceSilent){

        // console.log("--Stat0b.in", forceSilent, curLay.key, "=", newKey, curLay.epsg, ">", newLay.epsg);
        // self.deb();

        newCrsTL = (newKey === "arc-data") ? 
          getMaskCrsTLForMap(othLay.key, othMap) :
          [Crs[newLay.epsg](newLay.zoom), newLay.getTL(newKey, newLay.zoom, fnDate)];

        othCrsTL = (othLay.key === "arc-data") ? 
          getMaskCrsTLForMap(newKey, curMap) : [] ;

        mapR.map.sync();
        mapL.map.sync();          

        // console.log("--Stat0b.before", side, status.lay1, status.lay2);
        // replace base map in status
        curLayers.splice(0, 1);
        curLayers.unshift(newLay.index);

        // if (map === mapR.map) {mapR.ctrls.layers.updateActiveLayer(newKey);}

        // remove unsupported overlays
        curLayers.slice(1).forEach(function(idx){
          var key = Layers.byIndex(idx).key;
          if (newLay.overlays.indexOf(key) === -1){
            self.changeOverlay(curMap, key, false, true);
            self.toggleOverlay(curLayers, key);
          } else {
            mapR.ctrls.layers._overlays[key] = true;            
          }
        });

        if (isSplitScreen){
          crsZoomMin = Math.max(curMap.options.crs.options.zoomInfo.min, othMap.options.crs.options.zoomInfo.min);
          crsZoomMax = Math.min(curMap.options.crs.options.zoomInfo.max, othMap.options.crs.options.zoomInfo.max);
        } else {
          crsZoomMin = curMap.options.crs.options.zoomInfo.min;
          crsZoomMax = curMap.options.crs.options.zoomInfo.max;
        }
        status.zoom = H.bounds(status.zoom + curMap.options.crs.options.zoomInfo.min, crsZoomMin, crsZoomMax) - curMap.options.crs.options.zoomInfo.min;

        ignore.events = true;
        // remove old, add new
        curMap.removeLayer(curList[curToken]);
        curMap.options.crs = newCrsTL[0];
        curMap.addLayer(newCrsTL[1]);
        curList[newToken] = newCrsTL[1];

        // console.log("--after", side, status.lay1, status.lay2);

        // self.deb();

        if (othCrsTL.length) { // choose arc-data with better zoom support if applicable
          othMap.removeLayer(othList[othToken]);
          othMap.options.crs = othCrsTL[0];
          othMap.addLayer(othCrsTL[1]);
          othList[othToken] = othCrsTL[1];
          // self.deb();
        }
        ignore.events = false;

        othZoom = status.zoom //- othMap.options.crs.options.zoomInfo.min;
        curZoom = status.zoom //- curMap.options.crs.options.zoomInfo.min;
        othMap.setView([status.lat, status.lng], othZoom, {reset: true, animate: false, zoom: false});
        curMap.setView([status.lat, status.lng], curZoom, {reset: true, animate: false, zoom: false});

        if (map === mapR.map) {mapR.ctrls.layers.updateActiveLayer(newKey);}

        // console.log("--Stat0b.done", "r", H.countAttrs(mapR.map._layers), "l", H.countAttrs(mapR.map._layers));

        if (forceSilent){return;}


      } else { // happens only on right map, different EPSG

        // console.log("Stat0c.in ", forceSilent, curLay.key, "=", newKey, curLay.epsg, ">", newLay.epsg);

        // remove unsupported overlays
        curLayers.slice(1).forEach(function(idx){
          var key = Layers.byIndex(idx).key;
          if (newLay.overlays.indexOf(key) === -1){
            self.changeOverlay(curMap, key, false, true);
            self.toggleOverlay(curLayers, key);
          } else {
            mapR.ctrls.layers._overlays[key] = true;            
          }
        });
        
        // // remove all overlays on right
        // status.lay1.slice(1).forEach(function(idx){
        //   var key = Layers.byIndex(idx).key;
        //   self.changeOverlay(mapR.map, key, false, true);
        // });

        // // strip overlays, check date and set default coords from layer
        // status.lay1 = status.lay1.slice(0, 1);
        // status.lay2 = status.lay2.slice(0, 1);

        if (newLay.timeRange){
          status.day2 = status.day1 = newLay.timeRange.latest();  // search last date
        } else {
          status.day1 = "";          
          status.day2 = "";          
        }

        if (newCrs.options.domain !== curCrs.options.domain) {
          status.lat  = llzoom[0];
          status.lng  = llzoom[1];
          status.zoom = llzoom[2];
        }

        // console.log("Stat0c.did.zoom", status.zoom, status.lat, status.lng, status.day1, status.day2);

        self.changeBase(mapR.map, newKey, true);
        self.changeBase(mapL.map, newKey, true);

        self.prepBaseList("left");
        self.updateControls("left");
        mapR.ctrls.layers.update();

        // console.log("Stat0c.done");
      }

      self.updateSplitScreen(isSplitScreen);
      self.updateTime();       
      self.updateAttribution();
      self.updatePerma();

    },
    prepBaseList: function(side){

      var base   = (side === "right") ? 
            Layers.byIndex(status.lay1[0]) : 
            Layers.byIndex(status.lay2[0]),
          mapX   = (side === "right") ? mapR   : mapL,
          dayX   = (side === "right") ? "day1" : "day2",
          filter = (side === "right") ? 
            function(l){return l.type === "base";} : 
            function(l){return l.type === "base" && l.epsg === base.epsg;},
          layers = Layers.filter(filter),
          token;

      mapX.list = {};

      layers.forEach(function(l){
        token = (side === "right") ? l.key :  Layers.byKey(l.key).name;
        mapX.list[token] = l.getTL(l.key, l.zoom, function(){return MAPS.status[dayX];});
        mapX.list[token].options.side = side;
        mapX.list[token].options.timeRange = base.timeRange;
        mapX.list[token].options.key  = l.key;
      });

    },
    updateControls : function(side){

      var 
        mapX  = (side === "right") ? mapR : mapL,
        indx  = (side === "right") ? status.lay1[0] : status.lay2[0],
        base  = Layers.byIndex(indx)
      ;

      mapX.ctrls.loader   = mapX.ctrls.loader   || new L.Control.Loading().addTo(mapX.map);
      mapX.ctrls.slider   = mapX.ctrls.slider   || new L.Control.Zoom().addTo(mapX.map);        
      mapX.ctrls.recticle = mapX.ctrls.recticle || new L.Control.Recticle().addTo(mapX.map);
      mapX.ctrls.full     = mapX.ctrls.full     || new L.Control.FullScreen().addTo(mapX.map);
      mapX.ctrls.split    = mapX.ctrls.split    || new L.Control.SplitScreen().addTo(mapX.map);
      mapX.ctrls.coords   = mapX.ctrls.coords   || new L.control.coordinates().addTo(mapX.map);
      mapX.ctrls.calendar = mapX.ctrls.calendar || new L.Control.Calendar(utc(status.day1), {timeRange: base.timeRange}).addTo(mapX.map);
      mapX.ctrls.attribution = mapX.ctrls.attribution || new L.Control.Attribution({prefix: false}).addTo(mapX.map);

      if (mapX === mapR){
        mapR.ctrls.layers   = mapR.ctrls.layers || new L.Control.PrettyLayers(base.key).addTo(mapR.map).update();
      } 

      if (mapX === mapL){
        mapL.ctrls.layers = mapL.ctrls.layers || new L.Control.SimpleLayers(mapL.list, null, {position: "topright"}).addTo(mapL.map);
        mapL.ctrls.layers.update = L.Util.falseFn;
        mapL.ctrls.cursor   = mapL.ctrls.cursor || new L.Control.SplitCursor().addTo(mapL.map);
      }

    },
    createMap : function(side){
      
      var 
        mapX = (side === "right") ? mapR : mapL,
        base = (side === "right") ? 
          Layers.byIndex(status.lay1[0]) : 
          Layers.byIndex(status.lay2[0]),
        center = new L.LatLng(status.lat, status.lng),
        layers, name, key, zoom,
        $controlContainer
      ;

      zoom = H.clone(base.zoom); //zoomR.diff = layR.zoom.min;

      mapX.timeRange = base.timeRange || new TimeRange();

      // create actual map
      if (side === "right") {

        mapR.map = new L.Map('mapR', {
          side: "Right",
          tms: true,
          layers: [mapR.list[base.key]],
          crs: Crs[base.epsg](zoom, "mp-" + base.key),
          center: center,
          zoom: status.zoom - zoom.min,
          fullscreenControl: false,
          zoomControl: false,
          zoomsliderControl: false,
          calendarControl: false,
          trackResize: false,
          attributionControl: false
        });      

        if ($(mapR.map._controlContainer).children().length < 5){
          $controlContainer = $(mapR.map._controlContainer);
          $controlContainer.append('<div class="leaflet-top leaflet-center"></div>');
          mapR.map._controlCorners.topcenter = $controlContainer.children('.leaflet-top.leaflet-center').first()[0];
        }


      } else {

        mapL.map = new L.Map('mapL', {
          side: "Left",
          layers: [mapL.list[base.name]],
          tms: true,
          crs: Crs[base.epsg](zoom, base.key),
          center: center,
          zoom: status.zoom - zoom.min,
          fullscreenControl: false,
          zoomControl: false,
          zoomsliderControl: false,
          calendarControl: false,
          trackResize: false,
          attributionControl: false
        });      

        if ($(mapL.map._controlContainer).children().length < 5){
          $controlContainer = $(mapL.map._controlContainer);
          $controlContainer.append('<div class="leaflet-top leaflet-center"></div>');
          mapL.map._controlCorners.topcenter = $controlContainer.children('.leaflet-top.leaflet-center').first()[0];
        }

      }

    },

    changeSplitScreen : function(){
      isSplitScreen = !isSplitScreen;
      self.updateSize();
      self.updateSplitScreen(isSplitScreen);
      // self.updateCalendar();
    },

    updateSplitScreen : function(){

      var latlng = new L.LatLng(status.lat, status.lng),
          zoomR  = status.zoom - mapR.map.options.crs.options.zoomInfo.min,
          zoomL  = status.zoom - mapL.map.options.crs.options.zoomInfo.min,
          isTouch = L.Browser.touch;


      // console.log("SS.in", "zoomL", zoomL, "zoomR", zoomR);

      mapR.map.sync();
      mapL.map.sync();

      mapL.ctrls.recticle._container.style.visibility = isSplitScreen ? "visible" : "hidden";
      mapL.ctrls.slider._container.style.visibility   = isSplitScreen ? "visible" : "hidden";
      mapL.ctrls.full._container.style.visibility     = isSplitScreen ? "visible" : "hidden";
      mapL.ctrls.split._container.style.visibility    = isSplitScreen ? "visible" : "hidden";

      // mapL.ctrls.coords._container.style.visibility   = isTouch ? "hidden" : isSplitScreen ? "hidden"  : "visible";
      mapL.ctrls.cursor._container.style.visibility   = isTouch ? "hidden" : isSplitScreen ? "visible" : "hidden";

      mapR.ctrls.recticle._container.style.visibility = isSplitScreen ? "hidden"  : "visible";
      mapR.ctrls.slider._container.style.visibility   = isSplitScreen ? "hidden"  : "visible";
      mapR.ctrls.full._container.style.visibility     = isSplitScreen ? "hidden"  : "visible";
      mapR.ctrls.split._container.style.visibility    = isSplitScreen ? "hidden"  : "visible";
      
      // mapR.ctrls.coords._container.style.visibility   = isTouch ? "hidden" : isSplitScreen ? "visible" : "hidden";

      if (!isSplitScreen){
        mapL.ctrls.cursor.deactivate();

      } else {
        mapL.map.setView([ 0, 0] , 0, {reset: true, animate: false, zoom: false});
        mapR.map.sync(mapL.map);
        mapL.map.sync(mapR.map);
        mapL.map.setView(latlng , zoomL, {reset: true, animate: false, zoom: false});
        mapR.map.setView(latlng , zoomR, {reset: true, animate: false, zoom: false});

      }

      // console.log("SS.out", "LZ", zoomL, "RR", zoomR);

    }, 
    activateMap : function(side, activate){

      var map = (side === "right") ? mapR.map : mapL.map,
          ignoreMap = null;

      activate = (typeof activate === "undefined") ? true : false;

      function getMapX(e){
        return $(e.target._container).attr("id") === "mapR" ? mapR : mapL;
      }

      function otherMap(map){
        return (map === mapR.map) ? mapL.map : mapR.map;
      }

      function coords(map){
        var c = map.getCenter();
        return c.lng + ", " + c.lat + ", " + map.getZoom();
      }

      function onMapMouseMove(e, map, side) {
          console.log("EVENT." + side + ".move: " + e.latlng);
      }

      function onMapZoomStart(e, map, side) {

        // console.log(side, mapL.map._animateToCenter, mapR.map._animateToCenter);
        // console.log("Start", e);
      }


      function onMapZoomEnd(e) {

        var 
          mapX = getMapX(e),
          lay  = Layers.byIndex((mapX === mapR) ? status.lay1[0] : status.lay2[0]),
          zoom = lay.zoom,
          key  = lay.key
        ;

        if (!ignore.events){
          status.zoom = mapX.map.getZoom() //+ mapX.map.options.crs.options.zoomInfo.min;
          self.updatePerma();
        }

        // console.log("EVENT.zoom.end", mapX.map.options.side, key, "st", status.zoom, "map", mapX.map.getZoom(), JSON.stringify(zoom));

      }
      function onMapMoveEnd(e) {

        var mapX = getMapX(e), c = mapX.map.getCenter();
  
        if (!ignore.events){
          status.lng = c.lng;
          status.lat = c.lat;
          self.geocode();
          self.updatePerma();
        }

      }
      function onMapDragEnd(e, map, side) {
          // console.log("EVENT." + side + ".drag z:" + map.getZoom(), "ll", coords(map));
      }
      function onMapResize(e, map, side) {
          // console.log("EVENT." + side + ".resize w/h:", e.newSize.x, e.newSize.y);
      }

      // function onLayerAdd(e, map, side) {
      //     // console.log("EVENT." + side + ".addLayer :", e.layer);
      //     // if (side === "right"){mapR.layer = e.layer}
      //     if (side === "left") {
      //       // var layRight = Layers.byIndex(status.layers[0]),
      //       //     layLeft  = Layers.byKey(e.layer.options.key),
      //       //     realZoom = status.zoom - layRight.zoomDiff;
      //       //     newZoom = realZoom + layLeft.zoomDiff;
      //       // if (map.getZoom() !== newZoom) {
      //       //   map.setZoom(newZoom);
      //       //   console.log("Left Zoom:", newZoom);
      //       // }
      //     }
      // }

      // function onLayerRemove(e, map, side) {
      //     // console.log("EVENT." + side + ".layerremove :", e.layer);
      //     // if (side === "left") {mapL.layer = e.layer}
      //     // if (side === "right"){mapR.layer = e.layer}
      // }

      function onMouseOver(e) {
          var mapX = getMapX(e);
          // mapX.ctrls.coords._container.style.visibility = "visible";
          // mapX.ctrls.scale._container.style.visibility = "visible";
          // console.log("EVENT." + side + ".over:");
      }
      function onMouseOut(e) {
          var mapX = getMapX(e);
          // mapX.ctrls.coords._container.style.visibility = "hidden";
          // mapX.ctrls.scale._container.style.visibility = "hidden";
          // console.log("EVENT." + side + ".out:");
      }

      function onLayerRemove(e){
        var mapX = getMapX(e);
        // console.log("onLayerRemove", mapX.map.options.side, e.layer.key);
      }

      function onLayerAdd(e){
        var mapX = getMapX(e);
        // console.log("onLayerAdd", mapX.map.options.side, e.layer.key);
      }

      if (activate) {
        map.on('zoomend',       onMapZoomEnd);
        map.on('moveend',       onMapMoveEnd);
        map.on('dragend',       onMapDragEnd);
        map.on('resize',        onMapResize);
        map.on('layeradd',      onLayerAdd);
        map.on('mouseover',     onMouseOver);
        map.on('mouseout',      onMouseOut);
        map.on('layerremove',   onLayerRemove);
        map.on('layeradd',      onLayerAdd);
      } else {
        map.off('zoomend',        onMapZoomEnd);
        map.off('moveend',        onMapMoveEnd);
        map.off('dragend',        onMapDragEnd);
        map.off('resize',         onMapResize);
        map.off('layeradd',       onLayerAdd);
        map.off('mouseover',      onMouseOver);
        map.off('mouseout',       onMouseOut);
        map.off('layerremove',    onLayerRemove);
        map.off('layeradd',       onLayerAdd);
      }

    }
    // addLabel : function(lng, lat, html, map){
    //   // http://leafletjs.com/reference.html#divicon
    //   L.marker([lng, lat], {
    //     icon: new L.Label({className: 'aio-label-marker-red', html: html}),
    //     clickable: false
    //   }).addTo(map || mapR.map);

    //   if (isSplitScreen){
    //     L.marker([lng, lat], {
    //       icon: new L.Label({className: 'aio-label-marker-red', html: html}),
    //       clickable: false
    //     }).addTo(map || mapL.map);
    //   }
    // },


    // addAMSR : function(){

    //   var imageUrl = '/overlays/amsr2/Arc_20131004_res3.125.crop.png',
    //       imageBounds = [[40.712216, -74.22655], [40.773941, -74.12544]],
    //                    // left           up         right         down
    //       imageBounds = [[168.35, 34.36], [102.34, 31.00]];

    //   return L.imageOverlay(imageUrl, imageBounds).addTo(mapR.map);     

    // /*      
    //   noiv
    //   L.ImageOverlay is HACKT in SRC !!!!!!!!!!!!!!!!!!!!!!!!!
    //   i = L.imageOverlay('/overlays/amsr2/Arc_20131004_res3.125.crop.png', [[31.00, 168.35], [34.36, -9.98]], {opacity:0.5}).addTo(MAPS.right.map);  
    //   MAPS.right.map.removeLayer(i)
    // */


    // }


  };

}()).boot();
