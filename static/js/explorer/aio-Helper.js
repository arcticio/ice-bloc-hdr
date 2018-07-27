/*jslint bitwise: true, browser: true, evil:true, devel: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals */



/////////// THIS NEEDS NO EXTERNAL STUFF //////////////////////////////////////


var H = {
  bounds:     function (x, min, max){ return Math.min(Math.max(x, min), max); },
  msg:        function (side, txt){ if(false){document.getElementById(side + "info").innerHTML = txt;}},
  padZero:    function (num, len){len = len || 2; num = "0000" + num; return num.substr(num.length-2, 2);},
  clone:      function (o){var e, n = {}; for (e in o) {n[e] = o[e]}; return n;},
  attribs:    function (o){var e, n = []; for (e in o) {n.push(e)}; return n;},
  firstAttr:  function (o){var attr; for (attr in o) {if (o.hasOwnProperty(attr)) {return attr;} } },
  countAttrs: function (o){
    var attr,cnt=0;
    for(attr in o){
      if (o.hasOwnProperty(attr)){
        cnt+=1;
      }
    }return cnt;
  },
  range:      function (st, ed, sp){sp=sp||1; var i,r=[]; for(i=st;i<ed;i+=sp){r.push(i);}return r;},
  each:       function (o, fn) {var a; for (a in o) {if (o.hasOwnProperty(a)){fn(a,o[a]);}}},
  eat:        function (e){e.stopPropagation();e.preventDefault();e.returnValue = false;return false;}
};

// http://stackoverflow.com/questions/5916900/detect-version-of-browser

navigator.sayswho = (function(){
  var N= navigator.appName, ua= navigator.userAgent, tem;
  var M= ua.match(/(opera|chrome|safari|firefox|msie)\/?\s*(\.?\d+(\.\d+)*)/i);
  if(M && (tem= ua.match(/version\/([\.\d]+)/i))!= null) M[2]= tem[1];
  return  M ? [M[1], M[2]]: [N, navigator.appVersion, '-?'];
})();


//noiv, Cologne, 2006, http://ExploreOurPla.net
function $I(){
  var el, i, a, v;
  if (!arguments[0] && arguments[1]){return document.createTextNode(arguments[1]);}
  el = document.createElement(arguments[0]);
  for (i = 1; i < arguments.length; i++){
    a = arguments[i];
    switch (typeof a){
      case "string" :  el.appendChild(document.createTextNode(a)); break;
      case "object" :  if (a.nodeType) {el.appendChild(a);}
                       else {for (v in a) {el[v] = a[v];}}break;
    }
  }
  return el;
}

// /*
//   jQuery.reduce - a jQuery plugin for functional programming
//   @author John Hunter
//   created 2010-09-17
//   use: $.reduce(arr, fnReduce, valueInitial);
//   fnReduce is called with arguments: [valueInitial, value, i, arr]
  
//   reduce will never be jQuery core - its not prototype :p (http://dev.jquery.com/ticket/1886)
// */
// (function ($) {
  
//   $.reduce = function(arr, fnReduce, valueInitial) {
//     if (Array.prototype.reduce) {
//       return Array.prototype.reduce.call(arr, fnReduce, valueInitial);
//     }
    
//     $.each(arr, function(i, value) {
//       valueInitial = fnReduce.call(null, valueInitial, value, i, arr);
//     });
//     return valueInitial;
//   };
 
// })(jQuery);


// http://stackoverflow.com/questions/6213227/fastest-way-to-convert-a-number-to-radix-64-in-javascript

var Base62 = {

  _Rixits :
    // "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-!",
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",

  fromNumber : function(number) {

    if (isNaN(Number(number)) || number === null || number === Number.POSITIVE_INFINITY)
      {throw "The input is not valid";}

    if (number < 0)
      {throw "Can't represent negative numbers now";}

    var rixit; // like 'digit', only in some non-decimal radix 
    var residual = Math.floor(number);
    var result = '';

    while (true) {
      rixit = residual % 62;
      result = this._Rixits.charAt(rixit) + result;
      residual = Math.floor(residual / 62);
      if (residual == 0) {break;}
    }
    return result;
  },

    toNumber : function(rixits) {

      var e, result = 0;

      rixits = rixits.split('');
      for (e in rixits) {
        if (rixits.hasOwnProperty(e)){
          result = (result * 62) + this._Rixits.indexOf(rixits[e]);
        }
      }
      return result;
    }
};

