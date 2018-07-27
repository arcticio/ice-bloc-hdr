/*
 * Extends L.Map to synchronize the interaction on one map to one or more other maps.
 */

L.Map = L.Map.extend({

  sync: function (map) {

    var originalMap = this;

    this._syncMaps = this._syncMaps || [];

    function onZoomEnd() {
      originalMap._syncMaps.forEach(function (toSync) {
        toSync.setView(originalMap.getCenter(), originalMap.getZoom(), {reset: false}, true);
      });
    }

    function dragUpdate() {
      L.Draggable.prototype._updatePosition.call(this);
      var self = this;
      originalMap._syncMaps.forEach(function (toSync) {
        L.DomUtil.setPosition(toSync.dragging._draggable._element, self._newPos);

        // console.log("Drag", "org", self._newPos.x, self._newPos.x , "syc", toSync.dragging._draggable._newPos);

        toSync.fire('move');
      });
    }

    if (!map) {
      this._syncMaps = [];
      originalMap.off('zoomend', onZoomEnd);

    } else {

      this._syncMaps.push(L.extend(map, {
        setView: function (center, zoom, options, sync) {
          if (!sync) {
            this._syncMaps.forEach(function (toSync) {
              toSync.setView(center, zoom, options, true);
            });
          }
          return L.Map.prototype.setView.call(this, center, zoom, options);
        },

        panBy: function (offset, options, sync) {
          if (!sync) {
            this._syncMaps.forEach(function (toSync) {
              toSync.panBy(offset, options, true);
            });
          }
          return L.Map.prototype.panBy.call(this, offset, options);
        },

        _onResize: function (evt, sync) {
          if (!sync) {
            this._syncMaps.forEach(function (toSync) {
              toSync._onResize(evt, true);
            });
          }
          return L.Map.prototype._onResize.call(this, evt);
        }
      }));

      // function onZoomEnd() {
      //   originalMap._syncMaps.forEach(function (toSync) {
      //     toSync.setView(originalMap.getCenter(), originalMap.getZoom(), {reset: false}, true);
      //   });
      // }

      // function dragUpdate() {
      //   L.Draggable.prototype._updatePosition.call(this);
      //   var self = this;
      //   originalMap._syncMaps.forEach(function (toSync) {
      //     L.DomUtil.setPosition(toSync.dragging._draggable._element, self._newPos);
      //     toSync.fire('move');
      //   });
      // }

      originalMap.on('zoomend', onZoomEnd, this);


      originalMap.dragging._draggable._updatePosition = dragUpdate;

    }
    return originalMap;
  }
});

