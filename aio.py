

import logging
import config
import inspect

def debug(*args) :

	args = list(args)
	# (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

	if config.DEBUG : 
		args[0] = "\n\nDEBUG: " + str(args[0]) + "\n"
		logging.info(*args)

	else :
		# args[0] = "INFO: " + str(args[0])
		logging.debug(*args)

def info(*args) :

	if config.DEBUG : 
		args = list(args)
		args[0] = "\n\nINFO: " + str(args[0]) + "\n"
		logging.info(*args)

	else :
		# args[0] = "INFO: " + str(args[0])
		logging.info(*args)


def asciify(item) :

  try :
    return str(item)
  except:
    buffer = ""
    for letter in item :
      try:
        buffer += unicodedata.normalize('NFKD', letter.decode('utf-8', 'replace')).encode('ascii', 'ignore')
      except:
        buffer += "_"
    return buffer