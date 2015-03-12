from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import logging
import os
import os.path


LOG_LEVEL = 'INFO'
LOG_FILE = ''
LOG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

def parent_makedirs(file):
  path = os.path.dirname(os.path.expanduser(file))
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
      pass
    else:
      raise

def set_logs(level=None, file=None, format=None):  
  global HANDLER, LOG_LEVEL, LOG_FILE, LOG_FORMAT
  LOG_LEVEL = (level or LOG_LEVEL).upper()
  LOG_FILE = file or LOG_FILE
  LOG_FORMAT = format or LOG_FORMAT

  logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT)

  if LOG_FILE:
    parent_makedirs(LOG_FILE)
    HANDLER = logging.FileHandler(LOG_FILE)
  else:
    HANDLER = None

set_logs()

def logger(name=None):
  
  log = logging.getLogger(name or 'logging')
  if HANDLER and HANDLER not in log.handlers:
    log.addHandler(HANDLER)

  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', LOG_LEVEL)
