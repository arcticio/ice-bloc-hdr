# Site-specific legacy url mapping.
#
# The data is imported and used by the blog handler.
# This file can be (1) set manually or (2) created automatically 
# by utilities/drupal_uploader.
# Place below a "redirects" dictionary with aliases as the key 
# (without host uri stem) and the permalink as the value.
import config

redirects = {
# "blog/feeds/atom/latest/":          config.BLOG['atom_url'],
# "blog":                             "/",
# "blog/":                            "/",
# "atom":                              config.BLOG['atom_url'],
#  "explorer":                         "/explorer/",
#  "satellite/":                       "/explorer/",
#  "satellite":                        "/explorer/",
#  "observations/":                    "/explorer/",
#  "observations":                     "/explorer/",
#  # "observations/1544///ice-drift-sst", "????"
#  "double-zoom":                      "/split-zoom/",
#  "arctic-sea-ice-charts":            "/sea-ice-charts/",
#  "arctic-sea-ice-charts/":           "/sea-ice-charts/",
#  "/2011/9/microwave-versus-radar-satellite-images": "/2011/9/microwave-versus-envisat-radar-satellite-images"
}
