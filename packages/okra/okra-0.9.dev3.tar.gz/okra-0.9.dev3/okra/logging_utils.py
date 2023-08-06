import os
import logging

def enable_log(log_name):
    """ Enable logs written to file """
    logging.basicConfig(filename= log_name,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

def enable_cloud_log():
    """ Enable logs using default StreamHandler """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

