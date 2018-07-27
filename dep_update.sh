#!/bin/bash

set -e

echo 
echo 'app.yaml'
cat app.yaml | head -n3

./dep_increment.sh
./dep_pack.sh

/home/noiv/Programs/google_appengine/appcfg.py update .
