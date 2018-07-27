/*jslint bitwise: true, browser: true, evil:true, devel: true, todo: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, TIM, strftime, dataTimeRanges, H */


// https://github.com/samsonjs/strftime


"use strict";

var GALLERY = (function () {

  var self, utcFormat = strftime.timezone(0);

  return {
    boot: function () {
      return (self = this);
    

    }, utc: function () {
      var now = new Date();
      return new Date(Date.UTC(
        now.getUTCFullYear(),
        now.getUTCMonth(), 
        now.getUTCDate() ,       
        now.getUTCHours(), 
        now.getUTCMinutes(), 
        now.getUTCSeconds(), 
        now.getUTCMilliseconds()
      ));


    }, diffYM: function (dt, y, m) {
  
      y = y || 0; m = m || 0;
      
      var date = new Date(dt);
      
      return new Date(Date.UTC(
        date.getUTCFullYear() + y,
        date.getUTCMonth() + m, 
        date.getUTCDate() ,       
        date.getUTCHours(), 
        date.getUTCMinutes(), 
        date.getUTCSeconds(), 
        date.getUTCMilliseconds()
      )).getTime();
  

    }, diffMsecs: function(dt, off){
  
      var n = parseInt(off, 10), o = off.slice(-1);
      
      return {
        'S': function (n){ return dt + n * 1000;},
        'M': function (n){ return dt + n * 1000 * 60;},
        'H': function (n){ return dt + n * 1000 * 60 * 60;},
        'd': function (n){ return dt + n * 1000 * 60 * 60 * 24;},
        'w': function (n){ return dt + n * 1000 * 60 * 60 * 24 * 7;},
        'm': function (n){ return self.diffYM(dt, 0, n);},
        'Y': function (n){ return self.diffYM(dt, n);}
      }[o](n);
      

    }, computeOffset: function  (offset) {
  
      var msecs = Date.now();
      
      offset
        .split("+").join("/+")
        .split("-").join("/-")
        .split("/")
        .filter(function (t){ return !!t; })
        .forEach(function (token) {
          msecs = self.diffMsecs(msecs, token);
        })
      ;

      // console.log("msecs", msecs);
      return new Date(msecs);


    }, offFormat: function (offsetPattern) {

      var
        tokens  = offsetPattern.split(" "),
        offset  = tokens[0],
        pattern = tokens.slice(1).join(" "),
        offTime = self.computeOffset(offset);

      // console.log("offFormat", offset, pattern, offTime);

      return strftime.timezone(0)(pattern, offTime);


    }, initQuicklinks: function () {

      $("#data .exp-quick-link").each(function (idx, ele) {

        var link    = $(ele).find("a"),
            anchor  = link.attr('data-time-range'),
            img     = $(ele).find("img"),
            span    = $(ele).find(".exp-link-date"),
            range   = dataTimeRanges[anchor],
            last    = range[0][1],
            date    = H.iso2DayHour(last),
            pattern = {
              "sic-amsr2"    : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/amsr2/%Y/amsr2-%Y-%m-%d.png",
              "sit-smos"     : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/smos/%Y/smos2-%Y-%m-%d.png",
              "sit-piomas"   : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/piomas/%Y/piomas-%Y-%m.png",
              "sit-cryosat"  : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/cryosat/%Y/cryosat-%Y-%m.png",
              "sst-avhrr"    : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/sst/%Y/sst-%Y-%m-%d.png",
              "gfs-forecast" : "//ice-pics.appspot.com/pics/?mime=png&width=128&url=http://noiv.pythonanywhere.com/data/gfs/%Y/gfs-%Y-%m-%d-%H.png"
            }[anchor],
            src = strftime.timezone(0)(pattern, date);

          span.text(last);
          img.attr("src", src);

          // console.log(pattern, date, src);

      });


    }, initFigures: function () {

      var counter = 0;

      $("#data .row, #weather .row").each(function (idx, ele) {

        var groups = ["test", "ascat", "cryosat", "modis", "zonalmean", "dmitemps", "observations", "anomprob", "icetemps", "greenland"],
            caption, dataOff, row = $(ele), name = row.attr("data-name");

        if (groups.indexOf(name) !== -1){

          row.find("figure a").each(function (idx, ele){
            $(ele).attr('data-off') && $(ele).attr("href", self.offFormat($(ele).attr('data-off')));
          });

          row.find("figure img").each(function (idx, ele){
            $(ele).attr('data-off') && $(ele).attr("src", self.offFormat($(ele).attr('data-off')));
          });

          row.find("figure figcaption").each(function (idx, ele){
            if ((dataOff = $(ele).attr('data-off'))){
              caption = self.offFormat(dataOff);
              $(ele).text(caption);
              $(ele).parent().find("img").attr("alt", caption);
            }
          });

          counter += 1;

        }

      });

      return counter;

    }, init: function () {

      self.initQuicklinks();

      var groupsCOunter   = self.initFigures();

      var stickyElements  = initPhotoSwipeFromDOM('#sticky', 'figure');
      var dataElements    = initPhotoSwipeFromDOM('#data .data-gallery', 'figure');
      var weatherElements = initPhotoSwipeFromDOM('#weather .data-gallery', 'figure');

      TIM.step("LOADED", ["Gallery", "groups", groupsCOunter, "elements", stickyElements, dataElements, weatherElements].join(", "));

    }

  };


} ()).boot();