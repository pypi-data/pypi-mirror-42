""" Run redis worker. 

Configuration parameters are either handled by environment
variables placed within the job specification or passed
via the command line. The convention is to set environment 
variables that will be shared across okra tasks like storage
locations, redis dns name, etc.
"""
import logging
import os
import time
from urllib.parse import urljoin

from okra.playbooks import gcloud_persistance
import okra.rediswq as rediswq
import okra.redisloader as redislr

import redis


logger = logging.getLogger(__name__)


def redis_worker(job="job2"):
  """ Run redis worker. 

  :param job: job name <default: job2>
  :param host: host name <default: redis>
  :return: Completes specified jobs
  :rtype: void
  """
  host = os.getenv("REDIS_SERVICE_HOST") or "redis"
  q = rediswq.RedisWQ(name=job, host=host)
  recover = redislr.RedisLoader(name=job, host=host)

  logger.info("Worker with sessionID: {}".format(q.sessionID()))
  logger.info("Initial queue state: empty= {}".format(str(q.empty())))
  while not q.empty():
    
    item = q.lease(lease_secs=10, block=True, timeout=2)
    
    if item is not None:
      itemstr = item.decode("utf=8")
      logger.info("Working on {}".format(itemstr))

      try:
        gcloud_persistance(itemstr)
        q.complete(item)

      except Exception as exc:
        logger.warning("Trying to recover: {}".format(itemstr))
        recover._load_queue([itemstr])
        logger.info("Recovered: {}".format(itemstr))
        raise exc

    else:
      logger.info("Waiting for work")
  logger.info("Queue empty, exiting")

def redis_loader(job: str, fpath: str):
  """ Load redis queue from repo list file. """
  
  host = os.getenv("REDIS_SERVICE_HOST") or "redis"
  gpresent = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
  bucket_id = os.getenv("BUCKET_ID")
  cache = os.getenv("CACHE")
  
  q = redislr.RedisLoader(name=job, host=host)
  logger.info("Loader with sessionID: {}".format(q.sessionID()))

  if gpresent is not None and cache is not None:
    gpath = fpath
    file_path = urljoin(cache, fpath)
    q.read_gcloud_repolist(bucket_id, gpath, file_path)

  else:
    q.read_repolist(fpath)

def redis_merger(job: str):
  """ Merge db files. """
  pass
