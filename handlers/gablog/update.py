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

import models
import view

from datetime import datetime
from google.appengine.ext import db
from handlers import restful
from utils import authorized

class CommentAddPingbackHandler(restful.Controller):
	@authorized.role("admin")
	def get(self):
		query = models.blog.Article.gql("ORDER BY published DESC")
		articles = query.fetch(1000)
		n = 0
		comment_query = models.blog.Comment.all()
		ntotal = comment_query.count(1000)
		for article in articles:
			for comment in article.comments:
				comment.put()
				n = n + 1
		
		page = view.ViewPage()
		page.render(self, {"two_columns": True, "ncomments": n, 
			"ntotal": ntotal})

