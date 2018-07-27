# The MIT License
# 
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

__author__ = "Torsten Becker"

import aio

import config
import logging
import models
import string
import view

from google.appengine.ext.db import BadKeyError

from google.appengine.ext import db
from handlers import restful
from utils import authorized

# The post dict to be passed to the form editor
post = {
	"title": "",
	# "article": False,
	"tags": "",
	"date": "",
	"body": "",
	"format": "html",
	"href": "",
}

class NewPostHandler(restful.Controller):
	@authorized.role("admin")
	def get(self):

		aio.debug("post.NewPostHandler#get")

		page = view.ViewPage(cache_time = 0)
		params = {
			"handler_name": "form_editor", 
			"title": "New Post | " + config.APP["title"],
			"post": {
				"article": 	False, 
				"format": 	"html", 
				"type": 	"draft"
			}
		}
		page.render(self, params = params)

class EditPostHandler(restful.Controller):
	@authorized.role("admin")
	def get(self, key):
		
		aio.debug("post.EditPostHandler#get: key %s", key)

		page = view.ViewPage(cache_time = 0)
		
		# Get the article being edited
		try : 
			article = models.blog.Article.get(key)
			
		except BadKeyError:
			logging.error("No article with key %s could be found", key)
			self.error(404)
			return

		if not article:
			logging.error("No article with key %s could be found", key)
			self.error(404)
			return

		post["key"]      	= str(article.key())
 		post["type"]    	= article.article_type  ## "article", "blog entry", "draft"
		post["format"]  	= article.format
		post["href"]    	= article.permalink

		post["published"]   = article.published
		post["updated"]  	= article.updated

		post["title"]   	= article.title
		post["tags"]    	= string.join(article.tags, ",")

		post["body"]    	= article.body
		post["html"]     	= article.html
 		post["thumb"]   	= article.thumb
		post["excerpt"]  	= article.excerpt

		post["edithref"]	= "/post/edit/%s" % key

		# post["href"]    = "/" + article.permalink
		# post["article"] = article.article_type == "article"
		
		params = {
			"handler_name": "form_editor", 
			"title": "Edit Post | " + config.APP["title"],
			"post": post,
		}
		page.render(self, params = params)

