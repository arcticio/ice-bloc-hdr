#!/bin/bash

: << '--COMMENT--'

  Dependencies
    sudo apt-get install tree

    http://yui.github.io/yuicompressor/

--COMMENT--

set -e

pathRoot="/home/noiv/Octets/Projects/arctic.io/ice-bloc-hdr"

pathScripts="${pathRoot}/static/js"
pathSim="${pathRoot}/static/js/simulator"
pathExp="${pathRoot}/static/js/explorer"
pathGal="${pathRoot}/static/js/gallery"
compiler="${pathRoot}/static/js/compiler/compiler.jar"

cd $pathRoot
echo 
echo "-- Start Packing --"
echo 


echo "packing gallery"
cd $pathGal

    rm  -f \
        ../gallery.pack.js \
        ../gallery.pack.min.js

    cat \
        gallery.js                  \
        photoswipe.js               \
        photoswipe-ui-default.js    \
        init.gallery.js             \
        > ../gallery.pack.js


echo "packing simulator"
cd $pathSim

    rm  -f \
        ../simulator.pack.js \
        ../simulator.pack.min.js

    cat \
        canvas-toBlob.js    \
        FileSaver.min.js    \
        gifshot.min.js      \
        canvasjs.min.js     \
        sim.vars.js         \
        sim.marray.js       \
        sim.blender.js      \
        sim.model.js        \
        sim.syncer.js       \
        simulator.js        \
        > ../simulator.pack.js


echo "packing explorer"
cd $pathExp

    rm  -f \
        ../explorer.pack.js         \
        ../explorer.pack.min.js

    cat \
        leaflet-src.js              \
        proj4leaflet.2.js           \
        L.Control.Zoomslider.js     \
        L.Control.Coordinates.js    \
        L.Control.Loading.js        \
        L.Control.FullScreen.js     \
        L.FullCanvas.js             \
        L.SimOverlay.js             \
        L.Map.Sync.js               \
        L.Google.js                 \
        aio-Version.js              \
        aio-Time.js                 \
        aio-Plugins.js              \
        aio-Calendar.js             \
        aio-Layers.js               \
        aio-Maps.js                 \
        > ../explorer.pack.js


echo

echo compressing gallery ...
cd "${pathScripts}/compiler"

  java -jar $compiler \
    --compilation_level WHITESPACE_ONLY         \
    --js ../gallery.pack.js                     \
    --js_output_file ../gallery.pack.min.js


echo compressing simulator ...
cd "${pathScripts}/compiler"

  java -jar $compiler \
    --compilation_level WHITESPACE_ONLY         \
    --js ../simulator.pack.js                   \
    --js_output_file ../simulator.pack.min.js


echo compressing explorer ...
cd "${pathScripts}/compiler"

  java -jar $compiler \
    --compilation_level WHITESPACE_ONLY         \
    --js ../explorer.pack.js                    \
    --js_output_file ../explorer.pack.min.js


echo   
echo clean up
cd $pathRoot
rm  -f \
    static/js/.fuse*                    \
    static/js/explorer.pack.js          \
    static/js/simulator.pack.js         \
    static/js/gallery.pack.js


echo done
echo  
