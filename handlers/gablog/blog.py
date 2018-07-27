  # The MIT License
#
# Copyright (c) 2008 William T. Katz
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

"""A simple RESTful blog/homepage app for Google App Engine

This simple homepage application tries to follow the ideas put forth in the
book 'RESTful Web Services' by Leonard Richardson & Sam Ruby.  It follows a
Resource-Oriented Architecture where each URL specifies a resource that
accepts HTTP verbs.

Rather than create new URLs to handle web-based form submission of resources,
this app embeds form submissions through javascript.  The ability to send
HTTP verbs POST, PUT, and DELETE is delivered through javascript within the
GET responses.  In other words, a rich client gets transmitted with each GET.

This app's API should be reasonably clean and easily targeted by other
clients, like a Flex app or a desktop program.
"""
__author__ = 'William T. Katz'

import aio

import cgi
import config
import datetime
import hashlib
import httplib
import logging
import models
import re
import os
import string
import urllib
import view
import xmlrpclib
import time

import django

from configs import legacy_aliases

import webapp2

from django.template.loaders.filesystem import Loader
from django.template.loader import render_to_string

from google.appengine.api import users
from google.appengine.ext import db
# from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import urlfetch
from handlers import restful
from urlparse import urlsplit
from utils import authorized
from utils import sanitizer

# def asciify(item) :

#   try :
#     return str(item)
#   except:
#     buffer = ""
#     for letter in item :
#       try:
#         buffer += unicodedata.normalize('NFKD', letter.decode('utf-8', 'replace')).encode('ascii', 'ignore')
#       except:
#         buffer += "_"
#     return buffer


# Functions to generate permalinks depending on type of article
permalink_funcs = {
  'article':    lambda title, date: get_friendly_url(title),
  'blog entry': lambda title, date: str(date.year) + "/" + str(date.month) + "/" + get_friendly_url(title),
  'draft':      lambda title, date: get_friendly_url(title)
}

# Resolve legacy software mappings.
def resolve_legacy_mapping(path, software):
  if software:
    if isinstance(software, basestring):
      software = [software, ]

    # Try each enabled legacy software pattern. Return immediately
    # when a match is found.
    for elem in software:
      if elem == 'Drupal':
        url_match = re.match('node/(\d+)/?$', path)
        if url_match:
          return db.Query(models.blog.Article).filter('legacy_id =', url_match.group(1)).get()
      elif elem == 'Serendipity':
        url_match = re.match('archives/(\d+)-.*\.html$', path)
        if url_match:
          return db.Query(models.blog.Article).filter('legacy_id =', url_match.group(1)).get()
      elif elem == 'Blogger':
        url_match = re.match('(\d+/\d+/[\w-]+).html$', path)
        if url_match:
          return db.Query(models.blog.Article).filter('legacy_id =', url_match.group(0)).get()

  return None

# Module methods to handle incoming data
def get_datetime(time_string = None):
  if time_string:
    try :
      return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S').replace(microsecond=0)
    except ValueError :
      aio.debug("blog.get_datetime: timestring: %s", time_string)
  return datetime.datetime.utcnow().replace(microsecond=0)

def get_format(format_string):
  if not format_string or format_string not in ['html', 'textile', 'markdown', 'text']:
    format_string = 'html'
  return format_string

def get_type(format_string):
  if not format_string or format_string not in ['draft', 'blog entry', 'article']:
    format_string = 'draft'
  return format_string

def get_tag_key(tag_name):
  obj = models.blog.Tag.get_or_insert(tag_name)
  return obj.key()

def process_tag(tag_name, tags):
  # Check tag_name against all 'name' values in tags and coerce
  tag_name = tag_name.strip()
  if not isinstance(tag_name, unicode):
    tag_name = tag_name.decode(config.APP['charset'])
  lowercase_name = tag_name.lower()
  for tag in tags:
    if lowercase_name == tag['name'].lower():
      return tag['name']
  return tag_name

def get_tags(tags_string):
  logging.debug("get_tags: tags_string = %s", tags_string)
  if tags_string:
    from models.blog import Tag
    tags = Tag.list()
    logging.debug("tags = %s", str([tag for tag in tags if tag["count"] != 0]))
    return [process_tag(s, tags)
        for s in tags_string.split(",") if s != '']
  return None

def get_htmlTitle(titArt=""):
  if titArt :
    return config.APP['title'] + " - " + titArt
  else :
    return config.APP['title'] + " - " + config.APP['description']

def get_friendly_url(title):
  return re.sub('-+', '-',
          re.sub('[^\w-]', '',
             re.sub('\s+', '-', title.strip()))).lower()

def get_html(body, markup_type):
  
  aio.debug("blog.get_html: markup_type: %s, len: %s", markup_type, len(body))

  if markup_type == 'textile':
    from utils.external import textile
    return textile.textile(body)
  
  if markup_type == 'html' :
    return body

  if markup_type == 'markdown' :
    from utils.markdown import markdown
    return markdown(body, extensions=["utils.markdown.extensions.attr_list"])

  return body

def get_captcha(key):
  return ("%X" % abs(hash(str(key) + config.APP['title'])))[:6]

def get_sanitizer_func(handler, **kwargs):
  match_obj = re.match(r'.*;\s*charset=(?P<charset>[\w-]+)',
             handler.request.headers['CONTENT_TYPE'])
  kwlist = {}
  kwlist.update(kwargs)
  if match_obj:
    kwlist.update({ 'encoding': match_obj.group('charset').lower() })
  return lambda html : sanitizer.sanitize_html(html, **kwlist)

def do_sitemap_ping():
  sitemap = "%s/sitemap.xml" % (config.APP['base_url'])
  pingomatic_params = {"title": config.APP['title'], "blogurl":
      config.APP['base_url'], "rssurl": config.APP['base_url'] +
      config.BLOG['atom_url']}
  pingomatic_services = ["weblogscom", "blogs", "feedburner",
  "syndic8", "newsgator", "myyahoo", "pubsubcom", "blogdigger",
  "blogstreet", "moreover", "weblogalot", "icerocket", "newsisfree",
  "topicexchange", "google", "tailrank", "bloglines", "postrank",
  "skygrid", "collecta", "superfeedr"]

  for elem in pingomatic_services:
    pingomatic_params["chk_" + elem] = "on"

  # Ping Google
  logging.info("Sending sitemap ping to Google")
  urlfetch.fetch("http://www.google.com/webmasters/tools/ping?" + urllib.urlencode({ "sitemap": sitemap }))

  # Ping Bing
  logging.info("Sending sitemap ping to Bing")
  urlfetch.fetch("http://www.bing.com/webmaster/ping.aspx?" + urllib.urlencode({ "siteMap": sitemap }))

  # Ping Ping-o-matic
  logging.info("Sending ping to ping-o-matic")
  urlfetch.fetch("http://pingomatic.com/ping/?" +
      urllib.urlencode(pingomatic_params))

def process_embedded_code(article):
  # TODO -- Check for embedded code, escape opening triangular brackets
  # within code, and set article embedded_code strings so we can
  # use proper javascript.
  from utils import codehighlighter
  article.html, languages = codehighlighter.process_html(article.html)
  article.embedded_code = languages

def process_article_edit(handler, postlink):
  # For HTTP PUT, the parameters are passed in URIencoded string in body

  body = handler.request.body
  params = cgi.parse_qs(body)

  for key, value in params.iteritems():
    params[key] = value[0]
    if not isinstance(params[key], unicode):
      params[key] = params[key].decode(config.APP['charset'])


  aio.debug("blog.process_article_edit: params.keys: %s", params.keys())

  # article_type = restful.get_sent_properties(params.get, [('postType', get_type)])['postType']
  article_type = params['postType']

  aio.debug("blog.process_article_edit article with postlink: %s, type: %s/%s", postlink, article_type, params['postFormat'])

  tmp_hash = restful.get_sent_properties(params.get, [
    ('postTitle',     cgi.escape),
    ('postBody',      get_sanitizer_func(handler, trusted_source = True)),
    ('postFormat',    get_format),     ## markdown, html, text
    ('postType',      get_type),       ## draft, post, article
    ('postTags',      get_tags),
    ('html',          get_html, 'postBody', 'postFormat'),

    ('postPublished',   get_datetime, 'postPublished'),

    ('permalink',     permalink_funcs[article_type], 'postTitle', 'postPublished'),
    'postThumb',
    # 'postPublished',
  ])

  # aio.debug("blog.process_article_edit tmp_hash: %s", tmp_hash)

  property_hash = {}
  props = (
    ("postTitle",     "title"), 
    ("postBody",      "body"),
    ("postFormat",    "format"),
    ("postPublished", "published"), 
    ("postThumb",     "thumb"),
    ("legacy_id",     "legacy_id"), 
    ("article_id",    "article_id"), 
    ("postType",      "article_type"), 
    ("postTags",      "tags"),
    ("html",          "html"), 
    ("postPerma",     "permalink")
  )
  for pair in props :
    # aio.debug("PAIR: %s", pair)
    if pair is not None:
      if pair[0] in tmp_hash :
        # logging.info("COPY  PAIR %s", pair)
        property_hash[pair[1]] = tmp_hash[pair[0]]
      else : 
        pass
        # aio.debug("IGNORE %s from sent properties to %s in property hash", pair[0], pair[1])
    else :
      aio.debug("ERROR '%s' with pair", pair)


  if property_hash:
    if 'tags' in property_hash:
      property_hash['tag_keys'] = [get_tag_key(name) for name in property_hash['tags'] if name != ""]

    aio.debug("blog.process_article_edit search article by postlink: %s", postlink)


    ## adjust dates
    property_hash['updated'] = datetime.datetime.utcnow()

    if property_hash['article_type'] == 'draft' : 
      property_hash['published'] = None
    else :
      # property_hash['published'] = get_datetime(property_hash['published'])
      property_hash['published'] = property_hash['published']

    aio.debug("blog.process_article_edit pub: %s: upd: %s", property_hash['published'], property_hash['updated'])


    article = db.Query(models.blog.Article).filter('permalink =', postlink).get()
    before_tags = set(article.tag_keys)

    for key, value in property_hash.iteritems():
      # aio.debug("blog.process_article_edit: SAVE: " + key + " > " + aio.asciify(value)[:10]) ## utf errors
      setattr(article, key, value)

    after_tags = set(article.tag_keys)

    for removed_tag in before_tags - after_tags:
      tag = db.get(removed_tag)
      logging.debug("Decrementing tag '%s' with initial value %d", tag.name, tag.counter.count)
      tag.counter.decrement()
      if tag.counter.count == 0:
        logging.debug("Tag %s has count 0, removing tag", tag.name)
        tag.delete_counter()
        tag.delete()

    for added_tag in after_tags - before_tags:
      db.get(added_tag).counter.increment()

    process_embedded_code(article)
    article.put()

    # restful.send_successful_response(handler, '/' + article.permalink)
    restful.send_successful_response(handler, '/post/edit/' + str(article.key()))
    view.invalidate_cache(article.permalink)

  else:
    handler.error(400)

def process_article_submission(handler, article_type):
  """
  takes care of permalink
  """

  aio.debug("blog.process_article_submission article_type: %s", article_type)

  tmp_hash = restful.get_sent_properties(handler.request.get, [
    ('postTitle',     get_sanitizer_func(handler, trusted_source = True)),
    ('postBody',      get_sanitizer_func(handler, trusted_source = True)),
    ('postFormat',    get_format),
    ('postType',      get_type),
    ('postUpdated',   get_datetime),
    ('postTags',      get_tags),
    ('html',          get_html, 'postBody', 'postFormat'),
    ('permalink',     permalink_funcs[article_type], 'postTitle', 'postPublished'),
    'postExcerpt',
    'postThumb'
  ])

  property_hash = {}
  props = (
    ("key",           "key"), 
    ("postTitle",     "title"), 
    ("postBody",      "body"),
    ("postExcerpt",   "excerpt"),
    ("postThumb",     "thumb"),
    ("postFormat",    "format"),
    ("postType",      "article_type"), 
    ("postPublished", "published"), 
    ("postUpdated",   "updated"), 
    ("article_id",    "article_id"),
    ("permalink",     "permalink"), 
    ("html",          "html"), 
    ("postTags",      "tags"),
  )

  for pair in props:
    if pair[0] in tmp_hash:
      property_hash[pair[1]] = tmp_hash[pair[0]]

  if property_hash:

    if 'tags' in property_hash:
      property_hash['tag_keys'] = [get_tag_key(name) for name in property_hash['tags']]

    # property_hash['format']       = 'html'   # For now, convert all to HTML
    # property_hash['article_type'] = article_type

    article = models.blog.Article(**property_hash)
    article.set_associated_data({'relevant_links': handler.request.get('relevant_links'), })
    process_embedded_code(article)

    article.put()
    time.sleep(1)

    # Ensure there is a year entity for this entry's year
    if article.published :
      models.blog.Year.get_or_insert('Y%d' % (article.published.year, ))

    # Update tags
    for key in article.tag_keys:
      db.get(key).counter.increment()

    aio.debug("blog.process_article_submission perm: %s, key: %s", article.permalink, article.key())

    # restful.send_successful_response(handler, '/' + article.permalink)

    restful.send_successful_response(handler, '/post/edit/' + str(article.key()))

    view.invalidate_cache(article.permalink)

  else:
    aio.debug("blog.process_article_submission no property_hash")
    handler.error(400)

def do_pingback(permalink, post_text):
  pingback_re = re.compile(r'<link rel="pingback" href="([^"]+)" ?\/?>',
      re.MULTILINE | re.UNICODE)
  head_close_re = re.compile(r'<\/head>', re.MULTILINE | re.UNICODE)
  amp_re = re.compile(r'&amp;', re.UNICODE)
  quote_re = re.compile(r'&quot;', re.UNICODE)
  lt_re = re.compile(r'&lt;', re.UNICODE)
  gt_re = re.compile(r'&gt;', re.UNICODE)

  match_list = re.findall(r'<a.+?href="(http:\/\/[\w\d\-_\.:\/]+)".+?>',
    post_text, re.MULTILINE | re.UNICODE)
  logging.info("Preparing to send pingback to %d URLs",
      len(match_list))

  for group in match_list:
    logging.debug("Preparing to pingback: %s", str(group))
    components = urlsplit(group)
    if components[0] == 'http':
      logging.debug("Creating HTTPConnection object")
      conn = httplib.HTTPConnection(components[1])
    elif components[0] == 'https':
      logging.debug("Creating HTTPSConnection object")
      conn = httplib.HTTPSConnection(components[1])
    else:
      logging.debug("Only HTTP or HTTPS supported, %s found",
          components[0])
      continue

    reqstr = components[2]
    if components[3] != '':
      reqstr = string.join((reqstr, components[3]), '?')
    if components[4] != '':
      reqstr = string.join((reqstr, components[4]), '#')
    logging.debug("Requesting URL %s", reqstr)

    conn.request('GET', reqstr)
    resp = conn.getresponse()
    loc = resp.getheader('X-Pingback')
    if loc is None:
      logging.info("No X-Pingback header, searching page body")
      data = resp.read()
      for line in data.split("\n"):
        logging.debug("Processing line: %s", line)
        m = pingback_re.search(line)
        if m:
          loc = m.group(1)
          break
        else:
          m = head_close_re.search(line)
          if m:
            logging.debug("Found closing head tag")
            break

      if loc is None or loc == "":
        logging.debug("No match found, skipping pingback")
        continue

      loc = amp_re.sub('&', loc)
      loc = quote_re.sub('"', loc)
      loc = lt_re.sub('<', loc)
      loc = gt_re.sub('>', loc)
    conn.close()

    logging.info("Pingback will be sent to: %s", loc)

    xmlrpc_query = xmlrpclib.dumps((permalink, group),
      'pingback.ping')

    if config.DEBUG:
      # Don't want to really ping if we're in DEBUG mode
      logging.debug("Prepared XML-RPC query for %s:\n%s", loc,
        xmlrpc_query)
    else:
      components = urlsplit(group)
      if components[0] == 'http':
        logging.debug("Creating HTTPConnection object for XML-RPC request")
        conn = httplib.HTTPConnection(components[1])
      elif components[0] == 'https':
        logging.debug("Creating HTTPSConnection object for XML-RPC request")
        conn = httplib.HTTPSConnection(components[1])
      else:
        logging.debug("Only HTTP or HTTPS supported, %s found",
          components[0])
        continue

      reqstr = components[2]
      if components[3] != '':
        reqstr = string.join((reqstr, components[3]), '?')
      if components[4] != '':
        reqstr = string.join((reqstr, components[4]), '#')
      logging.debug("Sending XML-RPC request to %s", reqstr)

      conn.request('POST', reqstr, xmlrpc_query)
      resp = conn.getresponse()
      data = resp.read()
      conn.close()

      if data not in xmlrpc_fault_codes:
        logging.info("XML-RPC response: %s", data)
      else:
        logging.error("XML-RPC fault: %s",
            xmlrpc_fault_codes[data])


def render_article(handler, path, params = {}):
  """
    renders blods, drafts and articles
  """

  if view.render_if_cached(handler) :
    return

  article = db.Query(models.blog.Article).filter('permalink =', path).get()

  if not article:
    aio.debug("blog.render_article article not found: path: %s", path)
    handler.redirect('/404.html')
    # handler.error(404)
    # view.ViewPage(cache_time = 604800).render(handler, {
    #   'module_name':  'blog', 
    #   'handler_name': 'notfound',
    #   'sections':     ['Navigation', 'Home']
    # })
    return

  else :
    render_params = {
      "isBig":    article.is_big(),
      "article":  article,
      "title":    get_htmlTitle(article.title),
    }
    render_params.update(params)

    view.ViewPage().render(handler, render_params)


####################### H A N D L E R #########################################

#
#
######### CommentHandler #######

class CommentHandler(restful.Controller):
  @authorized.role("admin")
  def get(self, comment_id):
    logging.debug("CommentHandler#get")
    if not comment_id:
      self.error(403) # No one should be here...
      return

    comment = models.blog.Comment.get(db.Key(comment_id))
    if not comment:
      logging.error("No comment found for ID %s", comment_id)
      self.error(404)
      return

    try:
      accept_list = self.request.headers["Accept"]
    except KeyError:
      logging.info("Had no accept header: %s", self.request.headers)
      accept_list = None
    if accept_list and accept_list.split(',')[0] == 'application/json':
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(comment.to_json())
    else:
      logging.error("Non-JSON comment GET requests not permitted")
      self.error(403)
      return

  @restful.methods_via_query_allowed
  def post(self, comment_id):

    sanitize_comment = get_sanitizer_func(self,
      allow_attributes = ['href'],
      blacklist_tags = ['img', 'script', 'iframe']
    )

    tmp_hash = restful.get_sent_properties(self.request.get,
      [('key', cgi.escape),
      ('commentEmail', cgi.escape),
      ('commentHomepage', cgi.escape),
      ('commentTitle', cgi.escape),
      ('commentName', cgi.escape),
      ('commentBody', sanitize_comment),
      ('article_id', cgi.escape),
      'captcha',
      ('published', get_datetime)])
    property_hash = {}
    props = (("key", "key"), ("commentEmail", "email"),
    ("commentHomepage", "homepage"), ("commentTitle", "title"),
    ("commentBody", "body"), ("published", "published"), ("article_id",
      "article_id"), ("captcha", "captcha"), ('commentName', 'name')
    )

    for pair in props:
      if pair[0] in tmp_hash:
        logging.debug("Copying '%s' from received properties to '%s' in property hash (value: %s)", pair[0], pair[1], str(tmp_hash[pair[0]]))
        property_hash[pair[1]] = tmp_hash[pair[0]]

    if "article_id" not in property_hash:
      logging.error("No article_id found: %s", str(property_hash))
      self.error(400)
      return

    article = db.Query(models.blog.Article).filter('permalink =', property_hash["article_id"]).get()

    # If we aren't administrator, abort if bad captcha
    if not users.is_current_user_admin():
      if property_hash.get('captcha', None) != get_captcha(article.key()):
        logging.info("Received captcha (%s) != %s", property_hash.get('captcha', None), get_captcha(article.key()))
        self.error(403)
        self.response.out.write("Invalid CAPTCHA");
        return

    # Generate a thread string.
    if article:
      thread_string = article.next_comment_thread_string()
    else:
      logging.error("No article with ID %s found!", property_hash["article_id"])
      self.error(400)
      return

    logging.debug("New thread string: %s", thread_string)
    property_hash['thread'] = thread_string

    # Get and store some pieces of information from parent article.
    # TODO: See if this overhead can be avoided
    if not article.num_comments:
      article.num_comments = 1
    else:
      article.num_comments += 1
    property_hash['article'] = article.put()

    try:
      comment = models.blog.Comment(**property_hash)
      comment.put()
    except Exception, e:
      logging.error(e)
      logging.error("Bad comment: %s", property_hash)
      handler.error(400)
      return

    # Notify the author of a new comment (from matteocrippa.it)
    if config.BLOG['send_comment_notification'] and not users.is_current_user_admin():
      recipient = "%s <%s>" % (config.APP['author'], config.APP['email'],)
      body = ("A new comment has just been posted on %s/%s by %s:\n\n%s\n\nComment link:%s."
          % (config.APP['base_url'], article.permalink, comment.name, comment.body,
            config.APP['base_url'] + "/" + article.permalink +
            "#comment-" + comment.thread))
      mail.send_mail(sender = config.APP['email'],
               to = recipient,
               subject = "New comment by %s" % (comment.name,),
               body = body)

    # Render just this comment and send it to client
    view_path = view.find_file(view.templates, "gablog/blog/comment.html")
    allow_comments = article.allow_comments
    if allow_comments is None:
      age = (datetime.datetime.now() - article.published).days
      allow_comments = (age <= config.BLOG['comment_window'])

    # response = template.render(
    response = render_to_string(
      os.path.join(config.APP['template_dir'], view_path),
      { 'comment': comment, "use_gravatars": config.BLOG["use_gravatars"],
        "allow_comments": allow_comments, "user_is_admin":
        users.is_current_user_admin()},
      debug = config.DEBUG)
    self.response.out.write(response)
    view.invalidate_cache("/" + property_hash["article_id"])

  @authorized.role("admin")
  def put(self, comment_id):
    logging.debug("CommentHandler#put for comment %s", comment_id)
    # For HTTP PUT, the parameters are passed in URIencoded string in body
    sanitize_comment = get_sanitizer_func(self,
      allow_attributes = ['href', 'src'],
      blacklist_tags = ['img', 'script'])
    body = self.request.body
    params = cgi.parse_qs(body)
    for key, value in params.iteritems():
      params[key] = value[0]
      if not isinstance(params[key], unicode):
        params[key] = params[key].decode(config.APP['charset'])

    tmp_hash = restful.get_sent_properties(self.request.get,
      [('commentEmail', cgi.escape),
      ('commentHomepage', cgi.escape),
      ('commentTitle', cgi.escape),
      ('commentName', cgi.escape),
      ('commentBody', sanitize_comment)])
    property_hash = {}
    props = (("commentEmail", "email"), ("commentHomepage", "homepage"),
        ("commentTitle", "title"), ("commentBody", "body"),
        ('commentName', 'name'))
    for pair in props:
      if pair[0] in tmp_hash:
        logging.debug("Copying '%s' from received properties to '%s' in property hash (value: %s)", pair[0], pair[1], str(tmp_hash[pair[0]]))
        property_hash[pair[1]] = tmp_hash[pair[0]]
    if property_hash:
      comment = models.blog.Comment.get(db.Key(comment_id))
      for key, value in property_hash.iteritems():
        setattr(comment, key, value)
      comment.put()

      # Render just this comment and send it to client
      view_path = view.find_file(view.templates, "gablog/blog/comment.html")
      allow_comments = comment.article.allow_comments
      if allow_comments is None:
        age = (datetime.datetime.now() - comment.article.published).days
        allow_comments = (age <= config.BLOG['comment_window'])

      # response = template.render(os.path.join(config.APP['template_dir'], view_path),
      response = render_to_string(os.path.join(config.APP['template_dir'], view_path),
        { 'comment': comment, "use_gravatars": config.BLOG["use_gravatars"],
          "allow_comments": allow_comments, "user_is_admin":
          users.is_current_user_admin()},
        debug = config.DEBUG)
      self.response.out.write(response)
      view.invalidate_cache(comment.article.permalink)
    else:
      self.error(400)

  @authorized.role("admin")
  def delete(self, comment_id):
    logging.info("Deleting comment %s", comment_id)
    comment = models.blog.Comment.get(db.Key(comment_id))
    article = comment.article
    article.num_comments -= 1
    article.put()
    comment.delete()
    view.invalidate_cache(article.permalink)
    restful.send_successful_response(self, "/")

#
#
######### NotFoundHandler #######

class NotFoundHandler(webapp2.RequestHandler):
  def get(self):
    self.error(404)
    view.ViewPage(cache_time = 36000).render(self, params={
      "title" : "404 - Not Found"
    })

#
#
######### UnauthorizedHandler #######

class UnauthorizedHandler(webapp2.RequestHandler):
  def get(self):
    self.error(403)
    view.ViewPage(cache_time = 36000).render(self, params={
      "title" : "403 - Not Authorized"
    })
#
#
######### RootHandler #######

class RootHandler(restful.Controller):
  
  def get(self):

    aio.debug("RootHandler#get")

    if view.render_if_cached(self) :
      return

    page = view.ViewPage()

    page.render_query(
      self, 'articles',
      db.Query(models.blog.Article).filter('article_type =', 'blog entry').order('-published'),
      params = {
        "module_name": None, 
        "handler_name": "base", 
        "title": get_htmlTitle()
      }
    )

  @authorized.role("admin")
  def post(self):
    aio.debug("RootHandler#post")
    process_article_submission(handler = self, article_type = 'article')

#
#
######### ArticlesHandler #######

class ArticlesHandler(restful.Controller):

  def get(self):

    aio.debug("ArticlesHandler#get")

    if view.render_if_cached(self) :
      return

    page = view.ViewPage()
    page.render_query(
      self, "articles", 
      db.Query(models.blog.Article).filter("article_type =", "article").order("title"),
      params = {
        "title": "Articles | " + config.APP["title"]
      }
    )


#
#
######### ArticleHandler #######

class ArticleHandler(restful.Controller):
  def get(self, path):
    aio.debug("blog.ArticleHandler#get: Fetching article at path: /%s", path)
    self.response.headers['X-Pingback'] = config.APP['base_url'] + "/xmlrpc"
    render_article(self, path)

  @restful.methods_via_query_allowed
  def post(self, path):
    aio.debug('blog.ArticleHandler#post - ignoring')

  @authorized.role("admin")
  def put(self, path):
    aio.debug("blog.ArticleHandler#put for /%s", path)
    process_article_edit(self, permalink = path)

  @authorized.role("admin")
  def delete(self, path):
    """
    By using DELETE on /Article, /Comment, /Tag, you can delete the first
     entity of the desired kind.
    This is useful for writing utilities like clear_datastore.py.
    """
    # TODO: Add DELETE for articles off root like blog entry DELETE.
    model_class = path.lower()
    aio.debug("blog.ArticleHandler#delete on %s", path)

    def delete_entity(query):
      targets = query.fetch(limit = 1)
      if len(targets) > 0:
        if hasattr(targets[0], 'title'):
          title = targets[0].title
        elif hasattr(targets[0], 'name'):
          title = targets[0].name
        else:
          title = ''
        aio.debug('Deleting %s %s', model_class, title)
        targets[0].delete()
        self.response.out.write('Deleted ' + model_class + ' ' + title)
        view.invalidate_cache(path)
      else:
        self.response.set_status(204, 'No more ' + model_class + ' entities')

    if model_class == 'article':
      query = models.blog.Article.all()
      delete_entity(query)
    elif model_class == 'comment':
      query = models.blog.Comment.all()
      delete_entity(query)
    elif model_class == 'tag':
      query = models.blog.Tag.all()
      delete_entity(query)
    else:
      article = db.Query(models.blog.Article). \
             filter('permalink =', path).get()
      for key in article.tag_keys:
        tag = db.get(key)
        logging.debug("Decrementing tag %s with initial value %d", tag.name, tag.counter.count)
        tag.counter.decrement()
        if tag.counter.count == 0:
          logging.debug("Tag %s has count 0, removing tag", tag.name)
          tag.delete_counter()
          tag.delete()
      for comment in article.comments:
        comment.delete()
      article.delete()
      view.invalidate_cache(path)
      restful.send_successful_response(self, "/")

#
#
######### BlogEntryHandler #######

# Blog entries are dated articles
class BlogEntryHandler(restful.Controller):

  def get(self, year, month, permalink):

    perm_stem = [t for t in permalink.split("/") if len(t)][-1]
    aio.debug("BlogEntryHandler.get for year %s, month %s, and perm_stem '%s'", year, month, perm_stem)
    # self.response.headers['X-Pingback'] = config.APP['base_url'] + "/xmlrpc"

    # render_article(self, "%s/%s/%s" % (year, month, perm_stem), params = {"handler_name": "article"})
    render_article(self, "%s/%s/%s" % (year, month, perm_stem), params = {"handler_name": "blog"})

  @restful.methods_via_query_allowed
  def post(self, year, month, perm_stem):
    aio.debug("BlogEntryHandler#post - ignoring")

  @authorized.role("admin")
  def put(self, year, month, permalink):

    perm_stem = [t for t in permalink.split("/") if len(t)][-1]
    aio.debug("BlogEntryHandler.put: Processing article edit for /%s/%s/%s", year, month, perm_stem)

    process_article_edit(handler=self, postlink="%s/%s/%s" % (year, month, perm_stem))

  @authorized.role("admin")
  def delete(self, year, month, permalink):

    perm_stem = [t for t in permalink.split("/") if len(t)][-1]
    permalink = year + '/' + month + '/' + perm_stem
    aio.debug("BlogEntryHandler. delete Deleting blog entry %s", permalink)

    article = db.Query(models.blog.Article).filter('permalink =', permalink).get()
    for key in article.tag_keys:
      tag = db.get(key)
      aio.debug("BlogEntryHandler.delete: Decrementing tag '%s' with current count %d", tag.name, tag.counter.count)
      tag.counter.decrement()
      if tag.counter.count == 0:
        aio.debug("Tag '%s' has count 0, removing tag", tag.name)
        tag.delete_counter()
        tag.delete()

    article.delete()
    view.invalidate_cache(perm_stem)
    
    restful.send_successful_response(self, "/")

#
#
######### TagHandler #######

class TagHandler(restful.Controller):
  def get(self, encoded_tag=""):

    if view.render_if_cached(self):
      return
    
    tag = unicode(urllib.unquote(encoded_tag), config.APP['charset'])
    page = view.ViewPage()

    template_data = {
      'tag': tag,
      "title": config.APP["title"] + " - Articles tagged with &quot;" + tag + "&quot;"
    }

    if tag :
      page.render_query(
        self, 'articles',
        db.Query(models.blog.Article).filter('tags =', tag).order('-published'), template_data)
    else :
      ##TODO: render nice tag Cloud here
      page.render_query(
        self, 'articles',
        db.Query(models.blog.Article).order('-published'), template_data)

#
#
######### SearchHandler #######

class SearchHandler(restful.Controller):
  def get(self):
#    from google.appengine.api import datastore_errors
    search_term  = self.request.get("s")
    query_string = 's=' + urllib.quote_plus(search_term) + '&'

    view.ViewPage(cache_time=3600).render(self, {
      'search_term': cgi.escape(search_term),
      'query_string': query_string
      })

#    page = view.ViewPage()
#    try:
#      page.render_query(
#        self, 'articles',
#        models.blog.Article.all().search(search_term). \
#          order('-published'),
#        {'search_term': cgi.escape(search_term), 'query_string': query_string})
#    except datastore_errors.NeedIndexError:
#      page.render(self, {'search_term': cgi.escape(search_term),
#                 'search_error_message': """
#                 Sorry, full-text searches are currently limited
#                 to single words until a later AppEngine update.
#                 """})

#
#
######### YearHandler #######

class YearHandler(restful.Controller):
  def get(self, year):
    logging.debug("YearHandler#get for year %s", year)
    if view.render_if_cached(self):
      return
    start_date = datetime.datetime(string.atoi(year), 1, 1)
    end_date = datetime.datetime(string.atoi(year), 12, 31, 23, 59, 59)
    page = view.ViewPage()
    page.render_query(
      self, 'articles',
      db.Query(models.blog.Article).order('-published'). \
         filter('published >=', start_date). \
         filter('published <=', end_date).filter("article_type =", "blog entry"),
      {'title': config.APP['title'] + ' - Articles for ' + year + ' | ', 'year': year})


#
#
######### CollHandler #######

class CollHandler(restful.Controller):
  def get(self, what, year=None):
    """
      what = all, blogs, drafts, articles
    """

    aio.debug("CollHandler#get: %s for year: '%s'", what, year)

    start_date = None; end_date = None; 

    if view.render_if_cached(self) : return

    page = view.ViewPage()

    if what in ["all", "blogs", "articles", "drafts"] :

      if year :
        start_date = datetime.datetime(string.atoi(year), 1, 1)
        end_date   = datetime.datetime(string.atoi(year), 12, 31, 23, 59, 59)

      if what == "all" :
        query = db.Query(models.blog.Article)
      elif what == "drafts"   : 
        query = db.Query(models.blog.Article).filter('article_type =', 'draft')
      elif what == "blogs"    : 
        query = db.Query(models.blog.Article).filter('article_type =', 'blog entry')
      elif what == "articles" : 
        query = db.Query(models.blog.Article).filter('article_type =', 'article')

      if start_date and end_date :
        query = query.filter('updated >=', start_date).filter('updated <=', end_date)

      if year and what == "all" :
          title = "%s - Entries for year %s" % (config.APP['title'], year)
      else : 
          title = "%s - %s" % (config.APP['title'], what.title())

      page.render_query(self, 'articles', query, {
        'title': title,
        year:    year
      })

    else :
      self.error(404)
      view.ViewPage(cache_time = 604800).render(self, {
        'module_name': 'blog', 
        'handler_name': 'notfound',
        'sections': ['Navigation', 'Home']
      })


#
#
######### MonthHandler #######

class MonthHandler(restful.Controller):

  def get(self, year, month):

    aio.debug("blog.MonthHandler: get for year %s, month %s", year, month)

    if view.render_if_cached(self):
      return

    yr = string.atoi(year)
    mth = string.atoi(month)
    start_date = datetime.datetime(yr, mth, 1)

    if mth == 12:
      end_date = datetime.datetime(string.atoi(year)+1, 1, 1)
    else :
      end_date = datetime.datetime(string.atoi(year), string.atoi(month) + 1, 1)

    page = view.ViewPage()

    page.render_query(
      self, 'articles',
      db.Query(models.blog.Article).order('-published'). \
        filter('published >=', start_date). \
        filter('published <', end_date).filter("article_type =", "blog entry"),
        {'title': config.APP['title'] + ' - Articles for ' + month + '/' + year + ' | ',
        'year': year, 'month': month}
    )

  @authorized.role("admin")
  def post(self, year, month):
    """ Add a blog entry. Since we are POSTing, the server handles
      creation of the permalink url. """

    aio.debug("blog.MonthHandler #post on date %s, %s", year, month)
    process_article_submission(handler = self, article_type = 'blog entry')

  @authorized.role("admin")
  def put(self, year, month, perm_stem):

    permalink = year + '/' + month + '/' + perm_stem
    aio.debug("blog.MonthHandler #put on date %s, %s, perm: %s", year, month, perm_stem)
    process_article_edit(handler = self, permalink = permalink)


#
#
######### AtomHandler #######

class AtomHandler(restful.Controller):
  def get(self):
    logging.debug("Sending Atom feed")
    self.response.headers['Content-Type'] = 'application/atom+xml'
    if view.render_if_cached(self):
      return
    articles = db.Query(models.blog.Article). \
            filter('article_type =', 'blog entry'). \
            order('-published').fetch(limit = 10)
    updated = ''
    if articles:
      updated = articles[0].rfc3339_updated()

    page = view.ViewPage()
    page.render(self, {
      "blog_updated_timestamp": updated,
      "articles": articles, 
      "ext": "xml",
      "use_summary": config.BLOG['feed_use_summary']
    })


#
#
######### TagFeedHandler #######

class TagFeedHandler(restful.Controller):
  def get(self, encoded_tag):
    logging.debug("Sending atom feed for tag %s", encoded_tag)
    self.response.headers['Content-Type'] = 'application/atom+xml'
    if view.render_if_cached(self):
      return
    tag = unicode(urllib.unquote(encoded_tag),
        config.APP['charset'])
    articles = db.Query(models.blog.Article).filter('tags =',
        tag).order('-published')
    updated = ''
    if articles:
      updated = articles[0].rfc3339_updated()
    page = view.ViewPage()
    page.render(self, {"blog_updated_timestamp": updated,
      "articles": articles, "ext": "xml", "handler_name": "tag",
      "tag_name": tag})

#
#
######### SitemapHandler #######

class SitemapHandler(restful.Controller):
  def get(self):
    logging.debug("Sending Sitemap")
    self.response.headers['Content-Type'] = 'text/xml'
    if view.render_if_cached(self):
      return
    articles = db.Query(models.blog.Article).order('-published').fetch(1000)
    if articles:
      page = view.ViewPage()
      page.render(self, {
        "articles": articles,
        "ext": "xml",
        "root_url": config.APP['base_url']
      })

