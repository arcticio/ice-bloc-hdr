/*jslint bitwise: true, browser: true, evil:true, devel: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, L, jQuery, MAPS, Layers, Crs, TIM, TimeRange, utc, H, TimeStamp */

/*
 * L.TileLayer.Sentinel is used for putting Sentinel tile layers on the map.
 */

L.TileLayer.Sentinel = L.TileLayer.extend({

  defaultWmsParams: {
    service: 'WMS',
    request: 'GetMap',
    version: '1.1.1',
    layers: '',
    styles: '',
    format: 'image/jpeg',
    transparent: false
  },

  initialize: function (url, options) { // (String, Object)

    this._url = url;

    var wmsParams = L.extend({}, this.defaultWmsParams),
        tileSize = options.tileSize || this.options.tileSize;

    if (options.detectRetina && L.Browser.retina) {
      wmsParams.width = wmsParams.height = tileSize * 2;
    } else {
      wmsParams.width = wmsParams.height = tileSize;
    }

    for (var i in options) {
      // all keys that are not TileLayer options go to WMS params
      if (!this.options.hasOwnProperty(i) && i !== 'crs') {
        wmsParams[i] = options[i];
      }
    }

    if (options.buildDate) {
      this.buildDate = options.buildDate;
    }

    this.wmsParams = wmsParams;

    delete this.wmsParams.zoomdomains;
    delete this.wmsParams.transpic;
    delete this.wmsParams.continuousWorld;
    delete this.wmsParams.noWrap;
    delete this.wmsParams.buildDate;

    L.setOptions(this, options);

  },

  onAdd: function (map) {

    this._crs = this.options.crs || map.options.crs;

    var projectionKey = parseFloat(this.wmsParams.version) >= 1.3 ? 'crs' : 'srs';
    this.wmsParams[projectionKey] = this._crs.code;

    L.TileLayer.prototype.onAdd.call(this, map);
  },

  buildDate: function (day) {
    return "&TIME=" + day + "/" + day;
  },

  getTileUrl: function (tilePoint, zoom) { // (Point, Number) -> String

    var url, 
      map = this._map,
      tileSize = this.options.tileSize,

      nwPoint = tilePoint.multiplyBy(tileSize),
      sePoint = nwPoint.add([tileSize, tileSize]),

      nw = this._crs.project(map.unproject(nwPoint, zoom)),
      se = this._crs.project(map.unproject(sePoint, zoom)),

      toZoom = zoom === undefined ? map._zoom : zoom,

      bbox = [nw.x, se.y, se.x, nw.y].join(','),

      day = (this.options.side === "left") ? MAPS.status.day2 : MAPS.status.day1,

      url = L.Util.template(this._url, {s: this._getSubdomain(tilePoint)});
    ;

    // mind timeRange
    if (this.options.timeRange) {
     if (!this.options.timeRange.covers(utc(day))) {
       return this.options.transpic;
     } 
    }

    return url + L.Util.getParamString(this.wmsParams, url, true) + '&BBOX=' + bbox + this.buildDate(day);
  },

  setParams: function (params, noRedraw) {

    L.extend(this.wmsParams, params);

    if (!noRedraw) {
      this.redraw();
    }

    return this;
  }
});

L.tileLayer.sentinel = function (url, options) {
  return new L.TileLayer.Sentinel(url, options);
};




L.Proj.TileLayer = {};

L.Proj.TileLayer.TMS = L.TileLayer.extend({
  options: {
    tms: true,
    continuousWorld: true,
    date: L.Util.falseFn
  },

  initialize: function(urlTemplate, crs, options) {

    L.setOptions(this, options);

    this._url = urlTemplate;
    this.key = this.options.key;
    this.crs = crs;

  },

  getTileUrl: function(tilePoint) {

    // TODO: relies on some of TileLayer's internals
    var z = this._getZoomForUrl(),
        off = this.crs.options.zoomInfo.off,
        min = this.crs.options.zoomInfo.min,
        gridHeight = Math.ceil((this.crs.projectedBounds[3] - this.crs.projectedBounds[1]) / this._projectedTileSize(z - this.options.zoomOffset || 0)),
        day = (this.options.side === "left") ? MAPS.status.day2 : MAPS.status.day1,
        url;

    // no negative tiles
     if (tilePoint.y < 0 || tilePoint.x < 0) {
       return this.options.transpic;
     } 

    // no black stuff from NASA
    if (this.options.noBlack) {
     if (tilePoint.x >= gridHeight || tilePoint.y >= gridHeight) {
       return this.options.transpic;
     } 
    }

    // stay in timeRange
    if (this.options.timeRange) {
     if (!this.options.timeRange.covers(utc(day))) {
       return this.options.transpic;
     } 
    }
    
    // console.log(this.key, this.options.key, JSON.stringify(tilePoint));

    url = L.Util.template(this._url, L.Util.extend({
      d: this.options.date,
      s: this._getSubdomain(tilePoint),
      z: z + off, //- min,
      x: tilePoint.x  ,//-(off*2 -1),
      y: tilePoint.y  //-(off*2 -1),  //gridHeight - tilePoint.y - 1
    }, this.options));

    return url;


  },

  _projectedTileSize: function(zoom) {
    return (this.options.tileSize / this.crs.scale(zoom));
  }

});


L.TimeOverlay = L.ImageOverlay.extend({
  
  options: {
    opacity: 0.9
  },

  initialize: function (layer, isoh, options) { // (String, LatLngBounds, Object)

    this._layer = layer;
    this._key = layer.key;
    this._bounds = L.latLngBounds(layer.bounds);
    this._mybounds = layer.bounds;
    this.updateTime(isoh);
    this.options.opacity = layer.opacity;
    
  },
  onAdd: function (map) {

    this._map = map;

    if (!this._image) {
      this._initImage();
      this._image.onerror = L.bind(function(e){
        this._map.fire("dataload");
        this._image.src = MAPS.notavail;
        // console.log(this._key, "img.error.replace: ", this._image.src);
      }, this);
      this._image.onload = L.bind(function(e){
        this._map.fire("dataload");
        // console.log(this._key, "img.loaded: ", this._image.src);
      }, this);
    }

    map._panes.overlayPane.appendChild(this._image);

    map.on('viewreset', this._reset, this);

    if (map.options.zoomAnimation && L.Browser.any3d) {
      map.on('zoomanim', this._animateZoom, this);
    }

    this._reset();
  },
  updateTime : function(stamp){

    var tr = this._layer.timeRange;

    this._timeStamp = stamp;

    if (tr.covers(stamp)){
      this._url = stamp.format(this._layer.urlPattern);
    } else {
      this._url = MAPS.transpic;
      DEBUG && console.log("updateTime.not.covered", this._layer.key, this._timeStamp.toIso(4), this._layer.timeRange.toString());
    }
    
    if (this._image) {
      // console.log("updateTime.url", this._url, stamp.toString());
      this._map.fire("dataloading");
      this._image.src = this._url;
      if (this._image.complete || this._image.readyState === 4) {
        this._map.fire("dataload");
        // console.log(this._key, "img.cache: ", this._image.src);
      }
    }

  }

});
L.timeOverlay = function (url, bounds, options) {
  return new L.TimeOverlay(url, bounds, options);
};


L.MarkerOverlay = L.LayerGroup.extend({

  options: {},

  initialize: function (dataLayer, options) {

    var name, item, label, style = dataLayer.style;

    L.setOptions(this, options);
    this._layers = {};

    for (name in dataLayer.data){
      item  = dataLayer.data[name];
      label = L.marker(item.coords, {
        icon: new L.Label({className: style + item.style, html: name}),
        clickable: false,
        minzoom: item.lvl,
        riseOnHover: true
      });
      this._layers[name] = label;
    }

  },
  updateTime : L.Util.falseFn,
  onAdd: function (map) {
    var label;
    this._map = map;
    this._updateZoom();
    map.on('zoomend zoomlevelschange', this._updateZoom, this);
    return this;
  },
  onRemove: function (map) {
    var label;
    this._map = map;
    for (label in this._layers) {
      this.removeLayer(this._layers[label]);
    }    
    map.off('zoomend zoomlevelschange', this._updateZoom, this);
  },
  _updateZoom : function(){
    var lbl, name, zoom = MAPS.status.zoom; //this._map.getZoom();
    for (name in this._layers) {
      lbl = this._layers[name];
      if (this.hasLayer(lbl)) {
        if (lbl.options.minzoom > MAPS.status.zoom){this.removeLayer(lbl);}
      } else {
        if (lbl.options.minzoom <= MAPS.status.zoom){this.addLayer(lbl);}
      }
    }    

  } 
});



L.Control.Calendar = L.Control.extend({
  options: {
    position: 'topcenter',
    title: 'Date Picker',
    collapsed: true,
    timeRange: new TimeRange()
  },
  initialize: function (stamp, options) {
    L.setOptions(this, options);
    this._stamp = stamp;
  },
  onAdd: function (map) {
    
    var className = this._className = 'leaflet-control-calendar', 
        side = this.side = map.options.side.toLowerCase(),
        container = this._container  = L.DomUtil.create('div', className),
        link      = this._link       = L.DomUtil.create('a', className + '-toggle', container),
        contCal   = this._contCal    = L.DomUtil.create('div', className + "-container", container);

    this._map = map;

    //Makes this work on IE10 Touch devices by stopping it from firing a mouseout event when the touch is released
    container.setAttribute('aria-haspopup', true);

    link.href = '#';
    link.title = 'Layers';
    // link.innerHTML = this._stamp.toIso(5);

    contCal.style.width = "160px";    // avoids imploded layout

    this._calendar = jQuery(contCal).calendarPicker({
      date: this._stamp,
      parent: this,
      useWheel:true,
      years:1,
      months:2,
      days:2,
      hours:2,
      showDayArrows:true,
      timeRange: this.options.timeRange,
      callback: L.bind(this._onCalClick, this)
    });

    if (!this.options.collapsed) {
      this._expand();
    }

    this.activate(true);
    return container;

  },
  
  activate: function (onoff) {
    
    onoff = onoff || true;

    var container = this._container,
        link = this._link;

    if (onoff) {

      if (!L.Browser.touch) {
        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.on(container, 'mousewheel', L.DomEvent.stopPropagation);
      
      } else {
        L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation);
      }

      if (!L.Browser.android) {
        L.DomEvent
            .on(container, 'mouseover', this._expand, this)
            .on(container, 'mouseout', this._collapse, this);
      }
      

      if (L.Browser.touch) {
        L.DomEvent
            .on(link, 'click', L.DomEvent.stop)
            .on(link, 'click', this._expand, this);
      }
      else {
        L.DomEvent.on(this._link, 'focus', this._expand, this);
      }

      this._map.on('click', this._collapse, this);

    }    


  },
  onRemove: function(map){
    console.log("Cal.onremove...");
    this.activate(false);
  },
  updateDisplay: function(iso){
    this._link.innerHTML = iso;
  },
  updateTime: function(stamp){
    this._calendar.changeDate(stamp);
  },
  updateRange: function(range, stamp){  // calles after new LAyer
    this._calendar.options.timeRange = range;
    this._calendar.stamp = stamp;
    this._calendar.changeDate(stamp);
  },
  _onCalClick: function(cal, stamp){
      // console.log("_onCalClick.in", this.side, stamp.toString());
      MAPS.changeTime(this, stamp);
  },
  _expand: function () {
    L.DomUtil.addClass(this._container, this._className + '-expanded');
  },
  _collapse: function () {
    this._container.className = this._container.className.replace(this._className + '-expanded', '');
  }
  
});
L.control.calendar = function (options) {
  return new L.Control.Calendar(options);
};
L.Map.addInitHook(function () {
  if (this.options.calendarControl) {
    this.calendarControl = L.control.calendar(this.options.calendarControlOptions);
    this.addControl(this.calendarControl);
  }
});



/*
 * L.Control.Layers is a control to allow users to switch between different layers on the map.
 */

L.Control.SimpleLayers = L.Control.extend({
  options: {
    collapsed: true,
    position: 'topright',
    autoZIndex: true
  },

  initialize: function (baseLayers, overlays, options) {

    var i;

    L.setOptions(this, options);

    this._layers = {};
    this._lastZIndex = 0;
    this._handlingClick = false;

    for (i in baseLayers) {
      this._addLayer(baseLayers[i], i);
    }

    for (i in overlays) {
      this._addLayer(overlays[i], i, true);
    }
  },

  onAdd: function (map) {
    this._initLayout();
    this._update();

    map
        .on('layeradd', this._onLayerChange, this)
        .on('layerremove', this._onLayerChange, this);

    return this._container;
  },

  onRemove: function (map) {
    map
        .off('layeradd', this._onLayerChange)
        .off('layerremove', this._onLayerChange);
  },

  addBaseLayer: function (layer, name) {
    this._addLayer(layer, name);
    this._update();
    return this;
  },

  addOverlay: function (layer, name) {
    this._addLayer(layer, name, true);
    this._update();
    return this;
  },

  clear: function(){
    H.each(this._layers, L.bind(function(layer){
      var id = L.stamp(layer);
      delete this._layers[id];
    }, this));
    this._update();
  },

  removeLayer: function (layer) {
    var id = L.stamp(layer);
    delete this._layers[id];
    this._update();
    return this;
  },

  _initLayout: function () {
    var className = 'leaflet-control-layers',
        container = this._container = L.DomUtil.create('div', className);

    //Makes this work on IE10 Touch devices by stopping it from firing a mouseout event when the touch is released
    container.setAttribute('aria-haspopup', true);

    if (!L.Browser.touch) {
      L.DomEvent.disableClickPropagation(container);
      L.DomEvent.on(container, 'mousewheel', L.DomEvent.stopPropagation);
    } else {
      L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation);
    }

    var form = this._form = L.DomUtil.create('form', className + '-list');

    if (this.options.collapsed) {
      if (!L.Browser.android) {
        L.DomEvent
            .on(container, 'mouseover', this._expand, this)
            .on(container, 'mouseout', this._collapse, this);
      }
      var link = this._layersLink = L.DomUtil.create('a', className + '-toggle', container);
      link.href = '#';
      link.title = 'Layers';

      if (L.Browser.touch) {
        L.DomEvent
            .on(link, 'click', L.DomEvent.stop)
            .on(link, 'click', this._expand, this);
      }
      else {
        L.DomEvent.on(link, 'focus', this._expand, this);
      }

      this._map.on('click', this._collapse, this);
      // TODO keyboard accessibility
    } else {
      this._expand();
    }

    this._baseLayersList = L.DomUtil.create('div', className + '-base', form);
    this._separator = L.DomUtil.create('div', className + '-separator', form);
    this._overlaysList = L.DomUtil.create('div', className + '-overlays', form);

    container.appendChild(form);
  },

  _addLayer: function (layer, name, overlay) {
    var id = L.stamp(layer);

    this._layers[id] = {
      layer: layer,
      name: name,
      overlay: overlay
    };

    if (this.options.autoZIndex && layer.setZIndex) {
      this._lastZIndex++;
      layer.setZIndex(this._lastZIndex);
    }
  },

  _update: function () {
    if (!this._container) {
      return;
    }

    this._baseLayersList.innerHTML = '';
    this._overlaysList.innerHTML = '';

    var baseLayersPresent = false,
        overlaysPresent = false,
        i, obj;

    for (i in this._layers) {
      obj = this._layers[i];
      this._addItem(obj);
      overlaysPresent = overlaysPresent || obj.overlay;
      baseLayersPresent = baseLayersPresent || !obj.overlay;
    }

    this._separator.style.display = overlaysPresent && baseLayersPresent ? '' : 'none';
  },

  _onLayerChange: function (e) {
    var obj = this._layers[L.stamp(e.layer)];

    if (!obj) { return; }

    if (!this._handlingClick) {
      this._update();
    }

    var type = obj.overlay ?
      (e.type === 'layeradd' ? 'overlayadd' : 'overlayremove') :
      (e.type === 'layeradd' ? 'baselayerchange' : null);

    if (type) {
      this._map.fire(type, obj);
    }
  },

  // IE7 bugs out if you create a radio dynamically, so you have to do it this hacky way (see http://bit.ly/PqYLBe)
  _createRadioElement: function (name, checked) {

    var radioHtml = '<input type="radio" class="leaflet-control-layers-selector" name="' + name + '"';
    if (checked) {
      radioHtml += ' checked="checked"';
    }
    radioHtml += '/>';

    var radioFragment = document.createElement('div');
    radioFragment.innerHTML = radioHtml;

    return radioFragment.firstChild;
  },

  _addItem: function (obj) {
    var label = document.createElement('label'),
        input,
        checked = this._map.hasLayer(obj.layer);

    if (obj.overlay) {
      input = document.createElement('input');
      input.type = 'checkbox';
      input.className = 'leaflet-control-layers-selector';
      input.defaultChecked = checked;
    } else {
      input = this._createRadioElement('leaflet-base-layers', checked);
    }

    input.layerId = L.stamp(obj.layer);

    L.DomEvent.on(input, 'click', this._onInputClick, this);

    var name = document.createElement('span');
    name.innerHTML = ' ' + obj.name;

    label.appendChild(input);
    label.appendChild(name);

    var container = obj.overlay ? this._overlaysList : this._baseLayersList;
    container.appendChild(label);

    return label;
  },

  _onInputClick: function () {
    var i, input, obj,
        inputs = this._form.getElementsByTagName('input'),
        inputsLen = inputs.length;

    this._handlingClick = true;

    for (i = 0; i < inputsLen; i++) {
      input = inputs[i];
      obj = this._layers[input.layerId];

      if (input.checked && !this._map.hasLayer(obj.layer)) {
        // noiv
        MAPS.changeBase(this._map, obj.layer.options.key);
      }
    }

    this._handlingClick = false;
  },

  _expand: function () {
    L.DomUtil.addClass(this._container, 'leaflet-control-layers-expanded');
  },

  _collapse: function () {
    this._container.className = this._container.className.replace(' leaflet-control-layers-expanded', '');
  }
});
L.control.simplelayers = function (baseLayers, overlays, options) {
  return new L.Control.SimpleLayers(baseLayers, overlays, options);
};




L.Control.PrettyLayers = L.Control.Layers.extend({

  options: {
    collapsed: true,
    position: 'topright',
    autoZIndex: true
  },

  initialize: function (activeLayer, options) {

    L.setOptions(this, options);

    this._layers = Layers.filter(function(l){
      return l.type === "base";
    });
    this._activeLayer = activeLayer;
    this._lastZIndex = 0;
    this._handlingClick = false;
    this._overlays = {};

  },
  onAdd: function (map) {

    this._map = map;
    this._initLayout();
    // this.update();
    map.on('resize', this._onresize, this);
    return this._container;

  },
  onRemove: function (map) {
    
    map.off('resize', this._onresize);

  },
  _onresize: function (e) {

    var d = MAPS.isSplitScreen() ? 4 : 2,
        w = Math.min($(window).width()/d - 66 , 256),
        h = $(window).height()*0.8;

    // this._list.style.height =  h + "px";
    this._list.style.width  =  "256px"; //w + "px";

    this._list.style.height =  Math.min($(window).height()-70, this._height || 3000) + "px";

    // console.log("Layer: w/h", w, h, d);
  },

  _expand: function () {

    L.DomUtil.addClass(this._container, 'leaflet-control-layers-expanded');

    var height = 0, heights;
    
    // this is awkward
    heights = $("div.leaflet-control-layers-list").children().map(function(i, el){return $(el).height();});

    heights.each(function(e, t){
      height += t;
    });

    this._height = height;
    this._list.style.height =  Math.min($(window).height()-70, this._height) + "px";    

  },
  _collapse: function () {
    L.DomUtil.removeClass(this._container, 'leaflet-control-layers-expanded');
    // this._container.className = this._container.className.replace(' leaflet-control-layers-expanded', '');
  },

  _initLayout: function () {

    var className = 'leaflet-control-layers',
        container = this._container = L.DomUtil.create('div', className),
        list = this._list = L.DomUtil.create('div', className + "-list", container);

    //Makes this work on IE10 Touch devices by stopping it from firing a mouseout event when the touch is released
    container.setAttribute('aria-haspopup', true);

    list.style.overflowY = "scroll";
    this._onresize();

    if (!L.Browser.touch) {
      L.DomEvent.disableClickPropagation(container);
      L.DomEvent.on(container, 'mousewheel', L.DomEvent.stopPropagation);
    } else {
      L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation);
    }

    if (this.options.collapsed) {
      if (!L.Browser.android) {
        L.DomEvent
            .on(container, 'mouseover', this._expand, this)
            .on(container, 'mouseout', this._collapse, this);
      }
      var link = this._layersLink = L.DomUtil.create('a', className + '-toggle', container);
      link.href = '#';
      link.title = 'Layers';

      if (L.Browser.touch) {
        L.DomEvent
            .on(link, 'click', L.DomEvent.stop)
            .on(link, 'click', this._expand, this);
      }
      else {
        L.DomEvent.on(link, 'focus', this._expand, this);
      }

      this._map.on('click', this._collapse, this);
      // TODO keyboard accessibility
    } else {
      this._expand();
    }

    // container.appendChild(list);

  },  

  update: function () {

    var i, self = this, height = 0, heights;
    
    $(this._list).children().each(function(i, cont){
      L.DomEvent.off(cont, 'click', self._onInputClick);
    });

    this._list.innerHTML = '';

    //TODO: sort active first
    for (i in this._layers) {
      if (this._layers.hasOwnProperty(i)) {
        this._addLayer(this._layers[i].key, "base");
      }
    }  

    // // where is reduce?
    // heights = $("div.leaflet-control-layers-list").children().map(function(i, el){return $(el).height();});
    // heights.each(function(e, t){
    //   height += t;
    // });

    // this._height = height;
    // this._list.style.height =  Math.min($(window).height()-70, this._height) + "px";

    return this;

  }, 
  _addLayer: function (key, type) { 

    var self = this, layer = Layers.byKey(key), aDate, divCont,
        divTrenner, divTrennerD, imgLayer, divTitle, divComment, divDates;

    if (!layer.enabled){return;}

    divCont     = L.DomUtil.create('div');
    divTrenner  = L.DomUtil.create('div', "aio-prettylayers-trenner");
    divTrennerD = L.DomUtil.create('div', "aio-prettylayers-trenner-dates");
    imgLayer    = L.DomUtil.create('img', "aio-prettylayers-" + type + "-img");
    divTitle    = L.DomUtil.create('div', "aio-prettylayers-" + type + "-title");
    divComment  = L.DomUtil.create('div', "aio-prettylayers-" + type + "-comment");
    divDates    = L.DomUtil.create('div', "aio-prettylayers-" + type + "-dates");


    $(divCont).data("key", key);
    // L.DomEvent.on(divCont, 'click', this._onInputClick, this);
    $(divCont).click(L.bind(this._onInputClick, this));

    // L.DomEvent.on(divCont, 'mouseover', this._onInputOver, this);
    // L.DomEvent.on(divCont, 'mouseout',  this._onInputOut, this);

    divTitle.innerHTML    = layer.name;
    $(divTitle).attr("title", layer.comment);
    divComment.innerHTML  = layer.comment;
    // divDates.innerHTML    = layer.timeRange ? layer.timeRange.toString() : "";

    imgLayer.src = layer.icon;
    imgLayer.width  = (type === "base") ? "48" : "32";
    imgLayer.height = (type === "base") ? "48" : "32";

    divCont.appendChild(imgLayer);
    divCont.appendChild(divTitle);
    divCont.appendChild(divComment);
    if (layer.colorbar) {
      divCont.appendChild($I("IMG", {src: layer.colorbar, width: 180, height: 24, className:"aio-prettylayers-" + type + "-cbar"}));
    }
    if (layer.timeRange && layer.timeRange.ranges.length > 0) {
      divCont.appendChild(divTrennerD);
      divCont.appendChild(divDates);
      layer.timeRange.ranges.forEach(function(r){
        aDate = L.DomUtil.create('a', "aio-prettylayers-" + type + "-date", divDates);
        aDate.innerHTML = r[0] + " > " + r[1];
        aDate.href = "#";
        aDate.onclick = (function(){return function(e){
          // var tr = new TimeRange(r[0], r[1]).center()
          console.log(utc(r[0]).toString());
          return H.eat(e);
        };}());

      });
    }
    divCont.appendChild(divTrenner);

    divCont.className = (key === this._activeLayer || this._overlays[key]) ?
      "aio-prettylayers-" + type + "-cont-active" : 
      "aio-prettylayers-" + type + "-cont";

    this._list.appendChild(divCont);

    if (key === this._activeLayer) {
      if (layer.overlays) {
        layer.overlays.forEach(function(key){
          self._addLayer(key, "over");
        });
      }
    }


    
  },  
  updateActiveLayer: function (activeLayer) {

    // if (!this._container) {return;}

    this._activeLayer = activeLayer;
    this.update(); 

  },

  _onInputClick: function (e) {

    var key  = $(e.currentTarget).data("key"),
        type = Layers.byKey(key).type;

    if (type === "base") {
      this._overlays = {};
      MAPS.changeBase(this._map, key);

    } else {
      // this._overlays[key] = !this._overlays[key];
      MAPS.changeOverlay(this._map, key, !this._overlays[key]);

    }

  }

});


L.Citylayer = L.Class.extend({

  //  map.addLayer(new MyCustomLayer(latlng));

    initialize: function (latlng, options) {
        // save position of the layer or any options from the constructor
        this._latlng = latlng;
        L.Util.setOptions(this, options);
    },

    onAdd: function (map) {
        this._map = map;

        // create a DOM element and put it into one of the map panes
        this._el = L.DomUtil.create('div', 'my-custom-layer leaflet-zoom-hide');
        map.getPanes().overlayPane.appendChild(this._el);

        // add a viewreset event listener for updating layer's position, do the latter
        map.on('viewreset', this._reset, this);
        this._reset();
    },

    onRemove: function (map) {
        // remove layer's DOM elements and listeners
        map.getPanes().overlayPane.removeChild(this._el);
        map.off('viewreset', this._reset, this);
    },

    _reset: function () {
        // update layer's position
        var pos = this._map.latLngToLayerPoint(this._latlng);
        L.DomUtil.setPosition(this._el, pos);
    }
});

L.Label = L.Icon.extend({
  options: {
    // iconSize: [12, 12], // also can be set through CSS
    /*
    iconAnchor: (Point)
    popupAnchor: (Point)
    html: (String)
    bgPos: (Point)
    */
    className: 'leaflet-div-icon',
    html: false
  },

  createIcon: function (oldIcon) {
    var div = (oldIcon && oldIcon.tagName === 'DIV') ? oldIcon : document.createElement('div'),
        options = this.options;

    if (options.html !== false) {
      div.innerHTML = options.html;
    } else {
      div.innerHTML = '';
    }

    if (options.bgPos) {
      div.style.backgroundPosition =
              (-options.bgPos.x) + 'px ' + (-options.bgPos.y) + 'px';
    }

    this._setIconStyles(div, 'icon');
    return div;
  },

  _setIconStyles: function (img, name) {
    var options = this.options,
        size = null, //L.point(options[name + 'Size']),
        anchor;

    if (name === 'shadow') {
      anchor = L.point(options.shadowAnchor || options.iconAnchor);
    } else {
      anchor = L.point(options.iconAnchor);
    }

    if (!anchor && size) {
      anchor = size.divideBy(2, true);
    }

    img.className = 'leaflet-marker-' + name + ' ' + options.className;

    if (anchor) {
      img.style.marginLeft = (-anchor.x) + 'px';
      img.style.marginTop  = (-anchor.y) + 'px';
    }

    if (size) {
      img.style.width  = size.x + 'px';
      img.style.height = size.y + 'px';
    }
  },

  createShadow: function () {
    return null;
  }
});
  

L.Control.SplitScreen = L.Control.extend({
  
  options: {
    position: 'topleft',
    title: 'Toggle Split-Screen',
    forceSeparateButton: false
  },
  
  onAdd: function (map) {
    
    var className = 'leaflet-control-split-screen', container;
    
    container = L.DomUtil.create('div', 'leaflet-bar');
    this._createButton(this.options.title, className, container, this.toogleSplitScreen, map);
    return container;

  },
  
  _createButton: function (title, className, container, fn, context) {

    var link = L.DomUtil.create('a', className, container);
    link.href = '#';
    link.title = title;

    L.DomEvent
      .addListener(link, 'click', L.DomEvent.stopPropagation)
      .addListener(link, 'click', L.DomEvent.preventDefault)
      .addListener(link, 'click', fn, context);
    
    return link;
  },
  
  toogleSplitScreen: function () {
    MAPS.changeSplitScreen();
    this.invalidateSize();
  }
  
});
L.Map.addInitHook(function () {
  if (this.options.splitscreenControl) {
    this.splitscreenControl = L.control.splitscreen(this.options.splitscreenControlOptions);
    this.addControl(this.splitscreenControl);
  }
});
L.control.splitscreen = function (options) {
  return new L.Control.SplitScreen(options);
};



L.Control.SplitCursor = L.Control.extend({
  
  options: {
    position: 'topleft',
    title: 'Toggle Mousepointer',
    forceSeparateButton: false
  },
  onRemove: function (map) {
    console.log("Cursor.onRemove");
  },
  onAdd: function (map) {
    
    var self = this, className = 'leaflet-control-split-cursor', container;

    this._active = false;
    this._cursor = jQuery("#cursor");
    this._oldcss = jQuery(".leaflet-container").css("cursor");
    
    container = L.DomUtil.create('div', 'leaflet-bar');
    this._createButton(this.options.title, className, container, this.toogleSplitCursor, this);

    jQuery(window).mousemove(L.bind(function(e){
      if(self._active){
        var half = $(window).width()/2,
            bord = MAPS.layout.borderCenter;
        if(e.clientX > half){
          self._cursor.css({left: e.clientX - half - bord + "px", top: e.clientY - 2 + "px"});
        } else {
          self._cursor.css({left: e.clientX + half + bord - 2 + "px", top: e.clientY - 2 + "px"});
        }
      }
    }, self));

    jQuery(window).mouseenter(function(e){
      self._cursor.css({display: self._active ? "block" : "none"});
    });
    jQuery(window).mouseleave(function(e){
      self._cursor.css({display: "none"});
    });

    return container;

  },
  
  deactivate: function () {
    this._active = false;
    this._cursor.css({display: "none"});
    jQuery(".leaflet-container").css("cursor", this._oldcss);
  },
  toogleSplitCursor: function (e) {
    this._active = !this._active;
    this._cursor.css({display: this._active ? "block" : "none"});
    jQuery(".leaflet-container").css("cursor", this._active ? "default" : this._oldcss);
    console.log("toogleSplitCursor", this._active);
    // this.invalidateSize();
  },

  _createButton: function (title, className, container, fn, context) {

    var link = L.DomUtil.create('a', className, container);
    link.href = '#';
    link.title = title;

    L.DomEvent
      .addListener(link, 'click', L.DomEvent.stopPropagation)
      .addListener(link, 'click', L.DomEvent.preventDefault)
      .addListener(link, 'click', fn, context);
    
    return link;
  }

  
});
L.Map.addInitHook(function () {
  if (this.options.splitcursorControl) {
    this.splitcursorControl = L.control.splitcursor(this.options.splitcursorControlOptions);
    this.addControl(this.splitcursorControl);
  }
});
L.control.splitcursor = function (options) {
  return new L.Control.SplitCursor(options);
};


// Graticule
L.Control.Recticle = L.Control.extend({
  
  options: {
    position: 'topleft',
    title: 'Toggle Recticle',
    forceSeparateButton: false
  },
  onRemove: function (map) {
    console.log("Cursor.onRemove");
  },
  onAdd: function (map) {
    
    var i, container,
        lats = [38.8947, 47.3079, 51.5731, 52.6123, 51.3818, 47.3356];

    this._coords = [];
    this._active = false;
    this._map = map;

    function glat(i){
      return [i % 6];
    }
    
    for (i=-180; i<180; i+=15) {
      this._coords.push([[85, i], [lats[(i+180)/15 % 6], i]], [[85, i], [85, i +15]]);
    }

    container = L.DomUtil.create('div', 'leaflet-bar');
    this._createButton(this.options.title, 'leaflet-control-recticle', container, this.toggleRecticle, this);
    return container;
  },
  deactivate: function () {
    this._active = false;
    this._map.removeLayer(this._polygone);
  },
  toggleRecticle: function (e) {
    this._active = !this._active;
    if (this._active) {
      this._polygone = new L.MultiPolygon(this._coords, {color: '#ffff00', weight:2.5, dashArray:"3, 9"}).addTo(this._map);
    } else {
      this._map.removeLayer(this._polygone);
    }
    // console.log("toogle.Recticle", this._active);
    // this.invalidateSize();
  },

  _createButton: function (title, className, container, fn, context) {

    var link = L.DomUtil.create('a', className, container);
    link.href = '#';
    link.title = title;

    L.DomEvent
      .addListener(link, 'click', L.DomEvent.stopPropagation)
      .addListener(link, 'click', L.DomEvent.preventDefault)
      .addListener(link, 'click', fn, context);
    
    return link;
  }

  
});
L.Map.addInitHook(function () {
  if (this.options.recticleControl) {
    this.recticleControl = L.control.recticle(this.options.recticleControlOptions);
    this.addControl(this.recticleControl);
  }
});
L.control.recticle = function (options) {
  return new L.Control.Recticle(options);
};

