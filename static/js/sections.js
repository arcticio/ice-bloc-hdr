/*jslint bitwise: true, browser: true, evil:true, devel: true, todo: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, TIM, H,  */
/*jshint -W030 */

"use strict";

var Sections = (function () {

  var DEB = false;

  var self,
    lastTop     = NaN,
    sectionlist = ["home", "news", "simulation", "data", "weather", "contact"],
    sections    = {window: {}, navbar: {}}, 
    visibles    = [],
    listeners   = {},
    navbar      = null;

  return {
    boot: function () {return (self = this);

    }, isVisible: function (name) {

      return visibles.indexOf(name) !== -1;


    }, on: function (name, fn) {

      if (!listeners[name]){listeners[name] = [];}
      listeners[name].push(fn);
    

    }, off: function (name, fn) {

      var idx;

      if (!listeners[name]){ return; }

      idx = listeners[name].indexOf(fn);
      if (idx !== -1){
        listeners[name].splice(idx, 1);  
      }


    }, resize: function () {

      sections.navbar.height = $(".navbar").height();
      sections.window.height = $(window).height();

      sectionlist.forEach(function (name) {
      sections[name] = {
        header: {
          top:    $("#" + name + "-header").length ? $("#" + name + "-header").offset().top : 0,
          height: $("#" + name + "-header").length ? $("#" + name + "-header").height() : 0,
        },
        top:    $("#" + name).length ? $("#" + name).offset().top : 0,
        height: $("#" + name).length ? $("#" + name).height() : 0,
      };

      });

      
    }, scroll: function () {

      var 
        scrollTop   = $(window).scrollTop(), 
        winBottom   = scrollTop + sections.window.height,
        newVisibles = sectionlist.filter(function (name) {
          var secTop = sections[name].header.top, 
            secBottom = secTop + sections[name].header.height + sections[name].height;
          return secTop < winBottom && secBottom > scrollTop;
        });

      // check differences
      if (JSON.stringify(newVisibles.sort()) !== JSON.stringify(visibles.sort())){

        // send true, got visible
        newVisibles.forEach(function (name) {
          if (visibles.indexOf(name) === -1){
            if (listeners[name] && listeners[name].length){
              listeners[name].forEach(function (fn) {fn(true);} );

              DEB && console.log("  VIS > " + name);

            }
          }
        });

        // send false, no longer visible
        visibles.forEach(function (name) {
          if (newVisibles.indexOf(name) === -1){
            if (listeners[name] && listeners[name].length){
              listeners[name].forEach(function (fn) {fn(false);} );

              DEB && console.log("UNVIS > " + name);

            }
          }
        });

        visibles = newVisibles;

      }

      lastTop = scrollTop;

    }


  };

}()).boot();