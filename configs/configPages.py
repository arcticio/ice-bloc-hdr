
from utils.fusiontable import FusionTable

PAGES = {
  "radio-interviews-and-features": {
    ## http://www.google.com/fusiontables/DataSource?dsrcid=925673
    'module_name':  "page",
    'handler_name': "radio",
    'data': FusionTable("SELECT * FROM 925673 WHERE active=1 ORDER BY date_published DESC").get("liste")
  },
  "": {
    'module_name':  "page",
    'handler_name': "radio",
  },

}