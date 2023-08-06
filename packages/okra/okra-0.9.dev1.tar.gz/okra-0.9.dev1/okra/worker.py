""" Run redis worker. """
import logging
import os
import time
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

  logger.info("Worker with sessionID: {}".format(q.sessionID()))
  logger.info("Initial queue state: empty= {}".format(str(q.empty())))
  while not q.empty():
    
    item = q.lease(lease_secs=10, block=True, timeout=2)
    
    if item is not None:
      itemstr = item.decode("utf=8")
      logger.info("Working on {}".format(itemstr))
      time.sleep(10) # Put your actual work here instead of sleep.
      q.complete(item)
    else:
      logger.info("Waiting for work")
  logger.info("Queue empty, exiting")

def redis_loader(job: str, fpath: str):
  """ Load redis queue from repo list file. """
  host = os.getenv("REDIS_SERVICE_HOST") or "redis"
  q = redislr.RedisLoader(name=job, host=host)

  logger.info("Loader with sessionID: {}".format(q.sessionID()))
  q.read_repolist(fpath)

