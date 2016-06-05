#!/usr/bin/env python3
# log.py -*-python-*-
#
# I hereby waive all copyright and related or neighboring rights together with
# all associated claims and causes of action with respect to this work to the
# extent possible under the law.
#
# The prefix DIEF is used in an attempt to be unique, and to remind the user
# that the messages are formatted using (D)ebug, (I)nfo, (E)rror, and (F)atal
# tags.

import logging
import sys
import time

def DIEF_log_format_message(record):
  try:
    msg = '%s' % (record.msg % record.args)
  except:
    msg = record.msg
  return msg

def DIEF_log_set_level(newlevel):
  old_level = logger.getEffectiveLevel()
  if newlevel == 'DEBUG':
    logger.setLevel(10)
  elif newlevel == 'INFO':
    logger.setLevel(20)
  elif newlevel == 'ERROR':
    logger.setLevel(40)
  else:
    logger.setLevel(newlevel)
  new_level = logger.getEffectiveLevel()
  logger.info('Logging changed from level {} ({}) to level {} ({})'.format(
    old_level,
    logging.getLevelName(old_level),
    new_level,
    logging.getLevelName(new_level)))

def DIEF_log_init():
  DIEF_log_set_level('INFO')

class DIEFLogFormatter(logging.Formatter):
  def __init__(self):
    logging.Formatter.__init__(self)
    self.timestamps = True
    self.lineno = False

  def format(self, record):
    level = record.levelname[0]
    if self.timestamps:
      if self.lineno:
        date = time.localtime(record.created)
        date_msec = (record.created - int(record.created)) * 1000
        message = '%c%04d%02d%02d %02d:%02d:%02d.%03d %s:%d: %s' % (
          level,
          date.tm_year, date.tm_mon, date.tm_mday,
          date.tm_hour, date.tm_min, date.tm_sec, date_msec,
          record.filename, record.lineno,
          DIEF_log_format_message(record))
      else:
        date = time.localtime(record.created)
        date_msec = (record.created - int(record.created)) * 1000
        message = '%c%04d%02d%02d %02d:%02d:%02d.%03d %s' % (
          level,
          date.tm_year, date.tm_mon, date.tm_mday,
          date.tm_hour, date.tm_min, date.tm_sec, date_msec,
          DIEF_log_format_message(record))
    else:
      if self.lineno:
        message = '%c %s:%d: %s' % (
          level,
          record.filename, record.lineno,
          DIEF_log_format_message(record))
      else:
        message = '%c %s' % (
          level,
          DIEF_log_format_message(record))

    record.getMessage = lambda: message
    return logging.Formatter.format(self, record)

logger = logging.getLogger()
logging.addLevelName(50, 'FATAL')

handler = logging.StreamHandler()
handler.setFormatter(DIEFLogFormatter())

logger.addHandler(handler)

def DIEFFatal(message, *args, **kwargs):
  logging.fatal(message, args, kwargs)
  sys.exit(1)

DEBUG = logging.debug
INFO = logging.info
ERROR = logging.error
FATAL = DIEFFatal
