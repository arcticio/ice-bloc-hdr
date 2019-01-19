# The MIT License
# 
# Copyright (c) 2008 William T. Katz
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

"""
contact.py
This module provides a simple form for entering a message and the
handlers for receiving the message through a HTTP POST.
"""
__author__ = 'William T. Katz'

import aio

import config
import logging
import string
import time
import view
import os

from google.appengine.api import users
from handlers import restful

RANDOM_TOKEN = '08yzek30krn4l' + config.APP['base_url']

def getReferer(req):
  hkeys = req.headers.keys()
  if 'Referer' in hkeys:
    return req.headers['Referer']
  else :
    if 'HTTP_REFERER' in os.environ :
      return os.environ['HTTP_REFERER']  
  return ""


class ContactHandler(restful.Controller):

  def get(self):

    user = users.get_current_user()

    referer = getReferer(self.request)
    refererOK = "localhost" in referer or "arctic.io" in referer or "ice-bloc" in referer
    aio.debug("contact: referer.check '%s', %s", referer, refererOK)

    ## Fraud prevention
    ## if not refererOK :
    ##   self.redirect("403.html")
    ##   return

    # Don't use cache since we want to get current time for each post.
    view.ViewPage(cache_time=0).render(self, {

      'email':    user.email() if user else 'Required',
      'nickname': user.nickname() if user else '',
      'token':    RANDOM_TOKEN,
      'curtime':  time.time(),
      "title":    config.APP["title"] + " - Contact &amp; Feedback",
      'warning':  self.request.get('info'),
      'referer':  getReferer(self.request)
      
     })


  def post(self):

    from google.appengine.api import mail

    ## validation
    # if self.request.get('token') != RANDOM_TOKEN or \
    #    time.time() - string.atof(self.request.get('curtime')) < 2.0 :
    #   logging.warn("Aborted contact mailing because form submission was less than 2 seconds.")
    #   self.error(403)

    referer = getReferer(self.request)

    refererOK = "localhost" in referer or "arctic.io" in referer or "ice-bloc" in referer

    aio.debug("contact: referer.check %s, %s", referer, refererOK)

    if not refererOK :
      aio.debug("ContactHandler.post: referer failed: %s", referer)
      self.redirect("/contact/?info=no tricks, please")

    elif self.request.get('email') == "" :
      aio.debug("ContactHandler.post: no email")
      self.redirect("/contact/?info=no email given")

    elif self.request.get('subject') == "" :
      aio.debug("ContactHandler.post: no subject")
      self.redirect("/contact/?info=no subject given")

    elif self.request.get('message') == "" :
      aio.debug("ContactHandler.post: no message")
      self.redirect("/contact/?info=no message given")

    else :

      user      = users.get_current_user()
      sender    = user.email() if user else config.APP['email']
      reply_to  = self.request.get('email') or (user_email() if user else 'anonymous@unknown.com')
      mail.send_mail(
        sender    = sender,
        reply_to  = self.request.get('author') + '<' + reply_to + '>',
        to        = config.APP['email'],
        subject   = "[a.io.contact] " + self.request.get('subject') or 'No Subject Given',
        body      = (reply_to + " wrote:\n\n" + self.request.get('message')) or 'No Message Given'
      )
      
      logging.info("MAIL: %s, ref: %s", reply_to, referer)

      view.ViewPage(cache_time=36000).render(self)
