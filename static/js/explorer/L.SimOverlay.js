/*jslint bitwise: true, browser: true, evil:true, devel: true, todo: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, L, window, Simulator, TIM  */

"use strict";




L.SimOverlay = L.FullCanvas.extend({

  options: {
    opacity: 0.9
  },

  map: {
    x:    NaN,
    y:    NaN,
    size: NaN
  },

  sizes : {
    0: 512,
    1: 1024,
    2: 2048,
    3: 4096,
    4: 8192
  },

  initialize: function (layer, isoh, options) { // (String, LatLngBounds, Object)

      this._layer = layer;

      this._myCanvas = document.createElement('canvas');
      this._myCanvas.style.position = 'absolute';
      this._myCanvas.style.top = 0;
      this._myCanvas.style.left = 0;
      this._myContext = this._myCanvas.getContext('2d');

      $(this._myCanvas).attr("GFS", true);

      console.log("SimOverlay.initialize" ); //, layer, isoh, options);



  },

  updateTime: function (stamp){


  },

  canvasReset: function(){
      var size = this._myMap.getSize();
      this._myCanvas.width = size.x;
      this._myCanvas.height = size.y;
      this.drawCanvas();
  },

  onRemove: function (map) {

      // map._container.removeChild(this._staticPane);
      map._panes.staticPane.removeChild(this._myCanvas);

      map.off('viewreset', this.canvasReset, this);
      map.off('move', this.canvasReset, this);
      map.off('resize', this.canvasReset, this);
      map.off('click', this.handleClick, this);

      console.log("SimOverlay.onRemove");
  },

  onAdd: function (map) {

      this._myMap = map;
      if (!map._panes.staticPane) {
          map._panes.staticPane = map._createPane('leaflet-tile-pane', map._container);
      }
      this._staticPane = map._panes.staticPane;
      this._staticPane.appendChild(this._myCanvas);

      map.on('viewreset', this.canvasReset, this);
      map.on('move', this.canvasReset, this);
      map.on('resize', this.canvasReset, this);
      map.on('click', this.handleClick, this);

      this.canvasReset();

      console.log("SimOverlay.onAdd");
  },

  handleClick: function(e) {

      var j = e.containerPoint;
      var bounds = L.latLngBounds(this._myMap.containerPointToLatLng(j.add(L.point(3,3))), this._myMap.containerPointToLatLng(j.subtract(L.point(3,3))));

      console.log("SimOverlay.click", j, bounds);

      // var points = this._myQuad.retrieveInBounds(this.boundsToQuery(bounds));
      // if(points.length > 0)
      //     this.clickedPoints(points, e);
  },

  calcMap: function () {


      // layerPointToContainerPoint, Converts the point relative to the map layer to a point relative to the map container.
      // containerPointToLayerPoint, Converts the point relative to the map container to a point relative to the map layer.

      // var b = this._myMap.getPixelBounds(); // bounds of the current map view in projected pixel coordinates
      // var p = this._myMap.getPixelOrigin(); // projected pixel coordinates of the top left point of the map layer
      // var s = this._myMap.getSize();        // current size of the map container. //innerwidth


      var m = this._myMap;
      var bounds = m.getPixelBounds();

      this.map.size = this.sizes[m.getZoom()];

      this.map.x = -bounds.min.x;
      this.map.y = -bounds.min.y;

  },

  drawCanvas: function() {

      this.calcMap();

      var canvas = this.getCanvas();
      var ctx = canvas.getContext('2d');

      // var m = this._myMap;

      if (!this._myMap) {return;}

      
      // clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = "rgba(40, 0, 0, 0.2)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.strokeStyle = "rgba(40, 0, 0, 0.8)";
      ctx.strokeRect(64, 64, canvas.width -128, canvas.height -128);



      ctx.fillStyle = "rgba(255, 255, 0, 0.3)";
      ctx.fillRect(this.map.x, this.map.y, this.map.size, this.map.size);

      console.log("drawCanvas", this.map.x, this.map.y, this.map.size);




  },

  //over riding the getsource function

  drawSource: function(point) {
      //get the context
      
      var ctx = this._layer.getCanvas().getContext("2d");

      ctx.globalCompositeOperation = "lighter";
      //drawing the shape of the point
      ctx.beginPath();
      //adding gradient 
      var grd = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, 10);
      grd.addColorStop(0.200, 'rgba(255, 242, 0, 1)');
      grd.addColorStop(0.370, 'rgba(255, 157, 0, 1)');
      grd.addColorStop(0.5, 'rgba(255,255, 255, 1)');
      ctx.fillStyle = grd;
      ctx.arc(point.x, point.y , 2, 0, 2 * Math.PI, true);
      ctx.fill();
  },

  redraw: function(){
      this.drawCanvas();
  }

});

L.simOverlay = function (url, bounds, options) {
  return new L.SimOverlay(url, bounds, options);
};
