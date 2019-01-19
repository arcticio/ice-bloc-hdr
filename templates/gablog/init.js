/*jslint bitwise: true, browser: true, evil:true, devel: true, todo: true, debug: true, nomen: true, plusplus: true, sloppy: true, vars: true, white: true, indent: 2 */
/*globals $, window, WOW, initPhotoSwipeFromDOM, gablog, Simulator, TIM, GALLERY */

"use strict";

// OFFICIALLY GLOBAL

  var 
    wow,
    Sections
  ;


// PRELOADER

  $(window).load(function(){
    TIM.step("LOADED", "Window");
    $('.preloader').fadeOut(1000); // set duration in brackets    
  });


// INIT SIMULATION

  // {% if 'Simulation' in sections %}

  $(window).load(function(){
  
    Simulator.onload("#simulator");
    // SIM.Model.sync();
  
  });
  
  // {% endif %}


$(function(){

  TIM.step("LOADED", "Document");

  // INIT WOW

  wow = new WOW({mobile: false});
  wow.init();

  
// INIT PARALLAX
  // https://github.com/IanLunn/jQuery-Parallax/blob/master/scripts/jquery.parallax-1.1.3.js
  // function(xpos, speedFactor, outerHeight) {

  function initParallax() {
    $('#home').parallax("100%", 0.1);
    $('#contact').parallax("100%", 0.5);
    $('#disaster').parallax("100%", 0.5);
  }
  initParallax();


// INIT MOBILE MENU

  $('.navbar-collapse a').click(function(){
      $(".navbar-collapse").collapse('hide');
  });


// INIT NAVIGATION
  // https://github.com/istvan-ujjmeszaros/bootstrap-autohidingnavbar

  $(".navbar-fixed-top").autoHidingNavbar({
    disableAutohide:    false,
    showOnUpscroll:     true,
    showOnBottom:       true,
    hideOffset:         "auto",
    animationDuration:  200,
  });


// INIT SECTIONS

  $(window).resize(Sections.resize);
  $(window).scroll(Sections.scroll);
  Sections.resize();
  Sections.scroll();


// INIT Smotth Scroll
  
  // TODO: calc regarding fonts!

  $(function($){ $.localScroll({filter:'.smoothScroll', offset: { top: -96 }}); });

  // Do smooth scroll if hash detected
  if (location.hash){
    $('html, body').animate({
        scrollTop: $(location.hash).offset().top - $(".navBar").height() //50 //54
    }, 1000);
  }



// INIT GALLERY

  // {% if 'Data' in sections %}

    GALLERY.init();

  // {% endif %}



// INIT EXPLORER

  // {% if 'Explorer' in sections %}

    function exp_resize () {

      var 
       navHeight  = $(".navbar").height(),
       trnHeight  = $("#sec-maphead").height(),
       left       = 0,
       top        = fullScreenApi.isFullScreen() ? 0 : navHeight,
       width      = window.innerWidth,
       height     = window.innerHeight - top;

       $("#sec-maphead").css({left: left, top: top, width: width}); 

    }

    $(window).load(function(){
        window.addEventListener('resize', exp_resize);
        exp_resize();
    });

    TIM.step("LOADED", "Versions: Leaflet: " + L.version + ", $: " + $.fn.jquery + ", proj4: " + proj4.version + ", g.maps: " + google.maps.version + ", aio: " + VERSION);

  // {% endif %}



// INIT EDITOR

  // {% if 'Editor' in sections %}

    gablog.posts.availableTags = [];
    // {% if blog_tags %}
      // {% for tag in blog_tags %}
        // {% ifnotequal tag.count 0 %}
          gablog.posts.availableTags.push("{{ tag.name }}");
        // {% endifnotequal %}
      // {% endfor %}
    // {% endif %}

    $(document).ready(function() {
      
      // {% ifequal post.type 'article' %}
        document.getElementById("newarticle").checked = true;
      // {% endifequal %}
      // {% ifequal post.type 'blog entry' %}
        document.getElementById("newblog").checked = true;
      // {% endifequal %}
      // {% ifequal post.type 'draft' %}
        document.getElementById("newdraft").checked = true;
      // {% endifequal %}

      // {% ifequal post.format 'html' %}
        document.getElementById("fmtHT").checked = true;
      // {% endifequal %}
      // {% ifequal post.format 'markdown' %}
        document.getElementById("fmtMD").checked = true;
      // {% endifequal %}
      // {% ifequal post.format 'text' %}
        document.getElementById("fmtTX").checked = true;
      // {% endifequal %}

      $("#dbEdit").attr("href", "//localhost:8000/datastore/edit/" + location.pathname.split("/").slice(-1));

      function replaceSel(before, after) {
        var textarea = document.getElementById("postBody");
        var textBeforeSelection = textarea.value.substr(0, textarea.selectionStart);
        var textAfterSelection = textarea.value.substr(textarea.selectionEnd, textarea.value.length);
        var textSelected = textarea.value.substr(textarea.selectionStart, textarea.selectionEnd - textarea.selectionStart);
        textarea.value = textBeforeSelection + before + textSelected + after + textAfterSelection;
        textarea.focus();
        textarea.selectionStart = (textBeforeSelection + before + textSelected + after).length;
      }

      $("#btnEditA")[0].onclick = function(e){
        replaceSel('<a target="_blank" href="HTTP">', '</a>');
        e.preventDefault(); return false;
      };
      $("#btnEditP")[0].onclick = function(e){replaceSel('<p>', '</p>\n'); e.preventDefault(); return false;};
      $("#btnEditB")[0].onclick = function(e){replaceSel('<strong>', '</strong>'); e.preventDefault(); return false;};
      $("#btnEditI")[0].onclick = function(e){replaceSel('<i>', '</i>'); e.preventDefault(); return false;};
      $("#btnEditMore")[0].onclick = function(e){replaceSel(' [MORE] ', ''); e.preventDefault(); return false;};
      $("#btnEditImg")[0].onclick = function(e){
        replaceSel('<div class="postBackground" style="background: url(\'', '\')" ></div>\n');
        e.preventDefault(); return false;
      };
      $("#btnEditCredit")[0].onclick = function(e){
        replaceSel('<div class="postBackgroundCredit">credit:<a style="font-weight: normal" href="HTTP">@flickr' , '</a></div>\n');
        e.preventDefault(); return false;
      };
      $("#btnEditVid")[0].onclick = function(e){
        var html  = '<object width="460" height="286">';
        html += '<param name="movie" value="http://www.youtube.com/v/YOUTUBE"></param>';
        html += '<param name="allowFullScreen" value="true"></param>';
        html += '<param name="allowscriptaccess" value="always"></param>';
        html += '<param value="transparent" name="wmode">';
        html += '<embed src="http://www.youtube.com/v/YOUTUBE" ';
        html += 'type="application/x-shockwave-flash" width="460" height="286" ';
        html += 'wmode="transparent"></embed></object>\n';
        replaceSel(html, '');
        e.preventDefault(); return false;
      };

    });

  // {% endif %}



// PROLOG

  $("#footer-window-load").text(TIM.now());


});
