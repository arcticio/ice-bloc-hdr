# The MIT License
# 
# Copyright (c) 2010 Joel Goguen
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

__author__ = "Joel Goguen"

import config
import httplib
import logging
import models
import string
import xmlrpclib

from google.appengine.ext import db
from handlers import restful
from urlparse import urlsplit

xmlrpc_fault_codes = {
	"0": "Generic XML-RPC fault",
	"16": "Source URI does not exist",
	"17": "Source URI does not contain a link to the target; cannot be used as a source",
	"32": "Specified target URI does not exist",
	"33": "Specified target cannot be used as a target",
	"48": "The pingback has already been registered",
	"49": "Access denied",
	"50": "Server could not communicate with an upstream server, or received an error from an upstream server, and therefore could not complete the request.",
	"-32700": "Parse error - not well formed",
	"-32701": "Parse error - unsupported encoding",
	"-32702": "Parse error - invalid character for encoding",
	"-32600": "Server error - invalid XML-RPC",
	"-32601": "Server error - requested method not found",
	"-32602": "Server error - invalid method parameters",
	"-32603": "Server error - internal XML-RPC error",
	"-32500": "Application error",
	"-32400": "System error",
	"-32300": "Transport error",
}

class PingbackHandler(restful.Controller):
	def get(self):
		self.error(405)
	
	def send_err(self, code, text = None):
		fault = xmlrpclib.Fault
		fault.faultCode = code
		fault.faultString = xmlrpc_fault_codes[str(fault.faultCode)] if text is None else text
		output = xmlrpclib.dumps((fault,))
		logging.debug("Sending error: %s", output)
		self.response.out.write(output)
	
	def post(self):
		data = xmlrpclib.loads(self.request.body)
		
		# Did we get the right number of elements?
		if len(data) != 2:
			self.send_err(-32600)
			return
		logging.debug("Got 2 elements")
		
		# Is this the right call?
		if data[1] != 'pingback.ping':
			self.send_err(-32601)
			return
		logging.info("Got a call to pingback.ping")
		
		# Are there enough parameters?
		if len(data[0]) != 2:
			self.send_err(-32602)
			return
		logging.debug("Got 2 method parameters")
		
		remote_uri = data[0][0]
		local_uri = data[0][1]
		
		# Is this even ours?
		if not local_uri.startswith(config.APP['base_url']):
			self.send_err(0, text = "Specified target does not belong to this domain")
			return
		logging.info("Got a local URI on this host")
		
		# Does the local URI exist?
		local_components = urlsplit(local_uri)
		logging.debug("Searching for permalink: %s", string.join(local_components[2].split("/")[1:], "/"))
		article = models.blog.Article.gql("WHERE permalink = :1", string.join(local_components[2].split("/")[1:], "/")).fetch(1)[0]
		if not article:
			self.send_err(32)
			return
		logging.info("Got an existing permalink: %s", string.join(local_components[2].split("/")[1:], "/"))

		# Does the remote URI exist?
		remote_components = urlsplit(remote_uri)
		if remote_components[0] == 'http':
			conn = httplib.HTTPConnection(remote_components[1])
		elif remote_components[0] == 'https':
			conn = httplib.HTTPSConnection(remote_components[1])
		else:
			self.send_err(0, text = "Unsupported source URI scheme, not adding pingback")
			return
		reqstr = remote_components[2]
		if remote_components[3] != '':
			reqstr = string.join((reqstr, remote_components[3]), '?')
		if remote_components[4] != '':
			reqstr = string.join((reqstr, remote_components[4]), '#')
		logging.debug("Making request for %s on %s", reqstr, remote_components[1])
		conn.request("GET", reqstr)
		resp = conn.getresponse()
		remote_data = resp.read()
		conn.close()
		if local_uri not in remote_data:
			self.send_err(17)
			return
		logging.info("Remote URI (%s) exists and has a link to local URI (%s)", remote_uri, local_uri)
		
		# Is there a comment with this remote URI as an ID?
		for comment in article.comments:
			if comment.pingback_uri == remote_uri:
				self.send_err(48)
				return
		logging.info("Pingback does not appear to be already registered")
		
		# Create a comment for this pingback
		if not article.num_comments:
			article.num_comments = 1
		else:
			article.num_comments += 1
		props = {}
		props['homepage'] = remote_components[0] + "://" + remote_components[1]
		props['title'] = "Pingback"
		props['article'] = article.put()
		props['thread'] = article.next_comment_thread_string()
		props['pingback_uri'] = remote_uri
		props['body'] = "Pingback from <a href=\"" + remote_uri + "\">" + remote_uri + "</a>"
		
		comment = models.blog.Comment(**props)
		comment.put()

