# The MIT License
# 
# Copyright (c) 2008 William T. Katz
# Copyright (c) 2010 Joel Goguen
# Copyright (c) 2011 Torsten Becker
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.


__author__ = 'Torsten Becker'

# Add our own directories to sys.path for easy importing
import sys, config
sys.path.insert(0, config.BASEDIR)
sys.path.insert(1, config.ext_utils_path)

import os
import routes
import logging
import webapp2

import aio

# Enabling debugging prints extra messages about what's going on "under 
# the hood". Currently only enabled automatically when running on the 
# GAE development server.

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)

if logger.isEnabledFor(logging.DEBUG):
	aio.debug("Starting %s %s with debug logging enabled", config.APP['name'], config.APP['version'])
else:
	logging.info("Starting %s %s", config.APP['name'], config.APP['version'])

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

# Log a message each time this module get loaded.
logging.info('Loading %s, app version = %s, DEBUG: %s', __name__, config.APP['version'], config.DEBUG)

app = webapp2.WSGIApplication(routes.getRoutes(), debug=config.DEBUG)
