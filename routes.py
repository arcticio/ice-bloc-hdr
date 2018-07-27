
import logging

from handlers.gablog import blog, contact, post, page, plug, ajax

sections = {
    "0" : "Navigation",
    "1" : "Home",
    "2" : "Sticky",
    "3" : "Blog",
    "4" : "Editor",
    "5" : "News",
    "6" : "Data",
    "7" : "Explorer",
    "8" : "Simulation",
    "9" : "Contact",

    "10": "Simulation",
    "20": "Disaster",
    "30": "Bundle",
    "40": "Collection",
    "50": "Article",
    "60": "Zoom",
}

ful = [0, 1, 2, 3, 4, 5, 6, 10, 7, 8, 9]    ## all
hom = [0, 1, 2, 6, 10, 9]            ## all, no editor, no article == home, dropped 5
blg = [0, 1, 3]                         ## blog
art = [0, 1, 50]                        ## article
edt = [0, 4]                            ## editor + preview
sim = [0, 1, 2, 3, 6]                   ## page, simulation
dis = [0, 1, 20]                        ## 404, 403
lst = [0, 1, 30]                        ## List of Notes
zom = [0, 60]                           ## Zoom pages
exp = [0, 7]                            ## Explorer pages

entries = [

    [blog.RootHandler,                 '/*$',                           {'sections': hom}],
    [blog.UnauthorizedHandler,         '/403.html',                     {'sections': dis}],
    [blog.NotFoundHandler,             '/404.html',                     {'sections': dis}],
    # [blog.SitemapHandler,              '/sitemap.xml',                  {'sections': []}],          ## checked
    [blog.CollHandler,                 '/list/(.*?)/(.*?)/?$',          {'sections': [0, 40]}],     ## all, blogs, articles, drafts /?limit=&offset=
    [blog.YearHandler,                 '/([12]\d\d\d)/?$',              {'sections': lst}],
    [blog.MonthHandler,                '/([12]\d\d\d)/(\d|[01]\d)/?$',  {'sections': lst}],
    [blog.BlogEntryHandler,    '/([12]\d\d\d)/(\d|[01]\d)/([-\w]+)/?$', {'sections': blg}],
    # [blog.SearchHandler,               '/search',                       {'sections': []}],
    # [blog.TagFeedHandler,              '/tag/(.*?)/feed/?$',            {'sections': []}],
    [blog.TagHandler,                  '/tag/(.*?)/?$',                 {'sections': lst}],
    [plug.ExplorerHandler,             '/explorer/(.*)/(.*)/(.*)/(.*)', {'sections': exp}],
    [plug.ExplorerHandler,             '/explorer/(.*)/(.*)/(.*)',      {'sections': exp}],
    [plug.ExplorerHandler,             '/explorer/',                    {'sections': exp}],
    [plug.ExplorerHandler,             '/explorer',                     {'sections': exp}],
    [plug.WikipediaHandler,            '/wikipedia/',                   {'sections': []}],
    # [plug.SeaiceHandler,               '/sea-ice-charts/',              {'sections': []}],
    [plug.ZoomHandler,                 '/maps/(.*)/',                   {'sections': zom}],
    [contact.ContactHandler,           '/contact/?$',                   {'sections': [9]}],
    [post.NewPostHandler,              '/post/new/?$',                  {'sections': edt}],
    [post.EditPostHandler,             '/post/edit/([\d\w-]+)/?$',      {'sections': edt}],         ## rad minus
    [ajax.AjaxHandler,                 '/ajax/(.*)',                    {'sections': []}],
    [page.PageHandler,                 '/(.*)',                         {'sections': art}],

]

# for entry in entries :
#     entry[2]["sections"] = [sections[str(i)] for i in entry[2]['sections']]

def getRoutes() :
    routes = []
    for entry in entries :
        routes.append((entry[1], entry[0]))
    return routes

def getParams(handler) :

    name = handler.__class__.__module__ + ":" + handler.__class__.__name__

    for entry in entries :

        if isinstance(handler, entry[0]) :
            params = entry[2].copy()
            params['sections'] = [sections[str(i)] for i in entry[2]['sections']]
            params['handler']  = name
            return params
        
    logging.error("routes.getParams no entry for %s", name)
    return {}
