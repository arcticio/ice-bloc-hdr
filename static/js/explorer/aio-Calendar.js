/*jslint bitwise: true, browser: true, evil:true, devel: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, TimeRange, jQuery, utc */

jQuery.fn.calendarPicker = function(options) {

  var $ = jQuery, doTitle = true,
      calendar = {currentDate: options.date},
      theDiv = this.eq(0);

  if (!options.date) {options.date = new Date();}
  if (typeof(options.timeRange) === "undefined"){options.years=1;}
  if (typeof(options.years) === "undefined"){options.years=1;}
  if (typeof(options.months) === "undefined"){options.months=3;}
  if (typeof(options.days) === "undefined"){options.days=4;}
  if (typeof(options.hours) === "undefined"){options.hours=5;}
  if (typeof(options.showDayArrows) === "undefined"){options.showDayArrows=true;}
  if (typeof(options.showHourArrows) === "undefined"){options.showHourArrows=true;}
  if (typeof(options.useWheel) === "undefined"){options.useWheel=true;}
  if (typeof(options.callbackDelay) === "undefined"){options.callbackDelay=500;}
  if (typeof(options.monthNames) === "undefined"){
    options.monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];}
  if (typeof(options.dayNames) === "undefined"){
    options.dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];}

  calendar.options = options;

  //build the calendar on the first element in the set of matched elements.
  theDiv.addClass("calBox");

  //empty the div
  theDiv.empty();

  var divYears  = $("<div>").addClass("calYear");
  var divMonths = $("<div>").addClass("calMonth");
  var divDays   = $("<div>").addClass("calDay");
  var divHours  = $("<div>").addClass("calHour");

  function isDateAvailable(checkDate, what /* string */){

    var tr = options.timeRange,
        res = tr.resolution(),
        lvl = ["decade", "year", "month", "day", "hour"].indexOf(what);

    return tr.ranges.some(function(r){
      var t = new TimeRange(r[0], r[1]);
      if (t.resolution() < lvl) {return false;}
      return t.contains(what, checkDate, false);      
    });

  }

  theDiv.append(divYears).append(divMonths).append(divDays).append(divHours);

  calendar.changeDate = function(stamp) {

    var check, tr = calendar.options.timeRange;

    calendar.stamp = stamp || calendar.stamp;

    var fillYears = function(stamp) {

      var now = utc(),
          cal = calendar.stamp,
          nc = options.years *2 +1,
          w = parseInt((theDiv.width() -4 -nc*4) /nc, 10) + "px";

      stamp.neighbours("years", options.years).forEach(function(u){

        var d = u.toDate(),
            span = $("<span>").addClass("calElement")
            .attr("millis", u.time())
            .html(u.format("%Y"))
            .css("width", w);

          if (doTitle){span.attr("title", u.format("%Y"));}
          if (isDateAvailable(d, "year")){span.addClass("available");}
          if (now.year() === u.year()){span.addClass("today");}
          if (u.year() === cal.year()){span.addClass("selected");}
          divYears.append(span);

      });
    };

    var fillMonths = function(stamp) {

      var now = utc(),
          cal = calendar.stamp,
          nc = options.months *2 +1,
          w = parseInt((theDiv.width() -4 -nc*4) /nc, 10) + "px";

      stamp.neighbours("months", options.months).forEach(function(u){

        var d = u.toDate(),
            span = $("<span>").addClass("calElement")
              .attr("millis", u.time())
              .html(u.format("%b"))
              .css("width", w);

          if (doTitle){span.attr("title", u.format("%Y-%m"));}
          if (isDateAvailable(d, "month")){span.addClass("available");}
          if (now.toIso(2) === u.toIso(2)){span.addClass("today");}
          if (u.toIso(2) === cal.toIso(2)){span.addClass("selected");}
          divMonths.append(span);

      });      
    };

    var fillDays = function(stamp) {

      var now = utc(),
          cal = calendar.stamp,
          nc  = options.days *2 +1 +2,
          w   = parseInt((theDiv.width() -4 -nc*4)/(nc), 10) + 2 + "px",
          pre = $("<span>").addClass("calElement").addClass("prev")
                  .attr("millis", cal.delta("days", -5).time()),
          nxt = $("<span>").addClass("calElement").addClass("next")
                  .attr("millis", cal.delta("days", +5).time());

      // console.log("fillDays", theDiv.width(), nc, w);

      if (doTitle){pre.attr("title", cal.delta("days", -5).format("%Y-%m-%d"));}
      if (doTitle){nxt.attr("title", cal.delta("days",  5).format("%Y-%m-%d"));}

      divDays.append(pre);
      stamp.neighbours("days", options.days).forEach(function(u){

        var d = u.toDate(),
            span = $("<span>").addClass("calElement").css("width", w)
              .attr("millis", u.time());

          if (doTitle){span.attr("title", u.format("%Y-%m-%d"));}
          if (isDateAvailable(d, "day")){
            span.addClass("available");
            span.html(u.format("<span class=dayNumber>%e</span><br><span class=dayName>%a</span>"));         
          } else {
            span.html(u.format("%e<br><span class=dayName>%a</span>"));            
          }
          if (now.toIso(3) === u.toIso(3)){span.addClass("today");}
          if (u.toIso(3) === cal.toIso(3)){span.addClass("selected");}
          divDays.append(span);

      });      
      divDays.append(nxt);
    };

    var fillHours = function(stamp) {

      var now = utc(),
          cal = calendar.stamp,
          nc  = options.hours *2 +1,
          w   = parseInt((theDiv.width() -4 -nc*4) / nc, 10) -4 + "px";

      stamp.align("hours", 6).neighbours("hours", options.hours, 6).forEach(function(u){

        var d = u.toDate(),
            span = $("<span>").addClass("calElement").css("width", w)
              .attr("millis", u.time())
              .html(u.format("%H"));

          if (doTitle){span.attr("title", u.format("%Y-%m-%d %Hh"));}
          if (isDateAvailable(d, "hour")){span.addClass("available");}
          if (now.align("hours", 6).toIso(4) === u.toIso(4)){span.addClass("today");}
          if (u.toIso(4) === cal.toIso(4)){span.addClass("selected");}
          divHours.append(span);

      });      
    };

    divYears.empty();
    divMonths.empty();
    divDays.empty();
    divHours.empty();

    // console.log("changeDate", side, res, date);

    // always years
    fillYears(stamp);

    // if monthy avail in any show them
    if (tr.extend("year").contains("month", stamp)) {fillMonths(stamp);}

    // days 
    check = tr.ranges.some(function(r){
      var t = new TimeRange(r[0], r[1]);
      return (t.resolution() > 2) && t.extend("month").contains("day", stamp);
    });

    if (check) {fillDays(stamp);}

    // hours
    check = tr.ranges.some(function(r){
      var t = new TimeRange(r[0], r[1]);
      return t.resolution() > 3 && t.extend("day").contains("hour", stamp);
    });

    if (check) {fillHours(stamp);}

  };

  theDiv.click(function(ev) {

    var stamp, el = $(ev.target).closest(".calElement");
    
    if (el.hasClass("calElement")) {
      stamp = utc(parseInt(el.attr("millis"), 10));
      // console.log("--");
      // console.log("theDiv.CLick.in", stamp.toIso(4));
      options.callback(calendar, stamp);     
    }

  });

  theDiv.dblclick(function(e){ 
      e.preventDefault();
      return false;
  });

  if (options.useWheel) {

    var direc = function(e){
      if (!e) {e = event;}
      return (e.detail<0 || e.wheelDelta>0) ? 1 : -1;
    };

    $(divYears).bind("mousewheel DOMMouseScroll",  function (e) { 
      var checkDate = calendar.stamp.delta("years", direc(e.originalEvent));
      if (isDateAvailable(checkDate, "year")){
        options.callback(calendar, checkDate);
      }
    });
    $(divMonths).bind("mousewheel DOMMouseScroll", function (e) { 
      var checkDate = calendar.stamp.delta("months", direc(e.originalEvent));
      if (isDateAvailable(checkDate, "month")){
        options.callback(calendar, checkDate);
      }
    });
    $(divDays).bind("mousewheel DOMMouseScroll",  function (e) { 
      var checkDate = calendar.stamp.delta("days", direc(e.originalEvent));
      if (isDateAvailable(checkDate, "day")){
        options.callback(calendar, checkDate);
      }
    });
    $(divHours).bind("mousewheel DOMMouseScroll", function (e) { 
      var checkDate = calendar.stamp.delta("hours", direc(e.originalEvent) *6);
      if (isDateAvailable(checkDate, "hour")){
        options.callback(calendar, checkDate);
      }      
    });

  }

  return calendar;

};
