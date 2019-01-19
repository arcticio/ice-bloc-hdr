import logging
import os

from version import VERSION

BASEDIR = os.path.abspath(os.path.dirname(__file__))

utils_path     = os.path.join(BASEDIR, "utils")
ext_utils_path = os.path.join(utils_path, "external")

# Enabling debugging prints extra messages about what's going on "under 
# the hood". Currently only enabled automatically when running on the 
# GAE development server.

DEBUG = os.environ['APPLICATION_ID'].startswith('dev')

# This dict contains application-wide configuration values
APP = {
	"name": "arctic.io",
	"version": VERSION,
	# "version": "HUHUH",
	"description": "Look, it's melting",
	"title": "arctic.io",
	"author": "Torsten Becker",

	# Your Twitter username, for the Twitter widget. Set to None if you
	# don't want to use the widget or if you don't have a Twitter
	# account.
	"twitter_username": "arctic.io",

	# The number of posts to load from Twitter
	"twitter_posts": 3,

	# The AppEngine mail API requires that this be the email 
	# address for a registered admin of the application. This will be 
	# the email address emails sent from this application appear to 
	# come from.
	"email": "tb@arctic.io",

	# This will be the MIME type and character set used
	"mimetype": "application/xml+xhtml",
	"charset": "UTF-8",

	"base_url": "http://www.arctic.io",

	# The jQuery version to use
	"jquery_version": "1.4.2",

	# Timeout for memcache in seconds.
	"memcache_timeout": 3600,

	# The directory containing HTML templates.
	"template_dir": "templates",

	# Must be the name of a directory under the template_dir directory.
	# "theme": "arctic",

	# Your Google Analytics tracking code. Set to None if you don't have
	# one (or don't want to use one).
	"analytics": "UA-22811255-1",
  
	# The base domain for this app. For example, if you use
	# 'http://www.example.com' then the base domain would be 'example.com'.
	"base_domain": "arctic.io",

	# Your Google site verification code for Google Webmaster, if you 
	# are using this service.
	"google_webmaster_verify": None,

	# The legacy software to map URI's from. Adding support is a
	# two-step process: add the name here (either on its own or as part
	# of the list) and add required code to resolve_legacy_mapping in
	# handlers/gablog/blog.py
	#
	# This can either be a single supported value, or a list of
	# supported values. Currently supported legacy software packages
	# are:
	#	Drupal - URLs look like this: /node/3, /node/58/
	#	Serendipity - URLs look like this: /archives/54-something.html
	#	Blogger - URLs look like this:
	"legacy_software": None,

	# If this is set to False, legacy entries _not_ mapped through
	# legacy software in legacy_aliases.py will be served on their old
	# URIs.  If this is set to True, legacy URIs will be redirected to
	# their new permalink.
	"legacy_entry_redirect": True,
}

# This is the main configuration dict for things specific to the blog system
BLOG = {

  #truncater in blogs
  "truncater": "[MORE]", ## see /utils/templatefilters

	# RSS and Atom feeds are at these locations
	"rss_url": "/feeds/rss",
	"atom_url": "/feeds/atom",
	
	"pingback_url": "/pingback",
	
	# The CKEditor skin to use
	"ckeditor_skin": "kama",

	# Set to True if you want to have the post scanned for links to
	# other sites and pingbacks sent to those sites that support
	# pingbacks.
	# WARNING: Enabling this will substantially slow down the posting
	# process. Although this is the last thing to be done before
	# redirecting to the new permalink, it may appear that nothing is
	# happening. Please ensure that you wait for the redirect to occur
	# before navigating anywhere.
	"do_pingback": False,

	# Set to True if you want your feed to use the article excerpt
	# instead of the full article text.
	"feed_use_summary": False,

	# Number of days posts are open for commenting by default. If the 
	# selection on a post is set to "No" or "Yes", that will override
	# this setting.
	"comment_window": 14,	# 4 weeks

	# The number of blog posts to display on each page.
	"posts_per_page": 3, ##20 

	# The number of comments to display on each page of each post
	"comments_per_page": 40,

	# Check for a Gravatar for the email address each commenter 
	# provides?
	"use_gravatars": False,

	# Do you want to be emailed when new comments are posted?
	"send_comment_notification": True,
}
