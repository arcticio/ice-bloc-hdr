import aio

import logging
import os

import config
import view
import models
from handlers import restful

import routes

#from configPages import PAGES

from handlers.gablog.blog import process_article_edit, render_article

from utils import authorized


class PageHandler(restful.Controller):
  def get(self, path):

    aio.debug('page.PageHandler#get path: %s', path)
    self.response.headers['X-Pingback'] = config.APP['base_url'] + "/xmlrpc"
    
    try:
      from configPages import PAGES
      template_data.update(PAGES[path])
      loggin.warn("page.py. not found: " + path)
    except:
      pass

    render_article(self, path, {})

  @restful.methods_via_query_allowed
  def post(self, path):
    aio.debug('page.PageHandler#post - ignoring')

  @authorized.role("admin")
  def put(self, path):
    aio.debug("page.PageHandler#put path /%s", path)
    process_article_edit(self, postlink=path)

  @authorized.role("admin")
  def delete(self, path):
    """
    By using DELETE on /Article, /Comment, /Tag, you can delete the first
     entity of the desired kind.
    This is useful for writing utilities like clear_datastore.py.
    """
    # TODO: Add DELETE for articles off root like blog entry DELETE.
    model_class = path.lower()
    aio.debug('page.PageHandler#delete path: %s', path)

    def delete_entity(query):
      targets = query.fetch(limit = 1)
      if len(targets) > 0:
        if hasattr(targets[0], 'title'):
          title = targets[0].title
        elif hasattr(targets[0], 'name'):
          title = targets[0].name
        else:
          title = ''
        logging.debug('Deleting %s %s', model_class, title)
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
