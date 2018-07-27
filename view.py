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

import aio

import config
import logging
import os
import re
import string
import time
import urlparse

import routes

from google.appengine.api import users
from google.appengine.api import memcache

from django.template.loaders.filesystem import Loader
from django.template.loader import render_to_string

from models.blog import Tag     # Might rethink if this is leaking into view
from models.blog import Year
from utils import template

from configs.navigation import Navigation

NUM_FULL_RENDERS = {}     # Cached data for some timings.

def do_build_tree(base, path, tree):

  if path : 
    entries = os.listdir(os.path.join(base, path))
  else : 
    entries = os.listdir(base)

  for entry in entries:
    entry_path = os.path.join(path, entry)
    if os.path.isdir(os.path.join(base, entry_path)):
      do_build_tree(base, entry_path, tree.setdefault(entry, {}))
    elif entry not in tree:
      tree[entry] = entry_path

def build_tree(base):

  tree = {}
  basedir = os.path.join(config.BASEDIR, base)
  do_build_tree(basedir, "", tree)
  return tree

templates = build_tree(config.APP['template_dir'])

# aio.debug("view.build_tree: %s", dir(templates))

def find_file(tree, path):
  cur = tree
  for element in path.split('/'):
    cur = cur.get(element, {})
  if cur:
    return cur
  else:
    return None

def invalidate_cache(cache_key = None):
  if not cache_key:
    memcache.flush_all()
  else:
    memcache.delete(cache_key)

def to_filename(camelcase_handler_str):
  filename = camelcase_handler_str[0].lower()
  for ch in camelcase_handler_str[1:]:
    if ch in string.uppercase:
      filename += '_' + ch.lower()
    else:
      filename += ch
  return filename

def get_view_file(handler, params={}):
  """
  Looks for presence of template files with priority given to
   HTTP method (verb) and role.
  Full filenames are <handler>.<role>.<verb>.<ext> where
   <handler> = lower-case handler name
   <role> = role of current user
   <verb> = HTTP verb, e.g. GET or POST
   <ext> = html, xml, etc.
  Only <handler> and <ext> are required.
  Properties 'module_name' and 'handler_name' can be passed in
   params to override the current module/handler name.

  Returns:
    Tuple with first element = template file name and
    second element = template directory path tuple
  """
  if 'ext' in params:
    desired_ext = params['ext']
  else:
    desired_ext = 'html'

  verb = handler.request.method.lower()
  app_name = ''
  module_name = None
  handler_name = None
  cls = handler.__class__

  if (cls.__module__.startswith('handlers.') and cls.__name__.endswith('Handler')) :

    aio.debug("view.get_view_file: from: %s", cls.__name__)
    handler_path = cls.__module__.split('.')

    if len(handler_path) == 3:
      app_name = to_filename(handler_path[1])

    module_name  = to_filename(handler_path[-1])
    handler_name = to_filename(cls.__name__.partition('Handler')[0])

  if 'app_name' in params:      app_name = params['app_name']
  if 'module_name' in params:   module_name = params['module_name']
  if 'handler_name' in params:  handler_name = params['handler_name']

  aio.debug("view.get_view_file: app: %s, mod: %s, verb: %s, hnd/tmpl: %s", app_name, module_name, verb, handler_name)

  # Get template directory hierarchy -- Needed if we inherit from templates
  # in directories above us (due to sharing with other templates).
  template_dirs = []

  root_folder = os.path.join(config.BASEDIR, config.APP['template_dir'])

  if module_name : template_dirs += (os.path.join(root_folder, app_name, module_name),)
  if app_name :    template_dirs += (os.path.join(root_folder, app_name),)
    
  template_dirs += (root_folder,)

  # for direc in template_dirs :
  #   aio.debug("view.get_view_file: templates in: %s", direc)

  # Now check possible extensions for the given template file.
  if handler_name:
    entries = templates
    if app_name:
      entries = entries.get(app_name, {})
    if module_name:
      entries = entries.get(module_name, {})
    possible_roles = []
    if users.is_current_user_admin():
      possible_roles.append('.admin.')
    if users.get_current_user():
      possible_roles.append('.user.')
    possible_roles.append('.')

    for role in possible_roles:
      filename = ''.join([handler_name, role, verb, '.', desired_ext])
      # aio.debug("view.get_view_file: Searching for verbed filename: %s", filename)
      if filename in entries:
        return {'file': filename, 'dirs': template_dirs}

    for role in possible_roles:
      filename = ''.join([handler_name, role, desired_ext])
      # aio.debug("view.get_view_file: Searching for filename: %s", filename)
      if filename in entries:
        return {'file': filename, 'dirs': template_dirs}

  return {'file': 'notfound.html', 'dirs': template_dirs}

def render_if_cached(handler):
  """Checks if there's a non-stale cached page for the given URL, and
  if there is, render it and return true without any further handling
  of the request.  This allows a handler to, for instance, quickly
  render a page before doing a DB lookup"""
  if config.APP['memcache_timeout'] and not users.get_current_user():
    try:
      data = memcache.get(handler.request.url);
    except ValueError:
      data = None

    if data:
      aio.info("view.render_if_cached: quick render of %s", handler.request.url)
      handler.response.out.write(data)
      return True
      
    return False

class ViewPage(object):

  def __init__(self, cache_time=None):
    """Each ViewPage has a variable cache timeout"""
    if cache_time == None:
      self.cache_time = config.APP['memcache_timeout']
    else:
      self.cache_time = cache_time


  def render(self, handler, params={}):
    """
    Can pass overriding parameters within dict.  These parameters can
    include:
      'ext': 'xml' (or any other format type)
    """

    template_info = get_view_file(handler, params)
    aio.debug("view.render: Using template at %s", template_info['file'])
    output = self.render_or_get_cache(handler, template_info, params)
    handler.response.out.write(output)

  def render_or_get_cache(self, handler, template_info, template_params={}):
    """Checks if there's a non-stale cached version of this view,
       and if so, return it."""

    user = users.get_current_user()
    key = handler.request.url

    if self.cache_time and not user:
      # See if there's a cache within time.
      # The cache key suggests a problem with the url <-> function
      #  mapping, because a significant advantage of RESTful design
      #  is that a distinct url gets you a distinct, cacheable
      #  resource.  If we have to include states like "user?" and
      #  "admin?", then it suggests these flags should be in url.
      # TODO - Think about the above with respect to caching.
      try:
        data = memcache.get(key)
      except ValueError:
        data = None
      if data is not None:
        aio.debug("view.render_or_get_cache: REQUEST <= MEMCACHE")
        return data

    output = self.full_render(handler, template_info, template_params)
    
    if self.cache_time and not user:
      memcache.add(key, output, self.cache_time)

    return output


  def full_render(self, handler, template_info, more_params):
    """Render a dynamic page from scatch."""

    # aio.debug("view.full_render template_file: %s query:%s", template_info['file'], query)
    url = handler.request.uri
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)

    # query = handler.request.query_string
    DEBUG = config.DEBUG
    if "DEBUGON" in query :
      DEBUG = True
    if "NODEBUG" in query :
      DEBUG = False

    DEVELOP = os.environ['APPLICATION_ID'].startswith('dev')
    if "DEVELON" in query :
      DEVELOP = True
    if "NODEVEL" in query :
      DEVELOP = False

    # aio.debug("URI: %s, query: %s, DEBUG: %s", url, query, DEBUG)


    # global NUM_FULL_RENDERS
    # if not path in NUM_FULL_RENDERS:
    #   NUM_FULL_RENDERS[path] = 0
    # NUM_FULL_RENDERS[path] += 1   # This lets us see % of cached views in /admin/timings (see timings.py)

    tags  = [tag for tag in Tag.list() if tag["count"] != 0]
    years = Year.get_all_years()
    user  = users.get_current_user()

    # Define some parameters it'd be nice to have in views by default.
    template_params = {
      "current_url":    url,
      'navigation':     Navigation().get(), ##config.ArcticIo().getNavLinks(handler), ## relevant handler
      "user":           user,
      "user_is_admin":  users.is_current_user_admin(),
      "login_url":      users.create_login_url(handler.request.uri),
      "logout_url":     users.create_logout_url(handler.request.uri),
      "app":            config.APP,
      "blog":           config.BLOG,
      "blog_tags":      tags,
      "archive_years":  years,
      "ADMIN":          users.is_current_user_admin(),
      "DEBUG":          DEBUG,
      "DEVELOP":        DEVELOP,
      "VERSION":        config.APP["version"], 
      'IP':             os.environ['REMOTE_ADDR'],
    }
    
    template_params.update(routes.getParams(handler))
    template_params.update(more_params) ## allow overwrite of sections

    aio.debug("view.full_render VERSION: %s, TMPL: %s, DEVELOP: %s, ADMIN: %s, DEBUG: %s", 
      config.APP["version"], 
      template_info['file'],
      DEVELOP,
      users.is_current_user_admin(), 
      DEBUG
    )

    return template.render(
        template_info['file'], 
        template_params,
        # debug=config.DEBUG,
        debug=False, ## DEBUG,
        template_dirs=template_info['dirs']
    )

  def render_query(self, handler, model_name, query, params={}, num_limit=config.BLOG['posts_per_page'], num_offset=0):
    """
    Handles typical rendering of queries into datastore with paging.
    """

    limit = string.atoi(handler.request.get("limit") or str(num_limit))
    offset = string.atoi(handler.request.get("offset") or str(num_offset))

    # Trick is to ask for one more than you need to see if 'next' needed.
    models = query.fetch(limit+1, offset)

    render_params = {model_name: models, 'limit': limit}

    if len(models) > limit:
      render_params.update({ 'next_offset': str(offset+limit) })
      models.pop()

    if offset > 0:
      render_params.update({ 'prev_offset': str(offset-limit) })

    aio.debug("view.render_query: offset: %s, limit: %s", offset, limit)

    render_params.update(params)

    self.render(handler, render_params)

